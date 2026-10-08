"""Phase 3 - Evaluate saved models on the test set."""
import joblib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from config import TARGETS, MODELS_DIR, REPORTS_DIR
from phase3_model_training.split_data import get_split


def evaluate():
    REPORTS_DIR.mkdir(exist_ok=True)
    results = {}
    for target in TARGETS:
        _, Xte, _, yte = get_split(target)
        model = joblib.load(MODELS_DIR / f"xgb_{target}.joblib")
        pred = model.predict(Xte)
        results[target] = {
            "MAE": mean_absolute_error(yte, pred),
            "RMSE": float(np.sqrt(mean_squared_error(yte, pred))),
            "R2": r2_score(yte, pred),
        }
        print(f"[XGBoost] {target}: " + "  ".join(f"{k}={v:.3f}" for k, v in results[target].items()))

        plt.figure(figsize=(5, 5))
        plt.scatter(yte, pred, s=6, alpha=0.5)
        lim = [min(yte.min(), pred.min()), max(yte.max(), pred.max())]
        plt.plot(lim, lim, "r--")
        plt.xlabel("Actual"); plt.ylabel("Predicted"); plt.title(f"{target}: actual vs predicted")
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / f"phase3_{target}_actual_vs_pred.png", dpi=120)
        plt.close()
    return results


if __name__ == "__main__":
    evaluate()
