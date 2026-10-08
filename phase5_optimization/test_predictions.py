"""Phase 5 - Test prediction inputs and outputs.  Run:  pytest phase5_optimization -v"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "phase4_integration" / "backend"))
import pytest
from predictor import predict

PRICE_IN = dict(region=0, month=12, wheat_price=2400, rainfall=10, price_7d_avg=2600)
DEMAND_IN = dict(region=0, month=12, price=2600, demand_7d_avg=150)


def test_price_output_is_reasonable():
    assert 1000 < predict("price", PRICE_IN) < 5000


def test_demand_output_is_reasonable():
    assert 0 < predict("demand", DEMAND_IN) < 1000


def test_missing_input_raises():
    with pytest.raises(ValueError):
        predict("price", {"region": 0})


def test_higher_recent_price_raises_prediction():
    low = predict("price", {**PRICE_IN, "price_7d_avg": 2400})
    high = predict("price", {**PRICE_IN, "price_7d_avg": 2900})
    assert high > low
