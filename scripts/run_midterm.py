"""Re-run the documented binary experiment and current supplemental comparison."""
from pathlib import Path
import argparse, json, sys
from datetime import datetime, timezone
import platform

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import load_matches, prepare_binary, dataset_audit, BASE_FEATURES
from src.features import add_rolling_features, verify_rolling_features, ROLLING_FEATURES
from src.experiments import models, evaluate
import sklearn, pandas, numpy


def run(all_models=False):
    raw = load_matches()
    data = prepare_binary(raw)
    rolling = add_rolling_features(data)
    checks = verify_rolling_features(rolling)
    complete = rolling.dropna(subset=ROLLING_FEATURES).reset_index(drop=True)
    results = []
    for name, model in models().items():
        if name != "Random Forest" and not all_models:
            continue
        for feature_set, frame, columns in [
            ("four pre-match metadata fields", data, BASE_FEATURES),
            ("metadata + eight lagged form fields", complete, BASE_FEATURES + ROLLING_FEATURES),
        ]:
            results.append({"model": name, "feature_set": feature_set, **evaluate(model, frame, columns)})
    return {
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "provenance": "Reconstructed/re-run during snapshot preparation; not original semester execution logs.",
        "target": "binary team win=1; draw/loss=0; NOT fixture-level three-class probabilities",
        "calibrated": False,
        "versions": {"python": platform.python_version(), "sklearn": sklearn.__version__, "pandas": pandas.__version__, "numpy": numpy.__version__},
        "dataset": dataset_audit(raw), "rolling_verification": checks, "experiments": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-models", action="store_true", help="Additional comparison prepared now, not archived Week 5-6 scores.")
    parser.add_argument("--output", default=str(ROOT / "artifacts" / "generated" / "metrics.json"))
    args = parser.parse_args()
    result = run(args.all_models)
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    for row in result["experiments"]:
        print(f"{row['model']:20} | {row['feature_set']:36} | accuracy={row['accuracy']:.4f} win_precision={row['win_precision']:.4f}")
    print(f"Rolling checks: {result['rolling_verification']}; saved {path}")
