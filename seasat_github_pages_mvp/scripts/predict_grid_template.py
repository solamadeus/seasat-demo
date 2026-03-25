
"""
Starter template: make static GeoJSON layers for GitHub Pages.

This is the simplest shape for tonight's MVP:
- choose one fixed AOI
- choose one fixed date/datetime
- create a grid of points over the AOI
- extract S2 + weather features for each point
- run the 3 models
- save 3 GeoJSON files:
    data/sst.geojson
    data/sss.geojson
    data/chla.geojson

You do NOT need a backend for this.
"""

import json
import numpy as np
import pandas as pd

# TODO:
# 1) replace these bounds and spacing
MIN_LAT, MAX_LAT = 56.00, 56.15
MIN_LON, MAX_LON = -6.00, -5.75
STEP_DEG = 0.002

DATE_STR = "2025-07-15 10:30:00"

def make_grid(min_lat, max_lat, min_lon, max_lon, step_deg):
    rows = []
    lat = min_lat
    while lat <= max_lat + 1e-12:
        lon = min_lon
        while lon <= max_lon + 1e-12:
            rows.append({"LATITUDE": lat, "LONGITUDE": lon, "DATETIME": DATE_STR})
            lon += step_deg
        lat += step_deg
    return pd.DataFrame(rows)

grid = make_grid(MIN_LAT, MAX_LAT, MIN_LON, MAX_LON, STEP_DEG)

# TODO:
# - attach your feature extraction code here
# - run your three models here
# - create columns: sst, sss, chla

# Placeholder fake values so the page works
grid["sst"] = 12 + (grid["LATITUDE"] - MIN_LAT) * 40
grid["sss"] = 30 + (grid["LONGITUDE"] - MIN_LON) * 20
grid["chla"] = 5 + (grid["LATITUDE"] - MIN_LAT + grid["LONGITUDE"] - MIN_LON) * 20

def to_geojson(df, value_col, out_path):
    feats = []
    for _, r in df.iterrows():
        feats.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [float(r["LONGITUDE"]), float(r["LATITUDE"])]},
            "properties": {
                value_col: float(r[value_col]),
                "date": DATE_STR,
                "model": "replace-with-real-model-name"
            }
        })
    gj = {"type": "FeatureCollection", "features": feats}
    with open(out_path, "w") as f:
        json.dump(gj, f)

to_geojson(grid, "sst", "../data/sst.geojson")
to_geojson(grid, "sss", "../data/sss.geojson")
to_geojson(grid, "chla", "../data/chla.geojson")

print("Wrote demo GeoJSON files.")
