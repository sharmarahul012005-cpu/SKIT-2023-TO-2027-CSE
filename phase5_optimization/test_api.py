"""Phase 5 - Test the Flask API end-to-end."""
import sys
from pathlib import Path
backend = Path(__file__).resolve().parents[1] / "phase4_integration" / "backend"
sys.path.insert(0, str(backend))
from app import app

client = app.test_client()


def test_health():
    assert client.get("/health").json["status"] == "ok"


def test_predict_price_ok():
    r = client.post("/predict/price", json=dict(region=1, month=7, wheat_price=2500, rainfall=50, price_7d_avg=2700))
    assert r.status_code == 200 and "prediction" in r.json


def test_predict_demand_ok():
    r = client.post("/predict/demand", json=dict(region=0, month=1, price=2700, demand_7d_avg=160))
    assert r.status_code == 200 and r.json["prediction"] > 0


def test_bad_input_returns_400():
    assert client.post("/predict/demand", json={"region": 0}).status_code == 400


def test_unknown_target_returns_404():
    assert client.post("/predict/rice", json={}).status_code == 404
