"""Phase 2 - Feature engineering: calendar, season, rolling averages."""
import pandas as pd
from config import CLEAN_CSV, FEATURES_CSV


def season_boost(month):
    if month >= 11 or month <= 2:
        return 1       # winter
    if 6 <= month <= 9:
        return -1      # monsoon
    return 0


def build_features():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["date"]).sort_values(["region", "date"])
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].apply(season_boost)
    df["region_name"] = df["region"]
    df["region"] = df["region_name"].map({"Mandi A": 0, "Mandi B": 1})

    # previous 7-day averages (shifted by 1 day so today's value is never used)
    g = df.groupby("region")
    df["price_7d_avg"] = g["price"].transform(lambda s: s.shift(1).rolling(7).mean())
    df["demand_7d_avg"] = g["demand"].transform(lambda s: s.shift(1).rolling(7).mean())

    df = df.dropna(subset=["price_7d_avg", "demand_7d_avg"]).reset_index(drop=True)
    df.to_csv(FEATURES_CSV, index=False)
    print(f"Features saved: {df.shape} -> {FEATURES_CSV}")


if __name__ == "__main__":
    build_features()
