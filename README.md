# Premier League Match-Outcome Prediction

**Murtadaa Aliu · Junior Seminar · Weeks 1–7 scope**

A machine-learning research project investigating reliable Premier League match-outcome prediction. This repository brings together the cumulative midterm evidence, reproducible experiments, and an early React team-selection prototype.

## Progress through the first seven weeks

| Period | Research progression | Supporting material |
|---|---|---|
| Week 1 | Defined the forecasting problem and three-class research objective | Assignment 1 and proposal framing |
| Week 2 | Planned chronological evaluation, leakage controls, calibration, and model comparisons | Approved project proposal |
| Weeks 3–4 | Prepared match data, implemented a binary baseline, and calculated rolling form | Original CSV, scraper, and recorded notebook evidence |
| Weeks 5–6 | Reported exploratory comparisons across three model families and refined the research direction | Submitted progress report and comparison chart |
| Week 7 | Began the transition from research workflow to team-selection interface design | Combined Weeks 7–8 design evidence; exact completion boundary is qualified |

The [cumulative progress record](docs/PROGRESS.md) connects each stage to its evidence and distinguishes completed research from remaining milestones.

## Research goal and midpoint status

The final research goal is calibrated **home-win / draw / away-win** probabilities using pre-match features, chronological evaluation, model comparison, ablations, and interpretability. The midpoint experiments instead predict **a team's win versus non-win**. They are exploratory baselines, not the finished three-class system.

| Component | Midterm status |
|---|---|
| Frozen historical CSV and original scraping notebook | Included, with provenance and coverage audit |
| Binary Random Forest baseline and lagged form experiment | Reconstructed from recorded notebook evidence; reproducible |
| Rolling feature checks and chronological split details | Reproducibility verification included |
| Logistic Regression / Random Forest / Gradient Boosting | Reported comparison plus a separately labeled supplemental experiment |
| Team-selection interface | Early prototype; no prediction API or invented probabilities |
| Three-class fixture model, calibration, final test, interpretability | Planned / incomplete |

## Evidence and results

The archived recording shows a 1,107-row training set and 276-row test set, using a strict January 1, 2022 boundary. Six boundary-day rows are excluded. Its Random Forest baseline reports **61.23% accuracy** and **47.46% win precision**. The always-non-win baseline achieves **62.32% accuracy**, so the metadata-only model does not beat that baseline. Adding eight lagged form features raises recorded **win precision to 62.50%**—this is precision, not accuracy.

![Recorded chronological split](evidence/recorded_rf_split.png)

![Recorded binary Random Forest metrics](evidence/recorded_rf_metrics.png)

The rolling audit checks **10,560 values**, producing **1,317 complete-history rows**. It uses only each team's previous three appearances, excluding the current match.

![Recorded rolling-feature implementation](evidence/recorded_rolling_code.png)

![Recorded rolling-model precision](evidence/recorded_rolling_precision.png)

See [evidence provenance](evidence/README.md), [data coverage](docs/DATA.md), [week-by-week progress](docs/PROGRESS.md), [methodology and limitations](docs/METHODOLOGY.md), and [second-half roadmap](docs/ROADMAP.md).

## Reproduce the research

Requires Python 3.11 or 3.12. From the repository root:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_midterm.py
python scripts/run_midterm.py --all-models
```

Results go to `artifacts/generated/metrics.json`, with an execution timestamp, environment versions, split details, confusion matrices, and probability metrics. The checked-in [verification output](artifacts/verification/metrics.json) is supplementary reproducibility evidence, separate from [archived observations](artifacts/archived_observations.json). Binary Brier and log-loss values do **not** imply that calibration has been fitted.

For exploratory notebooks:

```sh
python -m pip install -r requirements-notebook.txt
jupyter lab
```

Open `notebooks/01_data_and_features.ipynb` and `notebooks/02_binary_experiments.ipynb`. The original scraper is preserved under `notebooks/archive/`; reproducing the experiments does not require re-scraping the web.

## Run the early interface

Requires Node.js 22.12+:

```sh
cd frontend
npm ci
npm run dev
```

Select two different teams, a date, and a kickoff time. The interface previews a request, but deliberately provides no forecast because the prediction service is not included at this midpoint. `npm run build` verifies the production build.

## Repository map

```text
data/raw/          Frozen CSV from the original project
src/               Reconstructed preparation, lagged features, experiments
scripts/           Reproducible command-line experiment runner
tests/             Target, date boundary, rolling-value and leakage checks
notebooks/         Midterm exploration and archived original scraper
evidence/          Cropped historical screenshots and provenance
artifacts/         Archived observations and supplementary verification
frontend/          Early React team-selection prototype, no model API
docs/              Progress, data limitations, methods, next milestones
```

## Evidence note

This is a curated midterm companion to the semester work, not a seven-week Git history. Reconstructed implementations and supplementary verification are distinguished from archived evidence in the [provenance record](evidence/README.md). The [original project](https://github.com/AMurtadaa/Premier-league) is retained as the source reference. Later integration and final-system work are outside this report's scope.
