"""
schemas.py
Esquemas Pydantic.
"""

from pydantic import BaseModel
from datetime import datetime


class ProcessDataSchema(BaseModel):

    temperatura: float
    presion: float
    flujo: float
    vibracion: float
    timestamp: datetime

    class Config:
        from_attributes = True
