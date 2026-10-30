"""Phase 2 - Plot monthly and seasonal price and demand trends."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import CLEAN_CSV, REPORTS_DIR

OUTPUT_PNG = REPORTS_DIR / "phase2_seasonal_trend.png"
REQUIRED_COLUMNS = {"date", "region", "price", "demand"}


def analyse_trends(input_csv=CLEAN_CSV, output_png=OUTPUT_PNG):
    df = pd.read_csv(input_csv)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")
    if df.empty:
        raise ValueError(f"No data found in {input_csv}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        raise ValueError(f"Invalid dates found in {input_csv}")
    for column in ("price", "demand"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["month"] = df["date"].dt.month
    monthly = (
        df.assign(period=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby(["period", "region"])[["price", "demand"]]
        .mean()
        .reset_index()
    )
    seasonal = df.groupby(["month", "region"])[["price", "demand"]].mean().reset_index()
    regions = sorted(df["region"].dropna().unique())

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for region in regions:
        monthly_region = monthly[monthly["region"] == region]
        seasonal_region = seasonal[seasonal["region"] == region]
        axes[0, 0].plot(monthly_region["period"], monthly_region["price"], label=region)
        axes[0, 1].plot(monthly_region["period"], monthly_region["demand"], label=region)
        axes[1, 0].plot(seasonal_region["month"], seasonal_region["price"], marker="o", label=region)
        axes[1, 1].plot(seasonal_region["month"], seasonal_region["demand"], marker="o", label=region)

    axes[0, 0].set_title("Monthly Average Price (Rs/quintal)")
    axes[0, 1].set_title("Monthly Average Demand (tonnes/day)")
    axes[1, 0].set_title("Seasonal Price by Month")
    axes[1, 1].set_title("Seasonal Demand by Month")
    for axis in axes.flat:
        axis.grid(True, linestyle="--", alpha=0.4)
        axis.legend()
    axes[1, 0].set_xticks(range(1, 13))
    axes[1, 1].set_xticks(range(1, 13))
    axes[1, 0].set_xlabel("Month")
    axes[1, 1].set_xlabel("Month")
    fig.tight_layout()

    output_path = Path(output_png)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
    print(f"Trend chart saved: {output_path}")


if __name__ == "__main__":
    analyse_trends()
