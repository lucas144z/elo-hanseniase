"""Limpa as extrações do TABNET (SINAN/hanseníase) e gera os gráficos do README.

Uso (a partir da raiz do repositório):
    python scripts/tratar_dados.py

Entradas:  dados/brutos/*.csv  (exportados do TABNET, separador ';', encoding cp1252)
Saídas:    dados/tratados/*.csv (UTF-8) e docs/graficos/*.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "dados" / "brutos"
TRATADOS = RAIZ / "dados" / "tratados"
GRAFICOS = RAIZ / "docs" / "graficos"

# Paleta do projeto (ver identidade-visual/README.md)
ROXO = "#5B2A86"
LAVANDA = "#B9A3D6"
VERDE = "#2E9E7A"
AMBAR = "#E8A33D"
GRAFITE = "#2B2733"
NEVOA = "#F6F3FA"

# 2026 só tem dados parciais (até jun/2026); fica fora dos gráficos
ULTIMO_ANO_FECHADO = 2025


def ler_tabnet(arquivo: Path, linha_cabecalho: int, colunas: int) -> pd.DataFrame:
    """Lê o CSV do TABNET e mantém só as linhas cujo 1º campo é um ano."""
    df = pd.read_csv(
        arquivo, sep=";", encoding="cp1252", header=None,
        skiprows=linha_cabecalho, usecols=range(colunas), dtype=str,
    )
    df = df[df[0].str.fullmatch(r"\d{4}", na=False)].copy()
    return df


def brasil_por_sexo() -> pd.DataFrame:
    df = ler_tabnet(BRUTOS / "tabnet_hanseniase_brasil_sexo_2011-2026.csv", 4, 4)
    df.columns = ["ano", "casos", "masculino", "feminino"]
    return df.astype(int)


def por_uf() -> pd.DataFrame:
    df = ler_tabnet(BRUTOS / "tabnet_hanseniase_uf_2001-2026.csv", 3, 6)
    df.columns = ["ano", "Amazonas", "Amapá", "Mato Grosso", "São Paulo", "Rio de Janeiro"]
    return df.astype(int)


def estilo(ax, titulo: str, subtitulo: str) -> None:
    ax.set_facecolor(NEVOA)
    ax.figure.set_facecolor(NEVOA)
    ax.set_title(titulo, loc="left", fontsize=15, fontweight="bold", color=ROXO, pad=26)
    ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=10, color=GRAFITE)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(LAVANDA)
    ax.tick_params(colors=GRAFITE)
    ax.grid(axis="y", color=LAVANDA, alpha=0.4)
    ax.set_axisbelow(True)


def grafico_brasil(df: pd.DataFrame) -> None:
    d = df[df.ano <= ULTIMO_ANO_FECHADO]
    fig, ax = plt.subplots(figsize=(10, 5))
    cores = [AMBAR if a in (2020, 2021) else ROXO for a in d.ano]
    ax.bar(d.ano, d.casos, color=cores)
    estilo(ax, "Casos novos de hanseníase no Brasil",
           "Ano de diagnóstico, 2011–2025 · em âmbar, os anos da pandemia")
    ax.set_xticks(d.ano)
    ax.tick_params(axis="x", rotation=45)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f} mil")
    c19 = int(d.loc[d.ano == 2019, "casos"].iloc[0])
    c20 = int(d.loc[d.ano == 2020, "casos"].iloc[0])
    ax.annotate(f"{(c20/c19 - 1):+.0%} em 2020:\nmenos diagnóstico,\nnão menos doença",
                xy=(2020, c20), xytext=(2020.6, c19 * 0.98), fontsize=9, color=GRAFITE,
                arrowprops=dict(arrowstyle="->", color=GRAFITE))
    fig.text(0.01, 0.01, "Fonte: SINAN/TABNET — Ministério da Saúde (dados de jul/2026; 2024–2025 parciais)",
             fontsize=8, color=GRAFITE)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(GRAFICOS / "casos_brasil.png", dpi=150)
    plt.close(fig)


def grafico_uf(df: pd.DataFrame) -> None:
    d = df[df.ano <= ULTIMO_ANO_FECHADO]
    fig, ax = plt.subplots(figsize=(10, 5))
    # cor e deslocamento vertical do rótulo (evita RJ e Amazonas sobrepostos)
    outros = {"São Paulo": ("#8E6BB5", 0), "Rio de Janeiro": ("#8E6BB5", 120),
              "Amazonas": ("#A58CC4", -60), "Amapá": ("#A58CC4", -40)}
    for uf, (cor, desloc) in outros.items():
        ax.plot(d.ano, d[uf], color=cor, linewidth=1.8)
        ax.text(d.ano.iloc[-1] + 0.3, d[uf].iloc[-1] + desloc, uf, color=cor, fontsize=9, va="center")
    ax.plot(d.ano, d["Mato Grosso"], color=VERDE, linewidth=3)
    ax.text(d.ano.iloc[-1] + 0.3, d["Mato Grosso"].iloc[-1], "Mato Grosso",
            color=VERDE, fontsize=10, fontweight="bold", va="center")
    estilo(ax, "Mato Grosso já tem mais casos que SP, RJ, AM e AP somados",
           "Casos novos de hanseníase por ano de diagnóstico, 2001–2025")
    ax.set_xlim(d.ano.min(), d.ano.max() + 3)
    fig.text(0.01, 0.01, "Fonte: SINAN/TABNET — Ministério da Saúde (dados de jul/2026; 2024–2025 parciais)",
             fontsize=8, color=GRAFITE)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(GRAFICOS / "casos_uf.png", dpi=150)
    plt.close(fig)


def main() -> None:
    TRATADOS.mkdir(parents=True, exist_ok=True)
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    # Inter é a fonte do projeto; usa a que estiver instalada, sem avisar a cada texto
    plt.rcParams["font.family"] = ["Inter", "Segoe UI", "DejaVu Sans"]
    import logging
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

    brasil = brasil_por_sexo()
    uf = por_uf()
    # utf-8-sig: abre com acento certo no Excel do Windows
    brasil.to_csv(TRATADOS / "hanseniase_brasil_sexo.csv", index=False, encoding="utf-8-sig")
    uf.to_csv(TRATADOS / "hanseniase_uf.csv", index=False, encoding="utf-8-sig")

    grafico_brasil(brasil)
    grafico_uf(uf)
    print(brasil.to_string(index=False))
    print(uf.to_string(index=False))


if __name__ == "__main__":
    main()
