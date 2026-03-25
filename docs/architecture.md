# Architecture

## Recommended architecture

```text
WordPress (seasat.org)
    |
    |-- Home / Services / About Us
    |
    |-- Demo button -> demo.seasat.org
                        |
                        |-- Frontend map app (Leaflet)
                        |
                        |-- FastAPI backend
                               |
                               |-- Google Earth Engine feature extraction
                               |-- Open-Meteo weather join
                               |-- XGBoost inference
                               |-- Raster / GeoJSON / tile response
```

## User flow
1. User opens `demo.seasat.org`
2. Frontend loads a default region and date
3. Backend finds the nearest Sentinel-2 image
4. Backend builds four outputs:
   - RGB base layer
   - SST prediction layer
   - SSS prediction layer
   - Chl-a prediction layer
5. Frontend shows a layer control so the user can toggle products on and off

## Two release modes

### Mode A — precomputed demo
Best first release.

- Precompute one AOI/date
- Save outputs as GeoTIFF / COG / PNG overlays
- Serve those layers directly
- Very robust and cheap to host

### Mode B — on-demand inference
Best second release.

- User picks date and ROI
- Backend processes live request
- More flexible but heavier and slower
- Needs queueing / caching / request limits

## Strong recommendation
Start with **Mode A** for the public site.

That gives you:
- a polished visual demo quickly
- lower running cost
- fewer authentication headaches
- less risk of long wait times

Then add Mode B once the SST/SSS feature builder is fully locked down.

## Data path

### Chl-a path
1. input date + point / grid
2. Open-Meteo features
3. closest Sentinel-2 L1C image
4. cloud probability join
5. 3x3 median bands + metadata
6. feature alignment
7. XGBoost predict

### SST / SSS path
1. input date + point / grid
2. Sentinel-2 bands + metadata
3. Open-Meteo features for S2+weather versions
4. exact engineered features expected by XGBoost JSONs
5. prediction

## Rendering choices

### Easiest
- return PNG overlays for the chosen bounding box
- good enough for a demo

### Better
- return Cloud Optimized GeoTIFFs and serve through a tile endpoint
- better for scaling and layer control

### Best later
- use titiler or a small raster tile service
- dynamic tiles from prediction rasters

## Authentication / secrets
- Earth Engine service account credentials should never sit in WordPress
- keep all secrets in backend environment variables
- frontend should only call your backend API

## Hosting notes

### Railway / Render
Good for first deployment if the demo is light.

### Azure
Best if you want this to grow into the real SeaSat product and match future cloud processing.

## WordPress integration
Do not try to run the model code inside WordPress.

Instead:
- make a new page called `Demo`
- add a button or iframe that points to `demo.seasat.org`
- keep WordPress only as the site shell

