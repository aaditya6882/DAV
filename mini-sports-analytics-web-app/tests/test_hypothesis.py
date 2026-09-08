"""
tests/test_hypothesis.py
Unit tests for the hypothesis testing service.
"""

import unittest
from app import create_app
from app.services.hypothesis_service import (
    test_home_advantage,
    test_stage_goal_intensity,
    test_outcome_uniformity,
    test_top_team_superiority,
    run_all_hypothesis_tests,
)


class TestHypothesisService(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_home_advantage(self):
        res = test_home_advantage(alpha=0.05)
        self.assertEqual(res["id"], "home_advantage")
        self.assertIn("p_value", res)
        self.assertIsInstance(res["p_value"], float)
        self.assertIn("statistic_value", res)
        self.assertIn("sample_metrics", res)

    def test_stage_goal_intensity(self):
        res = test_stage_goal_intensity(alpha=0.05)
        self.assertEqual(res["id"], "stage_intensity")
        self.assertIn("p_value", res)
        self.assertIn("stage_breakdown", res)
        self.assertGreater(len(res["stage_breakdown"]), 0)

    def test_outcome_uniformity(self):
        res = test_outcome_uniformity(alpha=0.05)
        self.assertEqual(res["id"], "outcome_uniformity")
        self.assertIn("p_value", res)
        self.assertIn("outcome_counts", res)
        self.assertEqual(res["outcome_counts"]["total_matches"], 64)

    def test_top_team_superiority(self):
        res = test_top_team_superiority(alpha=0.05)
        self.assertEqual(res["id"], "top_team_superiority")
        self.assertIn("p_value", res)
        self.assertIn("group_metrics", res)

    def test_run_all_hypothesis_tests(self):
        summary = run_all_hypothesis_tests(alpha=0.05)
        self.assertEqual(summary["total_tests"], 4)
        self.assertEqual(len(summary["tests"]), 4)
        self.assertIn("significant_findings", summary)


if __name__ == "__main__":
    unittest.main()
