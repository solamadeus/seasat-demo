#!/usr/bin/env python3
"""Reproducible SeaSat SST/SSS retraining with spatial and temporal holdouts.

Needs the original stitched matchup table -- NOT stored in this repository.
Produces validation metrics and a candidate model only on --export-candidate.
No predictions are made here. Do not treat these as Loch Etive validation.
"""
import argparse
import json
import pathlib
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

LEAK_PRONE = {
    "SST", "SSS", "DATE", "DATETIME", "TIMESTAMP", "TIME_DIFF",
    "TIMESTAMP_DIFF", "system_index", "platform", "Casestudy",
    "s2_acq_time", "S2_ACQ_TIME", "PRODUCT_ID",
}
def read_table(path):
    p = pathlib.Path(path)
    return pd.read_excel(p) if p.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(p)

def prepare(frame, target, sat_time_column):
    df = frame.copy()
    if target not in df:
        raise ValueError("Missing target column: " + target)
    if not {"LATITUDE", "LONGITUDE"} <= set(df.columns):
        raise ValueError("Need LATITUDE and LONGITUDE for spatial holdout")
    df["LATITUDE"] = pd.to_numeric(df["LATITUDE"], errors="coerce")
    df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"], errors="coerce")
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df = df.dropna(subset=["LATITUDE", "LONGITUDE", target]).copy()
    if sat_time_column:
        if sat_time_column not in df:
            raise ValueError("Missing explicit S2 acquisition time: " + sat_time_column)
        dt = pd.to_datetime(df[sat_time_column], utc=True, errors="coerce")
        if dt.notna().mean() < 0.9:
            raise ValueError("More than 10% missing satellite acquisition times")
        day = dt.dt.dayofyear.astype(float)
        hour = dt.dt.hour.astype(float) + dt.dt.minute.astype(float)/60
        df["sat_doy_sin"] = np.sin(2*np.pi*day/365.25)
        df["sat_doy_cos"] = np.cos(2*np.pi*day/365.25)
        df["sat_hour_sin"] = np.sin(2*np.pi*hour/24)
        df["sat_hour_cos"] = np.cos(2*np.pi*hour/24)
    else:
        dt = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")
    exclude = LEAK_PRONE | {target, sat_time_column}
    features = [x for x in df.columns
                if x not in exclude and
                pd.api.types.is_numeric_dtype(df[x])]
    # Only allow feature columns available at deployment. Exclude IDs and
    # any truth-derived time-differences, statistics or target proxies.
    features = [x for x in features if not str(x).lower().startswith(
        ("target_", "observed_", "truth_", "measured_", "label_"))]
    if not features: raise ValueError("No numeric predictors")
    x = df[features].apply(pd.to_numeric, errors="coerce")
    # Geographical ~0.2-degree groups: screening only; confirm spatial
    # autocorrelation length and use metric CRS for production blocking.
    groups = ((df.LATITUDE / .2).round().astype(int).astype(str) + "_" +
              (df.LONGITUDE / .2).round().astype(int).astype(str))
    if groups.nunique() < 5: raise ValueError("Too few distinct spatial groups")
    return df, x, df[target], groups, dt

def fit_eval(x, y, train_idx, test_idx, random_state):
    train = x.iloc[train_idx]
    test = x.iloc[test_idx]
    keep = train.columns[train.notna().mean() >= .60].tolist()
    if not keep: raise ValueError("No features pass training-only missingness threshold")
    model = XGBRegressor(n_estimators=400, max_depth=4, learning_rate=.05,
        subsample=.8, colsample_bytree=.8, objective="reg:squarederror",
        random_state=random_state, n_jobs=4, tree_method="hist")
    model.fit(train[keep], y.iloc[train_idx])
    pred = model.predict(test[keep])
    return model, {
      "rmse": float(mean_squared_error(y.iloc[test_idx],pred)**.5),
      "mae":float(mean_absolute_error(y.iloc[test_idx],pred)),
      "r2":float(r2_score(y.iloc[test_idx],pred)),
      "n_train":len(train_idx),"n_test":len(test_idx),"features":keep,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Original stitched matchup XLSX/CSV")
    p.add_argument("--target", required=True, choices=["SST","SSS"])
    p.add_argument("--satellite-time-column", default=None,
                   help="Verified S2 acquisition UTC column. NOT in-situ timestamp")
    p.add_argument("--output", default="scottish_model_validation")
    p.add_argument("--export-candidate", action="store_true")
    args=p.parse_args()
    out=pathlib.Path(args.output); out.mkdir(parents=True,exist_ok=True)
    df,x,y,groups,dt=prepare(read_table(args.input),args.target,args.satellite_time_column)
    splitter=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42)
    tr,te=next(splitter.split(x,y,groups))
    model,spatial=fit_eval(x,y,tr,te,42)
    results={"target":args.target,"source":str(args.input),
      "n_rows":int(len(df)),"spatial_holdout":spatial,
      "time_features":("S2 acquisition UTC cyclical features" if args.satellite_time_column
                       else "none; timestamp provenance unverified"),
      "excluded_columns":sorted(str(q) for q in LEAK_PRONE),
      "notes":"Spatial 0.2-degree blocks are screening, not independent UK site validation."}
    if args.satellite_time_column:
        cut=dt.quantile(.8)
        past=np.flatnonzero((dt<cut).to_numpy())
        future=np.flatnonzero((dt>=cut).to_numpy())
        if min(len(past),len(future))>10:
            _,time_metrics=fit_eval(x,y,past,future,42)
            results["future_holdout"]=time_metrics
    if args.export_candidate:
        filename=out/(args.target.lower()+"_xgb_candidate.json")
        model.save_model(str(filename))
        results["candidate_model"]=str(filename)
        results["warning"]="Candidate ONLY; not Loch Etive validated."
    (out/(args.target.lower()+"_validation.json")).write_text(
        json.dumps(results,indent=2))
    print(json.dumps({k:v for k,v in results.items() if k!="spatial_holdout"},indent=2))
    print("Spatial holdout:",spatial["rmse"],"RMSE;",spatial["r2"],"R2")

if __name__=="__main__":
    main()
