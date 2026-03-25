# SeaSat demo portal starter

This starter repo is designed for **seasat.org** and follows the architecture that best fits your current stack:

- **WordPress remains the main marketing site**
- the **Demo** page links to a separate app on a subdomain such as `demo.seasat.org`
- the demo app runs a **Python backend** for Earth Engine, Open-Meteo and XGBoost inference
- the frontend is a lightweight map viewer with layer toggles

## Recommended product path

### Phase 1 — fastest public demo
A fixed demo region and fixed date (or a small list of dates), with 4 map layers:
1. Sentinel-2 RGB
2. Predicted SST
3. Predicted SSS
4. Predicted Chl-a

Users only need to open the demo and toggle layers on and off.

This is the best first release because it avoids heavy live processing on every click.

### Phase 2 — queryable portal
Allow user input for:
- date
- point / polygon ROI

The backend then:
1. finds the closest Sentinel-2 image in time
2. extracts the required S2 bands + metadata
3. fetches Open-Meteo weather features
4. builds feature tables for each pixel or sampled grid
5. runs the three models
6. renders map layers back to the browser

## Why this is better than a pure Earth Engine App
A pure GEE App is attractive for speed, but it is **not the best long-term choice here** because your pipeline already depends on:

- Python
- XGBoost model serving
- Open-Meteo feature joins
- custom feature engineering
- eventual website / API integration

A GEE App is good for a quick visual prototype, but a **Python service + map frontend** is better for SeaSat as a product.

## Hosting recommendation

### Best fit for now
- **Frontend:** static page served from the same backend or from Cloudflare Pages / Netlify
- **Backend:** Railway, Render, or Azure App Service using Docker
- **Main site:** existing WordPress site on Krystal
- **Integration:** WordPress Demo page links to `https://demo.seasat.org`

### Domain setup
- `seasat.org` -> WordPress
- `demo.seasat.org` -> demo app
- optional later: `api.seasat.org` -> backend API only

## What is already known from your assets

### Chl-a
Your `remote-sensing-deployment` repo already has the right overall pattern:
- Open-Meteo weather join
- Earth Engine Sentinel-2 extraction
- closest-image logic
- cloud probability attach
- 3x3 median band sampling
- XGBoost prediction using a saved feature schema

### SST and SSS
Your uploaded JSON models are deployable, but they still need a small preprocessing wrapper that recreates the exact engineered feature columns expected by the models.

The uploaded model files show:
- `xgb_sst_s2pluswx.json` expects **117** features
- `xgb_sss_s2pluswx.json` expects **117** features
- `xgb_sst_s2only.json` expects **41** features
- `xgb_sss_s2only.json` expects **41** features

## Important deployment gap to close
For SST/SSS, the raw XGBoost JSONs tell us the **final feature names**, but not with certainty the **full training-time preprocessing recipe** for every `_scaled` field.

Examples:
- `cloud_3d_scaled`
- `t2m_inst_scaled`
- `MEAN_INCIDENCE_ZENITH_ANGLE_B1_scaled`

We can safely reconstruct:
- raw bands
- trig transforms (`sin`, `cos`)
- `log1p` transforms
- basic indices such as NDVI and ratio features if their formulas are confirmed

But to make SST/SSS predictions fully trustworthy in production, you should also provide the original feature-builder notebook or script used before training.

## Repo contents
- `backend/` FastAPI app skeleton
- `frontend/` simple Leaflet map demo
- `docs/architecture.md` deployment plan
- `docs/feature_gap.md` exact missing pieces to finalise SST/SSS
- `models/` your uploaded SST/SSS XGBoost JSONs plus a generated feature manifest

## Suggested launch order
1. Deploy a **fixed demo** first
2. Use the existing Chl-a Python path as the template
3. add SST and SSS once the exact preprocessing recipe is confirmed
4. only then expose free-date / free-ROI search to users

## What you still need to add
- `models/xgb_chla.joblib`
- GEE credentials / service account
- exact SST/SSS feature engineering notebook or script
- chosen demo bounding box and default date



## Included in this packaged version

- `models/xgb_chla.joblib` — uploaded Chl-a model
- `models/xgb_sst_from_stitched.json` — SST XGBoost retrained from stitched spreadsheet
- `models/xgb_sss_from_stitched.json` — SSS XGBoost retrained from stitched spreadsheet
- `config/demo_config.json` — fixed Mexico Gulf MVP AOI/date
- `scripts/train_models_from_stitched.py` — retrains SST/SSS locally
- `scripts/run_demo_stub.py` — placeholder entrypoint documenting the live pipeline flow

## Important hosting note

GitHub Pages can host the map UI, but it cannot run Python or do live model inference. So the fastest MVP is:

1. keep the frontend on GitHub Pages / your WordPress Demo link
2. use a fixed AOI/date
3. serve precomputed output layers (RGB, SST, SSS, Chl-a)

For a true dynamic search-by-date-and-AOI app, use either an Earth Engine App or a small backend later.
