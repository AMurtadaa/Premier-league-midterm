# Cumulative progress: Weeks 1–7

This account separates historical evidence, reported work, and code reconstructed now. No commit dates have been backdated.

| Stage | Significant work and output | Evidence / limitation |
|---|---|---|
| Week 1 | Defined Premier League forecasting problem, three-class research goal, probability evaluation and pre-match feature strategy. | Assignment 1 framing carried into approved proposal; proposal documents are private submissions, not republished here. |
| Week 2 | Planned chronological evaluation, leakage controls, model comparisons, ablations, interpretability and React/Python prototype. | Approved proposal; exact coverage and separate calibration partition required clarification. |
| Weeks 3–4 | Collected/preprocessed historical team-match data, converted dates and metadata, formed win/non-win target, ran Random Forest, constructed previous-three-match rolling features. | Original CSV/scraper and recorded notebook screenshots; current modules reconstruct visible methods. |
| Weeks 5–6 | Continued exploratory model comparisons and reported Logistic Regression, Random Forest and Gradient Boosting; refined data/feature preparation and discussed challenges. | Submitted progress report and Milestone 2 comparison chart. Original executable comparison notebook/protocol is unavailable, so approximate chart values are not treated as verified holdout scores. |
| Week 7 | Began the team-selection interface as the research-to-prototype transition. | Conservative allocation from a combined Weeks 7–8 source. Exact per-page completion dates are not established. The included React prototype was assembled now, not recovered as an original Week 7 commit. |

## Completed versus incomplete

Historical evidence supports data preparation, a binary Random Forest baseline, rolling form construction, and reported comparison work. Newly executed verification supplies explicit split counts, checked rolling values, and a reproducible supplemental comparison. It strengthens reproducibility **now**, not the historical record of when work was done.

At the midpoint, the final three-class target, independent calibration fitting, locked final testing, controlled ablations, and interpretation remain unfinished. The early interface is not connected to a prediction service. Completed results pages, full API integration, and later integration tests are excluded from the Week 7 scope.

## Response to instructor feedback

- **Dataset ambiguity:** `DATA.md` fixes the actual CSV, source commit, hash, seasons, dates and missing coverage.
- **Calibration/test separation:** `METHODOLOGY.md` specifies a separate planned calibration block; no test-set calibration fitting is claimed.
- **Missing experiment details:** archived observations and current verification distinguish accuracy, precision, confusion counts, dates and sample sizes.
- **Unchecked rolling features:** unit tests and a full 10,560-value audit demonstrate previous-only computation, including a manually checked Manchester City example.
- **Research before website:** the second-half roadmap puts the three-class comparison and probability study ahead of application integration.
