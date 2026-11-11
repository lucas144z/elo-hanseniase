"""API do Elo.

Rodar da raiz do repositório:
    python -m uvicorn api.main:app --reload
Documentação automática (Swagger): http://localhost:8000/docs
"""
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import calendario as cal
from .auth import criar_token, paciente_logado
from .database import Base, engine, get_db
from .models import Dose, Paciente, Tratamento
from .schemas import DiaCalendario, DoseEntrada, DoseSaida, LoginEntrada, Token, TratamentoSaida


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # cria as tabelas se ainda não existirem
    yield


app = FastAPI(
    title="Elo API",
    description="API do app Elo: calendário do tratamento e registro de doses.",
    version="0.1.0",
    lifespan=lifespan,
)

# Endereços do app (Vite) que podem chamar a API
ORIGENS = os.getenv("ELO_ORIGENS", "http://localhost:5173,http://localhost:4173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=ORIGENS, allow_methods=["*"], allow_headers=["*"])


def tratamento_atual(paciente: Paciente) -> Tratamento:
    if not paciente.tratamentos:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Nenhum tratamento cadastrado.")
    return max(paciente.tratamentos, key=lambda t: t.data_inicio)


@app.get("/", tags=["status"])
def raiz():
    return {"app": "Elo", "status": "ok", "documentacao": "/docs"}


@app.post("/login", response_model=Token, tags=["acesso"])
def login(entrada: LoginEntrada, db: Session = Depends(get_db)):
    codigo = entrada.codigo.strip().upper()
    paciente = db.scalar(select(Paciente).where(Paciente.codigo == codigo))
    if paciente is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Código não encontrado.")
    return Token(access_token=criar_token(paciente.id), nome=paciente.nome)


@app.get("/tratamento", response_model=TratamentoSaida, tags=["tratamento"])
def ver_tratamento(paciente: Paciente = Depends(paciente_logado)):
    t = tratamento_atual(paciente)
    ref = cal.hoje()
    fim = cal.data_fim(t.esquema, t.data_inicio)
    total = cal.total_de_doses(t.esquema)
    tomadas = {d.data for d in t.doses}
    proxima = cal.proxima_supervisionada(t.esquema, t.data_inicio, ref)
    return TratamentoSaida(
        esquema=t.esquema,
        data_inicio=t.data_inicio,
        data_fim=fim,
        em_andamento=t.data_inicio <= ref <= fim,
        dia_atual=min(max((ref - t.data_inicio).days + 1, 0), total),
        doses_total=total,
        doses_tomadas=len(tomadas),
        tomou_hoje=ref in tomadas,
        hoje_eh_supervisionada=cal.eh_supervisionada(t.esquema, t.data_inicio, ref),
        proxima_supervisionada=proxima,
        dias_para_supervisionada=(proxima - ref).days if proxima else None,
        ubs=paciente.ubs.nome,
    )


@app.get("/doses", response_model=list[DiaCalendario], tags=["doses"])
def doses_do_mes(
    mes: str = Query(pattern=r"^\d{4}-(0[1-9]|1[0-2])$", description="Mês no formato AAAA-MM",
                     examples=["2026-11"]),
    paciente: Paciente = Depends(paciente_logado),
):
    t = tratamento_atual(paciente)
    ano, numero_mes = map(int, mes.split("-"))
    ref = cal.hoje()
    fim = cal.data_fim(t.esquema, t.data_inicio)
    tomadas = {d.data for d in t.doses}

    dias = []
    for dia in cal.dias_do_mes(ano, numero_mes):
        situacao = cal.status_do_dia(dia, t.data_inicio, fim, tomadas, ref)
        if situacao == "fora":
            tipo = None
        elif cal.eh_supervisionada(t.esquema, t.data_inicio, dia):
            tipo = "supervisionada"
        else:
            tipo = "diaria"
        dias.append(DiaCalendario(data=dia, tipo=tipo, status=situacao))
    return dias


@app.post("/doses", response_model=DoseSaida, status_code=status.HTTP_201_CREATED, tags=["doses"])
def registrar_dose(
    response: Response,
    entrada: DoseEntrada | None = None,
    paciente: Paciente = Depends(paciente_logado),
    db: Session = Depends(get_db),
):
    t = tratamento_atual(paciente)
    ref = cal.hoje()
    dia = entrada.data if entrada and entrada.data else ref

    if dia > ref:
        raise HTTPException(422, "Não dá para registrar a dose de um dia que ainda não chegou.")
    if not t.data_inicio <= dia <= cal.data_fim(t.esquema, t.data_inicio):
        raise HTTPException(422, "Esse dia está fora do tratamento.")

    existente = db.scalar(select(Dose).where(Dose.tratamento_id == t.id, Dose.data == dia))
    if existente:
        response.status_code = status.HTTP_200_OK  # já estava registrada: não duplica
        return existente

    dose = Dose(tratamento_id=t.id, data=dia)
    db.add(dose)
    db.commit()
    db.refresh(dose)
    return dose
