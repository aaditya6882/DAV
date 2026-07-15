"""
services/preprocessing.py
Data Layer — Data Engineer role.

Cleans and transforms the raw dataset into an analysis-ready DataFrame.
"""

import os
import pandas as pd
from flask import current_app


def clean_data(df):
    """
    Clean dataset: handle missing values, fix data types, add derived
    columns used throughout the analysis and visualization layers.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw dataframe as loaded from CSV.

    Returns
    -------
    pandas.DataFrame
        Cleaned, analysis-ready dataframe.
    """
    df = df.copy()

    required = current_app.config["REQUIRED_COLUMNS"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    # --- Type fixes ---
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")

    # --- Handle missing values ---
    # Drop rows with no date or no scores — they cannot be analyzed.
    df = df.dropna(subset=["date", "home_score", "away_score"])

    text_cols = ["stage", "stadium", "city", "home_team", "away_team"]
    for col in text_cols:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)

    # --- Drop exact duplicate matches ---
    df = df.drop_duplicates()

    # --- Derived columns used by EDA / statistics / visualizations ---
    df["total_goals"] = df["home_score"] + df["away_score"]
    df["goal_difference"] = df["home_score"] - df["away_score"]

    def _result(row):
        if row["home_score"] > row["away_score"]:
            return "home_win"
        if row["home_score"] < row["away_score"]:
            return "away_win"
        return "draw"

    df["result"] = df.apply(_result, axis=1)

    df = df.reset_index(drop=True)
    return df


def save_processed_data(df, path=None):
    """
    Save cleaned data to data/processed/.

    Parameters
    ----------
    df : pandas.DataFrame
    path : str, optional
        Override output path. Defaults to config.PROCESSED_DATA_FILE.
    """
    if path is None:
        path = current_app.config["PROCESSED_DATA_FILE"]

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path
