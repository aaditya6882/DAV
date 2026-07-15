"""
tests/test_preprocessing.py
Tests for the Data Layer (services/preprocessing.py).

Run with: python -m tests.test_preprocessing
"""

import unittest
from app import create_app
from app.services.data_loader import load_raw_data
from app.services.preprocessing import clean_data


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.raw_df = load_raw_data()

    def tearDown(self):
        self.ctx.pop()

    def test_clean_data_adds_derived_columns(self):
        df = clean_data(self.raw_df)
        for col in ["total_goals", "goal_difference", "result"]:
            self.assertIn(col, df.columns)

    def test_clean_data_has_no_missing_scores(self):
        df = clean_data(self.raw_df)
        self.assertEqual(df["home_score"].isna().sum(), 0)
        self.assertEqual(df["away_score"].isna().sum(), 0)

    def test_result_values_are_valid(self):
        df = clean_data(self.raw_df)
        self.assertTrue(set(df["result"].unique()).issubset({"home_win", "away_win", "draw"}))

    def test_total_goals_matches_scores(self):
        df = clean_data(self.raw_df)
        expected = df["home_score"] + df["away_score"]
        self.assertTrue((df["total_goals"] == expected).all())


if __name__ == "__main__":
    unittest.main()
