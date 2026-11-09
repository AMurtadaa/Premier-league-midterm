"""Historical three-class inference; train and serve the same feature builder."""
from datetime import date, time
from functools import lru_cache
import re

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, log_loss

from .data import load_matches
from .features import ROLLING_INPUTS

CUTOFF = pd.Timestamp("2022-01-01")
LABELS = {"W": "home_win", "D": "draw", "L": "away_win"}
ALIASES = {
    "Brighton": "Brighton and Hove Albion", "Brighton & Hove Albion": "Brighton and Hove Albion",
    "Manchester Utd": "Manchester United", "Newcastle Utd": "Newcastle United",
    "Sheffield Utd": "Sheffield United", "Tottenham": "Tottenham Hotspur",
    "West Brom": "West Bromwich Albion", "West Ham": "West Ham United", "Wolves": "Wolverhampton Wanderers",
}


class Predictor:
    def __init__(self, data):
        self.last_date = data.date.max()
        self.history = {}
        for team, group in data.groupby("team"):
            group = group.sort_values("date")
            self.history[team] = (pd.DatetimeIndex(group.date), group[ROLLING_INPUTS].rolling(3).mean())
        records = []
        for row in data.loc[data.venue.eq("Home")].itertuples():
            try:
                features = self.features(row.team, ALIASES.get(row.opponent, row.opponent), row.date, row.time)
            except ValueError:
                continue
            records.append((row.date, features, LABELS[row.result]))
        train = [row for row in records if row[0] < CUTOFF]
        test = [row for row in records if row[0] > CUTOFF]
        self.model = GradientBoostingClassifier(n_estimators=70, max_depth=2, random_state=42)
        self.model.fit(pd.DataFrame([row[1] for row in train]), [row[2] for row in train])
        X = pd.DataFrame([row[1] for row in test])
        y = [row[2] for row in test]
        labels = self.model.predict(X)
        self.evaluation = {
            "train_fixtures": len(train), "test_fixtures": len(test),
            "accuracy": accuracy_score(y, labels), "macro_f1": f1_score(y, labels, average="macro"),
            "log_loss": log_loss(y, self.model.predict_proba(X), labels=self.model.classes_),
        }

    def features(self, home, away, match_date, kickoff):
        features = {"kickoff_minutes": int(kickoff[:2]) * 60 + int(kickoff[3:5]),
                    "weekday": match_date.dayofweek}
        for side, team in (("home", home), ("away", away)):
            if team not in self.history:
                raise ValueError(f"No match history is available for {team}.")
            dates, rolling = self.history[team]
            i = dates.searchsorted(match_date, side="left") - 1
            if i < 2 or rolling.iloc[i].isna().any():
                raise ValueError(f"Not enough prior match data for {team} on that date.")
            features.update({f"{side}_{name}": value for name, value in rolling.iloc[i].items()})
        return features

    def predict(self, request):
        fields = ("home_team", "away_team", "match_date", "kickoff_time")
        if not isinstance(request, dict) or not all(isinstance(request.get(k), str) and request[k].strip() for k in fields):
            raise ValueError("Choose both teams and enter a match date and kickoff time.")
        home, away, day, kickoff = (request[k].strip() for k in fields)
        home, away = ALIASES.get(home, home), ALIASES.get(away, away)
        if home == away:
            raise ValueError("Choose two different teams.")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day) or not re.fullmatch(r"\d{2}:\d{2}", kickoff):
            raise ValueError("Use YYYY-MM-DD for the match date and HH:MM for kickoff.")
        try:
            match_date = pd.Timestamp(date.fromisoformat(day))
            time.fromisoformat(kickoff)
        except (ValueError, OverflowError):
            raise ValueError("Enter a valid match date and kickoff time.") from None
        if not CUTOFF < match_date <= self.last_date:
            raise ValueError(f"Choose a historical date from 2022-01-02 through {self.last_date.date()}.")
        X = pd.DataFrame([self.features(home, away, match_date, kickoff)])
        values = self.model.predict_proba(X)[0]
        return {
            "probabilities": {label: float(value) for label, value in zip(self.model.classes_, values)},
            "model": "Gradient Boosting", "calibrated": False,
            "match_date": day, "kickoff_time": kickoff,
        }


@lru_cache(maxsize=1)
def load_predictor():
    return Predictor(load_matches())
