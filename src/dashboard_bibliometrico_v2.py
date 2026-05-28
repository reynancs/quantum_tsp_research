"""
Dashboard Bibliometrico v2 — Fase 1 (Exploracao Bibliografica)

Versao reorganizada do dashboard interativo Streamlit para o projeto
"TSP + Computacao Quantica" (Mestrado SENAI CIMATEC).

Estrutura linear de pipeline (inspirada no reference QML/Supply Chain):
    Home → Estrategia de Busca → Deduplicacao → Analise Bibliometrica
         → Geografia → Algoritmos e Abordagens (Phillipson 2025)

Bases de dados (todas em data/):
    - artigos_unicos.csv              (3.696 artigos pos-dedup)
    - resumo_deduplicacao.csv         (metricas do processo de dedup)
    - resumo_por_string.csv           (volume por string de busca)
    - base_algoritmos_abordagens.csv  (129 trabalhos catalogados — Phillipson 2025)
Auxiliar:
    - data/pesquisa_palavras_chave_tsp_quantico.xlsx (strings completas)

Como usar:
    streamlit run src/dashboard_bibliometrico_v2.py
"""

import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import pycountry


# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Análise Bibliométrica — TSP Quântico (v2)",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PALETA DE CORES E CONSTANTES TEMATICAS
# ============================================================
# Modelo HIBRIDO de paleta — duas paletas convivem, cada uma com seu papel:
#
# 1) MONOCROMATICA AZUL (ancorada no Pantone 293 #3C60A7)
#    Aplicada onde HA ordem narrativa ou escala numerica:
#      - Prioridade Alta/Media/Baixa  -> peso visual decrescente
#      - Heatmaps de intensidade       -> rampa branco -> azul escuro
#      - Treemap de Fields            -> rampa de frequencia
#      - Choropleth geografico        -> rampa de volume
#    Convencao de tons (escuro -> claro):
#      #0A1E47 -> #1E3A6F -> #3C60A7 -> #6585BD -> #8EA8D2 -> #D6DFEF
#
# 2) CATEGORICA SOBRIA (PALETA_CATEGORICA)
#    Aplicada em variaveis NOMINAIS sem ordem natural:
#      - Fields of Study, paradigma, topico, area, tipo de publicacao
#    Diferenciacao por MATIZ (nao luminancia) — categorias adjacentes ficam
#    visualmente separaveis mesmo quando 10+ series coexistem. Primeira cor
#    sempre = Pantone 293 (mantem coerencia de marca); ultima = cinza neutro
#    para "Outros".
#
# Cinza (#BFC4CC) e neutralizador universal em ambos os modelos:
# usado para "Outros", "Nao informado", baixa prioridade.

# --- Tokens base da marca ---
AZUL_PANTONE_293 = "#3C60A7"   # R60 G96 B167 — cor identidade

CORES = {
    # Tons da familia azul (ordenados do mais escuro ao mais claro)
    "deepest":   "#0A1E47",   # azul-quase-preto — peso maximo
    "dark":      "#1E3A6F",   # azul marinho — destaque forte / categoria dominante
    "primary":   AZUL_PANTONE_293,  # Pantone 293 — cor base da identidade
    "secondary": "#6585BD",   # azul medio-claro
    "accent":    "#8EA8D2",   # azul claro
    "highlight": "#D6DFEF",   # azul muito claro — fundos, inicio de escala
    "white":     "#FFFFFF",   # branco principal
    # Neutros para itens "apagados" (baixa prioridade, "Outros", nao informado)
    "muted":     "#BFC4CC",   # cinza claro
    "muted_dark":"#4A4D52",   # cinza escuro — anotacoes, linhas de referencia
    # Aliases semanticos (mantidos para nao quebrar referencias antigas;
    # remapeados para a familia azul/cinza — sem verde/laranja/amarelo)
    "success":   AZUL_PANTONE_293,  # Open Access -> azul Pantone (positivo)
    "warning":   "#1E3A6F",          # alertas -> azul marinho (peso)
    "danger":    "#0A1E47",          # destaque critico -> azul-quase-preto
}

# Paleta sequencial em azul — usada APENAS em escalas ordinais/numericas
# (Alta/Media/Baixa, heatmaps, treemap, choropleth). Para categorias nominais
# (Fields, paradigma, topico, etc.) use PALETA_CATEGORICA abaixo.
PALETTE = [
    "#0A1E47",  # quase preto
    "#1E3A6F",  # marinho
    "#2A4A85",  # escuro
    "#3C60A7",  # Pantone 293
    "#4D72B3",  # medio
    "#6585BD",  # medio claro
    "#7A97C8",  # claro alt
    "#8EA8D2",  # claro
    "#B6C8E2",  # muito claro
    "#D6DFEF",  # quase branco
]

# Paleta categorica HIBRIDA (sobria) para variaveis NOMINAIS sem ordem natural.
# Ancorada no Pantone 293 (#1, cor da marca) + 9 cores em saturacao media,
# escolhidas por diferenca de MATIZ (nao apenas luminancia) para garantir
# distincao mesmo em graficos com 10+ series. Ultima posicao reservada ao
# cinza neutro de "Outros" / "Nao informado".
PALETA_CATEGORICA = [
    AZUL_PANTONE_293,  # 1  — Pantone 293 (marca)
    "#D97757",         # 2  — terracota
    "#5BAA52",         # 3  — verde sobrio
    "#9B59B6",         # 4  — roxo
    "#E0AC2B",         # 5  — mostarda
    "#1E3A6F",         # 6  — azul marinho (familia)
    "#2A9D8F",         # 7  — teal
    "#C0506C",         # 8  — rosa-vinho
    "#8B6F47",         # 9  — marrom
    "#5A7A9F",         # 10 — azul-aco claro
    "#BFC4CC",         # cinza — reservado para "Outros"
]

# PALETTE_PUB_TYPE — tipos de publicacao. Categoria nominal: cada tipo recebe
# uma cor distinta da paleta categorica. Journal article (mais frequente)
# herda o Pantone 293; "other" recebe o cinza neutro.
PALETTE_PUB_TYPE = {
    "journal article":                AZUL_PANTONE_293,  # mais comum — cor da marca
    "preprint":                       "#1E3A6F",         # azul marinho — formal
    "conference proceedings article": "#D97757",         # terracota
    "book chapter":                   "#5BAA52",         # verde
    "book":                           "#E0AC2B",         # mostarda
    "dissertation":                   "#9B59B6",         # roxo
    "report":                         "#2A9D8F",         # teal
    "other":                          "#BFC4CC",         # cinza — neutralizado
}

# 26 strings de busca executadas no Lens.org (cf. data/resumo_por_string.csv)
STRINGS_BUSCA = {
    1:  "TSP + Quantum Computing",
    2:  "TSP + Quantum Algorithms",
    3:  "TSP + Quantum Annealing",
    4:  "TSP + QAOA",
    5:  "TSP + Hybrid Quantum",
    6:  "VRP + Quantum Computing",
    7:  "Comb. Opt. + QA",
    8:  "TSP + VQE",
    9:  "TSP + Grover",
    10: "QUBO + TSP",
    11: "Route Opt. + Quantum + Log.",
    12: "TSP + D-Wave",
    13: "TSP + IBM Quantum",
    14: "TSP + Ising Model",
    15: "VRP + QA + Logistics",
    16: "Hamiltonian Cycle + Quantum",
    17: "VRP + QAOA",
    18: "QC + Supply Chain Mgmt",
    19: "TSP + Quantum-Inspired",
    20: "QRL + Routing",
    21: "CVRP + QA",
    22: "Job Shop + Quantum",
    23: "Bin Packing + Quantum",
    24: "Facility Location + QC",
    25: "Knapsack + Quantum",
    26: "QML + Supply Chain",
}

# Prioridade tematica de cada string (relevancia ao TSP em logistica)
PRIORIDADES = {
    1: "Alta",  2: "Alta",  3: "Alta",  4: "Alta",  5: "Alta",
    6: "Alta", 17: "Alta", 18: "Alta",
    7: "Media", 8: "Media",  9: "Media", 10: "Media", 11: "Media",
    12: "Media", 19: "Media", 20: "Media", 21: "Media", 22: "Media",
    13: "Baixa", 14: "Baixa", 15: "Baixa", 16: "Baixa",
    23: "Baixa", 24: "Baixa", 25: "Baixa", 26: "Baixa",
}

# COR_PRIORIDADE — gradiente decrescente de peso visual.
# Alta atrai o olho primeiro (azul escuro saturado), Baixa recua (cinza).
COR_PRIORIDADE = {
    "Alta":  "#1E3A6F",         # azul marinho — protagonismo
    "Media": AZUL_PANTONE_293,  # Pantone — destaque medio
    "Baixa": "#BFC4CC",         # cinza — apagado, coro
}

# Areas tematicas para o bubble chart (fallback quando Field of Study esta vazio)
AREA_APLICACAO = {
    1: "TSP",  2: "TSP",  3: "TSP",  4: "TSP",  5: "TSP",
    8: "TSP",  9: "TSP", 10: "TSP", 12: "TSP", 13: "TSP",
    14: "TSP", 16: "TSP", 19: "TSP",
    6: "VRP/Logística", 11: "VRP/Logística", 15: "VRP/Logística",
    17: "VRP/Logística", 21: "VRP/Logística",
    18: "Supply Chain/QML", 20: "Supply Chain/QML", 26: "Supply Chain/QML",
    7: "Otim. Combinatória", 22: "Otim. Combinatória",
    23: "Otim. Combinatória", 24: "Otim. Combinatória",
    25: "Otim. Combinatória",
}

# COR_AREA — areas tematicas (categoria nominal). TSP (foco) recebe o Pantone;
# demais areas usam cores distintas da paleta categorica para nao se confundirem
# no bubble chart.
COR_AREA = {
    "TSP":                AZUL_PANTONE_293,  # foco principal — Pantone 293
    "VRP/Logística":      "#D97757",         # terracota
    "Supply Chain/QML":   "#5BAA52",         # verde
    "Otim. Combinatória": "#9B59B6",         # roxo
    "Outros":             "#BFC4CC",         # cinza
}

# PALETA_FIELDS — Top-10 Fields of Study + "Outros".
# Usa a PALETA_CATEGORICA: matizes distintos garantem que cada Field seja
# perceptualmente separavel no bubble chart e no leaderboard, mesmo quando
# 11 series coexistem no mesmo grafico.
PALETA_FIELDS = list(PALETA_CATEGORICA)

# Paletas da aba Algoritmos (base Phillipson 2025) — categorias NOMINAIS.
# Categoria dominante na literatura herda o Pantone 293 (cor da marca);
# demais categorias recebem cores distintas da paleta categorica para garantir
# diferenciacao por matiz em pizzas, treemaps e barras empilhadas.

# PARADIGMA — QA (Quantum Annealing) lidera nos artigos de TSP/VRP.
PALETTE_PARADIGMA = {
    "QA":       AZUL_PANTONE_293,  # Pantone — paradigma dominante na literatura
    "GBC":      "#D97757",         # terracota
    "QA e GBC": "#9B59B6",         # roxo — combinacao
    "CA":       "#5BAA52",         # verde
    "QML":      "#E0AC2B",         # mostarda
    "QRNG":     "#2A9D8F",         # teal
    "Generic":  "#BFC4CC",         # cinza — generico/nao especifico
}

# ABORDAGEM — Hybrid (classico-quantica) e a abordagem padrao na literatura atual.
PALETTE_ABORDAGEM = {
    "Hybrid":           AZUL_PANTONE_293,  # Pantone — predominante
    "Full Quantum":     "#D97757",         # terracota
    "Full e Hybrid":    "#9B59B6",         # roxo — combinacao
    "Não especificado": "#BFC4CC",         # cinza
}

# TOPICO — Routing concentra o foco do projeto (TSP/VRP); demais sao contexto.
PALETTE_TOPICO = {
    "Routing":            AZUL_PANTONE_293,  # Pantone — foco TSP/VRP
    "Network Design":     "#D97757",         # terracota
    "Scheduling":         "#9B59B6",         # roxo
    "Cargo":              "#5BAA52",         # verde
    "Fleet Optimization": "#E0AC2B",         # mostarda
    "Prediction":         "#2A9D8F",         # teal
}

# CATEGORIA_ALGORITMO — 6 categorias do resumo_algoritmos.md aplicadas aos 129
# trabalhos catalogados. Quantum Annealing (predominante) herda o Pantone 293.
# Coluna `categoria_algoritmo` no CSV vem do script scripts/classificar_categoria_algoritmo.py.
PALETTE_CATEGORIA_ALGORITMO = {
    "Quantum Annealing":          AZUL_PANTONE_293,  # Pantone — categoria dominante (52,7%)
    "Variacional (Gate-Based)":   "#D97757",         # terracota
    "Exato (Gate-Based)":         "#5BAA52",         # verde
    "Aprendizado Quântico (QML)": "#9B59B6",         # roxo
    "Não especificado":           "#BFC4CC",         # cinza
}

# Ordem canonica para apresentacao em graficos (segue resumo_algoritmos.md 1.1-1.5)
ORDEM_CATEGORIA_ALGORITMO = [
    "Quantum Annealing",
    "Variacional (Gate-Based)",
    "Exato (Gate-Based)",
    "Aprendizado Quântico (QML)",
    "Não especificado",
]


# ============================================================
# CARREGAMENTO DE DADOS
# ============================================================
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@st.cache_data
def carregar_dados():
    """Carrega data/artigos_unicos.csv (3.696 artigos) e prepara colunas derivadas."""
    caminho = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
    df = pd.read_csv(caminho, dtype=str)

    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    df["Citing Patents Count"] = pd.to_numeric(df["Citing Patents Count"], errors="coerce").fillna(0).astype(int)
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce").fillna(1).astype(int)
    df["Date Published"] = pd.to_datetime(df["Date Published"], errors="coerce")

    # citacoes_por_ano e pre-calculada por src/deduplicar_artigos.py (ano-ref: 2026).
    # NaN aqui = artigos sem Publication Year valido (~86 de 3.696).
    if "citacoes_por_ano" in df.columns:
        df["citacoes_por_ano"] = pd.to_numeric(df["citacoes_por_ano"], errors="coerce")

    # "strings_origem" = "1;3;7" → lista [1, 3, 7]
    df["strings_lista"] = df["strings_origem"].fillna("").apply(
        lambda x: [int(float(s.strip())) for s in x.split(";")
                   if s.strip() and s.strip() != "nan"]
    )
    df["prioridade"] = df["strings_lista"].apply(
        lambda lst: PRIORIDADES.get(lst[0], "Baixa") if lst else "Baixa"
    )
    df["Publication Type"] = df["Publication Type"].fillna("other").str.lower().str.strip()
    return df


@st.cache_data
def carregar_dedup():
    """Carrega data/resumo_deduplicacao.csv (1 linha de metricas)."""
    caminho = os.path.join(PASTA_PROJETO, "data", "resumo_deduplicacao.csv")
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        return None


@st.cache_data
def carregar_algoritmos():
    """Carrega data/base_algoritmos_abordagens.csv (129 trabalhos Phillipson 2025)."""
    caminho = os.path.join(PASTA_PROJETO, "data", "base_algoritmos_abordagens.csv")
    df = pd.read_csv(caminho, dtype=str)
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype("Int64")
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    if "ranking" in df.columns:
        df["ranking"] = pd.to_numeric(df["ranking"], errors="coerce").fillna(0.0)
    return df


# ============================================================
# HELPERS
# ============================================================
# Ano de referencia para o calculo de citacoes_por_ano (deve bater com
# ANO_REFERENCIA em src/deduplicar_artigos.py — fixo em 2026 para reprodutibilidade).
ANO_REFERENCIA = 2026


def _calcular_citacoes_por_ano(df):
    """Garante a presenca da coluna `citacoes_por_ano` no DataFrame.

    A coluna e pre-calculada por src/deduplicar_artigos.py e ja vem em
    data/artigos_unicos.csv (posicao 36). Esta funcao apenas recalcula como
    fallback se a coluna estiver ausente — util quando o CSV foi gerado por
    uma versao anterior do pipeline de deduplicacao.

    Formula: citacoes / max(ANO_REFERENCIA - ano_pub, 1). Permite ranquear
    trabalhos recentes com alta velocidade de citacao ao lado dos classicos
    consolidados, corrigindo o vies temporal do ranking por citacoes totais.
    """
    out = df.copy()
    if "citacoes_por_ano" in out.columns:
        # Coluna ja vem do CSV — apenas garante que esta numerica.
        out["citacoes_por_ano"] = pd.to_numeric(out["citacoes_por_ano"], errors="coerce")
        return out
    # Fallback: CSV antigo sem a coluna pre-calculada.
    anos_desde_pub = (ANO_REFERENCIA - out["Publication Year"]).clip(lower=1)
    out["citacoes_por_ano"] = (out["Citing Works Count"] / anos_desde_pub).round(2)
    return out


def _primary_field(val):
    """Extrai o primeiro Field of Study (multi-valor separado por ';')."""
    if pd.isna(val):
        return "Não informado"
    parts = [p.strip() for p in str(val).split(";") if p.strip()]
    return parts[0] if parts else "Não informado"


def _pais_para_iso3(nome):
    """Converte nome do pais para codigo ISO-3 (None se nao encontrado)."""
    try:
        return pycountry.countries.lookup(nome).alpha_3
    except LookupError:
        return None


# ============================================================
# FILTROS (SIDEBAR)
# ============================================================
def criar_filtros(df):
    """Cria widgets de filtro na sidebar e retorna o DataFrame filtrado."""
    st.sidebar.header("Filtros")
    st.sidebar.caption(
        "Os filtros abaixo afetam **todas as abas exceto Algoritmos e Abordagens** "
        "(que possui seus próprios filtros temáticos)."
    )

    # --- Periodo ---
    anos_validos = df["Publication Year"].dropna()
    ano_min = int(anos_validos.min())
    ano_max = int(anos_validos.max())
    ano_range = st.sidebar.slider(
        "Período (Ano)",
        min_value=ano_min, max_value=ano_max,
        value=(2018, ano_max),
    )

    # --- Tipo de publicacao ---
    tipos = sorted(df["Publication Type"].unique())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de Publicação",
        options=tipos, default=None, placeholder="Todos os tipos",
    )

    # --- String de busca ---
    strings_opcoes = [f"String-{num:02d}" for num in sorted(STRINGS_BUSCA.keys())]
    strings_selecionadas = st.sidebar.multiselect(
        "String de Busca",
        options=strings_opcoes, default=None, placeholder="Todas",
    )

    # --- Prioridade ---
    prioridades_sel = st.sidebar.multiselect(
        "Prioridade da String",
        options=["Alta", "Media", "Baixa"],
        default=None, placeholder="Todas",
    )

    # --- Open Access ---
    oa_opcao = st.sidebar.radio(
        "Open Access", options=["Todos", "Sim", "Não"], horizontal=True,
    )

    # --- Citacoes minimas ---
    cit_max = min(int(df["Citing Works Count"].max()), 500)
    cit_min = st.sidebar.slider(
        "Mínimo de Citações", min_value=0, max_value=cit_max, value=0,
    )

    # Aplicar filtros via mascara booleana
    mask = pd.Series(True, index=df.index)
    mask &= df["Publication Year"].between(ano_range[0], ano_range[1]) | df["Publication Year"].isna()
    if tipos_selecionados:
        mask &= df["Publication Type"].isin(tipos_selecionados)
    if strings_selecionadas:
        nums_sel = [int(s.replace("String-", "")) for s in strings_selecionadas]
        mask &= df["strings_lista"].apply(lambda lst: any(n in lst for n in nums_sel))
    if prioridades_sel:
        mask &= df["prioridade"].isin(prioridades_sel)
    if oa_opcao == "Sim":
        mask &= df["Is Open Access"].astype(str).str.lower() == "true"
    elif oa_opcao == "Não":
        mask &= df["Is Open Access"].astype(str).str.lower() == "false"
    if cit_min > 0:
        mask &= df["Citing Works Count"] >= cit_min

    return df[mask].copy()


# ============================================================
# KPIs DO CORPUS
# ============================================================
def exibir_kpis(df):
    """Cartoes de KPI no topo da aba bibliometrica."""
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    total = len(df)
    anos = df["Publication Year"].dropna()
    citacoes = int(df["Citing Works Count"].sum())
    media_cit = df["Citing Works Count"].mean() if total > 0 else 0.0
    oa_pct = (df["Is Open Access"].astype(str).str.lower() == "true").sum() / max(total, 1) * 100
    paises = df["Source Country"].dropna().nunique()

    col1.metric("Total de Artigos", f"{total:,}")
    col2.metric("Período", f"{int(anos.min())}-{int(anos.max())}" if len(anos) > 0 else "N/A")
    col3.metric("Total de Citações", f"{citacoes:,}")
    col4.metric("Média Citações", f"{media_cit:.1f}")
    col5.metric("Open Access", f"{oa_pct:.1f}%")
    col6.metric("Países", f"{paises}")


# ============================================================
# ABA HOME — PIPELINE DA PESQUISA
# ============================================================
def aba_home(df_dedup, df_unicos, df_algoritmos):
    """Visao macro do pipeline da Fase 1 — funil das etapas."""
    total_bruto = int(df_dedup["total_bruto"].iloc[0]) if df_dedup is not None else 0
    total_unicos = int(df_dedup["total_unico"].iloc[0]) if df_dedup is not None else len(df_unicos)
    n_algoritmos = len(df_algoritmos) if df_algoritmos is not None else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Strings de Busca", f"{len(STRINGS_BUSCA)}",
        help="Combinações booleanas aplicadas no Lens.org (filtro: Scholarly Works)",
    )
    col2.metric(
        "Registros Brutos", f"{total_bruto:,}",
        help="Soma de todos os resultados das 26 strings (com duplicatas)",
    )
    col3.metric(
        "Artigos Únicos", f"{total_unicos:,}",
        help="Após deduplicação por DOI + título normalizado",
    )
    col4.metric(
        "Algoritmos Catalogados", f"{n_algoritmos}",
        help="Trabalhos extraídos do artigo de referência Phillipson (2025), páginas 50-52",
    )
    st.divider()

    st.subheader("Pipeline da Fase 1 — Exploração Bibliográfica")
    st.caption(
        "Da busca bruta no Lens.org ao corpus único pós-deduplicação, com taxonomia adicional "
        "de algoritmos catalogados a partir do artigo de referência. Use a navegação no topo "
        "para explorar cada etapa em detalhe."
    )

    estagios = [
        "Busca bruta (Lens.org · 26 strings)",
        "Únicos (pós-dedup DOI + título)",
        "Catalogados (Phillipson 2025)",
    ]
    valores = [total_bruto, total_unicos, n_algoritmos]
    fig = go.Figure(go.Funnel(
        y=estagios, x=valores,
        textinfo="value+percent initial",
        marker=dict(color=[CORES["accent"], CORES["primary"], CORES["dark"]]),
    ))
    fig.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, width="stretch")

    st.divider()
    st.markdown("##### Próximas etapas do projeto")
    st.caption(
        "A Fase 1 (exploração) está concluída. As etapas seguintes — Fundamentação Teórica, "
        "Metodologia, Resultados e Montagem Final — usarão o corpus aqui caracterizado como "
        "insumo para o artigo técnico-científico. Triagem PRISMA-ScR e revisão full-text "
        "serão incorporadas em versões futuras deste dashboard."
    )


# ============================================================
# ABA — ESTRATEGIA DE BUSCA (STRINGS)
# ============================================================
def aba_strings(df):
    """Analise das 26 strings: volume, sobreposicao, coocorrencia e referencia."""

    st.subheader("Volume de Artigos por String de Busca")
    st.caption(
        "Número de artigos únicos recuperados por cada uma das 26 strings booleanas "
        "aplicadas no Lens.org, coloridas por prioridade temática. Permite identificar "
        "strings dominantes (Knapsack + Quantum, Combinatorial Optimization + QA) versus "
        "strings de nicho (TSP + IBM Quantum, CVRP + QA)."
    )

    contagem = {}
    for _, row in df.iterrows():
        for s in row["strings_lista"]:
            contagem[s] = contagem.get(s, 0) + 1

    dados_string = []
    for num in sorted(contagem.keys()):
        dados_string.append({
            "String": f"#{num}",
            "Descrição": STRINGS_BUSCA.get(num, ""),
            "Artigos": contagem[num],
            "Prioridade": PRIORIDADES.get(num, "Baixa"),
        })
    df_strings = pd.DataFrame(dados_string)

    fig = px.bar(
        df_strings, x="String", y="Artigos",
        color="Prioridade", color_discrete_map=COR_PRIORIDADE,
        hover_data=["Descrição"],
        labels={"Artigos": "Artigos Únicos"},
    )
    fig.update_layout(
        height=450, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_traces(texttemplate="%{y}", textposition="outside")
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("Sobreposição entre Strings")
    st.caption(
        "Distribuição de quantos artigos aparecem em 1, 2, 3+ strings simultaneamente. "
        "A predominância da barra 'aparece em 1 string' indica que as buscas são "
        "complementares (cobrem nichos diferentes) — sobreposição alta sinalizaria "
        "redundância nas combinações de termos."
    )
    contagem_overlap = df["qtd_strings"].value_counts().sort_index()
    fig_overlap = px.bar(
        x=contagem_overlap.index.astype(str),
        y=contagem_overlap.values,
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Aparece em N strings", "y": "Qtd Artigos"},
    )
    fig_overlap.update_layout(height=420, plot_bgcolor="white")
    fig_overlap.update_traces(
        text=[f"{v} ({v/len(df)*100:.1f}%)" for v in contagem_overlap.values],
        textposition="outside",
    )
    st.plotly_chart(fig_overlap, width="stretch")

    st.divider()

    st.subheader("Coocorrência entre Strings")
    st.caption(
        "Heatmap: quantos artigos compartilham cada par de strings de busca. "
        "Células escuras revelam pares com forte interseção temática (ex: TSP + QAOA "
        "frequentemente coocorre com TSP + Hybrid Quantum)."
    )

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

    fig_heat = go.Figure(data=go.Heatmap(
        z=matriz, x=labels_str, y=labels_str,
        colorscale=[[0, "#FFFFFF"], [0.15, "#D6DFEF"], [0.4, "#8EA8D2"], [0.7, "#3C60A7"], [1, "#0A1E47"]],
        text=matriz, texttemplate="%{text}", textfont={"size": 9},
    ))
    fig_heat.update_layout(height=600, xaxis=dict(tickangle=45))
    st.plotly_chart(fig_heat, width="stretch")

    st.divider()
    st.subheader("Referência — Strings de Busca Utilizadas")
    st.caption("Fonte: Levantamento bibliográfico no Lens.org (filtro: Scholarly Works · data: 13/03/2026)")

    dados_ref = []
    for num in sorted(STRINGS_BUSCA.keys()):
        dados_ref.append({
            "Código": f"String-{num:02d}",
            "Descrição Resumida": STRINGS_BUSCA[num],
            "Prioridade": PRIORIDADES.get(num, "Baixa"),
        })
    df_ref = pd.DataFrame(dados_ref)

    # Tentar enriquecer com strings completas e totais brutos da planilha auxiliar
    try:
        caminho_xlsx = os.path.join(
            PASTA_PROJETO, "data", "pesquisa_palavras_chave_tsp_quantico.xlsx"
        )
        # Fallback para localizacao antiga em docs/
        if not os.path.exists(caminho_xlsx):
            caminho_xlsx = os.path.join(
                PASTA_PROJETO, "docs", "pesquisa_palavras_chave_tsp_quantico.xlsx"
            )
        df_xlsx = pd.read_excel(
            caminho_xlsx, sheet_name="Palavras-Chave vs Artigos", header=None
        )
        strings_completas, totais = {}, {}
        for _, row in df_xlsx.iterrows():
            try:
                num = int(row.iloc[0])
                if 1 <= num <= 26:
                    strings_completas[num] = str(row.iloc[1]).strip()
                    totais[num] = int(row.iloc[5]) if pd.notna(row.iloc[5]) else 0
            except (ValueError, TypeError):
                continue
        df_ref["String de Busca Completa"] = df_ref["Código"].apply(
            lambda x: strings_completas.get(
                int(x.replace("String-", "")),
                STRINGS_BUSCA.get(int(x.replace("String-", "")), ""),
            )
        )
        df_ref["Total Bruto"] = df_ref["Código"].apply(
            lambda x: totais.get(int(x.replace("String-", "")), 0)
        )
    except Exception:
        df_ref["String de Busca Completa"] = df_ref["Descrição Resumida"]
        df_ref["Total Bruto"] = 0

    st.dataframe(
        df_ref[["Código", "String de Busca Completa", "Prioridade", "Total Bruto"]].reset_index(drop=True),
        height=560, width="stretch",
        column_config={
            "Código": st.column_config.TextColumn(width="small"),
            "String de Busca Completa": st.column_config.TextColumn(width="large"),
            "Prioridade": st.column_config.TextColumn(width="small"),
            "Total Bruto": st.column_config.NumberColumn(width="small"),
        },
    )


# ============================================================
# ABA — DEDUPLICACAO
# ============================================================
def aba_deduplicacao(df_dedup, df_unicos):
    """KPIs e mini-funil da etapa de deduplicacao."""
    st.subheader("Etapa 1 — Deduplicação do Corpus")
    st.caption(
        "Remoção de duplicatas por DOI (match exato) e por título normalizado. "
        "Artigos aparecendo em múltiplas strings de busca são contabilizados uma única vez."
    )

    if df_dedup is None or df_dedup.empty:
        st.warning("`data/resumo_deduplicacao.csv` não encontrado.")
        return

    row = df_dedup.iloc[0]
    total_bruto = int(row.get("total_bruto", 0))
    total_unico = int(row.get("total_unico", len(df_unicos)))
    removidos = int(row.get("total_removido", total_bruto - total_unico))
    rem_doi = int(row.get("removidos_por_doi", 0))
    rem_tit = int(row.get("removidos_por_titulo", 0))
    taxa_sobrep = float(row.get("taxa_sobreposicao_pct", 0.0))
    com_doi = int(row.get("artigos_com_doi", 0))
    sem_doi = int(row.get("artigos_sem_doi", 0))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros Brutos", f"{total_bruto:,}")
    col2.metric(
        "Artigos Únicos", f"{total_unico:,}",
        delta=f"-{removidos:,} duplicatas", delta_color="inverse",
    )
    col3.metric("Removidos por DOI", f"{rem_doi:,}")
    col4.metric(
        "Taxa de Sobreposição", f"{taxa_sobrep:.1f}%",
        help="Percentual do corpus bruto que era redundante entre strings de busca",
    )

    st.divider()

    col_esq, col_dir = st.columns([2, 1])

    with col_esq:
        st.markdown("##### Fluxo da Deduplicação")
        estagios = ["Registros brutos", "Após dedup por DOI", "Após dedup por título"]
        valores = [total_bruto, max(total_bruto - rem_doi, 0), total_unico]
        fig = go.Figure(go.Funnel(
            y=estagios, x=valores,
            textinfo="value+percent initial",
            marker=dict(color=[CORES["accent"], CORES["secondary"], CORES["primary"]]),
        ))
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")

    with col_dir:
        st.markdown("##### Detalhamento das Remoções")
        det = pd.DataFrame({
            "Critério": ["DOI duplicado", "Título duplicado"],
            "Removidos": [rem_doi, rem_tit],
        })
        fig_det = px.bar(
            det, x="Removidos", y="Critério", orientation="h",
            color_discrete_sequence=[CORES["danger"]], text="Removidos",
        )
        fig_det.update_traces(textposition="outside")
        fig_det.update_layout(
            height=320, plot_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_det, width="stretch")

    st.divider()
    st.markdown("##### Cobertura de DOI no Corpus Único")
    st.caption(
        "Artigos sem DOI (preprints e materiais cinzentos) não puderam ser deduplicados "
        "por chave forte — dependem do match por título normalizado."
    )
    col_doi1, col_doi2 = st.columns(2)
    col_doi1.metric("Com DOI", f"{com_doi:,}")
    col_doi2.metric("Sem DOI", f"{sem_doi:,}")


# ============================================================
# ABA BIBLIOMETRIA — VISAO GERAL (producao, composicao, fontes, autores)
# ============================================================
def aba_visao_geral(df):
    """Panorama do corpus: produção temporal, composição, fontes e autores."""

    st.markdown("### 📈 Produção ao Longo do Tempo")
    st.caption(
        "Evolução anual do corpus por tipo de publicação. Permite ver o crescimento "
        "acelerado da literatura sobre TSP quântico (especialmente pós-2018) e a "
        "predominância de journals versus preprints e conferências."
    )

    df_tempo = df.dropna(subset=["Publication Year"]).copy()
    df_tempo["Ano"] = df_tempo["Publication Year"].astype(int)
    tipos_principais = ["journal article", "preprint", "conference proceedings article",
                        "book chapter", "book", "dissertation", "report"]
    df_tempo["Tipo"] = df_tempo["Publication Type"].apply(
        lambda x: x if x in tipos_principais else "other"
    )
    contagem = df_tempo.groupby(["Ano", "Tipo"]).size().reset_index(name="Contagem")

    fig = px.bar(
        contagem, x="Ano", y="Contagem", color="Tipo",
        color_discrete_map=PALETTE_PUB_TYPE,
        labels={"Contagem": "Número de Artigos", "Ano": "Ano de Publicação", "Tipo": "Tipo"},
    )

    # Totais anuais como rotulo no topo de cada barra empilhada.
    # Tecnica: trace Scatter em mode="text" posicionado no valor agregado
    # (Plotly nao expõe diretamente o total de stacked bars; o trace flutuante
    # e a forma idiomatica de exibi-lo sem alterar o layout do grafico).
    totais = contagem.groupby("Ano", as_index=False)["Contagem"].sum()
    fig.add_trace(go.Scatter(
        x=totais["Ano"], y=totais["Contagem"],
        text=totais["Contagem"], mode="text",
        textposition="top center",
        textfont=dict(size=11, color=CORES["dark"]),
        showlegend=False, hoverinfo="skip",
        cliponaxis=False,
    ))

    fig.update_layout(
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420, plot_bgcolor="white",
        # Folga de 8% acima para o rotulo do total nao ser cortado
        yaxis=dict(range=[0, totais["Contagem"].max() * 1.08]),
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.markdown("### 🧩 Composição do Corpus")
    st.caption(
        "Distribuição dos artigos por tipo de publicação e status de acesso aberto."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Tipos de Publicação**")
        contagem_tipo = df["Publication Type"].value_counts().head(8)
        fig_tipo = px.pie(
            values=contagem_tipo.values, names=contagem_tipo.index,
            color=contagem_tipo.index, color_discrete_map=PALETTE_PUB_TYPE,
            hole=0.4,
        )
        fig_tipo.update_traces(textposition="inside", textinfo="percent+label")
        fig_tipo.update_layout(height=380, showlegend=False,
                               margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_tipo, width="stretch")

    with col2:
        st.markdown("**Open Access**")
        oa = df["Is Open Access"].astype(str).str.lower()
        oa_counts = oa.value_counts()
        # color_discrete_map garante cor estavel por categoria, independente
        # da ordem do value_counts (que muda quando ha filtro ativo).
        # Storytelling: Open Access (positivo) = Pantone 293; Restrito = cinza.
        df_oa = pd.DataFrame({
            "Status": ["Open Access" if "true" in k else "Acesso Restrito"
                       for k in oa_counts.index],
            "Artigos": oa_counts.values,
        })
        fig_oa = px.pie(
            df_oa, values="Artigos", names="Status",
            color="Status",
            color_discrete_map={
                "Open Access":     AZUL_PANTONE_293,  # destaque positivo
                "Acesso Restrito": CORES["muted"],    # cinza neutro
            },
            hole=0.4,
        )
        fig_oa.update_traces(textposition="inside", textinfo="percent+label")
        fig_oa.update_layout(height=380, showlegend=False,
                             margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_oa, width="stretch")

    st.divider()

    st.markdown("### 📚 Fontes e Autores")
    st.caption(
        "Principais veículos de publicação e autores mais produtivos do corpus. "
        "Indicadores de concentração temática e atores-chave da área."
    )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Top 15 Journals / Fontes**")
        contagem_src = df["Source Title"].fillna("Não informado").value_counts().head(15)
        fig_src = px.bar(
            x=contagem_src.values, y=contagem_src.index, orientation="h",
            color_discrete_sequence=[CORES["secondary"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig_src.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_src.update_traces(text=contagem_src.values, textposition="outside")
        st.plotly_chart(fig_src, width="stretch")

    with col4:
        st.markdown("**Top 20 Autores Mais Ativos**")
        todos_autores = []
        for autores in df["Author/s"].dropna():
            for autor in str(autores).split(";"):
                autor = autor.strip()
                if autor:
                    todos_autores.append(autor)
        contagem_autores = pd.Series(todos_autores).value_counts().head(20)

        fig_autores = px.bar(
            x=contagem_autores.values, y=contagem_autores.index, orientation="h",
            color_discrete_sequence=[CORES["accent"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig_autores.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_autores.update_traces(text=contagem_autores.values, textposition="outside")
        st.plotly_chart(fig_autores, width="stretch")

    st.divider()

    st.markdown("### 🏢 Editoras (Publishers)")
    st.caption("Top 10 editoras que concentram a produção do corpus.")
    contagem_pub = df["Publisher"].fillna("Não informado").value_counts().head(10)
    fig_pub = px.bar(
        x=contagem_pub.values, y=contagem_pub.index, orientation="h",
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Número de Artigos", "y": ""},
    )
    fig_pub.update_layout(
        height=400, plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig_pub.update_traces(text=contagem_pub.values, textposition="outside")
    st.plotly_chart(fig_pub, width="stretch")


# ============================================================
# ABA BIBLIOMETRIA — IMPACTO E TEMAS
# ============================================================
def aba_impacto(df):
    """Bubble chart dos 200 artigos mais citados por Field of Study principal."""
    st.subheader("Artigos Mais Citados ao Longo do Tempo")
    st.caption(
        "Top 200 artigos com mais citações, posicionados pela data de publicação. "
        "O tamanho da bolha é proporcional ao número de citações e a cor representa "
        "o Field of Study principal (Top-10 + Outros). Permite identificar marcos "
        "(outliers), ondas temáticas e a maturação da área ao longo do tempo."
    )

    df_bubble = df.dropna(subset=["Date Published"]).copy()
    df_bubble = df_bubble[df_bubble["Citing Works Count"] > 0]
    if df_bubble.empty:
        st.info("Sem artigos citados nos filtros atuais.")
        return

    df_bubble_top = df_bubble.nlargest(200, "Citing Works Count").copy()
    df_bubble_top["Field of Study"] = df_bubble_top["Fields of Study"].apply(_primary_field)
    top_fields = df_bubble_top["Field of Study"].value_counts().head(10).index.tolist()
    df_bubble_top["Field of Study"] = df_bubble_top["Field of Study"].where(
        df_bubble_top["Field of Study"].isin(top_fields), "Outros"
    )

    df_bubble_top["hover"] = (
        df_bubble_top["Title"].str[:80] + "<br>"
        + df_bubble_top["Author/s"].fillna("").str.split(";").str[0]
        + " (" + df_bubble_top["Publication Year"].astype(int).astype(str) + ")"
        + "<br>Citações: " + df_bubble_top["Citing Works Count"].astype(str)
        + "<br>Field: " + df_bubble_top["Field of Study"]
    )

    cor_map = {f: PALETA_FIELDS[i] for i, f in enumerate(top_fields)}
    cor_map["Outros"] = PALETA_FIELDS[-1]

    fig = px.scatter(
        df_bubble_top,
        x="Date Published", y="Citing Works Count",
        size="Citing Works Count", color="Field of Study",
        color_discrete_map=cor_map, hover_name="hover",
        size_max=40,
        labels={"Date Published": "Data de Publicação", "Citing Works Count": "Citações"},
        category_orders={"Field of Study": top_fields + ["Outros"]},
    )
    fig.update_layout(
        height=520, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, width="stretch")


def aba_relevancia_ajustada(df):
    """Top 10 por citacoes/ano — leaderboard com cor por Field of Study."""
    st.subheader("Top 10 por Citações/Ano")
    st.caption(
        "Métrica: **citações ÷ anos desde a publicação**. Ranking dos 10 artigos com "
        "maior velocidade média de citação — permite enxergar trabalhos recentes de "
        "alto impacto emergente ao lado de clássicos já consolidados, corrigindo o "
        "viés temporal do ranking por citações totais. A linha tracejada marca a "
        "média de citações/ano do corpus filtrado."
    )

    df_base = df.dropna(subset=["Publication Year"]).copy()
    df_base = df_base[df_base["Citing Works Count"] > 0]
    if df_base.empty:
        st.info("Sem artigos com citações nos filtros atuais.")
        return

    df_base = _calcular_citacoes_por_ano(df_base)
    media_corpus = float(df_base["citacoes_por_ano"].mean())
    df_top = df_base.nlargest(10, "citacoes_por_ano").copy()

    df_top["Field of Study"] = df_top["Fields of Study"].apply(_primary_field)
    top_fields = df_top["Field of Study"].value_counts().head(10).index.tolist()
    df_top["Field of Study"] = df_top["Field of Study"].where(
        df_top["Field of Study"].isin(top_fields), "Outros"
    )
    cor_map = {f: PALETA_FIELDS[i] for i, f in enumerate(top_fields)}
    cor_map["Outros"] = PALETA_FIELDS[-1]

    df_top["rotulo"] = (
        df_top["Title"].str[:70]
        + " — " + df_top["Publication Year"].astype(int).astype(str)
        + " [" + df_top.index.astype(str) + "]"
    )
    df_top["hover"] = (
        df_top["Title"].str[:100] + "<br>"
        + df_top["Author/s"].fillna("").str.split(";").str[0]
        + " (" + df_top["Publication Year"].astype(int).astype(str) + ")"
        + "<br>Citações totais: " + df_top["Citing Works Count"].astype(int).astype(str)
        + "<br>Citações/ano: " + df_top["citacoes_por_ano"].round(1).astype(str)
        + "<br>Field: " + df_top["Field of Study"]
    )

    df_top = df_top.sort_values("citacoes_por_ano", ascending=False).reset_index(drop=True)
    ordem_y = df_top["rotulo"].tolist()[::-1]

    fig = px.bar(
        df_top, x="citacoes_por_ano", y="rotulo",
        color="Field of Study", color_discrete_map=cor_map,
        orientation="h", hover_name="hover",
        labels={"citacoes_por_ano": "Citações / Ano", "rotulo": ""},
        category_orders={
            "rotulo": ordem_y,
            "Field of Study": top_fields + ["Outros"],
        },
        text=df_top["citacoes_por_ano"].round(1).astype(str),
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.add_vline(
        x=media_corpus, line_dash="dash", line_color=CORES["muted_dark"], line_width=2,
        annotation_text=f"Média corpus: {media_corpus:.1f}",
        annotation_position="top",
        annotation_font_size=11, annotation_font_color=CORES["muted_dark"],
    )
    # Legenda VERTICAL empilhada, ancorada a DIREITA do grafico (fora do plot).
    #  - orientation="v" + xanchor="left", x=1.02 -> legenda comeca logo apos
    #    a borda direita do plot, sem sobreposicao.
    #  - margin.r=200 reserva espaco lateral para os rotulos dos Fields
    #    (textos como "Computer science" podem ser longos).
    #  - margin.t=40 e suficiente porque nao ha mais legenda no topo.
    fig.update_layout(
        height=450, plot_bgcolor="white",
        yaxis=dict(tickfont=dict(size=11), categoryorder="array", categoryarray=ordem_y),
        legend=dict(
            orientation="v",
            yanchor="top", y=1.0, xanchor="left", x=1.02,
            title_text="Field of Study", font=dict(size=11),
            bgcolor="rgba(255,255,255,0.9)",
        ),
        margin=dict(l=10, r=200, t=40, b=40),
    )
    st.plotly_chart(fig, width="stretch")


def aba_top_citados(df):
    """Tabela ranqueada dos 100 artigos mais citados, com citacoes/ano, fields e keywords."""
    st.subheader("Top 100 Artigos Mais Citados")
    st.caption(
        "Ranking dos 100 artigos com maior contagem de citações do corpus filtrado. "
        "Inclui Campo de Pesquisa (Fields of Study) e Keywords para contextualizar o "
        "alinhamento temático dos trabalhos mais influentes — útil para identificar "
        "referências obrigatórias da área."
    )

    df_calc = _calcular_citacoes_por_ano(df)
    colunas_fonte = ["Title", "Author/s", "Publication Year", "DOI",
                     "Citing Works Count", "citacoes_por_ano",
                     "Fields of Study", "Keywords"]
    df_top = df_calc.nlargest(100, "Citing Works Count")[colunas_fonte].copy()
    df_top.columns = ["Titulo", "Autores", "Ano", "DOI", "Citações",
                      "Citações/Ano", "Campo de Pesquisa", "Keywords"]
    df_top["Autores"] = df_top["Autores"].fillna("").str.split(";").str[0]
    df_top["Titulo"] = df_top["Titulo"].str[:80]
    df_top["Ano"] = df_top["Ano"].fillna(0).astype(int)
    df_top["Citações/Ano"] = df_top["Citações/Ano"].round(1)
    total_cit = df["Citing Works Count"].sum()
    if total_cit > 0:
        df_top["Citações(%)"] = (df_top["Citações"] / total_cit * 100).round(1).astype(str) + "%"
    else:
        df_top["Citações(%)"] = "0.0%"

    for col in ("Campo de Pesquisa", "Keywords"):
        df_top[col] = df_top[col].fillna("—").astype(str).str.replace(";", ", ", regex=False)

    df_top = df_top[["Titulo", "Autores", "Ano", "Citações", "Citações/Ano", "Citações(%)",
                     "Campo de Pesquisa", "Keywords", "DOI"]]

    st.dataframe(
        df_top.reset_index(drop=True),
        height=720, width="stretch",
        column_config={
            "Titulo": st.column_config.TextColumn(width="medium"),
            "Citações/Ano": st.column_config.NumberColumn(
                width="small",
                help="Citações ÷ anos desde a publicação — relevância ajustada pela idade",
                format="%.1f",
            ),
            "Campo de Pesquisa": st.column_config.TextColumn(width="medium"),
            "Keywords": st.column_config.TextColumn(width="large"),
        },
    )


def aba_treemap_fields(df):
    """Treemap dos 30 campos de estudo mais frequentes."""
    st.subheader("Top 30 — Fields of Study")
    st.caption(
        "Treemap dos 30 campos de estudo mais frequentes no corpus (Fields of Study "
        "é multi-valor — cada artigo pode contribuir para vários campos). O tamanho "
        "e a intensidade de cor refletem a frequência, destacando os domínios "
        "dominantes e revelando a natureza interdisciplinar da literatura."
    )

    todos_campos = []
    for campos in df["Fields of Study"].dropna():
        for campo in str(campos).split(";"):
            campo = campo.strip()
            if campo:
                todos_campos.append(campo)

    if not todos_campos:
        st.info("Nenhum Field of Study disponível nos filtros atuais.")
        return

    contagem = pd.Series(todos_campos).value_counts().head(30).reset_index()
    contagem.columns = ["Campo", "Frequência"]

    fig = px.treemap(
        contagem, path=["Campo"], values="Frequência", color="Frequência",
        color_continuous_scale=["#D6DFEF", AZUL_PANTONE_293, "#0A1E47"],
    )
    fig.update_layout(height=600, plot_bgcolor="white")
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, width="stretch")


def aba_wordcloud_keywords(df):
    """Nuvem de palavras das keywords mais frequentes."""
    st.subheader("Nuvem de Palavras — Keywords")
    keywords_preenchidos = df["Keywords"].dropna()
    cobertura = len(keywords_preenchidos) / max(len(df), 1) * 100
    st.caption(
        f"Cobertura: {cobertura:.1f}% dos artigos possuem keywords. "
        "Termos maiores aparecem com mais frequência no corpus filtrado."
    )

    todas_kw = []
    for kws in keywords_preenchidos:
        for kw in str(kws).split(";"):
            kw = kw.strip()
            if kw:
                todas_kw.append(kw)

    if not todas_kw:
        st.info("Nenhum keyword disponível com os filtros atuais.")
        return

    freq_kw = dict(pd.Series(todas_kw).value_counts().head(100))
    wc = WordCloud(
        width=800, height=400, background_color="white",
        colormap="viridis", max_words=80,
        prefer_horizontal=0.7, min_font_size=10, max_font_size=80,
        relative_scaling=0.5,
    ).generate_from_frequencies(freq_kw)

    fig_wc, ax_wc = plt.subplots(figsize=(10, 6))
    ax_wc.imshow(wc, interpolation="bilinear")
    ax_wc.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig_wc)
    plt.close(fig_wc)


# ============================================================
# ABA BIBLIOMETRIA — GEOGRAFIA
# ============================================================
def aba_geografia(df):
    """Mapa choropleth mundial + ranking de paises."""
    cobertura = df["Source Country"].notna().sum() / max(len(df), 1) * 100
    st.caption(
        f"Cobertura: {cobertura:.1f}% dos artigos possuem informação de país de origem. "
        "Preprints frequentemente não informam o país — a contagem reflete apenas os artigos "
        "com o metadado preenchido no Lens.org."
    )

    st.subheader("Distribuição Geográfica das Publicações")
    contagem_pais = df["Source Country"].dropna().value_counts().reset_index()
    contagem_pais.columns = ["País", "Artigos"]
    contagem_pais["ISO3"] = contagem_pais["País"].apply(_pais_para_iso3)
    contagem_pais = contagem_pais.dropna(subset=["ISO3"])

    if contagem_pais.empty:
        st.info("Sem dados geográficos válidos nos filtros atuais.")
        return

    fig_mapa = px.choropleth(
        contagem_pais, locations="ISO3", locationmode="ISO-3",
        color="Artigos",
        color_continuous_scale=["#D6DFEF", "#A6BBDA", "#6585BD", AZUL_PANTONE_293, "#1E3A6F", "#0A1E47"],
        labels={"Artigos": "Número de Artigos"},
        hover_name="País",
    )
    fig_mapa.update_layout(
        height=500,
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    )
    st.plotly_chart(fig_mapa, width="stretch")

    st.subheader("Top 15 Países por Número de Publicações")
    top_paises = contagem_pais.head(15)
    fig_pais = px.bar(
        top_paises, x="Artigos", y="País", orientation="h",
        color_discrete_sequence=[CORES["secondary"]],
        text="Artigos",
    )
    fig_pais.update_layout(
        height=450, plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
    )
    fig_pais.update_traces(textposition="outside")
    st.plotly_chart(fig_pais, width="stretch")


# ============================================================
# ABA BIBLIOMETRIA — WRAPPER COM SUB-ABAS
# ============================================================
def aba_bibliometria(df):
    """Wrapper: divide a analise bibliometrica em 3 sub-abas tematicas."""
    if df.empty:
        st.warning("Nenhum artigo corresponde aos filtros atuais. Ajuste os filtros na sidebar.")
        return

    st.caption(
        "Caracterização do corpus único (até 3.696 artigos pós-deduplicação). "
        "Use os filtros da sidebar para restringir por período, tipo, string, "
        "prioridade, Open Access ou citações."
    )

    sub1, sub2, sub3 = st.tabs([
        "📈 Produção e Perfil",
        "🏆 Impacto e Temas de Pesquisa",
        "🌍 Geografia",
    ])
    with sub1:
        aba_visao_geral(df)
    with sub2:
        aba_impacto(df)
        st.divider()
        aba_treemap_fields(df)
        st.divider()
        aba_relevancia_ajustada(df)
        st.divider()
        aba_top_citados(df)
        st.divider()
        aba_wordcloud_keywords(df)
    with sub3:
        aba_geografia(df)


# ============================================================
# ABA — ALGORITMOS E ABORDAGENS (base Phillipson 2025)
# ============================================================
# Fonte: data/base_algoritmos_abordagens.csv (129 trabalhos catalogados).
# Esta aba usa fonte de dados diferente das demais — possui filtros proprios.

CRITERIOS_DESCRICAO = {
    "C1": "C1 — Qualidade da solução",
    "C2": "C2 — Escalabilidade",
    "C3": "C3 — Aplicação real",
    "C4": "C4 — Comparação com clássico",
    "C5": "C5 — Análise de limitações",
    "C6": "C6 — Taxa de sucesso",
}
DESCRICAO_CRITERIOS = {v: k for k, v in CRITERIOS_DESCRICAO.items()}

CRITERIOS_RADAR = {
    "C1": "Qualidade da Solução",
    "C2": "Escalabilidade",
    "C3": "Aplicação Real",
    "C4": "Comparação c/ Clássico",
    "C5": "Análise de Limitações",
    "C6": "Taxa de Sucesso",
}
PESOS_RADAR = {"C1": 20, "C2": 15, "C3": 20, "C4": 15, "C5": 10, "C6": 20}


def aba_algoritmos():
    """Taxonomia de 129 trabalhos quanticos catalogados a partir de Phillipson (2025)."""

    df_algo = carregar_algoritmos()

    st.caption(
        "Taxonomia de **129 trabalhos** extraídos do artigo de referência **Phillipson (2025)** "
        "— *Quantum Computing in Logistics and Supply Chain Management: An Overview*. "
        "Esta aba tem **filtros próprios** (independentes da sidebar)."
    )

    # --- Filtros da aba ---
    st.markdown("##### Filtros de Algoritmos")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        paradigma_sel = st.multiselect(
            "Paradigma",
            options=sorted(df_algo["paradigma"].dropna().unique()),
            default=None, placeholder="Todos", key="algo_paradigma",
        )
    with fc2:
        algoritmo_sel = st.multiselect(
            "Algoritmo Quântico",
            options=sorted(df_algo["algoritmo_quantico"].dropna().unique()),
            default=None, placeholder="Todos", key="algo_algoritmo",
        )
    with fc3:
        topico_sel = st.multiselect(
            "Tópico",
            options=sorted(df_algo["topico"].dropna().unique()),
            default=None, placeholder="Todos", key="algo_topico",
        )

    fc4, fc5, fc6 = st.columns(3)
    with fc4:
        problema_sel = st.multiselect(
            "Problema",
            options=sorted(df_algo["problema"].dropna().unique()),
            default=None, placeholder="Todos", key="algo_problema",
        )
    with fc5:
        abordagem_sel = st.multiselect(
            "Abordagem",
            options=sorted(df_algo["abordagem"].dropna().unique()),
            default=None, placeholder="Todas", key="algo_abordagem",
        )
    with fc6:
        criterio_sel = st.multiselect(
            "Critério de Seleção",
            options=list(CRITERIOS_DESCRICAO.values()),
            default=None, placeholder="Todos", key="algo_criterio",
        )

    # Aplicar filtros
    mask = pd.Series(True, index=df_algo.index)
    if paradigma_sel:
        mask &= df_algo["paradigma"].isin(paradigma_sel)
    if algoritmo_sel:
        mask &= df_algo["algoritmo_quantico"].isin(algoritmo_sel)
    if topico_sel:
        mask &= df_algo["topico"].isin(topico_sel)
    if problema_sel:
        mask &= df_algo["problema"].isin(problema_sel)
    if abordagem_sel:
        mask &= df_algo["abordagem"].isin(abordagem_sel)
    if criterio_sel:
        codigos_sel = [DESCRICAO_CRITERIOS[d] for d in criterio_sel]
        criterio_mask = pd.Series(False, index=df_algo.index)
        for codigo in codigos_sel:
            criterio_mask |= df_algo["criterios"].fillna("").str.contains(codigo, na=False)
        mask &= criterio_mask
    df_f = df_algo[mask].copy()

    st.divider()

    # --- KPIs ---
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Trabalhos", len(df_f))
    k2.metric("Paradigmas", df_f["paradigma"].nunique())
    k3.metric("Algoritmos", df_f["algoritmo_quantico"].nunique())
    k4.metric("Tópicos", df_f["topico"].nunique())
    k5.metric("Problemas", df_f["problema"].nunique())
    k6.metric("Abordagens", df_f["abordagem"].nunique())

    if df_f.empty:
        st.warning("Nenhum trabalho corresponde aos filtros selecionados.")
        return

    st.divider()

    # --- Distribuicao por categoria de algoritmo (sintese das 6 categorias) ---
    if "categoria_algoritmo" in df_f.columns:
        st.subheader("Distribuição por Categoria de Algoritmo")
        st.caption(
            "Classificação dos algoritmos quânticos em 6 categorias principais conforme "
            "`artefatos/resumo_algoritmos.md` (Seções 1.1–1.6). Permite uma visão de "
            "alto nível antes do detalhamento por algoritmo específico abaixo. "
            "Fonte da coluna: `scripts/classificar_categoria_algoritmo.py`."
        )

        cont_cat = df_f["categoria_algoritmo"].fillna("Não especificado").value_counts()
        # Reordenar conforme ordem canonica (categorias ausentes nao aparecem)
        cont_cat = cont_cat.reindex(
            [c for c in ORDEM_CATEGORIA_ALGORITMO if c in cont_cat.index]
        )
        total_cat = int(cont_cat.sum())
        df_cat = cont_cat.reset_index()
        df_cat.columns = ["Categoria", "Trabalhos"]
        df_cat["Percentual"] = (df_cat["Trabalhos"] / max(total_cat, 1) * 100).round(1)

        col_pie, col_bar = st.columns([1, 1])
        with col_pie:
            fig_cat_pie = px.pie(
                df_cat, values="Trabalhos", names="Categoria",
                color="Categoria",
                color_discrete_map=PALETTE_CATEGORIA_ALGORITMO,
                hole=0.4,
                category_orders={"Categoria": ORDEM_CATEGORIA_ALGORITMO},
            )
            fig_cat_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                texttemplate="%{label}<br>%{percent:.1%}",
            )
            fig_cat_pie.update_layout(
                height=400, showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_cat_pie, width="stretch")

        with col_bar:
            # Barra horizontal com percentual explicito + valor absoluto (n)
            df_bar = df_cat.sort_values("Percentual", ascending=True)
            fig_cat_bar = px.bar(
                df_bar, x="Percentual", y="Categoria", orientation="h",
                color="Categoria", color_discrete_map=PALETTE_CATEGORIA_ALGORITMO,
                text=df_bar.apply(lambda r: f"{r['Percentual']:.1f}%  (n={int(r['Trabalhos'])})", axis=1),
            )
            fig_cat_bar.update_traces(textposition="outside", cliponaxis=False)
            fig_cat_bar.update_layout(
                height=400, showlegend=False, plot_bgcolor="white",
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(title="% dos trabalhos catalogados", range=[0, max(df_bar["Percentual"]) * 1.25]),
                yaxis=dict(title=""),
            )
            st.plotly_chart(fig_cat_bar, width="stretch")

        st.divider()

    # --- Distribuicao por paradigma + abordagem ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição por Paradigma Quântico")
        st.caption("QA = Quantum Annealing · GBC = Gate-Based Computing · QML = Quantum Machine Learning")
        contagem_p = df_f["paradigma"].value_counts().reset_index()
        contagem_p.columns = ["Paradigma", "Trabalhos"]
        fig_p = px.pie(
            contagem_p, values="Trabalhos", names="Paradigma",
            color="Paradigma", color_discrete_map=PALETTE_PARADIGMA, hole=0.4,
        )
        fig_p.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_p.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_p, width="stretch")

    with col2:
        st.subheader("Distribuição por Abordagem")
        st.caption("Full Quantum (puramente quântica) vs Hybrid (clássico-quântica)")
        contagem_a = df_f["abordagem"].value_counts().reset_index()
        contagem_a.columns = ["Abordagem", "Trabalhos"]
        fig_a = px.pie(
            contagem_a, values="Trabalhos", names="Abordagem",
            color="Abordagem", color_discrete_map=PALETTE_ABORDAGEM, hole=0.4,
        )
        fig_a.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_a.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_a, width="stretch")

    # --- Topico + Algoritmo ---
    # Helper inline: para cada barra simples, exibir "N (XX,X%)" — o percentual
    # e calculado sobre o total de trabalhos do dataset filtrado (len(df_f)),
    # nao sobre a soma das barras exibidas (relevante quando ha truncamento Top-N).
    total_f = max(len(df_f), 1)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Distribuição por Tópico")
        contagem_t = df_f["topico"].value_counts().reset_index()
        contagem_t.columns = ["Tópico", "Trabalhos"]
        contagem_t["label"] = contagem_t.apply(
            lambda r: f"{int(r['Trabalhos'])} ({100*r['Trabalhos']/total_f:.1f}%)", axis=1
        )
        fig_t = px.bar(
            contagem_t, x="Trabalhos", y="Tópico", orientation="h",
            color="Tópico", color_discrete_map=PALETTE_TOPICO,
            text="label",
        )
        fig_t.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"), showlegend=False,
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(range=[0, contagem_t["Trabalhos"].max() * 1.25]),
        )
        fig_t.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_t, width="stretch")

    with col4:
        st.subheader("Algoritmos Quânticos Mais Frequentes")
        # Cada algoritmo herda a cor da sua CATEGORIA (mesma classificacao do
        # grafico "Distribuição por Categoria de Algoritmo" no topo da aba).
        # Mapeamento algoritmo -> categoria e deterministico (vem da coluna
        # `categoria_algoritmo` do CSV, gerada por classificar_categoria_algoritmo.py).
        if "categoria_algoritmo" in df_f.columns:
            contagem_alg = (
                df_f.groupby("algoritmo_quantico")
                    .agg(
                        Trabalhos=("algoritmo_quantico", "size"),
                        Categoria=("categoria_algoritmo", "first"),
                    )
                    .reset_index()
                    .rename(columns={"algoritmo_quantico": "Algoritmo"})
                    .sort_values("Trabalhos", ascending=False)
            )
        else:
            # Fallback: CSV sem a coluna categoria_algoritmo
            contagem_alg = df_f["algoritmo_quantico"].value_counts().reset_index()
            contagem_alg.columns = ["Algoritmo", "Trabalhos"]
            contagem_alg["Categoria"] = "Não especificado"

        contagem_alg["label"] = contagem_alg.apply(
            lambda r: f"{int(r['Trabalhos'])} ({100*r['Trabalhos']/total_f:.1f}%)", axis=1
        )
        ordem_alg = contagem_alg["Algoritmo"].tolist()

        fig_alg = px.bar(
            contagem_alg, x="Trabalhos", y="Algoritmo", orientation="h",
            color="Categoria", color_discrete_map=PALETTE_CATEGORIA_ALGORITMO,
            text="label",
            category_orders={
                "Algoritmo": ordem_alg,
                "Categoria": ORDEM_CATEGORIA_ALGORITMO,
            },
        )
        fig_alg.update_traces(textposition="outside", cliponaxis=False)
        # Legenda no RODAPE (y negativo) para nao comprimir a area do plot —
        # com 5 categorias na horizontal acima, o grafico ficava espremido.
        # height aumentado e margin.b ampliado para acomodar a legenda abaixo.
        fig_alg.update_layout(
            height=480, plot_bgcolor="white",
            yaxis=dict(autorange="reversed", title=""),
            margin=dict(l=10, r=80, t=10, b=70),
            xaxis=dict(range=[0, contagem_alg["Trabalhos"].max() * 1.25]),
            legend=dict(
                orientation="h",
                yanchor="top", y=-0.08,
                xanchor="center", x=0.5,
                title_text="Categoria",
            ),
        )
        st.plotly_chart(fig_alg, width="stretch")

    # --- Problemas Top 15 + Paradigma por Topico ---
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Problemas Mais Frequentes (Top 15)")
        # Cada problema e colorido pelo seu TOPICO DOMINANTE (mais frequente
        # no CSV), reusando PALETTE_TOPICO para manter coerencia visual com
        # o grafico "Distribuição por Tópico" ao lado.
        # Quando um problema aparece em multiplos topicos (raro), o .mode()
        # pega o predominante; em empate, retorna o primeiro alfabeticamente.
        contagem_sub = (
            df_f.groupby("problema")
                .agg(
                    Trabalhos=("problema", "size"),
                    Tópico=("topico", lambda s: s.mode().iloc[0] if not s.mode().empty else "Outros"),
                )
                .reset_index()
                .nlargest(15, "Trabalhos")
        )
        contagem_sub["label"] = contagem_sub.apply(
            lambda r: f"{int(r['Trabalhos'])} ({100*r['Trabalhos']/total_f:.1f}%)", axis=1
        )
        # Ordem dos problemas no eixo Y (do maior para o menor)
        ordem_problemas = contagem_sub["problema"].tolist()

        fig_sub = px.bar(
            contagem_sub, x="Trabalhos", y="problema", orientation="h",
            color="Tópico", color_discrete_map=PALETTE_TOPICO,
            text="label",
            category_orders={
                "problema": ordem_problemas,
                "Tópico": list(PALETTE_TOPICO.keys()),
            },
            labels={"problema": ""},
        )
        fig_sub.update_traces(textposition="outside", cliponaxis=False)
        fig_sub.update_layout(
            height=450, plot_bgcolor="white",
            yaxis=dict(autorange="reversed", title=""),
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(range=[0, contagem_sub["Trabalhos"].max() * 1.25]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_sub, width="stretch")

    with col6:
        st.subheader("Paradigma por Tópico")
        # Stacked bar: percentual de cada segmento exibido DENTRO (texttemplate),
        # base do calculo = total do TOPICO (linha), nao total geral —
        # responde a pergunta "dentro de cada topico, qual a divisao por paradigma?".
        contagem_pt = df_f.groupby(["topico", "paradigma"]).size().reset_index(name="Trabalhos")
        total_por_topico = contagem_pt.groupby("topico")["Trabalhos"].transform("sum")
        contagem_pt["pct_topico"] = 100 * contagem_pt["Trabalhos"] / total_por_topico
        contagem_pt["label"] = contagem_pt.apply(
            lambda r: f"{int(r['Trabalhos'])} ({r['pct_topico']:.0f}%)", axis=1
        )
        fig_pt = px.bar(
            contagem_pt, x="Trabalhos", y="topico", orientation="h",
            color="paradigma", color_discrete_map=PALETTE_PARADIGMA,
            labels={"topico": "Tópico", "paradigma": "Paradigma"},
            text="label",
        )
        fig_pt.update_traces(textposition="inside", insidetextanchor="middle",
                             textfont=dict(size=10, color="white"))
        fig_pt.update_layout(
            barmode="stack", height=450, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_pt, width="stretch")

    # --- Heatmap Topico x Algoritmo ---
    st.subheader("Heatmap: Tópico × Algoritmo Quântico")
    st.caption("Intensidade indica o número de trabalhos que combinam cada tópico com cada algoritmo")

    heat_data = df_f.groupby(["topico", "algoritmo_quantico"]).size().reset_index(name="Qtd")
    heat_pivot = heat_data.pivot_table(
        index="topico", columns="algoritmo_quantico", values="Qtd", fill_value=0
    )
    heat_pivot = heat_pivot.loc[heat_pivot.sum(axis=1).sort_values(ascending=False).index]
    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_pivot.values,
        x=heat_pivot.columns.tolist(),
        y=heat_pivot.index.tolist(),
        colorscale=[[0, "#FFFFFF"], [0.15, "#D6DFEF"], [0.4, "#8EA8D2"], [0.7, "#3C60A7"], [1, "#0A1E47"]],
        text=heat_pivot.values, texttemplate="%{text}",
    ))
    fig_heat.update_layout(height=400, xaxis_title="Algoritmo Quântico", yaxis_title="Tópico")
    st.plotly_chart(fig_heat, width="stretch")

    # --- Treemap hierarquico ---
    st.subheader("Treemap: Tópico → Problema → Paradigma")
    st.caption("Visualização hierárquica da distribuição dos trabalhos")

    df_tree = df_f[["topico", "problema", "paradigma"]].copy()
    df_tree["count"] = 1
    fig_tree = px.treemap(
        df_tree, path=["topico", "problema", "paradigma"], values="count",
        color="topico", color_discrete_map=PALETTE_TOPICO,
    )
    fig_tree.update_layout(height=500)
    fig_tree.update_traces(textinfo="label+value")
    st.plotly_chart(fig_tree, width="stretch")

    # --- Radar de criterios por autor ---
    st.subheader("Radar de Critérios por Autor")
    st.caption(
        "Pontuação dos critérios de seleção aplicados por autor (peso do critério se atendido). "
        "Útil para comparar a qualidade metodológica de trabalhos individuais."
    )

    codigos = list(CRITERIOS_RADAR.keys())
    labels_radar = list(CRITERIOS_RADAR.values())

    if "ranking" in df_f.columns:
        df_com_rank = df_f[df_f["ranking"] > 0].sort_values("ranking", ascending=False)
        df_sem_rank = df_f[df_f["ranking"] == 0].sort_values("autores")
        autores_com_rank = df_com_rank["autores"].unique().tolist()
        autores_sem_rank = df_sem_rank["autores"].unique().tolist()
        todos_autores = autores_com_rank + [a for a in autores_sem_rank if a not in autores_com_rank]
    else:
        todos_autores = sorted(df_f["autores"].unique().tolist())
        autores_com_rank = []

    default_autores = autores_com_rank[:5] if autores_com_rank else todos_autores[:5]

    if todos_autores:
        autores_sel_radar = st.multiselect(
            "Selecione autores para comparar",
            options=todos_autores, default=default_autores, key="radar_autores_sel",
        )
        if autores_sel_radar:
            fig_radar = go.Figure()
            cores_radar = px.colors.qualitative.Set2
            for i, autor in enumerate(autores_sel_radar):
                row_autor = df_f[df_f["autores"] == autor].iloc[0]
                criterios_str = row_autor["criterios"] if pd.notna(row_autor["criterios"]) else ""
                if str(criterios_str).strip().lower() == "nao reportada":
                    criterios_presentes = set()
                else:
                    criterios_presentes = {c.strip() for c in str(criterios_str).split(",")}
                values = [PESOS_RADAR[cod] if cod in criterios_presentes else 0 for cod in codigos]
                values.append(values[0])
                ranking_val = int(row_autor["ranking"]) if pd.notna(row_autor.get("ranking")) else 0
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels_radar + [labels_radar[0]],
                    fill="toself",
                    name=f"{autor} (R:{ranking_val})",
                    line_color=cores_radar[i % len(cores_radar)],
                    opacity=0.6,
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 20])),
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            st.plotly_chart(fig_radar, width="stretch")
    else:
        st.info("Nenhum autor disponível nos dados filtrados.")

    # --- Tabela completa ---
    st.subheader("Tabela Detalhada dos Trabalhos")
    st.caption("Ordenada por **Score Geral** (ranking ponderado dos critérios C1-C6) decrescente.")

    colunas_exibir = [
        "autores", "ano", "paradigma", "algoritmo_quantico", "topico",
        "problema", "abordagem", "hardware", "num_cidades",
        "formulacao", "contribuicao", "escala_testada", "qualidade_solucao",
        "tempo_execucao", "taxa_sucesso", "sensibilidade_parametros",
        "robustez_ruido", "metricas_avaliadas", "criterios", "ranking",
    ]
    colunas_exibir = [c for c in colunas_exibir if c in df_f.columns]
    colunas_nomes = {
        "autores": "Autores", "ano": "Ano", "paradigma": "Paradigma",
        "algoritmo_quantico": "Algoritmo Quântico", "topico": "Tópico",
        "problema": "Problema", "abordagem": "Abordagem", "hardware": "Hardware",
        "num_cidades": "Nº Cidades", "formulacao": "Formulação",
        "contribuicao": "Contribuição", "escala_testada": "Escala",
        "qualidade_solucao": "Qualidade", "tempo_execucao": "Tempo Execução",
        "taxa_sucesso": "Taxa Sucesso", "sensibilidade_parametros": "Sensib. Parâmetros",
        "robustez_ruido": "Robustez Ruído", "metricas_avaliadas": "Métricas Avaliadas",
        "criterios": "Critérios", "ranking": "Score Geral",
    }

    df_tabela = df_f[colunas_exibir].copy()
    if "ranking" in df_tabela.columns:
        df_tabela = df_tabela.sort_values("ranking", ascending=False)
    df_tabela = df_tabela.rename(columns=colunas_nomes)
    if "Ano" in df_tabela.columns:
        df_tabela["Ano"] = df_tabela["Ano"].apply(
            lambda x: str(int(x)) if pd.notna(x) and x != 0 else "N/D"
        )

    st.dataframe(
        df_tabela.reset_index(drop=True),
        height=520, width="stretch",
    )


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================
def main():
    st.title("Análise Bibliométrica — TSP Quântico (v2)")
    st.caption(
        "Pipeline da Fase 1 — Exploração Bibliográfica: 5.320 registros brutos → "
        "3.696 artigos únicos (26 strings de busca, Lens.org). "
        "Aplicação de Computação Quântica ao Problema do Caixeiro Viajante (TSP) "
        "em Logística | Mestrado Profissional — SENAI CIMATEC"
    )

    # Carregamento (tudo cacheado)
    df = carregar_dados()
    df_dedup = carregar_dedup()
    df_algoritmos = carregar_algoritmos()

    # Filtros da sidebar (afetam todas abas exceto Algoritmos)
    df_filtrado = criar_filtros(df)

    # Navegacao por radio horizontal (persiste a aba ativa entre reruns)
    ABAS = [
        "🏠 Pipeline",
        "🔎 Estratégia de Busca",
        "🧹 Deduplicação",
        "📚 Análise Bibliométrica",
        "🔬 Algoritmos e Abordagens",
    ]
    aba_ativa = st.radio(
        "Navegação", ABAS,
        horizontal=True, key="aba_ativa", label_visibility="collapsed",
    )
    st.divider()

    if aba_ativa == ABAS[0]:
        aba_home(df_dedup, df, df_algoritmos)

    elif aba_ativa == ABAS[1]:
        # KPIs fixos da estrategia de busca
        total_strings = len(STRINGS_BUSCA)
        total_bruto = int(df_dedup["total_bruto"].iloc[0]) if df_dedup is not None else 0
        total_unicos = int(df_dedup["total_unico"].iloc[0]) if df_dedup is not None else len(df)
        taxa_sobrep = float(df_dedup["taxa_sobreposicao_pct"].iloc[0]) if df_dedup is not None else 0.0
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Strings de Busca", f"{total_strings}",
                  help="Combinações booleanas no Lens.org")
        k2.metric("Registros Brutos", f"{total_bruto:,}")
        k3.metric("Artigos Únicos", f"{total_unicos:,}")
        k4.metric("Taxa de Sobreposição", f"{taxa_sobrep:.1f}%",
                  help="% do corpus bruto redundante entre strings")
        st.divider()
        aba_strings(df_filtrado)

    elif aba_ativa == ABAS[2]:
        aba_deduplicacao(df_dedup, df_filtrado)

    elif aba_ativa == ABAS[3]:
        exibir_kpis(df_filtrado)
        st.divider()
        aba_bibliometria(df_filtrado)

    elif aba_ativa == ABAS[4]:
        aba_algoritmos()


if __name__ == "__main__":
    main()
