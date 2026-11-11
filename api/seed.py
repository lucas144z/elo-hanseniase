"""Dados fictícios para o protótipo.

Rodar da raiz do repositório:
    python -m api.seed

Apaga o banco e recria com pacientes inventados. As datas são calculadas a
partir de hoje, então a demonstração sempre mostra um tratamento em andamento.
A dose de hoje fica em aberto para dar para testar o botão "Tomei".

Renato: amplie aqui (mais UBS, mais pacientes, perfis de adesão diferentes).
"""
import random
from datetime import datetime, time, timedelta

from .calendario import data_fim, hoje
from .database import Base, SessionLocal, engine
from .models import UBS, Dose, Paciente, Tratamento


def registrar_doses(tratamento: Tratamento, chance: float, rng: random.Random) -> None:
    """Marca como tomadas as doses de antes de hoje, cada uma com a chance indicada."""
    dia = tratamento.data_inicio
    ultimo = min(hoje() - timedelta(days=1), data_fim(tratamento.esquema, tratamento.data_inicio))
    while dia <= ultimo:
        if rng.random() < chance:
            horario = time(hour=rng.randint(7, 21), minute=rng.randint(0, 59))
            tratamento.doses.append(Dose(data=dia, registrada_em=datetime.combine(dia, horario)))
        dia += timedelta(days=1)


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    rng = random.Random(42)  # semente fixa: sempre gera os mesmos dados

    ubs = UBS(nome="UBS Jardim das Flores", municipio="Cuiabá", uf="MT")
    pacientes = [
        # código, nome fictício, esquema, começou há N dias, chance de tomar a dose
        ("ELO-001", "Maria Aparecida", "MB", 75, 0.92),
        ("ELO-002", "João Batista", "PB", 20, 0.60),
    ]

    with SessionLocal() as db:
        db.add(ubs)
        for codigo, nome, esquema, dias_atras, chance in pacientes:
            paciente = Paciente(codigo=codigo, nome=nome, ubs=ubs)
            tratamento = Tratamento(
                paciente=paciente, esquema=esquema, data_inicio=hoje() - timedelta(days=dias_atras)
            )
            registrar_doses(tratamento, chance, rng)
            db.add(paciente)
        db.commit()

    print("Banco recriado com", len(pacientes), "pacientes fictícios:",
          ", ".join(p[0] for p in pacientes))


if __name__ == "__main__":
    main()
