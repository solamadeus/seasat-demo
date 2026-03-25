from pathlib import Path

from .model_introspection import load_model_manifest


def build_prediction_job(date: str, bbox: list[float], mode: str = "demo") -> dict:
    manifest = load_model_manifest()
    return {
        "status": "scaffold-only",
        "mode": mode,
        "date": date,
        "bbox": bbox,
        "message": (
            "Backend scaffold is in place. Chl-a can follow the existing Python Earth Engine + Open-Meteo path. "
            "SST/SSS need the exact feature-builder recipe finalised before live inference is enabled."
        ),
        "models": manifest,
        "next_step": "Add xgb_chla.joblib and the original SST/SSS preprocessing code, then replace this stub with live raster generation.",
    }
