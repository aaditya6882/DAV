"""
tests/test_loader.py
Tests for the Data Layer (services/data_loader.py).

Run with: python -m tests.test_loader
"""

import unittest
from app import create_app
from app.services.data_loader import load_raw_data, get_file_paths


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_get_file_paths_returns_expected_keys(self):
        paths = get_file_paths()
        for key in ["raw_dir", "processed_dir", "raw_file", "processed_file"]:
            self.assertIn(key, paths)

    def test_load_raw_data_returns_dataframe_with_rows(self):
        df = load_raw_data()
        self.assertGreater(len(df), 0)

    def test_load_raw_data_has_required_columns(self):
        df = load_raw_data()
        required = self.app.config["REQUIRED_COLUMNS"]
        for col in required:
            self.assertIn(col, df.columns)


if __name__ == "__main__":
    unittest.main()
