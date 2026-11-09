import unittest

import pandas as pd
from src.api import create_app
from src.recent import RecentPredictor


class RecentCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Synthetic records exercise date handling without network access.
        rows = []
        for year in (2023, 2024, 2025):
            for i, day in enumerate(pd.date_range(f"{year}-08-01", periods=32, freq="7D")):
                hg, ag = [(2, 0), (1, 1), (0, 2)][i % 3]
                rows.append((day, "Club A", "Club B", hg, ag, "HDA"[i % 3], year))
        cls.model = RecentPredictor(pd.DataFrame(
            rows, columns=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "season_start"]
        ))
        cls.client = create_app(cls.model).test_client()

    def test_range_tracks_feed_and_supports_near_future(self):
        coverage = self.client.get("/api/status").json["coverage"]
        target = str((self.model.last_date + pd.Timedelta(days=7)).date())
        self.assertGreater(coverage["max_date"], target)
        response = self.client.post("/api/predict", json={"home_team": "Club A", "away_team": "Club B",
                                                          "match_date": target, "kickoff_time": "16:30"})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(sum(response.json["probabilities"].values()), 1)
        self.assertEqual(response.json["last_result"], coverage["last_result"])

    def test_rejects_beyond_freshness_window(self):
        response = self.client.post("/predict", json={"home_team": "Club A", "away_team": "Club B",
                                                     "match_date": "2030-01-01", "kickoff_time": "16:30"})
        self.assertEqual(response.status_code, 400)

    def test_excludes_requested_day_from_form(self):
        day = pd.Timestamp("2025-08-22")
        self.assertAlmostEqual(self.model.features("Club A", "Club B", day)["home_points"], 8 / 5)
