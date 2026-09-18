from pathlib import Path

import joblib
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "ai" / "models" / "car_price_tensorflow.keras"
PIPELINE_PATH = BASE_DIR / "ai" / "models" / "feature_pipeline.pkl"


app = FastAPI(
    title="Vehicle ML API",
    version="1.0.0",
    description="API de previsão de preço de veículos usando TensorFlow.",
)


model = tf.keras.models.load_model(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)


class VehicleInput(BaseModel):
    make: str
    year: int = Field(..., ge=1900)
    engine_cc: float = Field(..., gt=0)
    mileage_km: float = Field(..., ge=0)
    doors: int = Field(..., ge=1)
    fuel_type: str
    transmission: str
    body_type: str
    state: str


class PredictionResponse(BaseModel):
    predicted_price: float
    model: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "tensorflow",
        "model_loaded": model is not None,
        "pipeline_loaded": pipeline is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_price(vehicle: VehicleInput):
    u = pd.DataFrame([vehicle.model_dump()])
    v = pipeline.transform(u)
    w = model.predict(v, verbose=0)

    predicted_price = float(w.flatten()[0])

    return {
        "predicted_price": round(predicted_price, 2),
        "model": "tensorflow",
    }
