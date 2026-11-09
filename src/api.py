from flask import Flask, jsonify, request
import pandas as pd

from .predictor import load_predictor
from .recent import CACHE, RecentPredictor


def create_app(predictor=None):
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16_384
    model = predictor if predictor is not None else (
        RecentPredictor(pd.read_csv(CACHE)) if CACHE.exists() else load_predictor()
    )

    @app.get("/api/status")
    def status():
        coverage = model.coverage() if isinstance(model, RecentPredictor) else {
            "min_date": "2022-01-02", "max_date": str(model.last_date.date()),
            "last_result": str(model.last_date.date()), "source": "Bundled historical dataset",
        }
        return jsonify(teams=sorted(model.history), evaluation=model.evaluation, coverage=coverage)

    @app.post("/predict")
    @app.post("/api/predict")
    def predict():
        try:
            return jsonify(model.predict(request.get_json(silent=True)))
        except ValueError as exc:
            return jsonify(error=str(exc)), 400

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
