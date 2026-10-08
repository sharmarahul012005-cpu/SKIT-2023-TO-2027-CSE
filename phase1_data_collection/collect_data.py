"""Phase 1 - Collect historical millet demand & pricing data from data/raw/*.csv."""
import pandas as pd
from config import RAW_DIR, PROCESSED_DIR, MERGED_CSV, RAW_COLUMNS


def collect():
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DIR}")

    frames = []
    for f in files:
        df = pd.read_csv(f)
        missing = set(RAW_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"{f.name} is missing columns: {missing}")
        df["source_file"] = f.name
        frames.append(df[RAW_COLUMNS + ["source_file"]])

    merged = pd.concat(frames, ignore_index=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(MERGED_CSV, index=False)
    print(f"Merged {len(files)} file(s) -> {merged.shape[0]} rows saved to {MERGED_CSV}")
    return merged


if __name__ == "__main__":
    collect()
