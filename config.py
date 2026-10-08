"""Shared paths and feature lists used by every phase."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

MERGED_CSV = PROCESSED_DIR / "merged.csv"
CLEAN_CSV = PROCESSED_DIR / "clean.csv"
FEATURES_CSV = PROCESSED_DIR / "features.csv"

# Expected raw columns: date, region, price, demand, wheat_price, rainfall
RAW_COLUMNS = ["date", "region", "price", "demand", "wheat_price", "rainfall"]

# Inputs for each model (match the fields in the web form)
PRICE_FEATURES = ["region", "month", "wheat_price", "rainfall", "price_7d_avg"]
DEMAND_FEATURES = ["region", "month", "price", "demand_7d_avg"]

TARGETS = {
    "price": PRICE_FEATURES,
    "demand": DEMAND_FEATURES,
}

TEST_FRACTION = 0.2
RANDOM_STATE = 42
