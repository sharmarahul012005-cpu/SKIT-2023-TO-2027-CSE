"""Phase 3 - Time-based train/test split (no shuffling, avoids data leakage)."""
import pandas as pd
from config import FEATURES_CSV, TARGETS, TEST_FRACTION


def get_split(target):
    df = pd.read_csv(FEATURES_CSV, parse_dates=["date"]).sort_values("date")
    cut = int(len(df) * (1 - TEST_FRACTION))
    train, test = df.iloc[:cut], df.iloc[cut:]
    feats = TARGETS[target]
    return train[feats], test[feats], train[target], test[target]


if __name__ == "__main__":
    for t in TARGETS:
        Xtr, Xte, ytr, yte = get_split(t)
        print(f"{t}: train={len(Xtr)}, test={len(Xte)}")
