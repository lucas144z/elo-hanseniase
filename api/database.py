"""Conexão com o banco.

Por padrão usa SQLite (arquivo api/elo.db), que não precisa instalar nada.
Para usar PostgreSQL, defina a variável de ambiente DATABASE_URL, por exemplo:
    postgresql+psycopg://elo:elo@localhost:5432/elo
"""
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

PASTA_API = Path(__file__).resolve().parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(PASTA_API / 'elo.db').as_posix()}")

# check_same_thread é uma opção só do SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Abre uma sessão por requisição e fecha no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
