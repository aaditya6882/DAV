"""
config.py
Configuration Layer.

Centralizes all paths, settings, and environment variables used across
the application so that no other module has to hard-code a file path.
"""

import os

# Project root directory (folder containing this file)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Flask configuration + project-wide settings."""

    # --- Flask settings ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "herald-college-sports-analytics-2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # --- Data paths ---
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

    RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "matches.csv")
    PROCESSED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, "matches_clean.csv")

    # --- Static / visualization paths ---
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    PLOTS_DIR = os.path.join(STATIC_DIR, "images", "plots")

    # Path Flask/Jinja should use when building <img src="..."> URLs
    PLOTS_URL_PREFIX = "images/plots"

    # --- Required schema for data/raw/matches.csv ---
    REQUIRED_COLUMNS = [
        "year",
        "date",
        "stage",
        "stadium",
        "city",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
    ]
