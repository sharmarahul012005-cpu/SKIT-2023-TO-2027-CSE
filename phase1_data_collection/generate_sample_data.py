"""Creates a SAMPLE dataset so the pipeline can be tested.
Replace data/raw/*.csv with the real millet dataset for final results."""
import numpy as np
import pandas as pd
from config import RAW_DIR

rng = np.random.default_rng(42)
dates = pd.date_range("2022-01-01", "2025-12-31", freq="D")
rows = []
for region in ["Mandi A", "Mandi B"]:
    base_p, base_d = (2500, 150) if region == "Mandi A" else (2800, 200)
    for d in dates:
        m = d.month
        season = 1 if (m >= 11 or m <= 2) else (-1 if 6 <= m <= 9 else 0)
        rain = max(0, rng.normal(40 if 6 <= m <= 9 else 8, 10))
        wheat = rng.normal(2400, 150)
        price = base_p + 100 * season - 1.5 * rain - 0.05 * (wheat - 2200) + rng.normal(0, 40)
        demand = base_d + 20 * season - 0.02 * (price - 2750) + rng.normal(0, 8)
        rows.append([d, region, price, demand, wheat, rain])

df = pd.DataFrame(rows, columns=["date", "region", "price", "demand", "wheat_price", "rainfall"])
RAW_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(RAW_DIR / "sample_millet_data.csv", index=False)
print("Saved sample data:", df.shape)
