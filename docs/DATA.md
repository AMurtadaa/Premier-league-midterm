# Dataset manifest and audit

## Fixed source

- Source project: https://github.com/AMurtadaa/Premier-league
- Frozen source commit: `f8b34f2cdd7f57340d5dd62191a1738fc1fe792d`
- CSV: `Backend/matches.csv` in the original project; `data/raw/matches.csv` here.
- SHA-256: `d9a5595ba17308065f0d31cd9a7713c80e60a68274fcf1603a78d09e1c1a57dd`
- Original acquisition code: `notebooks/archive/scraping.ipynb` (FBref scraping workflow).
- Source attribution is retained; no new license is asserted over the source dataset or code. Users should check upstream terms before redistribution or new collection.

## Observed coverage, not assumed coverage

| Property | Observed value |
|---|---|
| Team-appearance rows | 1,389 |
| Substantive columns | 27, plus saved CSV index |
| Date range | September 12, 2020–April 25, 2022 |
| 2020–21 (`season=2021`) | 760 rows; 20 clubs |
| 2021–22 (`season=2022`) | 629 rows; 19 clubs; partial season |
| Clubs across both seasons | 23 |
| Duplicate team/date/opponent keys | 0 |
| Home records | 694 |

Liverpool is absent from the partial 2021–22 extract. The file must not be described as two complete seasons. Team appearances are not independent fixtures: most fixtures appear twice, once for each team. The current binary experiments retain this legacy representation; the future three-class study will use one verified home-team record per fixture.

## Historical exploratory boundary

Training: dates **before January 1, 2022** (1,107 rows). Testing: dates **after January 1, 2022** (276 rows). Six January 1 records are excluded to reproduce the recording's strict inequalities. This is a historical two-way experiment, not a tuning/calibration/final-test protocol.

## Planned three-class partitions

On the current 694 home-record extract, the proposed disjoint blocks are:

| Purpose | Dates | Home records |
|---|---|---:|
| Training | September 2020–December 2021 | 554 |
| Model selection / tuning | January 2022 | 30 |
| Calibration fitting | February 2022 | 39 |
| Final holdout | March 1–April 25, 2022 | 71 |

These blocks are **planned, not completed**. Counts and fixture integrity must be rechecked before fitting. The tiny calibration and test sets, partial coverage, and missing club limit conclusions; improve coverage or extend historical data before the final study, then freeze a revised manifest before experiments. Never choose season coverage based on final-test performance.
