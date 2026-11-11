"""Painel epidemiológico do Elo (parte do Christian).

Rodar da raiz do repositório:
    streamlit run painel/app.py

Dados: dados/tratados/ (SINAN/TABNET). Cores e escolhas de gráfico: seguir o
Sugestoes.md do Renato.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DADOS = Path(__file__).resolve().parent.parent / "dados" / "tratados"
ROXO = "#5B2A86"
ULTIMO_ANO_COMPLETO = 2025  # 2026 só tem dados até junho

st.set_page_config(page_title="Elo · Painel epidemiológico", page_icon="💜", layout="wide")


@st.cache_data
def carregar() -> tuple[pd.DataFrame, pd.DataFrame]:
    brasil = pd.read_csv(DADOS / "hanseniase_brasil_sexo.csv", encoding="utf-8-sig")
    uf = pd.read_csv(DADOS / "hanseniase_uf.csv", encoding="utf-8-sig")
    return (
        brasil[brasil["ano"] <= ULTIMO_ANO_COMPLETO],
        uf[uf["ano"] <= ULTIMO_ANO_COMPLETO],
    )


brasil, uf = carregar()

st.title("Hanseníase no Brasil")
st.caption("Casos novos diagnosticados por ano · Fonte: SINAN/TABNET, Ministério da Saúde "
           "(extração de jul/2026; 2024 e 2025 ainda parciais)")

fig = px.line(brasil, x="ano", y="casos", markers=True,
              labels={"ano": "Ano", "casos": "Casos novos"})
fig.update_traces(line_color=ROXO)
st.plotly_chart(fig, width="stretch")

# TODO (Christian):
#  - números de destaque (total do período, último ano, variação)
#  - gráfico por UF (tabela `uf`) com Mato Grosso em destaque
#  - faixa marcando a pandemia (2020-2021), como sugere o Sugestoes.md
#  - filtro de período
