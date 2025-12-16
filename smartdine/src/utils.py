"""
utils.py
Reusable helper functions for SmartDine project.
"""

import os
import json
import numpy as np
import pandas as pd


# ------------------------------
# File Helpers
# ------------------------------

def load_csv(path: str) -> pd.DataFrame:
    """Safe CSV loader with error handling."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: str):
    """Safe CSV writer."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def load_npy(path: str) -> np.ndarray:
    """Load numpy array with safety checks."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Numpy file not found: {path}")
    return np.load(path)


# ------------------------------
# Text & Normalization Helpers
# ------------------------------

def clean_text(text: str) -> str:
    """Basic cleanup for text inputs."""
    if not isinstance(text, str):
        return ""
    return text.strip().lower()


def normalize_city(city: str) -> str:
    """
    Normalize city names consistently across the project.

    IMPORTANT:
    - Must return lowercase
    - Must NOT title-case

    Reason:
    FAISS indexes, dataframe city column,
    and city_stats all use lowercase keys.
    """
    return clean_text(city)


# ------------------------------
# Recommendation Helpers
# ------------------------------

def price_bucket(is_expensive: int) -> str:
    """Convert binary price flag into human-readable bucket."""
    return "expensive" if is_expensive == 1 else "affordable"


def rating_bucket(is_highly_rated: int) -> str:
    """Convert rating flag into text."""
    return "highly rated" if is_highly_rated == 1 else "average rated"


def safe_std(series: pd.Series) -> float:
    """
    Robust standard deviation to avoid division explosions.
    """
    std = series.std()
    return std if std and std > 1e-3 else 1.0


# ------------------------------
# Randomness Helpers
# ------------------------------

def smart_random_sample(df: pd.DataFrame, n: int = 1) -> pd.DataFrame:
    """
    Sample rows safely even when df is small.
    """
    if df.empty:
        return df
    n = min(len(df), n)
    return df.sample(n)


# ------------------------------
# JSON Helpers
# ------------------------------

def save_json(obj, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)


def load_json(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)
