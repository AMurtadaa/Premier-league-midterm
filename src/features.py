import numpy as np

ROLLING_INPUTS = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
ROLLING_FEATURES = [f"{column}_rolling" for column in ROLLING_INPUTS]


def add_rolling_features(data):
    """Three previous observed appearances per club, including across seasons.

    Gaps in the underlying data remain gaps; this does not repair missing games.
    Current-match outcomes/statistics are never included in their own window.
    """
    data = data.sort_values(["team", "date"], kind="stable").reset_index(drop=True).copy()
    for column, feature in zip(ROLLING_INPUTS, ROLLING_FEATURES):
        data[feature] = data.groupby("team")[column].transform(
            lambda values: values.shift(1).rolling(3, min_periods=3).mean()
        )
    return data


def verify_rolling_features(data):
    checks = 0
    for team, group in data.groupby("team", sort=False):
        for i in range(3, len(group)):
            prior = group.iloc[i - 3:i]
            for column, feature in zip(ROLLING_INPUTS, ROLLING_FEATURES):
                expected = prior[column].mean() if prior[column].notna().all() else np.nan
                actual = group.iloc[i][feature]
                equal = (np.isnan(expected) and np.isnan(actual)) or np.isclose(expected, actual)
                if not equal:
                    raise AssertionError(f"Rolling mismatch: {team}, row {i}, {feature}")
                checks += 1
    return {"checks_passed": checks, "complete_rows": int(data[ROLLING_FEATURES].notna().all(axis=1).sum())}
