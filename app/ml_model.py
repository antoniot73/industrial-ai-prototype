"""
ml_model.py
Modelo supervisado para predicción industrial.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from app.database import SessionLocal
from app.models import ProcessData


def cargar_datos() -> pd.DataFrame:
    """
    Carga datos históricos desde SQLite.
    """

    db = SessionLocal()

    try:

        datos = db.query(ProcessData).all()

        registros = []

        for d in datos:

            registros.append({
                "temperatura": d.temperatura,
                "presion": d.presion,
                "flujo": d.flujo,
                "vibracion": d.vibracion
            })

        return pd.DataFrame(registros)

    finally:

        db.close()


def entrenar_modelo():
    """
    Entrena RandomForestRegressor.
    """

    df = cargar_datos()

    if len(df) < 20:
        return None, None

    X = df[[
        "presion",
        "flujo",
        "vibracion"
    ]]

    y = df["temperatura"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    modelo = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predicciones
    )

    return modelo, round(mae, 3)


def predecir_temperatura(
    presion: float,
    flujo: float,
    vibracion: float
):
    """
    Predicción de temperatura.
    """

    modelo, mae = entrenar_modelo()

    if modelo is None:

        return {
            "message": "No hay suficientes datos para entrenar modelo"
        }

    entrada = [[
        presion,
        flujo,
        vibracion
    ]]

    prediccion = modelo.predict(entrada)[0]

    return {
        "temperatura_predicha": round(prediccion, 2),
        "mae_modelo": mae
    }
