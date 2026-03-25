"""MVP placeholder for fixed AOI/date demo.

This script documents the flow needed for the full backend:
1. Read config/demo_config.json
2. Pull closest Sentinel-2 image for bbox/date (via Earth Engine or pre-export)
3. Build feature stack: S2 bands + metadata + weather variables
4. Run SST / SSS / Chl-a models over pixels
5. Export rasters/tiles for the frontend layer toggles

For tonight's MVP on GitHub Pages, the frontend can point at pre-generated layer URLs.
GitHub Pages cannot run Python server-side, so live inference needs either:
- Earth Engine App, or
- a tiny backend on Render/Railway, or
- precomputed static outputs committed to the repo.
"""
import json, os
cfg = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'demo_config.json')))
print(json.dumps(cfg, indent=2))
print('Next step: connect EE/weather fetch + raster inference pipeline.')
