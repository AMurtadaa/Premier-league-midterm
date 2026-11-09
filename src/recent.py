"""Refreshable Premier League results and point-in-time model estimates."""
from datetime import date, time
from functools import lru_cache
from io import BytesIO
from pathlib import Path
import re
from urllib.request import urlopen

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, log_loss

from .data import ROOT
from .predictor import ALIASES, CUTOFF, LABELS

CACHE = ROOT / "data" / "local" / "premier_league_results.csv"
SOURCE = "https://www.football-data.co.uk/mmz4281/{season}/E0.csv"
COLUMNS = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
WINDOW_DAYS = 21
TEAM_ALIASES = {**ALIASES, "Man City": "Manchester City", "Man United": "Manchester United",
                "Newcastle": "Newcastle United", "Nott'm Forest": "Nottingham Forest",
                "Sheffield United": "Sheffield United", "Leeds": "Leeds United",
                "Leicester": "Leicester City", "Norwich": "Norwich City"}


def refresh_results(path=CACHE, today=None):
    today = today or date.today()
    current = today.year - (today.month < 8)
    seasons = []
    for year in range(2021, current + 1):
        season = f"{year % 100:02d}{(year + 1) % 100:02d}"
        with urlopen(SOURCE.format(season=season), timeout=20) as response:
            data = pd.read_csv(BytesIO(response.read()), usecols=COLUMNS)
        data = data.dropna(subset=COLUMNS)
        data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", errors="raise")
        data = data.loc[data.FTR.isin(["H", "D", "A"])]
        if data.empty or (year < current and len(data) != 380):
            raise ValueError(f"Unexpected fixture count for {year}/{year+1}; old cache retained.")
        data["season_start"] = year
        seasons.append(data)
    results = pd.concat(seasons).sort_values("Date")
    if results.duplicated(["Date", "HomeTeam", "AwayTeam"]).any():
        raise ValueError("Duplicate fixtures; old cache retained.")
    if (results.Date > pd.Timestamp(today)).any():
        raise ValueError("Source includes future result dates; old cache retained.")
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(".tmp")
    results.to_csv(pending, index=False, date_format="%Y-%m-%d")
    pending.replace(path)
    return len(results), results.Date.max().date()


class RecentPredictor:
    def __init__(self, data):
        data = data.copy()
        data["Date"] = pd.to_datetime(data["Date"])
        for column in ("HomeTeam", "AwayTeam"):
            data[column] = data[column].replace(TEAM_ALIASES)
        self.last_date = data.Date.max()
        self.max_date = self.last_date + pd.Timedelta(days=WINDOW_DAYS)
        self.active_since = pd.Timestamp(year=int(data.season_start.max()), month=8, day=1)
        active = data.loc[data.season_start.eq(data.season_start.max())]
        self.active_teams = sorted(set(active.HomeTeam) | set(active.AwayTeam))
        home = data[["Date", "HomeTeam", "FTHG", "FTAG"]].copy()
        home.columns = ["date", "team", "gf", "ga"]
        away = data[["Date", "AwayTeam", "FTAG", "FTHG"]].copy()
        away.columns = home.columns
        history = pd.concat([home, away]).sort_values("date")
        history["points"] = (history.gf > history.ga) * 3 + (history.gf == history.ga)
        self.history = {}
        for team, group in history.groupby("team"):
            self.history[team] = (pd.DatetimeIndex(group.date), group[["gf", "ga", "points"]].to_numpy())
        features, labels, dates = [], [], []
        for row in data.sort_values("Date").itertuples():
            try:
                values = self.features(row.HomeTeam, row.AwayTeam, row.Date)
            except ValueError:
                continue
            features.append(values)
            labels.append(LABELS[{"H": "W", "D": "D", "A": "L"}[row.FTR]])
            dates.append(row.Date)
        self.X = pd.DataFrame(features)
        self.y = pd.Series(labels)
        self.dates = pd.Series(dates)
        first_trainable = self.dates.groupby(self.y).min().max() + pd.offsets.MonthBegin()
        self.min_date = max(CUTOFF + pd.Timedelta(days=1), first_trainable)
        cutoff = pd.Timestamp(year=int(data.season_start.max()) - 1, month=8, day=1)
        fit = self.model_before(cutoff)
        test = self.dates >= cutoff
        p = fit.predict_proba(self.X[test])
        y = self.y[test]
        labels = fit.classes_[p.argmax(axis=1)]
        self.evaluation = {
            "holdout_start": str(cutoff.date()), "train_fixtures": int((~test).sum()),
            "test_fixtures": int(test.sum()), "accuracy": accuracy_score(y, labels),
            "macro_f1": f1_score(y, labels, average="macro"), "log_loss": log_loss(y, p, labels=fit.classes_),
        }

    def features(self, home, away, match_date):
        values = {"weekday": match_date.dayofweek}
        for side, team in (("home", home), ("away", away)):
            if team not in self.history:
                raise ValueError(f"No results are available for {team}.")
            dates, history = self.history[team]
            stop = dates.searchsorted(match_date, side="left")
            start = max(stop - 5, dates.searchsorted(match_date - pd.Timedelta(days=365)))
            if stop - start < 3:
                raise ValueError(f"{team} needs three recorded matches in the year before this date.")
            values.update({f"{side}_{key}": value for key, value in zip(
                ("gf", "ga", "points"), history[start:stop].mean(axis=0)
            )})
        return values

    @lru_cache(maxsize=12)
    def model_before(self, cutoff):
        train = self.dates < cutoff
        model = GradientBoostingClassifier(n_estimators=70, max_depth=2, random_state=42)
        return model.fit(self.X[train], self.y[train])

    def coverage(self):
        return {"min_date": str(self.min_date.date()),
                "max_date": str(self.max_date.date()), "last_result": str(self.last_date.date()),
                "active_teams": self.active_teams, "active_since": str(self.active_since.date()),
                "source": "Football-Data.co.uk"}

    def predict(self, request):
        fields = ("home_team", "away_team", "match_date", "kickoff_time")
        if not isinstance(request, dict) or not all(isinstance(request.get(k), str) and request[k].strip() for k in fields):
            raise ValueError("Choose both teams and enter a date and kickoff time.")
        home, away, day, kickoff = (request[k].strip() for k in fields)
        home, away = TEAM_ALIASES.get(home, home), TEAM_ALIASES.get(away, away)
        if home == away:
            raise ValueError("Choose two different teams.")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day) or not re.fullmatch(r"\d{2}:\d{2}", kickoff):
            raise ValueError("Use YYYY-MM-DD for the date and HH:MM for kickoff.")
        try:
            match_date = pd.Timestamp(date.fromisoformat(day))
            time.fromisoformat(kickoff)
        except (ValueError, OverflowError):
            raise ValueError("Enter a valid date and kickoff time.") from None
        if not self.min_date <= match_date <= self.max_date:
            raise ValueError(f"Date outside available coverage ({self.coverage()['min_date']} to {self.max_date.date()}). Refresh results for newer dates.")
        if match_date >= self.active_since and not {home, away}.issubset(self.active_teams):
            raise ValueError("Select clubs in the covered Premier League season.")
        X = pd.DataFrame([self.features(home, away, match_date)])
        # Monthly model snapshots ensure targets from the requested month never
        # enter training. Features may use results strictly before kickoff day.
        fit = self.model_before(match_date.replace(day=1))
        values = fit.predict_proba(X)[0]
        return {"probabilities": {label: float(value) for label, value in zip(fit.classes_, values)},
                "model": "Gradient Boosting", "calibrated": False, "match_date": day,
                "kickoff_time": kickoff, "last_result": str(self.last_date.date()),
                "source": "Football-Data.co.uk"}


if __name__ == "__main__":
    count, last = refresh_results()
    print(f"Cached {count} completed Premier League matches through {last}.")
