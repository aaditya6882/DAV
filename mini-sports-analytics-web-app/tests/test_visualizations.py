"""
tests/test_visualizations.py
Tests for the Visualization Layer.

Run with: python -m tests.test_visualizations
"""

import os
import unittest
from app import create_app
from app.services.data_loader import load_raw_data
from app.services.preprocessing import clean_data
from app.services.visualizations.generate import generate_all_plots


class TestVisualizations(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        raw_df = load_raw_data()
        self.df = clean_data(raw_df)

    def tearDown(self):
        self.ctx.pop()

    def test_generate_all_plots_returns_metadata_for_each_plot(self):
        plots = generate_all_plots(self.df)
        self.assertGreaterEqual(len(plots), 5)
        for plot in plots:
            for key in ["title", "filename", "caption", "url"]:
                self.assertIn(key, plot)

    def test_generated_plot_files_exist_on_disk(self):
        plots = generate_all_plots(self.df)
        plots_dir = self.app.config["PLOTS_DIR"]
        for plot in plots:
            filepath = os.path.join(plots_dir, plot["filename"])
            self.assertTrue(os.path.exists(filepath), f"Missing plot file: {filepath}")


if __name__ == "__main__":
    unittest.main()
