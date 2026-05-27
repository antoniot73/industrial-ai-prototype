"""
simulator.py
Simulador industrial de variables de proceso.
"""

import time
import random
import logging

from app.database import SessionLocal
from app.models import ProcessData


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def generar_variables() -> dict:
    """
    Genera variables industriales simuladas.
    """

    presion = random.normalvariate(50, 3)

    flujo = (
        presion * 0.8 +
        random.normalvariate(0, 2)
    )

    vibracion = random.normalvariate(5, 0.5)

    temperatura = (
        0.6 * presion +
        0.3 * flujo +
        0.1 * vibracion +
        random.normalvariate(0, 1)
    )

    return {
        "temperatura": round(temperatura, 2),
        "presion": round(presion, 2),
        "flujo": round(flujo, 2),
        "vibracion": round(vibracion, 2)
    }


def guardar_dato(data: dict) -> None:
    """
    Guarda variables en SQLite.
    """

    db = SessionLocal()

    try:

        registro = ProcessData(
            temperatura=data["temperatura"],
            presion=data["presion"],
            flujo=data["flujo"],
            vibracion=data["vibracion"]
        )

        db.add(registro)

        db.commit()

        logging.info("Dato guardado: %s", data)

    except Exception as exc:

        logging.error("Error guardando dato: %s", exc)

        db.rollback()

    finally:

        db.close()


def iniciar_simulacion() -> None:
    """
    Loop principal del simulador.
    """

    while True:

        data = generar_variables()

        guardar_dato(data)

        time.sleep(10)
