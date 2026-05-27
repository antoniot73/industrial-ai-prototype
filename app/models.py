"""
models.py
Modelo de datos del proceso industrial.
"""

from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

from app.database import Base


class ProcessData(Base):
    """
    Tabla principal del Historian.
    """

    __tablename__ = "process_data"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    temperatura = Column(Float)
    presion = Column(Float)
    flujo = Column(Float)
    vibracion = Column(Float)
