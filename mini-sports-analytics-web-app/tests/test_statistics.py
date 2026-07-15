"""
tests/test_statistics.py
Tests for the Business Logic Layer (services/statistics.py, services/eda.py).

Run with: python -m tests.test_statistics
"""

import unittest
from app import create_app
from app.services.data_loader import load_raw_data
from app.services.preprocessing import clean_data
from app.services import statistics as stats_service
from app.services import eda


class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        raw_df = load_raw_data()
        self.df = clean_data(raw_df)

    def tearDown(self):
        self.ctx.pop()

    def test_compute_team_stats_played_equals_wins_draws_losses(self):
        team_stats = stats_service.compute_team_stats(self.df)
        computed = team_stats["wins"] + team_stats["draws"] + team_stats["losses"]
        self.assertTrue((team_stats["played"] == computed).all())

    def test_compute_team_stats_points_formula(self):
        team_stats = stats_service.compute_team_stats(self.df)
        expected_points = team_stats["wins"] * 3 + team_stats["draws"]
        self.assertTrue((team_stats["points"] == expected_points).all())

    def test_compute_year_stats_has_expected_columns(self):
        year_stats = stats_service.compute_year_stats(self.df)
        for col in ["year", "matches", "total_goals", "avg_goals_per_match"]:
            self.assertIn(col, year_stats.columns)

    def test_generate_summary_matches_count(self):
        summary = eda.generate_summary(self.df)
        self.assertEqual(summary["n_matches"], len(self.df))

    def test_detect_outliers_returns_dataframe_subset(self):
        outliers = eda.detect_outliers(self.df, column="total_goals")
        self.assertLessEqual(len(outliers), len(self.df))


if __name__ == "__main__":
    unittest.main()
