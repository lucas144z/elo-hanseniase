# Modelagem do banco

Responsável: Renato.

As tabelas estão em [`api/models.py`](../../api/models.py) e seguem a 3ª forma normal:

```
ubs 1──N paciente 1──N tratamento 1──N dose
```

| Tabela | Colunas |
|---|---|
| `ubs` | id, nome, municipio, uf |
| `paciente` | id, codigo (único), nome, ubs_id → ubs |
| `tratamento` | id, paciente_id → paciente, esquema (PB ou MB), data_inicio |
| `dose` | id, tratamento_id → tratamento, data, registrada_em (único por tratamento + data) |

O tipo da dose (diária ou supervisionada), a data de fim e o total de doses não ficam
guardados: são calculados a partir do esquema e da data de início (`api/calendario.py`).

## A fazer

### 1. Alimentar o banco: `api/seed.py` (até quinta, meio-dia)

Os dados entram **pelo seed**, não digitados no pgAdmin: assim todo mundo que rodar
`python -m api.seed` tem os mesmos pacientes.

- [ ] Pelo menos 3 UBS (sugestão: municípios de MT, MA e PA, os estados com mais casos)
- [ ] Pelo menos 8 pacientes, com perfis diferentes:
  - em dia (toma quase todas as doses)
  - irregular (esquece várias)
  - **abandono**: tomou bem no começo e parou há uns 15 dias (precisa de um parâmetro novo em `registrar_doses`)
  - começou ontem
  - quase terminando o tratamento
  - PB e MB misturados
- [ ] Manter `ELO-001` e `ELO-002` como estão (são usados no README, nos prints e no vídeo)
- [ ] Nomes inventados, códigos `ELO-003`, `ELO-004`...; datas sempre relativas a `hoje()`

Para testar: `python -m api.seed`, subir a API e entrar no app com os códigos novos.

### 2. Documentar a modelagem (até quinta à noite)

- [ ] Diagrama (DER) em `docs/modelagem/der.png`. No pgAdmin: botão direito no banco →
  **ERD For Database** → exportar imagem. No DBeaver (SQLite): aba **ER Diagram** da conexão.
- [ ] Dicionário de dados neste arquivo: tabela, coluna, tipo, obrigatória, descrição, exemplo
- [ ] Justificativa curta de 1FN, 2FN e 3FN para as quatro tabelas

### 3. Se sobrar tempo (para a banca)

- [ ] Modelar no DER, sem mexer na API, as tabelas `sintoma` ("Estou sentindo algo") e
  `contato` (contatos da casa examinados), que estão na proposta do CP1
