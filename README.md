# SeaSat GitHub Pages MVP

This is the fastest no-extra-hosting route for a same-day SeaSat demo.

## What this MVP is
A static web map hosted for free on GitHub Pages with:
- one fixed AOI
- one fixed date
- a base map
- optional fixed Sentinel-2 RGB overlay
- three toggleable prediction layers: SST, SSS, Chl-a

## Why this route
For tonight, this avoids:
- backend hosting
- API secrets on a public server
- live Earth Engine authentication in the browser

## Folder layout
- `index.html` - the page
- `style.css` - styling
- `app.js` - map + layer toggles
- `config.js` - edit titles, bounds, and file names
- `data/*.geojson` - SST, SSS, Chl-a point/grid layers
- `layers/*.png` - optional image overlays such as Sentinel-2 RGB
- `docs/WORDPRESS_LINKING.md` - how to link from seasat.org
- `docs/GITHUB_PAGES_STEPS.md` - exact GitHub Pages setup
- `scripts/predict_grid_template.py` - starter script for making GeoJSON layers
- `scripts/export_rgb_template.py` - starter note for making a Sentinel-2 RGB overlay

## Tonight's recommendation
Do not retrain models tonight unless you have to.
Use your existing Chl-a deployment logic and your notebook's champion setup for SST/SSS.
The important milestone tonight is getting a working public map page online.

## What you need to fill in
1. Put your three prediction GeoJSON files into `data/`
2. Optionally put a fixed Sentinel-2 PNG in `layers/`
3. Update `config.js`
4. Push this folder to a GitHub repo
5. Turn on GitHub Pages
