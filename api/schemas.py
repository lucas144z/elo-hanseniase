"""Formato dos dados que entram e saem da API (validados pelo Pydantic)."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoginEntrada(BaseModel):
    codigo: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nome: str


class TratamentoSaida(BaseModel):
    esquema: Literal["PB", "MB"]
    data_inicio: date
    data_fim: date
    em_andamento: bool
    dia_atual: int
    doses_total: int
    doses_tomadas: int
    tomou_hoje: bool
    hoje_eh_supervisionada: bool
    proxima_supervisionada: date | None
    dias_para_supervisionada: int | None
    ubs: str


class DiaCalendario(BaseModel):
    data: date
    tipo: Literal["diaria", "supervisionada"] | None  # None = fora do tratamento
    status: Literal["tomada", "esquecida", "hoje", "futura", "fora"]


class DoseEntrada(BaseModel):
    data: date | None = None  # vazio = hoje


class DoseSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: date
    registrada_em: datetime
