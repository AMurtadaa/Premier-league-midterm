"""Generate notebook companions and capture actual Python execution output.

These are newly reconstructed notebooks, not original semester files.
Code cells are executed sequentially in one namespace; no historical execution
counts or scores are invented. Jupyter can subsequently re-run the same cells.
"""
from pathlib import Path
from datetime import datetime, timezone
from contextlib import redirect_stdout
import io, json, os, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code(text):
    return {"cell_type": "code", "metadata": {}, "source": text.splitlines(keepends=True), "execution_count": None, "outputs": []}

SETUP = '''from pathlib import Path
import sys, json
ROOT = Path.cwd() if (Path.cwd() / "src").exists() else Path.cwd().parent
sys.path.insert(0, str(ROOT))
from src.data import load_matches, prepare_binary, dataset_audit, chronological_split, BASE_FEATURES
from src.features import add_rolling_features, verify_rolling_features, ROLLING_FEATURES
from src.experiments import models, evaluate
'''

def save(name, cells):
    namespace = {"__name__": "__main__"}
    count = 0
    for cell in cells:
        if cell["cell_type"] != "code":
            continue
        count += 1
        output = io.StringIO()
        with redirect_stdout(output):
            exec(compile("".join(cell["source"]), name, "exec"), namespace)
        cell["execution_count"] = count
        cell["outputs"] = [{"output_type": "stream", "name": "stdout", "text": output.getvalue().splitlines(keepends=True)}] if output.getvalue() else []
    notebook = {"nbformat": 4, "nbformat_minor": 5, "cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": sys.version.split()[0]},
        "snapshot_provenance": "Reconstructed and executed during snapshot preparation, not an original semester notebook.",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
    }}
    for index, cell in enumerate(cells):
        cell["id"] = f"cell-{index:03d}"
    path = ROOT / "notebooks" / name
    path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print(f"Executed {count} code cells: {path.name}")

if __name__ == "__main__":
    os.chdir(ROOT)
    save("01_data_and_features.ipynb", [
        markdown("# Data coverage and lagged form audit\n\nReconstructed midterm companion, executed now. Original source CSV and scraper are preserved separately. These outputs verify reproducibility; they do not backdate work."),
        code(SETUP),
        code('raw = load_matches()\nprint(json.dumps(dataset_audit(raw), indent=2))'),
        markdown("## Explicit historical split\n\nStrict inequalities reproduce the recorded binary experiment. The cutoff-day records are excluded. This is not the planned four-way three-class protocol."),
        code('train, test = chronological_split(raw)\nprint(f"Train: {len(train)} rows, through {train.date.max().date()}")\nprint(f"Test: {len(test)} rows, from {test.date.min().date()}")\nprint("Excluded cutoff rows:", int(raw.date.eq("2022-01-01").sum()))'),
        markdown("## Rolling features: prior appearances only\n\nEach value is checked against the previous three rows of the same team. The Manchester City example must equal 10/3 goals for and 1/3 goals against."),
        code('rolling = add_rolling_features(raw)\nprint(json.dumps(verify_rolling_features(rolling), indent=2))\nexample = rolling[(rolling.team == "Manchester City") & rolling.date.eq("2021-09-11")]\nprint(example[["date", "team", "gf_rolling", "ga_rolling"]].to_string(index=False))'),
        markdown("## Remaining work\n\nAudit one record per fixture, fix missing coverage, build H/D/A targets, and freeze training/tuning/calibration/final-test partitions before the final research comparison."),
    ])
    save("02_binary_experiments.ipynb", [
        markdown("# Binary baseline and supplemental comparison\n\nReconstructed and executed during snapshot preparation. RF settings reproduce recorded code. Logistic Regression and Gradient Boosting results below are supplemental executions now, not original Weeks 5–6 logs. No calibration is fitted."),
        code(SETUP),
        code('data = prepare_binary(load_matches())\ncomplete = add_rolling_features(data).dropna(subset=ROLLING_FEATURES).reset_index(drop=True)\nprint("Target: team win=1; draw/loss=0")\nprint("Raw rows:", len(data), "complete rolling rows:", len(complete))'),
        code('result = evaluate(models()["Random Forest"], data, BASE_FEATURES)\nprint(json.dumps(result, indent=2))'),
        markdown("The recorded baseline achieved 61.23% accuracy, below the 62.32% always-non-win baseline. Accuracy alone is not enough. The final project must evaluate three-class probabilities and calibration separately."),
        code('rolling_result = evaluate(models()["Random Forest"], complete, BASE_FEATURES + ROLLING_FEATURES)\nprint(json.dumps(rolling_result, indent=2))'),
        markdown("Recorded rolling **precision** was 0.625. The complete score set above is from this new execution. Eligible rows differ between raw and rolling runs; a final ablation must use the same fixtures."),
        code('for name, estimator in models().items():\n    row = evaluate(estimator, complete, BASE_FEATURES + ROLLING_FEATURES)\n    print(f"{name:20} accuracy={row[\'accuracy\']:.4f} win_precision={row[\'win_precision\']:.4f} log_loss={row[\'binary_log_loss\']:.4f}")'),
        markdown("## Next stage\n\nDo not use these exploratory test scores to claim a calibrated final system. See `docs/METHODOLOGY.md` for independent tuning/calibration/final testing, three-class metrics, controlled feature ablation, and interpretation."),
    ])
