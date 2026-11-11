"""Tabelas do banco do Elo, em 3ª forma normal.

    ubs 1──N paciente 1──N tratamento 1──N dose

Nada que possa ser calculado fica guardado: o tipo de cada dose (diária ou
supervisionada), a data de fim e o total de doses saem do esquema + data de
início (ver calendario.py).
"""
from datetime import date, datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class UBS(Base):
    __tablename__ = "ubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    municipio: Mapped[str] = mapped_column(String(80))
    uf: Mapped[str] = mapped_column(String(2))

    pacientes: Mapped[list["Paciente"]] = relationship(back_populates="ubs")


class Paciente(Base):
    __tablename__ = "paciente"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True)  # usado no login, ex.: ELO-001
    nome: Mapped[str] = mapped_column(String(120))
    ubs_id: Mapped[int] = mapped_column(ForeignKey("ubs.id"))

    ubs: Mapped[UBS] = relationship(back_populates="pacientes")
    tratamentos: Mapped[list["Tratamento"]] = relationship(back_populates="paciente")


class Tratamento(Base):
    __tablename__ = "tratamento"
    __table_args__ = (CheckConstraint("esquema IN ('PB', 'MB')", name="ck_tratamento_esquema"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("paciente.id"))
    esquema: Mapped[str] = mapped_column(String(2))  # PB = 6 meses, MB = 12 meses
    data_inicio: Mapped[date]

    paciente: Mapped[Paciente] = relationship(back_populates="tratamentos")
    doses: Mapped[list["Dose"]] = relationship(back_populates="tratamento")


class Dose(Base):
    __tablename__ = "dose"
    __table_args__ = (UniqueConstraint("tratamento_id", "data", name="uq_dose_por_dia"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tratamento_id: Mapped[int] = mapped_column(ForeignKey("tratamento.id"))
    data: Mapped[date]  # dia a que a dose se refere
    registrada_em: Mapped[datetime] = mapped_column(default=datetime.now)  # quando tocou em "Tomei"

    tratamento: Mapped[Tratamento] = relationship(back_populates="doses")
