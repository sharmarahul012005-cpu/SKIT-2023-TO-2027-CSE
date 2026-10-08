"""Phase 1 - Basic analysis of the collected dataset."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import MERGED_CSV, REPORTS_DIR


def analyse():
    df = pd.read_csv(MERGED_CSV, parse_dates=["date"])
    print("Shape:", df.shape)
    print("Date range:", df["date"].min().date(), "to", df["date"].max().date())
    print("\nMissing values:\n", df.isna().sum())
    print("\nSummary statistics:\n", df.describe().round(2))

    REPORTS_DIR.mkdir(exist_ok=True)
    monthly = df.groupby([df["date"].dt.to_period("M"), "region"])[["price", "demand"]].mean().reset_index()
    monthly["date"] = monthly["date"].dt.to_timestamp()
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    for region, g in monthly.groupby("region"):
        ax[0].plot(g["date"], g["price"], label=region)
        ax[1].plot(g["date"], g["demand"], label=region)
    ax[0].set_title("Monthly avg price (Rs/quintal)")
    ax[1].set_title("Monthly avg demand (tonnes)")
    ax[0].legend()
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "phase1_overview.png", dpi=120)
    print("Saved reports/phase1_overview.png")


if __name__ == "__main__":
    analyse()
