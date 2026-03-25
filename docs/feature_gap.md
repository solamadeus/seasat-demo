# Feature gap for SST / SSS deployment

## What we know
From the uploaded XGBoost JSON files, the models expect final engineered columns including:

- raw Sentinel-2 bands (`B1`, `B2`, ..., `B12`, `B8A`, `B9`)
- image cloud metrics
- solar irradiance metadata
- trig transforms for incidence / solar angles
- ratio features such as `chl_ratio`, `moisture_ratio`, `turbidity_ratio`
- `log1p` versions of some ratios and precipitation variables
- weather variables for the `s2pluswx` models
- `_scaled` versions of multiple variables

## What is safe to recreate now
- `sin(angle)` / `cos(angle)`
- `log1p(x)`
- NDVI if formula is confirmed
- raw Open-Meteo features
- raw S2 bands and metadata

## What needs confirmation before production use
These should be confirmed from the original notebook / script:

1. Exact formulas for:
   - `chl_ratio`
   - `moisture_ratio`
   - `turbidity_ratio`
   - any other custom band ratios

2. Exact scaling recipe for every `*_scaled` feature:
   - min-max?
   - z-score?
   - fixed physical divisor?

3. Whether the SST / SSS features are built from:
   - single-pixel values
   - 3x3 median values
   - clipped-region medians

4. Whether weather timestamps are matched to:
   - requested datetime
   - image acquisition hour
   - nearest hourly weather sample

## Why this matters
The JSON model only stores the trained tree ensemble and feature names.
It does **not** guarantee the exact preprocessing recipe used before fitting.

A small mismatch here can make the predictions look plausible but be wrong.

## Practical fix
Upload or point to the training feature-builder script / notebook for SST and SSS.
Once that is available, the backend in this starter repo can be finalised quickly.

