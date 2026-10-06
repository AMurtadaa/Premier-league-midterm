import unittest
import hashlib
import pandas as pd
import numpy as np
from src.data import load_matches, prepare_binary, chronological_split, DATASET
from src.features import add_rolling_features, verify_rolling_features, ROLLING_INPUTS, ROLLING_FEATURES


class ResearchChecks(unittest.TestCase):
    def test_frozen_csv_checksum(self):
        self.assertEqual(hashlib.sha256(DATASET.read_bytes()).hexdigest(),
                         "d9a5595ba17308065f0d31cd9a7713c80e60a68274fcf1603a78d09e1c1a57dd")

    def test_binary_target_keeps_draws_non_win(self):
        data = prepare_binary(load_matches())
        self.assertTrue(data.loc[data.result == "W", "target"].eq(1).all())
        self.assertTrue(data.loc[data.result.isin(["D", "L"]), "target"].eq(0).all())

    def test_chronological_boundary_is_explicit(self):
        data = load_matches()
        train, test = chronological_split(data)
        self.assertEqual((len(train), len(test)), (1107, 276))
        self.assertEqual(int(data.date.eq("2022-01-01").sum()), 6)
        self.assertLess(train.date.max(), test.date.min())

    def test_no_current_or_future_match_enters_form(self):
        data = add_rolling_features(load_matches())
        row = data[(data.team == "Manchester City") & data.date.eq("2021-09-11")].iloc[0]
        self.assertAlmostEqual(row.gf_rolling, 10 / 3)
        self.assertAlmostEqual(row.ga_rolling, 1 / 3)
        changed = load_matches()
        changed.loc[(changed.team == "Manchester City") & (changed.date >= "2021-09-11"), "gf"] = 9999
        recalculated = add_rolling_features(changed)
        value = recalculated[(recalculated.team == "Manchester City") & recalculated.date.eq("2021-09-11")].iloc[0].gf_rolling
        self.assertAlmostEqual(value, row.gf_rolling)

    def test_first_three_appearances_have_no_complete_history(self):
        data = add_rolling_features(load_matches())
        for _, group in data.groupby("team"):
            self.assertTrue(group.iloc[:3][ROLLING_FEATURES].isna().all().all())

    def test_all_rolling_values_match_prior_rows(self):
        result = verify_rolling_features(add_rolling_features(load_matches()))
        self.assertEqual(result, {"checks_passed": 10560, "complete_rows": 1317})


if __name__ == "__main__":
    unittest.main()
