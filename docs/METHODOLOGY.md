# Methods, evaluation, and limitations

## What is implemented

The target is binary: `W → 1`, `D/L → 0`. Four legacy metadata fields encode venue, opponent, kickoff hour and weekday. Opponent category codes reproduce the frozen historical dataset and are not a production preprocessing contract; future training must fit its encoders on training data and handle unknown teams explicitly.

Random Forest uses 50 trees, `min_samples_split=10`, and `random_state=1`, matching recorded code. The new supplemental comparison uses scaled Logistic Regression and Gradient Boosting with a fixed seed. It is not a recovered Weeks 5–6 execution.

Eight form fields—goals for/against, shots, shots on target, distance, free kicks, penalties attempted and scored—are averaged over the prior three appearances of the same team. Stable date ordering plus `shift(1).rolling(3)` excludes current-match information. Rows without a complete history are dropped. Historical data available before later test fixtures may update their form; this is sequential pre-match evaluation, not a fixed-origin multi-month forecast.

The unchanged January cutoff is used for both feature sets. Raw and rolling experiments may have different eligible samples because early-history rows are removed; report the counts rather than treating them as a fully controlled ablation. Check-in verification reports accuracy, win precision/recall/F1, macro-F1, confusion counts, binary log loss and Brier score, and always-non-win accuracy. No probability calibration has been fitted.

## Archived versus current observations

The recorded metadata-only confusion matrix is `[[141,31],[76,28]]` (actual rows, predicted columns; labels non-win, win). It implies 169/276 correct, 28/59 win precision, and 28/104 win recall. The archived rolling-model observation is 0.625 win precision; its full historical confusion matrix is not available. Do not substitute newly reconstructed scores for missing original logs.

## Next research protocol

1. Audit one home record per fixture; set target H/D/A. Verify opponent joins, coverage, duplicates and feature availability.
2. Freeze disjoint chronological training, tuning, calibration and final-test blocks as specified in `DATA.md`, revising coverage before any final testing if needed.
3. Fit preprocessing only on training data. Compare a class-frequency baseline, multinomial Logistic Regression, Random Forest and Gradient Boosting. Use tuning data for model/feature selection, not the final holdout.
4. Fit a low-complexity calibration mapping on the separate calibration block only (e.g., a temperature parameter over clipped log probabilities, fitted by multiclass log loss). Freeze model and mapping before final testing. Revisit the very small calibration sample before relying on it.
5. Report multiclass log loss, multiclass Brier score, accuracy, macro-F1, class-wise precision/recall, confusion matrices and reliability plots, comparing calibrated with uncalibrated probabilities.
6. Compare metadata-only, rolling-form and additional pre-match feature groups on the same eligible fixtures. Use permutation importance or appropriate model explanations without interpreting correlated features as causal effects.

No match's own goals, shots or other post-match statistics may enter its prediction. Future features must use prior matches only. Final-test data cannot be used to select models, thresholds, features or calibration settings.

## Prototype scope

The approved plan named Django; later materials describe Flask. Python serving-framework selection is secondary to the research comparison and remains an integration decision. The current React prototype only validates team selection and previews a request. It neither calls an API nor displays random percentages as model forecasts.
