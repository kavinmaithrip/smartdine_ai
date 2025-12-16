"""
logging.py
Logging configuration for SmartDine backend.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# -------------------------------
# LOG DIRECTORY
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "smartdine.log")

# -------------------------------
# LOGGER SETUP
# -------------------------------

def setup_logger():
    """
    Configure root logger so that:
    - App logs
    - FastAPI logs
    - Uvicorn logs
    all go through the same handlers.
    """

    logger = logging.getLogger()  # ROOT LOGGER
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # ---------------- File Handler ----------------
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2_000_000,  # 2 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    # ---------------- Console Handler ----------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # ---------------- Formatter ----------------
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ---------------- Attach Handlers ----------------
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent double logging
    logger.propagate = False

    return logger


# Initialize logger
logger = setup_logger()
