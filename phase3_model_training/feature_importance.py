"""Phase 3 - Which inputs matter most for each model?"""
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import TARGETS, MODELS_DIR, REPORTS_DIR


def plot_importance():
    REPORTS_DIR.mkdir(exist_ok=True)
    for target, feats in TARGETS.items():
        model = joblib.load(MODELS_DIR / f"xgb_{target}.joblib")
        imp = sorted(zip(feats, model.feature_importances_), key=lambda x: x[1])
        plt.figure(figsize=(6, 3))
        plt.barh([f for f, _ in imp], [v for _, v in imp], color="#2e6b35")
        plt.title(f"Feature importance - {target}")
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / f"phase3_{target}_importance.png", dpi=120)
        plt.close()
        print(target, {f: round(float(v), 3) for f, v in imp[::-1]})


if __name__ == "__main__":
    plot_importance()
