# API do Elo

FastAPI + SQLAlchemy. Guarda pacientes, tratamentos e doses e calcula o calendário do tratamento.

## Como rodar

Todos os comandos são rodados **da raiz do repositório**.

```bash
pip install -r requirements.txt
python -m api.seed                       # cria o banco com dados fictícios
python -m uvicorn api.main:app --reload  # sobe a API em http://localhost:8000
```

Abra **http://localhost:8000/docs** para ver e testar as rotas no navegador.

Códigos de teste: `ELO-001` (esquema MB, 12 meses) e `ELO-002` (esquema PB, 6 meses).

## Usar PostgreSQL (opcional)

Sem configurar nada, a API usa SQLite (`api/elo.db`). Para usar PostgreSQL:

1. Crie um banco vazio chamado `elo` (pgAdmin: Databases → Create → Database).
2. Crie o arquivo `api/.env` (ele não vai para o GitHub) com:
   ```
   DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost:5432/elo
   ```
3. Rode `python -m api.seed` e suba a API normalmente. As tabelas aparecem no pgAdmin em
   `elo → Schemas → public → Tables`.

## Rotas

| Rota | O que faz |
|---|---|
| `POST /login` | recebe `{"codigo": "ELO-001"}` e devolve o token (JWT) |
| `GET /tratamento` | resumo do tratamento: dia atual, doses tomadas, próxima dose na UBS |
| `GET /doses?mes=AAAA-MM` | cada dia do mês com o tipo (diária ou supervisionada) e o status |
| `POST /doses` | registra a dose de hoje (não duplica se já estiver registrada) |

As rotas de tratamento e doses exigem o cabeçalho `Authorization: Bearer <token>`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `main.py` | rotas |
| `calendario.py` | regras do tratamento (supervisionada a cada 28 dias, status de cada dia) |
| `models.py` | tabelas: `ubs`, `paciente`, `tratamento`, `dose` |
| `schemas.py` | formato dos dados que entram e saem |
| `auth.py` | login com JWT |
| `database.py` | conexão (SQLite por padrão; PostgreSQL com a variável `DATABASE_URL`) |
| `seed.py` | dados fictícios |
