"""
api_ml.py
Endpoints Machine Learning.
"""

from fastapi import APIRouter

from app.ml_model import predecir_temperatura

router_ml = APIRouter()


@router_ml.get("/predict")
def predict(
    presion: float,
    flujo: float,
    vibracion: float
):

    return predecir_temperatura(
        presion,
        flujo,
        vibracion
    )
