"""
api.py
Endpoints REST del sistema.
"""

from fastapi import APIRouter

from app.database import SessionLocal
from app.models import ProcessData
from app.schemas import ProcessDataSchema

router = APIRouter()


@router.get("/")
def root():

    return {
        "message": "Industrial AI Prototype API"
    }


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.get(
    "/current",
    response_model=ProcessDataSchema
)
def current_data():

    db = SessionLocal()

    try:

        dato = (
            db.query(ProcessData)
            .order_by(ProcessData.id.desc())
            .first()
        )

        if dato is None:

            return {
                "temperatura": 0,
                "presion": 0,
                "flujo": 0,
                "vibracion": 0,
                "timestamp": "2000-01-01T00:00:00"
            }

        return dato

    finally:

        db.close()


@router.get(
    "/history",
    response_model=list[ProcessDataSchema]
)
def history(limit: int = 100):

    db = SessionLocal()

    try:

        datos = (
            db.query(ProcessData)
            .order_by(ProcessData.id.desc())
            .limit(limit)
            .all()
        )

        return datos

    finally:

        db.close()
