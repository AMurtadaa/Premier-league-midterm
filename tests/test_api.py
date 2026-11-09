import unittest

import pandas as pd
from src.api import create_app
from src.data import load_matches
from src.predictor import load_predictor


FIXTURE = dict(home_team="Manchester City", away_team="Manchester United",
               match_date="2022-03-06", kickoff_time="16:30")


class PredictionApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = create_app(load_predictor()).test_client()

    def test_returns_three_normalized_probabilities(self):
        response = self.client.post("/api/predict", json=FIXTURE)
        self.assertEqual(response.status_code, 200)
        values = response.json["probabilities"]
        self.assertEqual(set(values), {"home_win", "draw", "away_win"})
        self.assertAlmostEqual(sum(values.values()), 1)
        self.assertTrue(all(0 < value < 1 for value in values.values()))
        other = self.client.post("/api/predict", json={**FIXTURE, "away_team": "Chelsea"})
        self.assertEqual(other.status_code, 200)
        self.assertNotEqual(values, other.json["probabilities"])

    def test_rejects_invalid_and_out_of_coverage_requests(self):
        for change in ({"away_team": "Manchester City"}, {"away_team": "Sunderland"},
                       {"match_date": "2022-01-01"}, {"match_date": "2025-03-01"},
                       {"match_date": "2022-02-30"}, {"kickoff_time": "30:00"}):
            with self.subTest(change=change):
                response = self.client.post("/predict", json={**FIXTURE, **change})
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json)
        self.assertEqual(self.client.post("/predict", json={}).status_code, 400)

    def test_feature_lookup_excludes_same_day_and_future_rows(self):
        features = load_predictor().features(FIXTURE["home_team"], FIXTURE["away_team"],
                                             pd.Timestamp(FIXTURE["match_date"]), FIXTURE["kickoff_time"])
        data = load_matches()
        for side in ("home", "away"):
            prior = data.loc[data.team.eq(FIXTURE[f"{side}_team"]) & data.date.lt(FIXTURE["match_date"])]
            self.assertAlmostEqual(features[f"{side}_gf"], prior.sort_values("date").tail(3).gf.mean())

    def test_evaluation_has_a_nonempty_holdout(self):
        status = self.client.get("/api/status").json
        self.assertGreater(status["evaluation"]["test_fixtures"], 0)
        self.assertIn("Manchester City", status["teams"])
