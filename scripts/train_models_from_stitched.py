import json, os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA = {
    'sst': (os.path.join(ROOT, '..', 'df_sst.stitched.xlsx'), 'SST', 'xgb_sst_from_stitched.json'),
    'sss': (os.path.join(ROOT, '..', 'df_sss.stitched.xlsx'), 'SSS', 'xgb_sss_from_stitched.json'),
}

for key, (path, target, outname) in DATA.items():
    df = pd.read_excel(path).dropna(subset=[target]).copy()
    drop = {target, 'DATE', 'DATETIME', 'platform', 'Casestudy', 'system_index'}
    X = df[[c for c in df.columns if c not in drop]].apply(pd.to_numeric, errors='coerce')
    X = X[[c for c in X.columns if X[c].notna().mean() >= 0.6]]
    X = X.fillna(X.median(numeric_only=True))
    y = df[target].astype(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = xgb.XGBRegressor(
        n_estimators=400, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        objective='reg:squarederror', random_state=42, n_jobs=4,
    )
    model.fit(Xtr, ytr, eval_set=[(Xte, yte)], verbose=False)
    pred = model.predict(Xte)
    metrics = {
        'rmse': float(mean_squared_error(yte, pred) ** 0.5),
        'mae': float(mean_absolute_error(yte, pred)),
        'r2': float(r2_score(yte, pred)),
        'n_rows': int(len(df)),
        'n_features': int(X.shape[1]),
        'features': list(X.columns),
    }
    out_model = os.path.join(ROOT, 'models', outname)
    out_metrics = out_model.replace('.json', '_metrics.json')
    model.save_model(out_model)
    with open(out_metrics, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(key, metrics)
