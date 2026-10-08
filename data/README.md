# Data

Put the historical millet dataset (CSV) in `data/raw/`.

Required columns: `date, region, price, demand, wheat_price, rainfall`

- `region`: "Mandi A" / "Mandi B"
- `price`: Rs per quintal, `demand`: tonnes per day
- `wheat_price`: Rs per quintal, `rainfall`: mm

No dataset yet? Run `python -m phase1_data_collection.generate_sample_data` to make a **synthetic sample for testing only**.
