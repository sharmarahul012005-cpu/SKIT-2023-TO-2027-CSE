"""Phase 5 - Prediction speed and accuracy summary."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "phase4_integration" / "backend"))
from predictor import predict
from phase3_model_training.evaluate import evaluate

sample = dict(region=0, month=12, price=2600, demand_7d_avg=150)
predict("demand", sample)  # warm-up (loads model)
start = time.perf_counter()
for _ in range(200):
    predict("demand", sample)
ms = (time.perf_counter() - start) / 200 * 1000
print(f"Average latency: {ms:.2f} ms per prediction")
evaluate()
