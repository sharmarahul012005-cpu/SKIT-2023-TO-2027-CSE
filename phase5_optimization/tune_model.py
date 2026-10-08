"""Phase 5 - Hyper-parameter tuning with time-series cross-validation."""
import joblib
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
from config import TARGETS, MODELS_DIR, RANDOM_STATE
from phase3_model_training.split_data import get_split

PARAM_GRID = {
    "n_estimators": [200, 300, 500],
    "max_depth": [3, 4, 5, 6],
    "learning_rate": [0.02, 0.05, 0.1],
    "subsample": [0.7, 0.8, 1.0],
    "colsample_bytree": [0.7, 0.8, 1.0],
    "min_child_weight": [1, 3, 5],
}


def tune():
    for target in TARGETS:
        Xtr, Xte, ytr, yte = get_split(target)
        search = RandomizedSearchCV(
            XGBRegressor(random_state=RANDOM_STATE), PARAM_GRID, n_iter=15,
            cv=TimeSeriesSplit(n_splits=4), scoring="neg_mean_absolute_error",
            random_state=RANDOM_STATE, n_jobs=-1)
        search.fit(Xtr, ytr)
        pred = search.best_estimator_.predict(Xte)
        print(f"[Tuned] {target}: MAE={mean_absolute_error(yte, pred):.2f}  R2={r2_score(yte, pred):.3f}")
        print("   best params:", search.best_params_)
        joblib.dump(search.best_estimator_, MODELS_DIR / f"xgb_{target}.joblib")


if __name__ == "__main__":
    tune()
