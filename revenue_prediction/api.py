"""FastAPI server exposing /api/revenue/predict.

Run locally: uvicorn api:app --host 0.0.0.0 --port 3000

Loads SUPABASE_URL / SUPABASE_SERVICE_KEY / BRAIN_URL / BRAIN_KEY from
environment. Falls back to a sensible default Brain URL for read-only
calls if BRAIN_KEY is set.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from predictor import predict

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("revenue_prediction.api")

app = FastAPI(title="KJE Revenue Prediction", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "revenue_prediction", "version": "1.0.0"}


@app.get("/api/revenue/predict")
def revenue_predict() -> dict:
    try:
        return predict()
    except Exception as exc:
        log.exception("predict failed")
        raise HTTPException(status_code=500, detail=str(exc))
