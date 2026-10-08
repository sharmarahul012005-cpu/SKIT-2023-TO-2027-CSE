"""Phase 3 - Linear Regression baseline to compare XGBoost against."""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from config import TARGETS
from phase3_model_training.split_data import get_split


def run():
    for target in TARGETS:
        Xtr, Xte, ytr, yte = get_split(target)
        pred = LinearRegression().fit(Xtr, ytr).predict(Xte)
        print(f"[Baseline] {target}: MAE={mean_absolute_error(yte, pred):.2f}  R2={r2_score(yte, pred):.3f}")


if __name__ == "__main__":
    run()
