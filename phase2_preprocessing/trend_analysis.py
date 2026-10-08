"""Phase 2 - Trend & correlation analysis."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import FEATURES_CSV, REPORTS_DIR


def analyse_trends():
    df = pd.read_csv(FEATURES_CSV, parse_dates=["date"])
    REPORTS_DIR.mkdir(exist_ok=True)

    cols = ["price", "demand", "wheat_price", "rainfall", "month", "price_7d_avg", "demand_7d_avg"]
    corr = df[cols].corr().round(2)
    print("Correlation matrix:\n", corr)

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    df.groupby("month")["price"].mean().plot(ax=ax[0], marker="o", title="Avg price by month")
    df.groupby("month")["demand"].mean().plot(ax=ax[1], marker="o", title="Avg demand by month")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "phase2_seasonal_trend.png", dpi=120)

    plt.figure(figsize=(6, 5))
    plt.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
    plt.yticks(range(len(cols)), cols)
    plt.colorbar()
    plt.title("Correlation heatmap")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "phase2_correlation.png", dpi=120)
    print("Saved trend plots in reports/")


if __name__ == "__main__":
    analyse_trends()
