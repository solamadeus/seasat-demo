# Scottish SST/SSS model readiness (Loch Etive)

The original models and reported metrics are in this repo. A new **candidate** training/validation script is at [scripts/retrain_validated_sst_sss.py](scripts/retrain_validated_sst_sss.py).

## Why not deploy the existing models directly?

- The 41/117-feature archived XGBoost models and their original `*_scaled` transforms require the training-time feature builder, which has not been recovered.
- UK salinity tests in `models/metrics.json` report RMSE about **7.41 PSU** (S2-only) and **9.11 PSU** (S2 + weather), with negative R². The S2 + weather SST has UK RMSE **1.86 °C**, but this is not validation for Loch Etive.
- Some models expect L1C Sentinel-2 bands including **B10**, which is **absent from the L2A surface-reflectance collection** used for visualisation in the new Loch Etive explorer. Raw reflectance bands must not be substituted across processing levels.
- Original tabular training uses `TIMESTAMP`, `TIME_DIFF` and `TIMESTAMP_DIFF`. These require provenance. A time difference to an **in-situ measurement** is not a legitimate feature for a public pixel prediction, where that measurement does not exist.
- The old stitched training example uses a random row holdout, so the saved metrics do not demonstrate Scottish site transfer.

## Prepared: reproducible candidate training

The script deliberately excludes ground-truth-related timestamps and target columns. It uses numerical features, offers optional **cyclical time features derived from verified Sentinel-2 acquisition UTC**, and reports spatial-group holdout performance. If acquisition timestamps are supplied, it also reports future-period holdout performance. Only training-fold missingness is used to select predictors.

It does not silently invent unknown `_scaled` transformations. Any columns in the input table already scaled elsewhere still require provenance and proper fold-aware preprocessing checks.

Example, **only after restoring original inputs**:

```bash
python3 scripts/retrain_validated_sst_sss.py \
  --input /path/to/df_sst.stitched.xlsx \
  --target SST \
  --satellite-time-column s2_acq_time \
  --output outputs/scottish_sst_screen
```

For salinity use `--target SSS` and the corresponding table. If the column is not definitely the satellite acquisition timestamp, **omit** the satellite-time flag. Add `--export-candidate` only if a candidate model file is required; it must still pass external Scottish site validation.

## Before publishing sea-temperature or salinity layers

1. Restore the original stitched SST and SSS training tables, the original preprocessor, and independent UK/Scottish in-situ observations.
2. Confirm band level (L1C versus L2A), numeric scaling, weather joins, calendar/time features and every expected model feature.
3. Train with an appropriate spatial block design based on actual dependence distances, plus future-period and independent site checks. Current 0.2° spatial grouping is a **screening default**, not a validated block size.
4. Produce reproducible pixel inference rasters and QA against independent observations. Reject physically implausible predictions.
5. Export fixed-date layers once and host the rendered maps and optional per-pixel stacks as static assets. No per-visit training or GEE inference.

**Current status:** Code prepared, no source matchups accessible to this session, no new model trained and no Scottish model accuracy claimed. The live MVP and original models are unchanged.
