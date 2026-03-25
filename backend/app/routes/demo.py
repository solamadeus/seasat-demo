from fastapi import APIRouter

router = APIRouter(tags=["demo"])


@router.get("/demo-config")
def demo_config() -> dict:
    return {
        "default_date": "2025-07-01",
        "default_bbox": [-5.5, 55.0, -5.0, 55.4],
        "layers": [
            {"id": "s2_rgb", "label": "Sentinel-2 RGB", "type": "placeholder"},
            {"id": "sst", "label": "Predicted SST", "type": "placeholder"},
            {"id": "sss", "label": "Predicted SSS", "type": "placeholder"},
            {"id": "chla", "label": "Predicted Chl-a", "type": "placeholder"},
        ],
    }
