"""Phase 2 - Data preprocessing: clean types, duplicates, missing values, outliers."""
import pandas as pd
from config import MERGED_CSV, CLEAN_CSV

NUMERIC = ["price", "demand", "wheat_price", "rainfall"]


def preprocess():
    df = pd.read_csv(MERGED_CSV)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "region"]).drop_duplicates(subset=["date", "region"])
    df = df.sort_values(["region", "date"]).reset_index(drop=True)

    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # fill gaps inside each region's time series
        df[col] = df.groupby("region")[col].transform(lambda s: s.interpolate().bfill().ffill())

    # clip extreme outliers using the IQR rule
    for col in NUMERIC:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        df[col] = df[col].clip(q1 - 3 * iqr, q3 + 3 * iqr)

    df.drop(columns=["source_file"], errors="ignore").to_csv(CLEAN_CSV, index=False)
    print(f"Clean data saved: {df.shape[0]} rows -> {CLEAN_CSV}")


if __name__ == "__main__":
    preprocess()
