"""
database.py
Gestión SQLite para Historian industrial.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------
# Crear carpeta data automáticamente
# ---------------------------------------------------

os.makedirs("data", exist_ok=True)

# ---------------------------------------------------
# SQLite database
# ---------------------------------------------------

DATABASE_URL = "sqlite:///./data/process.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
