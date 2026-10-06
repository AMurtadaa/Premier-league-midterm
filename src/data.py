from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "raw" / "matches.csv"
BASE_FEATURES = ["venue_code", "opp_code", "hour", "day_code"]


def load_matches(path=DATASET):
    """Load the frozen team-appearance CSV without its saved index."""
    data = pd.read_csv(path, index_col=0)
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    required = {"date", "team", "opponent", "venue", "result", "time"}
    if not required.issubset(data.columns):
        raise ValueError(f"Missing columns: {required - set(data.columns)}")
    if not data["result"].isin(["W", "D", "L"]).all():
        raise ValueError("Only completed W/D/L records may enter this snapshot.")
    if data.duplicated(["date", "team", "opponent"]).any():
        raise ValueError("Duplicate team appearances need investigation.")
    return data


def prepare_binary(data):
    """Reconstruct the recording's coding; preserve input order for comparison.

    Category codes use the frozen club/venue catalog for legacy compatibility.
    This is not an exported inference preprocessor for future/unseen teams.
    """
    data = data.drop(columns=["notes"], errors="ignore").copy()
    data["target"] = data["result"].eq("W").astype(int)
    data["venue_code"] = data["venue"].astype("category").cat.codes
    data["opp_code"] = data["opponent"].astype("category").cat.codes
    data["hour"] = data["time"].str.split(":").str[0].astype(int)
    data["day_code"] = data["date"].dt.dayofweek
    return data


def chronological_split(data, cutoff="2022-01-01"):
    """Strict inequalities reproduce the recording; cutoff-day rows are excluded."""
    cutoff = pd.Timestamp(cutoff)
    return data[data.date < cutoff].copy(), data[data.date > cutoff].copy()


def dataset_audit(data):
    return {
        "rows": len(data),
        "columns_without_saved_index": len(data.columns),
        "start": str(data.date.min().date()),
        "end": str(data.date.max().date()),
        "season_rows": {str(k): int(v) for k, v in data.groupby("season").size().items()},
        "season_clubs": {str(k): int(v) for k, v in data.groupby("season").team.nunique().items()},
        "outcomes": {str(k): int(v) for k, v in data.result.value_counts().items()},
        "duplicate_team_date_opponent": int(data.duplicated(["team", "date", "opponent"]).sum()),
        "missing_2021_22_liverpool": not bool(((data.season == 2022) & (data.team == "Liverpool")).any()),
    }
