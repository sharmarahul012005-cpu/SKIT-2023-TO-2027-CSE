"""Phase 4 - Loads the trained models and makes predictions."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import joblib
import pandas as pd
from config import MODELS_DIR, TARGETS

_models = {}


def _get_model(target):
    if target not in _models:
        _models[target] = joblib.load(MODELS_DIR / f"xgb_{target}.joblib")
    return _models[target]


def predict(target, inputs):
    """target: 'price' or 'demand'; inputs: dict with the model's feature names."""
    feats = TARGETS[target]
    missing = [f for f in feats if f not in inputs]
    if missing:
        raise ValueError(f"Missing inputs: {missing}")
    row = pd.DataFrame([{f: float(inputs[f]) for f in feats}])
    return float(_get_model(target).predict(row)[0])
