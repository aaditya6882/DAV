"""
services/data_loader.py
Data Layer — Data Engineer role.

Responsible ONLY for reading raw data off disk and knowing where files
live. Contains no cleaning or business logic (that belongs to
preprocessing.py / eda.py / statistics.py).
"""

import os
import pandas as pd
from flask import current_app


def get_file_paths():
    """
    Manage file paths for raw and processed data.

    Returns
    -------
    dict with keys: raw_dir, processed_dir, raw_file, processed_file
    """
    cfg = current_app.config
    return {
        "raw_dir": cfg["RAW_DATA_DIR"],
        "processed_dir": cfg["PROCESSED_DATA_DIR"],
        "raw_file": cfg["RAW_DATA_FILE"],
        "processed_file": cfg["PROCESSED_DATA_FILE"],
    }


def load_raw_data(path=None):
    """
    Load raw dataset from data/raw/.

    Parameters
    ----------
    path : str, optional
        Override path to a CSV file. Defaults to config.RAW_DATA_FILE.

    Returns
    -------
    pandas.DataFrame
    """
    if path is None:
        path = current_app.config["RAW_DATA_FILE"]

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw data file not found at {path}. "
            "Place a matches.csv file in data/raw/ (see Section 7 of the "
            "instruction set for the required schema)."
        )

    df = pd.read_csv(path)
    return df


def load_processed_data(path=None):
    """
    Load cleaned dataset from data/processed/. Falls back to cleaning
    the raw data on the fly if a processed file does not yet exist.
    """
    if path is None:
        path = current_app.config["PROCESSED_DATA_FILE"]

    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["date"])

    # Lazy import to avoid a circular import between data_loader and
    # preprocessing at module load time.
    from app.services.preprocessing import clean_data, save_processed_data

    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    save_processed_data(clean_df)
    return clean_df
