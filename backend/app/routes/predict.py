from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..services.predict_service import build_prediction_job

router = APIRouter(tags=["predict"])


class PredictRequest(BaseModel):
    date: str = Field(..., description="Requested date, e.g. 2025-07-01")
    bbox: list[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]")
    mode: str = Field(default="demo", description="demo or live")


@router.post("/predict")
def predict(req: PredictRequest) -> dict:
    return build_prediction_job(date=req.date, bbox=req.bbox, mode=req.mode)
