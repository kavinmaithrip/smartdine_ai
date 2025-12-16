"""
config.py
Global configuration for SmartDine backend.
"""

import os

# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "SmartDine Recommendation API"
VERSION = "1.2.0"
DEBUG = True   # Set False in production


# ============================================================
# SERVER SETTINGS
# ============================================================

HOST = "0.0.0.0"
PORT = 8000
RELOAD = DEBUG


# ============================================================
# BASE PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# ============================================================
# DATA FILES
# ============================================================

CLEANED_DATA = os.path.join(PROCESSED_DIR, "smartdine_cleaned.csv")
PREPROCESSED_DATA = os.path.join(PROCESSED_DIR, "smartdine_preprocessed.csv")
CITY_STATS = os.path.join(PROCESSED_DIR, "city_stats.csv")

# ============================================================
# FAISS SETTINGS (CITY-WISE INDEXING)
# ============================================================

FAISS_DIR = os.path.join(BASE_DIR, "backend", "faiss_indexes")
FAISS_META_DIR = os.path.join(FAISS_DIR, "metadata")

# NOTE:
# Each city will have:
#   FAISS_DIR/<city>.index
#   FAISS_META_DIR/<city>.pkl


# ============================================================
# MODEL SETTINGS
# ============================================================

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


# ============================================================
# RECOMMENDATION POLICY (INTERNAL DEFAULTS)
# ============================================================

FAISS_TOP_K = 40        # semantic retrieval depth
RETURN_K = 5            # final recommendations shown to user

# These are INTERNAL policy values.
# They are NOT part of API contract.


# ============================================================
# LOGGING
# ============================================================

LOG_DIR = os.path.join(BASE_DIR, "backend", "logs")
LOG_FILE = os.path.join(LOG_DIR, "smartdine.log")
