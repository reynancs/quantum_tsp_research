"""
Exportacao de Imagens — Dashboard Bibliometrico (TSP Quantico)

Gera versoes ESTATICAS e PADRONIZADAS de todos os graficos do
dashboard_bibliometrico.py para uso na apresentacao do evento SAPCT 2026.

Padrao aplicado a TODAS as imagens:
    - Tamanho      : 1280 x 720 px (logico) | proporcao 16:9 (slide PowerPoint)
    - Resolucao    : scale=2  ->  2560 x 1440 px reais (alta definicao / ~192 DPI)
    - Paleta       : Azul Pantone 293 (#3C60A7, R60 G96 B167) + branco
    - Fundo        : branco (#FFFFFF)
    - Fonte        : Arial
    - Titulo       : cada imagem carrega o proprio titulo (auto-explicativa)

As imagens sao numeradas conforme a aba correspondente do painel:
    01_visao_geral_*       -> aba "Visao Geral"
    02_fontes_autores_*    -> aba "Fontes e Autores"
    03_impacto_citacoes_*  -> aba "Impacto e Citacoes"
    04_campos_estudo_*     -> aba "Campos de Estudo"
    05_geografia_*         -> aba "Geografia"
    06_strings_busca_*     -> aba "Strings de Busca"
    07_algoritmos_*        -> aba "Algoritmos e Abordagens"

Como usar:
    python src/exportar_imagens.py

Dependencias:
    pip install pandas plotly numpy wordcloud matplotlib pycountry openpyxl kaleido
"""

import os
import random

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pycountry

# ============================================================
# 1. PADRAO VISUAL DA EMPRESA
# ============================================================

# --- Cor institucional ---
# Azul Pantone 293 C  =  R60 G96 B167  =  #3C60A7
AZUL_PANTONE = "#3C60A7"
BRANCO       = "#FFFFFF"

# Tons de apoio derivados do azul institucional (escuro -> claro)
AZUL_ESCURO  = "#16243F"   # textos e titulos
AZUL_MEDIO   = "#2A4677"
AZUL_CLARO   = "#8AA3D4"
AZUL_GRID    = "#E8ECF4"   # linhas de grade discretas
CINZA_TEXTO  = "#3A4252"   # corpo de texto
CINZA_FONTE  = "#9AA3B2"   # rodape / fonte dos dados

FONTE = "Arial"

# --- Dimensoes padronizadas ---
LARGURA = 1280   # px logico
ALTURA  = 720    # px logico  (16:9)
ESCALA  = 2      # multiplicador -> 2560 x 1440 px reais (alta definicao)
DPI_MPL = 200    # DPI equivalente para imagens matplotlib (wordcloud)

# Pasta de saida
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SAIDA   = os.path.join(PASTA_PROJETO, "docs", "images")
RODAPE = "Fonte: Levantamento bibliográfico — Lens.org  |  Mestrado Profissional SENAI CIMATEC"


def gerar_tons(n):
    """Retorna n tons de azul institucional interpolados (escuro -> primario -> claro).

    Usado para colorir categorias de forma harmonica e na identidade da marca.
    """
    # Pontos de controle em RGB: escuro, Pantone 293, claro
    pts = [(22, 36, 63), (60, 96, 167), (138, 163, 212)]
    if n == 1:
        return [AZUL_PANTONE]
    tons = []
    for i in range(n):
        t = i / (n - 1)
        if t <= 0.5:
            a, b, tt = pts[0], pts[1], t / 0.5
        else:
            a, b, tt = pts[1], pts[2], (t - 0.5) / 0.5
        rgb = tuple(int(round(a[k] + (b[k] - a[k]) * tt)) for k in range(3))
        tons.append("#%02X%02X%02X" % rgb)
    return tons


# Paleta categorica: tons de azul alternados (escuro/claro) para garantir
# contraste entre categorias VIZINHAS em pizzas e barras empilhadas.
PALETA_CATEGORICA = [
    "#1B2E50", "#5E7FC0", "#3C60A7", "#A9BBDD", "#2A4677",
    "#8AA3D4", "#16243F", "#6E8AC4", "#4E72B5", "#C5D0E8",
]


def mapa_cores(categorias):
    """Mapeia uma lista de categorias para tons de azul (dict {categoria: cor})."""
    cats = list(categorias)
    return {cat: PALETA_CATEGORICA[i % len(PALETA_CATEGORICA)]
            for i, cat in enumerate(cats)}


# Escala continua branco -> azul (treemaps, choropleth, heatmaps)
ESCALA_CONTINUA = [
    [0.0, "#FFFFFF"],
    [0.15, "#DCE3F2"],
    [0.40, "#8AA3D4"],
    [0.70, "#3C60A7"],
    [1.0, "#16243F"],
]


def estilizar(fig, titulo, legenda_topo=True):
    """Aplica o padrao visual da empresa a uma figura Plotly.

    Escala tipografica (boas praticas para projecao):
        - Titulo do grafico        : 28 pt
        - Corpo (eixos / legenda)  : 18 pt   <- base
        - Rodape (fonte dos dados) : 13 pt
    """
    fig.update_layout(
        title=dict(
            text=titulo,
            x=0.5, xanchor="center",
            font=dict(size=28, color=AZUL_ESCURO, family=FONTE),
        ),
        font=dict(family=FONTE, size=18, color=CINZA_TEXTO),
        plot_bgcolor=BRANCO,
        paper_bgcolor=BRANCO,
        width=LARGURA, height=ALTURA,
        margin=dict(l=120, r=85, t=130, b=120),
    )
    # Rodape com a fonte dos dados
    fig.add_annotation(
        text=RODAPE, xref="paper", yref="paper",
        x=0.0, y=-0.18, showarrow=False, xanchor="left",
        font=dict(size=13, color=CINZA_FONTE, family=FONTE),
    )
    fig.update_xaxes(showgrid=True, gridcolor=AZUL_GRID, zeroline=False,
                     linecolor=AZUL_GRID, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor=AZUL_GRID, zeroline=False,
                     linecolor=AZUL_GRID, automargin=True)
    # impede que rotulos de valor "outside" sejam cortados pela area do plot
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))
    return fig


def salvar(fig, nome):
    """Exporta a figura Plotly em PNG de alta definicao na pasta docs/images."""
    caminho = os.path.join(PASTA_SAIDA, nome)
    fig.write_image(caminho, width=LARGURA, height=ALTURA, scale=ESCALA)
    print(f"  [OK] {nome}")


# ============================================================
# 2. CONSTANTES DO DOMINIO  (replicadas do dashboard)
# ============================================================

STRINGS_BUSCA = {
    1: "TSP + Quantum Computing", 2: "TSP + Quantum Algorithms",
    3: "TSP + Quantum Annealing", 4: "TSP + QAOA", 5: "TSP + Hybrid Quantum",
    6: "VRP + Quantum Computing", 7: "Comb. Opt. + QA", 8: "TSP + VQE",
    9: "TSP + Grover", 10: "QUBO + TSP", 11: "Route Opt. + Quantum + Log.",
    12: "TSP + D-Wave", 13: "TSP + IBM Quantum", 14: "TSP + Ising Model",
    15: "VRP + QA + Logistics", 16: "Hamiltonian Cycle + Quantum",
    17: "VRP + QAOA", 18: "QC + Supply Chain Mgmt", 19: "TSP + Quantum-Inspired",
    20: "QRL + Routing", 21: "CVRP + QA", 22: "Job Shop + Quantum",
    23: "Bin Packing + Quantum", 24: "Facility Location + QC",
    25: "Knapsack + Quantum", 26: "QML + Supply Chain",
}

PRIORIDADES = {
    1: "Alta", 2: "Alta", 3: "Alta", 4: "Alta", 5: "Alta",
    6: "Alta", 17: "Alta", 18: "Alta",
    7: "Media", 8: "Media", 9: "Media", 10: "Media", 11: "Media",
    12: "Media", 19: "Media", 20: "Media", 21: "Media", 22: "Media",
    13: "Baixa", 14: "Baixa", 15: "Baixa", 16: "Baixa",
    23: "Baixa", 24: "Baixa", 25: "Baixa", 26: "Baixa",
}

# Tres tons de azul para as prioridades (Alta -> mais escuro)
COR_PRIORIDADE = {"Alta": AZUL_ESCURO, "Media": AZUL_PANTONE, "Baixa": AZUL_CLARO}

AREA_APLICACAO = {
    1: "TSP", 2: "TSP", 3: "TSP", 4: "TSP", 5: "TSP",
    8: "TSP", 9: "TSP", 10: "TSP", 12: "TSP", 13: "TSP",
    14: "TSP", 16: "TSP", 19: "TSP",
    6: "VRP/Logística", 11: "VRP/Logística", 15: "VRP/Logística",
    17: "VRP/Logística", 21: "VRP/Logística",
    18: "Supply Chain/QML", 20: "Supply Chain/QML", 26: "Supply Chain/QML",
    7: "Otim. Combinatória", 22: "Otim. Combinatória",
    23: "Otim. Combinatória", 24: "Otim. Combinatória",
    25: "Otim. Combinatória",
}
ORDEM_AREA = ["TSP", "VRP/Logística", "Supply Chain/QML", "Otim. Combinatória", "Outros"]
COR_AREA = {a: PALETA_CATEGORICA[i] for i, a in enumerate(ORDEM_AREA)}


# ============================================================
# 3. CARREGAMENTO DE DADOS
# ============================================================

def carregar_dados():
    """Carrega data/artigos_unicos.csv e prepara colunas derivadas."""
    df = pd.read_csv(os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv"), dtype=str)
    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    df["Citing Patents Count"] = pd.to_numeric(df["Citing Patents Count"], errors="coerce").fillna(0).astype(int)
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce").fillna(1).astype(int)
    df["Date Published"] = pd.to_datetime(df["Date Published"], errors="coerce")
    df["strings_lista"] = df["strings_origem"].fillna("").apply(
        lambda x: [int(float(s.strip())) for s in x.split(";") if s.strip() and s.strip() != "nan"]
    )
    df["prioridade"] = df["strings_lista"].apply(
        lambda lst: PRIORIDADES.get(lst[0], "Baixa") if lst else "Baixa"
    )
    df["Publication Type"] = df["Publication Type"].fillna("other").str.lower().str.strip()
    return df


def carregar_algoritmos():
    """Carrega data/base_algoritmos_abordagens.csv (129 trabalhos catalogados)."""
    df = pd.read_csv(os.path.join(PASTA_PROJETO, "data", "base_algoritmos_abordagens.csv"), dtype=str)
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype(int)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    if "ranking" in df.columns:
        df["ranking"] = pd.to_numeric(df["ranking"], errors="coerce").fillna(0.0)
    return df


# ============================================================
# 4. ABA 1 — VISAO GERAL
# ============================================================

def aba_visao_geral(df):
    print("Aba 1 — Visão Geral")

    # 01 — Publicacoes ao longo do tempo (barras empilhadas)
    # Foco a partir de 2010: anos anteriores tem volume insignificante e
    # poluiriam o eixo X. O periodo 2010+ concentra a curva de crescimento.
    df_tempo = df.dropna(subset=["Publication Year"]).copy()
    df_tempo["Ano"] = df_tempo["Publication Year"].astype(int)
    df_tempo = df_tempo[df_tempo["Ano"] >= 2010]
    tipos_principais = ["journal article", "preprint", "conference proceedings article",
                        "book chapter", "book", "dissertation", "report"]
    df_tempo["Tipo"] = df_tempo["Publication Type"].apply(
        lambda x: x if x in tipos_principais else "other")
    contagem = df_tempo.groupby(["Ano", "Tipo"]).size().reset_index(name="Contagem")
    ordem_tipo = [t for t in tipos_principais + ["other"]
                  if t in contagem["Tipo"].unique()]
    fig = px.bar(
        contagem, x="Ano", y="Contagem", color="Tipo",
        color_discrete_map=mapa_cores(ordem_tipo),
        category_orders={"Tipo": ordem_tipo},
        labels={"Contagem": "Número de Artigos", "Ano": "Ano de Publicação", "Tipo": "Tipo"},
    )
    fig.update_layout(barmode="stack",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    estilizar(fig, "Publicações ao Longo do Tempo")
    # Rotaciona os rotulos de ano para evitar sobreposicao no eixo X
    fig.update_xaxes(dtick=1, tickangle=-45, tickfont=dict(size=13))
    salvar(fig, "01_visao_geral_01_publicacoes_tempo.png")

    # 02 — Tipos de publicacao (rosca)
    contagem_tipo = df["Publication Type"].value_counts().head(8)
    fig = px.pie(values=contagem_tipo.values, names=contagem_tipo.index,
                 color=contagem_tipo.index,
                 color_discrete_map=mapa_cores(contagem_tipo.index), hole=0.4)
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      marker=dict(line=dict(color=BRANCO, width=2)))
    estilizar(fig, "Tipos de Publicação")
    salvar(fig, "01_visao_geral_02_tipos_publicacao.png")

    # 03 — Open Access
    oa = df["Is Open Access"].astype(str).str.lower()
    oa_counts = oa.value_counts()
    labels_oa = ["Open Access" if "true" in k else "Acesso Restrito" for k in oa_counts.index]
    cores_oa = [AZUL_PANTONE if "true" in k else AZUL_CLARO for k in oa_counts.index]
    fig = px.pie(values=oa_counts.values, names=labels_oa,
                 color_discrete_sequence=cores_oa, hole=0.4)
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      marker=dict(line=dict(color=BRANCO, width=2)))
    estilizar(fig, "Open Access vs. Acesso Restrito")
    salvar(fig, "01_visao_geral_03_open_access.png")

    # 04 — Modalidades de Open Access
    oa_cor = df[oa == "true"]["Open Access Colour"].fillna("unknown").value_counts()
    if len(oa_cor) > 0:
        fig = px.bar(x=oa_cor.index, y=oa_cor.values,
                     color=oa_cor.index, color_discrete_map=mapa_cores(oa_cor.index),
                     labels={"x": "Modalidade de Open Access", "y": "Número de Artigos"})
        fig.update_layout(showlegend=False)
        fig.update_traces(text=oa_cor.values, textposition="outside")
        estilizar(fig, "Modalidades de Open Access")
        salvar(fig, "01_visao_geral_04_modalidades_open_access.png")


# ============================================================
# 5. ABA 2 — FONTES E AUTORES
# ============================================================

def aba_fontes_autores(df):
    print("Aba 2 — Fontes e Autores")

    # 01 — Top 15 Journals
    contagem = df["Source Title"].fillna("Não informado").value_counts().head(15)
    fig = px.bar(x=contagem.values, y=contagem.index, orientation="h",
                 color_discrete_sequence=[AZUL_PANTONE],
                 labels={"x": "Número de Artigos", "y": ""})
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=contagem.values, textposition="outside")
    estilizar(fig, "Top 15 Journals / Fontes")
    salvar(fig, "02_fontes_autores_01_top_journals.png")

    # 02 — Top 20 Autores
    todos_autores = []
    for autores in df["Author/s"].dropna():
        for autor in str(autores).split(";"):
            autor = autor.strip()
            if autor:
                todos_autores.append(autor)
    contagem_autores = pd.Series(todos_autores).value_counts().head(20)
    fig = px.bar(x=contagem_autores.values, y=contagem_autores.index, orientation="h",
                 color_discrete_sequence=[AZUL_MEDIO],
                 labels={"x": "Número de Artigos", "y": ""})
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=contagem_autores.values, textposition="outside")
    estilizar(fig, "Top 20 Autores Mais Ativos")
    salvar(fig, "02_fontes_autores_02_top_autores.png")

    # 03 — Top 10 Editoras
    contagem_pub = df["Publisher"].fillna("Não informado").value_counts().head(10)
    fig = px.bar(x=contagem_pub.values, y=contagem_pub.index, orientation="h",
                 color_discrete_sequence=[AZUL_PANTONE],
                 labels={"x": "Número de Artigos", "y": ""})
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=contagem_pub.values, textposition="outside")
    estilizar(fig, "Top 10 Editoras (Publishers)")
    salvar(fig, "02_fontes_autores_03_top_editoras.png")


# ============================================================
# 6. ABA 3 — IMPACTO E CITACOES
# ============================================================

def aba_impacto(df):
    print("Aba 3 — Impacto e Citações")

    # 01 — Bubble chart de artigos mais citados
    df_bubble = df.dropna(subset=["Date Published"]).copy()
    df_bubble = df_bubble[df_bubble["Citing Works Count"] > 0]
    df_bubble_top = df_bubble.nlargest(200, "Citing Works Count").copy()
    df_bubble_top["Área de Aplicação"] = df_bubble_top["strings_lista"].apply(
        lambda lst: AREA_APLICACAO.get(lst[0], "Outros") if lst else "Outros")
    fig = px.scatter(
        df_bubble_top, x="Date Published", y="Citing Works Count",
        size="Citing Works Count", color="Área de Aplicação",
        color_discrete_map=COR_AREA, size_max=40,
        labels={"Date Published": "Data de Publicação", "Citing Works Count": "Citações"},
        category_orders={"Área de Aplicação": ORDEM_AREA},
    )
    fig.update_traces(marker=dict(line=dict(color=BRANCO, width=1)))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    estilizar(fig, "Artigos Mais Citados ao Longo do Tempo")
    salvar(fig, "03_impacto_citacoes_01_artigos_citados.png")

    # 02 — Distribuicao de citacoes (histograma)
    df_cit = df[df["Citing Works Count"] > 0].copy()
    fig = px.histogram(df_cit, x="Citing Works Count", nbins=50,
                       color_discrete_sequence=[AZUL_PANTONE],
                       labels={"Citing Works Count": "Número de Citações"}, log_y=True)
    fig.update_layout(yaxis_title="Quantidade de Artigos (escala log)")
    estilizar(fig, "Distribuição de Citações")
    salvar(fig, "03_impacto_citacoes_02_distribuicao_citacoes.png")


# ============================================================
# 7. ABA 4 — CAMPOS DE ESTUDO
# ============================================================

def aba_campos_estudo(df):
    print("Aba 4 — Campos de Estudo")

    # 01 — Treemap de Fields of Study
    todos_campos = []
    for campos in df["Fields of Study"].dropna():
        for campo in str(campos).split(";"):
            campo = campo.strip()
            if campo:
                todos_campos.append(campo)
    contagem = pd.Series(todos_campos).value_counts().head(30).reset_index()
    contagem.columns = ["Campo", "Frequência"]
    fig = px.treemap(contagem, path=["Campo"], values="Frequência",
                     color="Frequência", color_continuous_scale=ESCALA_CONTINUA)
    fig.update_traces(textinfo="label+value",
                      marker=dict(line=dict(color=BRANCO, width=2)))
    estilizar(fig, "Top 30 Campos de Estudo (Fields of Study)")
    salvar(fig, "04_campos_estudo_01_treemap_campos.png")

    # 02 — Nuvem de palavras (matplotlib) com paleta azul institucional
    todas_kw = []
    for kws in df["Keywords"].dropna():
        for kw in str(kws).split(";"):
            kw = kw.strip()
            if kw:
                todas_kw.append(kw)
    if todas_kw:
        freq_kw = dict(pd.Series(todas_kw).value_counts().head(100))
        tons_kw = ["#16243F", "#2A4677", "#3C60A7", "#5E7FC0", "#8AA3D4"]

        def cor_azul(word, font_size, position, orientation, random_state=None, **kwargs):
            # Palavras maiores recebem azul mais escuro (mais destaque)
            idx = min(int((font_size / 220) * len(tons_kw)), len(tons_kw) - 1)
            return tons_kw[len(tons_kw) - 1 - idx]

        # Dimensoes reais padronizadas: 2560 x 1440 px
        larg_px, alt_px = LARGURA * ESCALA, ALTURA * ESCALA
        # A nuvem ocupa a faixa central; sobram margens para titulo e rodape
        marg_topo, marg_base = 150, 90
        alt_nuvem = alt_px - marg_topo - marg_base

        wc = WordCloud(
            width=larg_px, height=alt_nuvem,
            background_color=BRANCO, color_func=cor_azul,
            max_words=80, prefer_horizontal=0.75,
            min_font_size=18, max_font_size=220, relative_scaling=0.5,
        ).generate_from_frequencies(freq_kw)

        fig = plt.figure(figsize=(larg_px / DPI_MPL, alt_px / DPI_MPL), dpi=DPI_MPL)
        fig.patch.set_facecolor(BRANCO)
        ax = fig.add_axes([0, marg_base / alt_px, 1, alt_nuvem / alt_px])
        ax.imshow(wc, interpolation="bilinear", aspect="auto")
        ax.axis("off")
        fig.text(0.5, 1 - (marg_topo / 2) / alt_px, "Nuvem de Palavras — Keywords",
                 ha="center", va="center", fontsize=28, fontfamily=FONTE,
                 color=AZUL_ESCURO, fontweight="bold")
        fig.text(0.02, (marg_base / 2) / alt_px, RODAPE, ha="left", va="center",
                 fontsize=13, color=CINZA_FONTE, fontfamily=FONTE)
        caminho = os.path.join(PASTA_SAIDA, "04_campos_estudo_02_nuvem_palavras.png")
        fig.savefig(caminho, dpi=DPI_MPL, facecolor=BRANCO)
        plt.close(fig)
        print("  [OK] 04_campos_estudo_02_nuvem_palavras.png")


# ============================================================
# 8. ABA 5 — GEOGRAFIA
# ============================================================

def aba_geografia(df):
    print("Aba 5 — Geografia")

    contagem_pais = df["Source Country"].dropna().value_counts().reset_index()
    contagem_pais.columns = ["País", "Artigos"]

    def pais_para_iso3(nome):
        try:
            return pycountry.countries.lookup(nome).alpha_3
        except LookupError:
            return None

    contagem_pais["ISO3"] = contagem_pais["País"].apply(pais_para_iso3)
    contagem_pais = contagem_pais.dropna(subset=["ISO3"])

    # 01 — Mapa choropleth
    fig = px.choropleth(contagem_pais, locations="ISO3", locationmode="ISO-3",
                        color="Artigos", color_continuous_scale=ESCALA_CONTINUA,
                        labels={"Artigos": "Número de Artigos"})
    fig.update_geos(showframe=False, showcoastlines=True, coastlinecolor=AZUL_CLARO,
                    projection_type="natural earth", bgcolor=BRANCO,
                    landcolor="#F2F4F8", showland=True)
    estilizar(fig, "Distribuição Geográfica das Publicações")
    salvar(fig, "05_geografia_01_mapa_mundial.png")

    # 02 — Top 15 paises
    top_paises = contagem_pais.head(15)
    fig = px.bar(top_paises, x="Artigos", y="País", orientation="h",
                 color_discrete_sequence=[AZUL_PANTONE])
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=top_paises["Artigos"], textposition="outside")
    estilizar(fig, "Top 15 Países por Número de Publicações")
    salvar(fig, "05_geografia_02_top_paises.png")


# ============================================================
# 9. ABA 6 — STRINGS DE BUSCA
# ============================================================

def aba_strings(df):
    print("Aba 6 — Strings de Busca")

    # 01 — Volume por string
    contagem = {}
    for _, row in df.iterrows():
        for s in row["strings_lista"]:
            contagem[s] = contagem.get(s, 0) + 1
    dados = [{"String": f"#{n}", "Descrição": STRINGS_BUSCA.get(n, ""),
              "Artigos": contagem[n], "Prioridade": PRIORIDADES.get(n, "Baixa")}
             for n in sorted(contagem.keys())]
    df_strings = pd.DataFrame(dados)
    fig = px.bar(df_strings, x="String", y="Artigos", color="Prioridade",
                 color_discrete_map=COR_PRIORIDADE,
                 category_orders={"Prioridade": ["Alta", "Media", "Baixa"]},
                 hover_data=["Descrição"], labels={"Artigos": "Artigos Únicos"})
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig.update_traces(texttemplate="%{y}", textposition="outside")
    estilizar(fig, "Volume de Artigos por String de Busca")
    salvar(fig, "06_strings_busca_01_volume_strings.png")

    # 02 — Sobreposicao entre strings
    contagem_overlap = df["qtd_strings"].value_counts().sort_index()
    fig = px.bar(x=contagem_overlap.index.astype(str), y=contagem_overlap.values,
                 color_discrete_sequence=[AZUL_PANTONE],
                 labels={"x": "Aparece em N strings", "y": "Quantidade de Artigos"})
    fig.update_traces(text=[f"{v} ({v/len(df)*100:.1f}%)" for v in contagem_overlap.values],
                      textposition="outside")
    estilizar(fig, "Sobreposição entre Strings de Busca")
    salvar(fig, "06_strings_busca_02_sobreposicao.png")

    # 03 — Heatmap de coocorrencia
    strings_presentes = sorted(set(s for lst in df["strings_lista"] for s in lst))
    n = len(strings_presentes)
    idx_map = {s: i for i, s in enumerate(strings_presentes)}
    matriz = np.zeros((n, n), dtype=int)
    for lst in df["strings_lista"]:
        if len(lst) > 1:
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    si, sj = lst[i], lst[j]
                    if si in idx_map and sj in idx_map:
                        matriz[idx_map[si]][idx_map[sj]] += 1
                        matriz[idx_map[sj]][idx_map[si]] += 1
    labels_str = [f"#{s}" for s in strings_presentes]
    fig = go.Figure(data=go.Heatmap(
        z=matriz, x=labels_str, y=labels_str,
        colorscale=ESCALA_CONTINUA, text=matriz, texttemplate="%{text}",
        textfont={"size": 11}, colorbar=dict(title="Artigos")))
    estilizar(fig, "Coocorrência entre Strings de Busca")
    fig.update_xaxes(tickangle=45, showgrid=False)
    fig.update_yaxes(showgrid=False, autorange="reversed")
    salvar(fig, "06_strings_busca_03_coocorrencia.png")


# ============================================================
# 10. ABA 7 — ALGORITMOS E ABORDAGENS
# ============================================================

def aba_algoritmos(df_algo):
    print("Aba 7 — Algoritmos e Abordagens")

    # Helper local: rotulo combinado "valor absoluto + (percentual)" em pt-BR.
    def _rotulo_abs_pct(serie):
        total = float(serie.sum())
        return serie.apply(
            lambda v: f"{int(v)}<br>({(v/total*100):.1f}".replace(".", ",")
                      + "%)"
        )

    # 01 — Distribuição por paradigma (barras verticais com valor + %)
    contagem_p = df_algo["paradigma"].value_counts().reset_index()
    contagem_p.columns = ["Paradigma", "Trabalhos"]
    contagem_p["Rotulo"] = _rotulo_abs_pct(contagem_p["Trabalhos"])
    fig = px.bar(contagem_p, x="Paradigma", y="Trabalhos",
                 color_discrete_sequence=[AZUL_PANTONE], text="Rotulo",
                 labels={"Trabalhos": "Número de Trabalhos",
                         "Paradigma": "Paradigma"})
    fig.update_traces(textposition="outside", cliponaxis=False,
                      textfont=dict(size=16, color=AZUL_ESCURO, family=FONTE),
                      marker=dict(line=dict(color=BRANCO, width=0)))
    fig.update_layout(showlegend=False, bargap=0.35)
    fig.update_yaxes(rangemode="tozero")
    estilizar(fig, "Distribuição por Paradigma Quântico")
    salvar(fig, "07_algoritmos_01_paradigma.png")

    # 02 — Distribuição por abordagem (barras HORIZONTAIS com valor + %)
    contagem_a = df_algo["abordagem"].value_counts().reset_index()
    contagem_a.columns = ["Abordagem", "Trabalhos"]
    total_a = float(contagem_a["Trabalhos"].sum())
    # rotulo em linha unica fica melhor a direita da barra horizontal
    contagem_a["Rotulo"] = contagem_a["Trabalhos"].apply(
        lambda v: f"{int(v)}   ({(v/total_a*100):.1f}".replace(".", ",")
                  + "%)")
    fig = px.bar(contagem_a, x="Trabalhos", y="Abordagem", orientation="h",
                 color_discrete_sequence=[AZUL_MEDIO], text="Rotulo",
                 labels={"Trabalhos": "Número de Trabalhos",
                         "Abordagem": "Abordagem"})
    fig.update_layout(yaxis=dict(autorange="reversed"),
                      showlegend=False, bargap=0.35)
    fig.update_traces(textposition="outside", cliponaxis=False,
                      textfont=dict(size=16, color=AZUL_ESCURO, family=FONTE),
                      marker=dict(line=dict(color=BRANCO, width=0)))
    fig.update_xaxes(rangemode="tozero")
    estilizar(fig, "Distribuição por Abordagem")
    salvar(fig, "07_algoritmos_02_abordagem.png")

    # 03 — Distribuicao por topico
    contagem_t = df_algo["topico"].value_counts().reset_index()
    contagem_t.columns = ["Tópico", "Trabalhos"]
    fig = px.bar(contagem_t, x="Trabalhos", y="Tópico", orientation="h",
                 color="Tópico", color_discrete_map=mapa_cores(contagem_t["Tópico"]),
                 text="Trabalhos")
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
    fig.update_traces(textposition="outside")
    estilizar(fig, "Distribuição por Tópico")
    salvar(fig, "07_algoritmos_03_topico.png")

    # 04 — Algoritmos quanticos mais frequentes
    contagem_alg = df_algo["algoritmo_quantico"].value_counts().reset_index()
    contagem_alg.columns = ["Algoritmo", "Trabalhos"]
    fig = px.bar(contagem_alg, x="Trabalhos", y="Algoritmo", orientation="h",
                 color_discrete_sequence=[AZUL_PANTONE])
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=contagem_alg["Trabalhos"], textposition="outside")
    estilizar(fig, "Algoritmos Quânticos Mais Frequentes")
    salvar(fig, "07_algoritmos_04_algoritmos_frequentes.png")

    # 05 — Problemas mais frequentes (Top 15)
    contagem_sub = df_algo["problema"].value_counts().head(15).reset_index()
    contagem_sub.columns = ["Problema", "Trabalhos"]
    fig = px.bar(contagem_sub, x="Trabalhos", y="Problema", orientation="h",
                 color_discrete_sequence=[AZUL_MEDIO])
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(text=contagem_sub["Trabalhos"], textposition="outside")
    estilizar(fig, "Problemas Mais Frequentes (Top 15)")
    salvar(fig, "07_algoritmos_05_problemas.png")

    # 06 — Paradigma por topico (barras empilhadas)
    contagem_pt = df_algo.groupby(["topico", "paradigma"]).size().reset_index(name="Trabalhos")
    fig = px.bar(contagem_pt, x="Trabalhos", y="topico", orientation="h",
                 color="paradigma", color_discrete_map=mapa_cores(sorted(df_algo["paradigma"].dropna().unique())),
                 labels={"topico": "Tópico", "paradigma": "Paradigma"})
    fig.update_layout(barmode="stack", yaxis=dict(autorange="reversed"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    estilizar(fig, "Paradigma por Tópico")
    salvar(fig, "07_algoritmos_06_paradigma_por_topico.png")

    # 07 — Heatmap Topico x Algoritmo
    heat = df_algo.groupby(["topico", "algoritmo_quantico"]).size().reset_index(name="Qtd")
    pivot = heat.pivot_table(index="topico", columns="algoritmo_quantico",
                             values="Qtd", fill_value=0)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=ESCALA_CONTINUA, text=pivot.values, texttemplate="%{text}",
        colorbar=dict(title="Trabalhos")))
    estilizar(fig, "Heatmap: Tópico × Algoritmo Quântico")
    fig.update_xaxes(title="Algoritmo Quântico", showgrid=False, tickangle=30)
    fig.update_yaxes(title="Tópico", showgrid=False, autorange="reversed")
    salvar(fig, "07_algoritmos_07_heatmap_topico_algoritmo.png")

    # 08 — Treemap hierarquico
    df_tree = df_algo[["topico", "problema", "paradigma"]].copy()
    df_tree["count"] = 1
    fig = px.treemap(df_tree, path=["topico", "problema", "paradigma"], values="count",
                     color="topico", color_discrete_map=mapa_cores(df_algo["topico"].dropna().unique()))
    fig.update_traces(textinfo="label+value", marker=dict(line=dict(color=BRANCO, width=2)))
    estilizar(fig, "Treemap: Tópico → Problema → Paradigma")
    salvar(fig, "07_algoritmos_08_treemap.png")

    # 09 — Radar de criterios por autor (top 5 por ranking)
    CRITERIOS_RADAR = {
        "C1": "Qualidade da Solução", "C2": "Escalabilidade", "C3": "Aplicação Real",
        "C4": "Comparação c/ Clássico", "C5": "Análise de Limitações", "C6": "Taxa de Sucesso",
    }
    PESOS_RADAR = {"C1": 20, "C2": 15, "C3": 20, "C4": 15, "C5": 10, "C6": 20}
    codigos = list(CRITERIOS_RADAR.keys())
    labels_radar = list(CRITERIOS_RADAR.values())

    if "ranking" in df_algo.columns:
        df_rank = df_algo[df_algo["ranking"] > 0].sort_values("ranking", ascending=False)
        autores_sel = df_rank["autores"].drop_duplicates().head(5).tolist()
    else:
        autores_sel = df_algo["autores"].drop_duplicates().head(5).tolist()

    if autores_sel:
        tons_radar = gerar_tons(len(autores_sel))
        fig = go.Figure()
        for i, autor in enumerate(autores_sel):
            row = df_algo[df_algo["autores"] == autor].iloc[0]
            crit = row["criterios"] if pd.notna(row["criterios"]) else ""
            presentes = (set() if crit.strip().lower() == "nao reportada"
                         else {c.strip() for c in crit.split(",")})
            valores = [PESOS_RADAR[c] if c in presentes else 0 for c in codigos]
            valores.append(valores[0])
            rank = int(row["ranking"]) if "ranking" in row.index and pd.notna(row["ranking"]) else 0
            fig.add_trace(go.Scatterpolar(
                r=valores, theta=labels_radar + [labels_radar[0]], fill="toself",
                name=f"{autor} (R:{rank})", line_color=tons_radar[i], opacity=0.55))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 20]),
                                     bgcolor=BRANCO),
                          legend=dict(orientation="h", yanchor="bottom", y=-0.18))
        estilizar(fig, "Radar de Critérios por Autor (Top 5 por Ranking)")
        salvar(fig, "07_algoritmos_09_radar_criterios.png")


# ============================================================
# 11. EXECUCAO PRINCIPAL
# ============================================================

def main():
    random.seed(42)
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    print("=" * 60)
    print("EXPORTACAO DE IMAGENS — Dashboard Bibliometrico TSP Quantico")
    print(f"Padrao: {LARGURA}x{ALTURA}px @ {ESCALA}x  |  Azul Pantone 293 (#3C60A7)")
    print(f"Destino: {PASTA_SAIDA}")
    print("=" * 60)

    df = carregar_dados()
    df_algo = carregar_algoritmos()

    aba_visao_geral(df)
    aba_fontes_autores(df)
    aba_impacto(df)
    aba_campos_estudo(df)
    aba_geografia(df)
    aba_strings(df)
    aba_algoritmos(df_algo)

    print("=" * 60)
    print(f"Concluido. Imagens salvas em: {PASTA_SAIDA}")
    print("=" * 60)


if __name__ == "__main__":
    main()
