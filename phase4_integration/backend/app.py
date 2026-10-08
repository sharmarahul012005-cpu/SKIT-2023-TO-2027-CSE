"""Phase 4 - Flask REST API connecting the ML models to the web platform.
Run from project root:  python phase4_integration/backend/app.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, jsonify, request
from flask_cors import CORS
from predictor import predict

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/predict/<target>")
def predict_route(target):
    if target not in ("price", "demand"):
        return jsonify(error="target must be 'price' or 'demand'"), 404
    try:
        value = predict(target, request.get_json(force=True))
        return jsonify(target=target, prediction=round(value, 2))
    except (ValueError, KeyError) as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)
