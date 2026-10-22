# Dados

Todos os dados deste repositório são **públicos e agregados** (contagens por ano, sexo e UF).
Nenhum dado pessoal de paciente é usado.

## Já incluídos

| Arquivo | Conteúdo | Fonte |
|---|---|---|
| `brutos/tabnet_hanseniase_brasil_sexo_2011-2026.csv` | Casos novos no Brasil por ano de diagnóstico e sexo, 2011–2026 | SINAN via TABNET/DATASUS — Ministério da Saúde |
| `brutos/tabnet_hanseniase_uf_2001-2026.csv` | Casos novos por ano de diagnóstico em AM, AP, MT, SP e RJ, 2001–2026 | SINAN via TABNET/DATASUS — Ministério da Saúde |
| `tratados/hanseniase_brasil_sexo.csv` | Mesmo conteúdo, limpo (UTF-8, só as linhas de dados) | gerado por `scripts/tratar_dados.py` |
| `tratados/hanseniase_uf.csv` | Mesmo conteúdo, limpo | gerado por `scripts/tratar_dados.py` |

Os arquivos em `brutos/` estão exatamente como saíram do TABNET (separador `;`, encoding Windows-1252).
Extração de julho de 2026. Segundo a nota do próprio TABNET, **2024, 2025 e 2026 são parciais** e
podem mudar, porque os municípios continuam digitando fichas depois do fechamento. 2026 fica fora
dos gráficos.

## Previstos para as próximas etapas

| Base | Para quê | Onde |
|---|---|---|
| Microdados do SINAN — Hanseníase | Cura, abandono e modo de saída por município (o indicador que o Elo quer melhorar) | DATASUS (FTP), lidos com a biblioteca PySUS |
| Estimativas populacionais do IBGE | Calcular a taxa de detecção por 100 mil habitantes, que permite comparar UFs | IBGE / DATASUS |
| CNES — Cadastro Nacional de Estabelecimentos de Saúde | Localizar as UBS que fazem o tratamento, para o paciente achar a mais próxima | DATASUS |

## Como regenerar

```bash
pip install -r requirements.txt
python scripts/tratar_dados.py
```
