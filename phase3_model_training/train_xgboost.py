"""Phase 3 - Train XGBoost models for demand and price and save them."""
import joblib
from xgboost import XGBRegressor
from config import TARGETS, MODELS_DIR, RANDOM_STATE
from phase3_model_training.split_data import get_split

DEFAULT_PARAMS = dict(
    n_estimators=300, max_depth=5, learning_rate=0.05,
    subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE,
)


def train(params=None):
    MODELS_DIR.mkdir(exist_ok=True)
    for target in TARGETS:
        Xtr, Xte, ytr, yte = get_split(target)
        model = XGBRegressor(**(params or DEFAULT_PARAMS))
        model.fit(Xtr, ytr)
        joblib.dump(model, MODELS_DIR / f"xgb_{target}.joblib")
        print(f"Trained & saved models/xgb_{target}.joblib")


if __name__ == "__main__":
    train()
