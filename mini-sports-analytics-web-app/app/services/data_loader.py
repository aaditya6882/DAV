"""
services/data_loader.py
Data Layer — Data Engineer role.

Responsible ONLY for reading raw data off disk and knowing where files
live. Contains no cleaning or business logic (that belongs to
preprocessing.py / eda.py / statistics.py).

Caching: DataFrames are cached in module-level dict after first load
so repeated calls within the same process do not re-read CSV files.
"""

import os
import pandas as pd
from flask import current_app

_CACHE: dict = {}


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


def load_groups_data(path=None):
    """
    Load final group-stage standings from data/raw/groups.csv.

    Returns
    -------
    pandas.DataFrame
    """
    if path is None:
        path = current_app.config["GROUPS_DATA_FILE"]

    if not os.path.exists(path):
        raise FileNotFoundError(f"Groups data file not found at {path}.")

    return pd.read_csv(path)


def load_stats_data(path=None):
    """
    Load individual player scoring stats from data/raw/stats.csv.

    Returns
    -------
    pandas.DataFrame
    """
    if path is None:
        path = current_app.config["STATS_DATA_FILE"]

    if not os.path.exists(path):
        raise FileNotFoundError(f"Stats data file not found at {path}.")

    return pd.read_csv(path)


def load_achievements_data(path=None):
    """
    Load tournament awards from data/raw/achievements.csv.

    Returns
    -------
    pandas.DataFrame
    """
    if path is None:
        path = current_app.config["ACHIEVEMENTS_DATA_FILE"]

    if not os.path.exists(path):
        raise FileNotFoundError(f"Achievements data file not found at {path}.")

    return pd.read_csv(path)


def load_processed_data(path=None):
    """
    Load cleaned dataset from data/processed/. Falls back to cleaning
    the raw data on the fly if a processed file does not yet exist.
    Results are cached in memory for the lifetime of the process.
    """
    if path is None:
        path = current_app.config["PROCESSED_DATA_FILE"]

    if path in _CACHE:
        return _CACHE[path]

    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=["date"])
        # Add match_id if missing
        if "match_id" not in df.columns:
            df.insert(0, "match_id", range(1, len(df) + 1))
        _CACHE[path] = df
        return df

    # Lazy import to avoid a circular import between data_loader and
    # preprocessing at module load time.
    from app.services.preprocessing import clean_data, save_processed_data

    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    save_processed_data(clean_df)
    if "match_id" not in clean_df.columns:
        clean_df.insert(0, "match_id", range(1, len(clean_df) + 1))
    _CACHE[path] = clean_df
    return clean_df

