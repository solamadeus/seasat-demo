import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODELS = ROOT / "models"


def _feature_names(path: Path) -> list[str]:
    data = json.loads(path.read_text())
    return data.get("learner", {}).get("feature_names", [])


def load_model_manifest() -> dict:
    out = {}
    for name in [
        "xgb_sst_s2only.json",
        "xgb_sst_s2pluswx.json",
        "xgb_sss_s2only.json",
        "xgb_sss_s2pluswx.json",
    ]:
        path = MODELS / name
        if path.exists():
            feats = _feature_names(path)
            out[name] = {
                "path": str(path),
                "feature_count": len(feats),
                "sample_features": feats[:8],
            }
    return out
