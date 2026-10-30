"""Phase 2 - Split feature data chronologically into training and test sets."""
from pathlib import Path

import pandas as pd

from config import FEATURES_CSV, PROCESSED_DIR, TEST_FRACTION

TRAIN_CSV = PROCESSED_DIR / "train.csv"
TEST_CSV = PROCESSED_DIR / "test.csv"


def split_dataset(
    input_csv=FEATURES_CSV,
    train_csv=TRAIN_CSV,
    test_csv=TEST_CSV,
    test_fraction=TEST_FRACTION,
):
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")

    df = pd.read_csv(input_csv)
    missing_columns = {"date", "region"}.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")
    if df.empty:
        raise ValueError(f"No data found in {input_csv}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        raise ValueError(f"Invalid dates found in {input_csv}")

    dates = df["date"].drop_duplicates().sort_values().reset_index(drop=True)
    if len(dates) < 2:
        raise ValueError("At least two distinct dates are required for a chronological split")

    split_index = int(len(dates) * (1 - test_fraction))
    split_index = min(max(split_index, 1), len(dates) - 1)
    cutoff = dates.iloc[split_index]
    train = df[df["date"] < cutoff].sort_values(["date", "region"]).reset_index(drop=True)
    test = df[df["date"] >= cutoff].sort_values(["date", "region"]).reset_index(drop=True)

    train_csv = Path(train_csv)
    test_csv = Path(test_csv)
    train_csv.parent.mkdir(parents=True, exist_ok=True)
    test_csv.parent.mkdir(parents=True, exist_ok=True)
    train.to_csv(train_csv, index=False)
    test.to_csv(test_csv, index=False)
    print(f"Training data: {len(train)} rows -> {train_csv}")
    print(f"Test data: {len(test)} rows -> {test_csv}")
    print(f"Chronological cutoff: {cutoff.date()}")


if __name__ == "__main__":
    split_dataset()
