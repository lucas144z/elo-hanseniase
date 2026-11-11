"""Regras do tratamento (PQT-U), sem depender do banco.

- PB (paucibacilar): 6 doses supervisionadas; MB (multibacilar): 12.
- A dose supervisionada é tomada na UBS a cada 28 dias, a partir do dia de início.
- Nos outros dias o paciente toma a dose diária em casa.
- O tratamento termina 28 dias depois da última supervisionada.
"""
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone

DOSES_SUPERVISIONADAS = {"PB": 6, "MB": 12}
INTERVALO = 28  # dias entre duas supervisionadas
FUSO_BRASILIA = timezone(timedelta(hours=-3))


def hoje() -> date:
    """Data de hoje no horário de Brasília (o servidor pode estar em outro fuso)."""
    return datetime.now(FUSO_BRASILIA).date()


def data_fim(esquema: str, inicio: date) -> date:
    return inicio + timedelta(days=INTERVALO * DOSES_SUPERVISIONADAS[esquema] - 1)


def total_de_doses(esquema: str) -> int:
    return INTERVALO * DOSES_SUPERVISIONADAS[esquema]


def eh_supervisionada(esquema: str, inicio: date, dia: date) -> bool:
    dias = (dia - inicio).days
    return 0 <= dias and dia <= data_fim(esquema, inicio) and dias % INTERVALO == 0


def proxima_supervisionada(esquema: str, inicio: date, referencia: date) -> date | None:
    """Primeira supervisionada a partir de `referencia` (inclusive). None se já acabaram."""
    dias = max(0, (referencia - inicio).days)
    k = -(-dias // INTERVALO)  # divisão arredondando para cima
    if k >= DOSES_SUPERVISIONADAS[esquema]:
        return None
    return inicio + timedelta(days=k * INTERVALO)


def status_do_dia(dia: date, inicio: date, fim: date, tomadas: set[date], referencia: date) -> str:
    if dia < inicio or dia > fim:
        return "fora"
    if dia in tomadas:
        return "tomada"
    if dia < referencia:
        return "esquecida"
    if dia == referencia:
        return "hoje"
    return "futura"


def dias_do_mes(ano: int, mes: int) -> list[date]:
    return [date(ano, mes, d) for d in range(1, monthrange(ano, mes)[1] + 1)]
