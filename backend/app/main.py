from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routes.predict import router as predict_router
from .routes.demo import router as demo_router

app = FastAPI(title="SeaSat Demo Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api")
app.include_router(demo_router, prefix="/api")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse("frontend/index.html")
