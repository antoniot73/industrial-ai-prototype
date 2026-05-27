"""
main.py
Aplicación principal FastAPI.
"""

import threading

from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.api import router
from app.simulator import iniciar_simulacion


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Industrial AI Prototype"
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    """
    Inicia simulador automáticamente.
    """

    hilo = threading.Thread(
        target=iniciar_simulacion,
        daemon=True
    )

    hilo.start()
