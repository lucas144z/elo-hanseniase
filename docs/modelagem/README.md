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

- [ ] Diagrama (DER) em `docs/modelagem/der.png`
- [ ] Dicionário de dados (tipo e significado de cada coluna)
- [ ] Mais dados fictícios em `api/seed.py` (UBS, pacientes e perfis de adesão diferentes)
