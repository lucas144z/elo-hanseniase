"""Login do paciente com JWT.

No protótipo o paciente entra só com o código (ex.: ELO-001). Na versão final
o código vem junto com uma senha ou um PIN definido na UBS.
"""
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import Paciente

SEGREDO = os.getenv("ELO_SEGREDO", "segredo-so-para-desenvolvimento")
ALGORITMO = "HS256"
VALIDADE = timedelta(hours=12)

bearer = HTTPBearer(auto_error=False)


def criar_token(paciente_id: int) -> str:
    payload = {"sub": str(paciente_id), "exp": datetime.now(timezone.utc) + VALIDADE}
    return jwt.encode(payload, SEGREDO, algorithm=ALGORITMO)


def paciente_logado(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Paciente:
    """Dependência das rotas protegidas: devolve o paciente dono do token."""
    nao_autorizado = HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão expirada. Entre de novo.")
    if credenciais is None:
        raise nao_autorizado
    try:
        dados = jwt.decode(credenciais.credentials, SEGREDO, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise nao_autorizado
    paciente = db.get(Paciente, int(dados["sub"]))
    if paciente is None:
        raise nao_autorizado
    return paciente
