"""
Dashboard Bibliometrico — Fase 1 (Exploracao Bibliografica)

Dashboard interativo em Streamlit para explorar os 3.696 artigos
unicos identificados na pesquisa bibliografica sobre TSP + Computacao Quantica.

Como usar:
    streamlit run src/dashboard_bibliometrico.py

Dependencias:
    pip install streamlit pandas plotly numpy wordcloud matplotlib pycountry openpyxl

Estrutura do arquivo:
    1. Imports e configuracao da pagina
    2. Constantes (cores, strings de busca, mapeamentos)
    3. Carregamento de dados (CSV → DataFrame pandas)
    4. Filtros (sidebar com widgets interativos)
    5. KPIs (metricas resumo no topo)
    6. Abas do dashboard (7 abas, cada uma com graficos Plotly)
    7. Funcao main() que orquestra tudo
"""

import os
# streamlit (st): framework web para dashboards em Python.
#   Cada vez que o usuario interage com um widget, o script inteiro re-executa.
#   Documentacao: https://docs.streamlit.io
import streamlit as st
# pandas (pd): manipulacao de dados tabulares (DataFrames = tabelas).
import pandas as pd
# plotly.express (px): graficos interativos de alto nivel (bar, scatter, pie, etc.)
#   Documentacao: https://plotly.com/python/plotly-express/
import plotly.express as px
# plotly.graph_objects (go): graficos de baixo nivel (Heatmap, Scatterpolar/radar, etc.)
#   Usado quando px nao oferece o tipo de grafico desejado.
import plotly.graph_objects as go
import numpy as np
# WordCloud: gera imagens de nuvem de palavras a partir de frequencias.
from wordcloud import WordCloud
# matplotlib: usado apenas para renderizar a WordCloud como imagem.
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Backend sem interface grafica (necessario para servidores)
# pycountry: converte nomes de paises para codigos ISO-3 (ex: "Brazil" → "BRA")
#   Necessario para o mapa choropleth do Plotly.
import pycountry

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================

# st.set_page_config() DEVE ser o primeiro comando Streamlit do script.
# Define o titulo da aba do navegador, icone, e layout.
# layout="wide" usa toda a largura da tela (padrao e "centered").
# Para alterar o titulo da pagina, modifique page_title abaixo.
st.set_page_config(
    page_title="Análise Bibliométrica - TSP Quântico",
    page_icon=":bar_chart:",       # Icone da aba (emoji ou URL de imagem)
    layout="wide",                  # "wide" = largura total | "centered" = coluna central
    initial_sidebar_state="expanded",  # Sidebar aberta ao carregar
)

# ============================================================
# PALETA DE CORES
# ============================================================
# Para alterar as cores do dashboard, modifique os valores hexadecimais (#RRGGBB) abaixo.
# Use sites como https://colorhunt.co ou https://coolors.co para escolher paletas.

# CORES: dicionario principal de cores usadas em todo o dashboard.
# Referenciado como CORES["primary"], CORES["danger"], etc.
CORES = {
    "primary": "#0077B6",     # Azul principal — usado na maioria dos graficos
    "secondary": "#00B4D8",   # Azul claro — graficos secundarios
    "accent": "#90E0EF",      # Azul muito claro — destaques sutis
    "highlight": "#CAF0F8",   # Azul pastel — fundos e escalas de cor
    "dark": "#03045E",        # Azul escuro — textos e contrastes fortes
    "success": "#70AD47",     # Verde — Open Access, itens positivos
    "warning": "#FFC000",     # Amarelo — alertas, criterios de selecao
    "danger": "#ED7D31",      # Laranja — prioridade Alta, destaques criticos
}

# PALETTE: lista de cores para graficos com muitas categorias (10 cores).
# Plotly usa estas cores ciclicamente quando ha mais categorias que cores.
PALETTE = ["#0077B6", "#00B4D8", "#48CAE4", "#90E0EF", "#023E8A",
           "#0096C7", "#ADE8F4", "#70AD47", "#FFC000", "#ED7D31"]

# PALETTE_PUB_TYPE: cor fixa para cada tipo de publicacao.
# Usado no grafico de barras empilhadas "Publicacoes ao Longo do Tempo".
# Para adicionar um novo tipo, adicione uma entrada "tipo": "#COR" aqui.
PALETTE_PUB_TYPE = {
    "journal article": "#0077B6",
    "preprint": "#03045E",
    "conference proceedings article": "#48CAE4",
    "book chapter": "#90E0EF",
    "book": "#ADE8F4",
    "dissertation": "#70AD47",
    "report": "#0096C7",
    "other": "#A5A5A5",
}

# PRIORIDADES: classifica cada string de busca (1-26) por relevancia ao tema central.
# Alta = diretamente sobre TSP + computacao quantica
# Media = termos mais amplos ou perifericos
# Baixa = complementares, hardware especifico, problemas adjacentes
PRIORIDADES = {
    1: "Alta", 2: "Alta", 3: "Alta", 4: "Alta", 5: "Alta",
    6: "Alta", 17: "Alta", 18: "Alta",
    7: "Media", 8: "Media", 9: "Media", 10: "Media", 11: "Media",
    12: "Media", 19: "Media", 20: "Media", 21: "Media", 22: "Media",
    13: "Baixa", 14: "Baixa", 15: "Baixa", 16: "Baixa",
    23: "Baixa", 24: "Baixa", 25: "Baixa", 26: "Baixa",
}

# STRINGS_BUSCA: descricao resumida de cada uma das 26 strings de busca usadas no Lens.org.
# O numero (chave) corresponde ao arquivo CSV em data/exportacoes_lens/.
# Ex: string 1 → "Traveling Salesman Problem" AND "Quantum Computing"
STRINGS_BUSCA = {
    1: "TSP + Quantum Computing",
    2: "TSP + Quantum Algorithms",
    3: "TSP + Quantum Annealing",
    4: "TSP + QAOA",
    5: "TSP + Hybrid Quantum",
    6: "VRP + Quantum Computing",
    7: "Comb. Opt. + QA",
    8: "TSP + VQE",
    9: "TSP + Grover",
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

COR_PRIORIDADE = {
    "Alta": CORES["danger"],
    "Media": CORES["primary"],
    "Baixa": "#A5A5A5",
}

# AREA_APLICACAO: classifica cada string em uma area tematica para uso no
# grafico de bolhas "Artigos Mais Citados ao Longo do Tempo" (aba Impacto).
# Para alterar a classificacao de uma string, mude o valor aqui.
# Para adicionar uma nova area, adicione tambem em COR_AREA abaixo.
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

COR_AREA = {
    "TSP": "#0077B6",
    "VRP/Logística": "#ED7D31",
    "Supply Chain/QML": "#70AD47",
    "Otim. Combinatória": "#9B59B6",
}


# ============================================================
# CARREGAMENTO DE DADOS
# ============================================================
# Fonte de dados principal: data/artigos_unicos.csv (3.696 artigos deduplicados)
# Fonte de dados secundaria: data/base_algoritmos_abordagens.csv (38 algoritmos catalogados)
#   → usada apenas na aba "Algoritmos e Abordagens"
# Fonte auxiliar: docs/pesquisa_palavras_chave_tsp_quantico.xlsx
#   → usada apenas na aba "Strings de Busca" para exibir strings completas

# Caminho raiz do projeto (um nivel acima de src/)
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# @st.cache_data: decorator do Streamlit que faz CACHE dos dados carregados.
# Como o Streamlit re-executa o script inteiro a cada interacao do usuario,
# sem cache o CSV seria relido do disco toda vez. Com cache, le apenas 1 vez.
# Para forcar recarregamento, clique no botao "Clear Cache" no menu do Streamlit
# ou reinicie o servidor.
@st.cache_data
def carregar_dados():
    """Carrega o CSV principal e prepara colunas derivadas.

    Retorna um DataFrame pandas com as colunas do CSV original mais:
    - strings_lista: lista de inteiros com os numeros das strings de busca de cada artigo
    - prioridade: "Alta", "Media" ou "Baixa" (baseada na primeira string)
    """
    caminho = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
    # dtype=str: le todas as colunas como texto para evitar erros de tipo
    df = pd.read_csv(caminho, dtype=str)

    # Converter colunas de texto para numeros (pd.to_numeric com errors="coerce"
    # converte valores invalidos para NaN em vez de dar erro)
    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    df["Citing Patents Count"] = pd.to_numeric(df["Citing Patents Count"], errors="coerce").fillna(0).astype(int)
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce").fillna(1).astype(int)

    # Converter data de publicacao para formato datetime (permite eixo temporal nos graficos)
    df["Date Published"] = pd.to_datetime(df["Date Published"], errors="coerce")

    # Coluna "strings_origem" contem "1;3;7" (separado por ";").
    # Aqui convertemos para lista Python [1, 3, 7] para facilitar filtros.
    df["strings_lista"] = df["strings_origem"].fillna("").apply(
        lambda x: [int(float(s.strip())) for s in x.split(";") if s.strip() and s.strip() != "nan"]
    )

    # Atribui prioridade ao artigo baseada na primeira string de origem
    df["prioridade"] = df["strings_lista"].apply(
        lambda lst: PRIORIDADES.get(lst[0], "Baixa") if lst else "Baixa"
    )

    # Padronizar tipos de publicacao (minusculas, sem espacos extras)
    df["Publication Type"] = df["Publication Type"].fillna("other").str.lower().str.strip()

    return df


# ============================================================
# FILTROS (SIDEBAR)
# ============================================================
# A sidebar e o painel lateral esquerdo do Streamlit.
# Todos os widgets aqui filtram o DataFrame globalmente,
# afetando TODAS as abas do dashboard (exceto "Algoritmos e Abordagens"
# que usa sua propria fonte de dados e filtros).
#
# Para ADICIONAR UM NOVO FILTRO:
#   1. Crie o widget na sidebar (st.sidebar.slider, multiselect, radio, etc.)
#   2. Adicione a logica de filtragem na secao "Aplicar filtros" (mask &= ...)
#   3. O filtro sera aplicado automaticamente em todas as abas

def criar_filtros(df):
    """Cria widgets de filtro na sidebar e retorna o DataFrame filtrado.

    Args:
        df: DataFrame completo com todos os artigos

    Returns:
        DataFrame filtrado conforme selecoes do usuario na sidebar
    """
    # st.sidebar.header(): exibe um titulo na barra lateral
    st.sidebar.header("Filtros")

    # --- Widget: Slider de periodo ---
    # st.sidebar.slider() cria uma barra deslizante. Com value=(min, max),
    # cria um slider de INTERVALO (duas alças). Retorna uma tupla (inicio, fim).
    anos_validos = df["Publication Year"].dropna()
    ano_min = int(anos_validos.min())
    ano_max = int(anos_validos.max())
    ano_range = st.sidebar.slider(
        "Periodo (Ano)",                          # Label exibido ao usuario
        min_value=ano_min, max_value=ano_max,     # Limites do slider
        value=(2018, ano_max),                    # Valor inicial (intervalo padrao)
    )

    # --- Widget: Multiselect de tipo de publicacao ---
    # st.sidebar.multiselect() cria um dropdown onde o usuario pode selecionar
    # multiplas opcoes. Retorna uma lista com os itens selecionados.
    # Se nada for selecionado, retorna lista vazia [] (interpretado como "todos").
    tipos = sorted(df["Publication Type"].unique())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de Publicação",
        options=tipos,               # Lista de opcoes disponiveis
        default=None,                # Nenhum selecionado por padrao
        placeholder="Todos os tipos", # Texto quando nada selecionado
    )

    # --- Widget: Multiselect de string de busca ---
    strings_opcoes = [f"String-{num:02d}" for num in sorted(STRINGS_BUSCA.keys())]
    strings_selecionadas = st.sidebar.multiselect(
        "String de Busca",
        options=strings_opcoes,
        default=None,
        placeholder="Todas",
    )

    # --- Widget: Multiselect de prioridade ---
    prioridades_sel = st.sidebar.multiselect(
        "Prioridade da String",
        options=["Alta", "Media", "Baixa"],
        default=None,
        placeholder="Todas",
    )

    # --- Widget: Radio buttons para Open Access ---
    # st.sidebar.radio() cria botoes de opcao unica (apenas 1 selecionado).
    # horizontal=True coloca os botoes lado a lado em vez de empilhados.
    oa_opcao = st.sidebar.radio(
        "Open Access",
        options=["Todos", "Sim", "Não"],
        horizontal=True,
    )

    # --- Widget: Slider simples de citacoes minimas ---
    # Diferente do slider de periodo, este tem apenas UMA alça (valor unico).
    cit_max = min(int(df["Citing Works Count"].max()), 500)
    cit_min = st.sidebar.slider(
        "Minimo de Citações",
        min_value=0, max_value=cit_max, value=0,  # value=0 → sem filtro inicial
    )

    # -----------------------------------------------
    # APLICAR FILTROS
    # -----------------------------------------------
    # Tecnica: cria uma mascara booleana (True/False para cada linha).
    # Comeca com tudo True e vai aplicando AND (&=) com cada filtro.
    # No final, df[mask] retorna apenas as linhas que passaram em TODOS os filtros.
    mask = pd.Series(True, index=df.index)

    # Filtro de periodo: mantem artigos no intervalo OU sem ano definido
    mask &= df["Publication Year"].between(ano_range[0], ano_range[1]) | df["Publication Year"].isna()

    # Filtro de tipo: so aplica se o usuario selecionou algo
    if tipos_selecionados:
        mask &= df["Publication Type"].isin(tipos_selecionados)

    # Filtro de string: mantem artigos que pertencem a QUALQUER string selecionada
    if strings_selecionadas:
        nums_sel = [int(s.replace("String-", "")) for s in strings_selecionadas]
        mask &= df["strings_lista"].apply(
            lambda lst: any(n in lst for n in nums_sel)
        )

    # Filtro de prioridade
    if prioridades_sel:
        mask &= df["prioridade"].isin(prioridades_sel)

    # Filtro de Open Access
    if oa_opcao == "Sim":
        mask &= df["Is Open Access"].astype(str).str.lower() == "true"
    elif oa_opcao == "Não":
        mask &= df["Is Open Access"].astype(str).str.lower() == "false"

    # Filtro de citacoes minimas
    if cit_min > 0:
        mask &= df["Citing Works Count"] >= cit_min

    # .copy() cria uma copia independente para evitar SettingWithCopyWarning
    return df[mask].copy()


# ============================================================
# METRICAS KPI (cartoes com numeros no topo da pagina)
# ============================================================

def exibir_kpis(df, df_dedup=None):
    """Exibe cartoes de metricas KPI no topo da pagina.

    Fonte de dados:
      - data/artigos_unicos.csv (filtrado) → metricas do dataset filtrado
      - data/resumo_deduplicacao.csv → metricas do processo de deduplicacao
    """
    # ---- Linha 1: Metricas do dataset filtrado ----
    # st.columns(6) cria 6 colunas lado a lado na pagina.
    # Cada coluna pode receber widgets independentes.
    # Para alterar o numero de KPIs, mude o numero e ajuste as variaveis col.
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    total = len(df)
    anos = df["Publication Year"].dropna()
    citacoes = df["Citing Works Count"].sum()
    media_cit = df["Citing Works Count"].mean()
    oa_pct = (df["Is Open Access"].astype(str).str.lower() == "true").sum() / max(total, 1) * 100
    paises = df["Source Country"].dropna().nunique()

    # st.metric() exibe um cartao com label e valor numerico destacado.
    # Pode receber um terceiro parametro "delta" para mostrar variacao (ex: +10%).
    col1.metric("Total de Artigos", f"{total:,}")
    col2.metric("Periodo", f"{int(anos.min())}-{int(anos.max())}" if len(anos) > 0 else "N/A")
    col3.metric("Total de Citações", f"{citacoes:,}")
    col4.metric("Media Citações", f"{media_cit:.1f}")
    col5.metric("Open Access", f"{oa_pct:.1f}%")
    col6.metric("Paises", f"{paises}")

    # ---- Linha 2: Metricas de deduplicacao ----
    # Fonte: data/resumo_deduplicacao.csv — estatisticas do processo de limpeza dos dados
    if df_dedup is not None and not df_dedup.empty:
        st.divider()
        st.caption("📊 Estatísticas de Deduplicação")
        d1, d2, d3, d4, d5, d6 = st.columns(6)
        row = df_dedup.iloc[0]  # CSV tem apenas 1 linha de dados

        d1.metric("Total Bruto", f"{int(row['total_bruto']):,}")
        d2.metric("Total Único", f"{int(row['total_unico']):,}")
        d3.metric("Removidos", f"{int(row['total_removido']):,}")
        d4.metric("Removidos (DOI)", f"{int(row['removidos_por_doi']):,}")
        d5.metric("Removidos (Título)", f"{int(row['removidos_por_titulo']):,}")
        d6.metric("Sobreposição", f"{row['taxa_sobreposicao_pct']:.1f}%")


# ============================================================
# ABA 1 — VISAO GERAL
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado pela sidebar)
# Graficos: barras empilhadas (temporal), pizza (tipos), pizza (OA)

def aba_visao_geral(df):
    """Graficos de visao geral: temporal, tipos de publicacao, open access."""

    # --- Grafico 1: Barras empilhadas por ano e tipo de publicacao ---
    # px.bar() com color= cria barras coloridas por categoria.
    # barmode="stack" empilha as categorias (padrao e "group" = lado a lado).
    st.subheader("Publicações ao Longo do Tempo")

    df_tempo = df.dropna(subset=["Publication Year"]).copy()
    df_tempo["Ano"] = df_tempo["Publication Year"].astype(int)

    # Normalizar tipos para os mais comuns
    tipos_principais = ["journal article", "preprint", "conference proceedings article",
                        "book chapter", "book", "dissertation", "report"]
    df_tempo["Tipo"] = df_tempo["Publication Type"].apply(
        lambda x: x if x in tipos_principais else "other"
    )

    contagem = df_tempo.groupby(["Ano", "Tipo"]).size().reset_index(name="Contagem")

    # px.bar(): cria grafico de barras.
    #   x, y: colunas do DataFrame para eixos
    #   color: coluna para colorir as barras (cada valor vira uma serie)
    #   color_discrete_map: dicionario {valor: cor_hex} para cores fixas
    #   labels: renomeia os eixos na exibicao
    fig = px.bar(
        contagem, x="Ano", y="Contagem", color="Tipo",
        color_discrete_map=PALETTE_PUB_TYPE,
        labels={"Contagem": "Número de Artigos", "Ano": "Ano de Publicação", "Tipo": "Tipo"},
    )
    # fig.update_layout(): personaliza aparencia do grafico.
    #   height: altura em pixels | plot_bgcolor: cor de fundo
    #   legend: posicao e orientacao da legenda
    fig.update_layout(
        barmode="stack",  # "stack" = empilhado | "group" = lado a lado
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
        plot_bgcolor="white",
    )
    fig.update_xaxes(dtick=1)  # dtick=1: mostra TODOS os anos no eixo X
    # st.plotly_chart(): renderiza o grafico Plotly na pagina.
    # width="stretch": ocupa toda a largura disponivel.
    st.plotly_chart(fig, width="stretch")

    # --- Graficos 2 e 3 lado a lado (2 colunas) ---
    # st.columns(2) cria 2 colunas de largura igual.
    # "with col1:" coloca tudo dentro na coluna esquerda.
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tipos de Publicação")
        contagem_tipo = df["Publication Type"].value_counts().head(8)
        # px.pie(): grafico de pizza/rosca.
        #   hole=0.4: cria um furo central (rosca/donut). 0 = pizza cheia, 1 = so borda.
        #   Para alterar quantos tipos aparecem, mude .head(8) acima.
        fig_tipo = px.pie(
            values=contagem_tipo.values,
            names=contagem_tipo.index,
            color=contagem_tipo.index,
            color_discrete_map=PALETTE_PUB_TYPE,
            hole=0.4,
        )
        fig_tipo.update_traces(textposition="inside", textinfo="percent+label")
        fig_tipo.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_tipo, width="stretch")

    with col2:
        st.subheader("Open Access")
        oa = df["Is Open Access"].astype(str).str.lower()
        oa_counts = oa.value_counts()
        labels_oa = ["Open Access" if "true" in k else "Acesso Restrito" for k in oa_counts.index]
        cores_oa = [CORES["success"] if "true" in k else CORES["primary"] for k in oa_counts.index]

        fig_oa = px.pie(
            values=oa_counts.values,
            names=labels_oa,
            color_discrete_sequence=cores_oa,
            hole=0.4,
        )
        fig_oa.update_traces(textposition="inside", textinfo="percent+label")
        fig_oa.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_oa, width="stretch")

        # Tipos de OA
        oa_cor = df[oa == "true"]["Open Access Colour"].fillna("unknown").value_counts()
        if len(oa_cor) > 0:
            cores_mapa = {"gold": "#FFC000", "green": "#70AD47", "bronze": "#C65911",
                          "hybrid": "#5B9BD5", "unknown": "#A5A5A5"}
            fig_oa_tipo = px.bar(
                x=oa_cor.index, y=oa_cor.values,
                color=oa_cor.index,
                color_discrete_map=cores_mapa,
                labels={"x": "Tipo de OA", "y": "Artigos"},
            )
            fig_oa_tipo.update_layout(height=250, showlegend=False, plot_bgcolor="white")
            st.plotly_chart(fig_oa_tipo, width="stretch")


# ============================================================
# ABA 2 — FONTES E AUTORES
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Graficos: 3 barras horizontais (journals, autores, editoras)

def aba_fontes_autores(df):
    """Top journals, autores mais ativos e editoras. Barras horizontais."""

    col1, col2 = st.columns(2)

    with col1:
        # --- Top Journals ---
        st.subheader("Top 15 Journals / Fontes")
        contagem = df["Source Title"].fillna("Nao informado").value_counts().head(15)
        fig = px.bar(
            x=contagem.values, y=contagem.index,
            orientation="h",
            color_discrete_sequence=[CORES["secondary"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig.update_traces(
            text=contagem.values, textposition="outside",
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        # --- Most Active Authors ---
        st.subheader("Top 20 Autores Mais Ativos")
        todos_autores = []
        for autores in df["Author/s"].dropna():
            for autor in str(autores).split(";"):
                autor = autor.strip()
                if autor:
                    todos_autores.append(autor)
        contagem_autores = pd.Series(todos_autores).value_counts().head(20)

        fig_autores = px.bar(
            x=contagem_autores.values, y=contagem_autores.index,
            orientation="h",
            color_discrete_sequence=[CORES["accent"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig_autores.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_autores.update_traces(
            text=contagem_autores.values, textposition="outside",
        )
        st.plotly_chart(fig_autores, width="stretch")

    # --- Top Publishers ---
    st.subheader("Top 10 Editoras (Publishers)")
    contagem_pub = df["Publisher"].fillna("Nao informado").value_counts().head(10)
    fig_pub = px.bar(
        x=contagem_pub.values, y=contagem_pub.index,
        orientation="h",
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Número de Artigos", "y": ""},
    )
    fig_pub.update_layout(
        height=400, plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
    )
    fig_pub.update_traces(text=contagem_pub.values, textposition="outside")
    st.plotly_chart(fig_pub, width="stretch")


# ============================================================
# ABA 3 — IMPACTO E CITACOES
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Graficos: bubble chart (scatter com tamanho), histograma, tabela top 20

def aba_impacto(df):
    """Analise de citacoes: bubble chart por area, histograma e ranking."""

    # --- Bubble chart (grafico de bolhas) ---
    # Usa px.scatter() com parametro size= para criar bolhas proporcionais.
    # Cada bolha e um artigo; tamanho = numero de citacoes.
    # Cor = Area de Aplicacao (derivada da string de busca do artigo).
    st.subheader("Artigos Mais Citados ao Longo do Tempo")

    df_bubble = df.dropna(subset=["Date Published"]).copy()
    df_bubble = df_bubble[df_bubble["Citing Works Count"] > 0]

    # .nlargest(200, ...): pega os 200 artigos mais citados.
    # Para mostrar mais ou menos bolhas, altere este numero.
    df_bubble_top = df_bubble.nlargest(200, "Citing Works Count")

    # Classificar por Area de Aplicacao (baseada na primeira string do artigo)
    df_bubble_top["Área de Aplicação"] = df_bubble_top["strings_lista"].apply(
        lambda lst: AREA_APLICACAO.get(lst[0], "Outros") if lst else "Outros"
    )

    # Criar label de hover
    df_bubble_top["hover"] = (
        df_bubble_top["Title"].str[:80] + "<br>" +
        df_bubble_top["Author/s"].fillna("").str.split(";").str[0] +
        " (" + df_bubble_top["Publication Year"].astype(int).astype(str) + ")" +
        "<br>Citações: " + df_bubble_top["Citing Works Count"].astype(str) +
        "<br>Área: " + df_bubble_top["Área de Aplicação"]
    )

    # px.scatter(): grafico de dispersao. Com size= vira grafico de bolhas.
    #   size: coluna que define o tamanho das bolhas
    #   size_max: tamanho maximo em pixels da maior bolha (ajustar se ficarem grandes demais)
    #   color: coluna para colorir os pontos por categoria
    #   color_discrete_map: mapa de cores fixas (definido em COR_AREA)
    #   hover_name: texto exibido ao passar o mouse sobre a bolha
    #   category_orders: ordem das categorias na legenda
    fig = px.scatter(
        df_bubble_top,
        x="Date Published",
        y="Citing Works Count",
        size="Citing Works Count",
        color="Área de Aplicação",
        color_discrete_map=COR_AREA,
        hover_name="hover",
        size_max=40,
        labels={"Date Published": "Data de Publicação", "Citing Works Count": "Citações"},
        category_orders={"Área de Aplicação": ["TSP", "VRP/Logística", "Supply Chain/QML", "Otim. Combinatória"]},
    )
    fig.update_layout(
        height=500, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, width="stretch")

    # --- Histograma + Tabela top 20 (lado a lado) ---
    col1, col2 = st.columns(2)

    #with col1:
    st.subheader("Distribuição de Citações")
    df_cit = df[df["Citing Works Count"] > 0].copy()
    # px.histogram(): agrupa valores em faixas (bins) e conta frequencia.
    #   nbins: numero de faixas (mais = maior resolucao, menos = mais agregado)
    #   log_y=True: eixo Y em escala logaritmica (util quando poucos artigos tem muitas citacoes)
    fig_hist = px.histogram(
        df_cit, x="Citing Works Count",
        nbins=50,
        color_discrete_sequence=[CORES["primary"]],
        labels={"Citing Works Count": "Número de Citações"},
        log_y=True,
     )
    fig_hist.update_layout(
        height=400, plot_bgcolor="white",
        yaxis_title="Quantidade de Artigos (log)",
      )
    st.plotly_chart(fig_hist, width="stretch")

        # Info contextual
    mediana = df["Citing Works Count"].median()
    p90 = df["Citing Works Count"].quantile(0.9)
    st.caption(
        f"Mediana: {mediana:.0f} citações | "
        f"90% dos artigos tem ate {p90:.0f} citações | "
        f"Artigos sem citação: {(df['Citing Works Count'] == 0).sum()}"
    )

    #with col2:
     # st.dataframe(): exibe uma tabela interativa (ordenavel, pesquisavel).
     # Para alterar o numero de artigos, mude nlargest(20, ...) abaixo.
    st.subheader("Top 20 Artigos Mais Citados")
    df_top = df.nlargest(20, "Citing Works Count")[
            ["Title", "Author/s", "Publication Year", "DOI","Citing Works Count"]
     ].copy()
    df_top.columns = ["Titulo", "Autores", "Ano", "DOI", "Citações"]
    df_top["Autores"] = df_top["Autores"].fillna("").str.split(";").str[0]
    df_top["Titulo"] = df_top["Titulo"].str[:80]
    df_top["Ano"] = df_top["Ano"].fillna(0).astype(int)
    # Calcula o percentual de citações em relação ao artigo mais citado do dataset
    df_top["Citações(%)"] = (df_top["Citações"] / df["Citing Works Count"].sum() * 100).round(1).astype(str) + "%"
    st.dataframe(
        df_top.reset_index(drop=True),
        height=740,
        width="stretch",
        use_container_width=True
        )


# ============================================================
# ABA 4 — CAMPOS DE ESTUDO
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Colunas usadas: "Fields of Study" (multi-valor, separado por ";") e "Keywords"
# Graficos: treemap (Plotly) + nuvem de palavras (matplotlib/WordCloud)

def aba_campos_estudo(df):
    """Treemap de campos de estudo e nuvem de palavras de keywords."""

    #col1, col2 = st.columns(2)

    #with col1:
    st.subheader("Top 30 - Fields of Study")
    todos_campos = []
    for campos in df["Fields of Study"].dropna():
        for campo in str(campos).split(";"):
            campo = campo.strip()
            if campo:
                todos_campos.append(campo)

    contagem = pd.Series(todos_campos).value_counts().head(30).reset_index()
    contagem.columns = ["Campo", "Frequencia"]

    # px.treemap(): retangulos aninhados proporcionais ao valor.
    #   path: hierarquia de categorias (aqui so 1 nivel)
    #   values: coluna que define o tamanho de cada retangulo
    #   color_continuous_scale: gradiente de cores [mais claro → mais escuro]
    fig = px.treemap(
        contagem,
        path=["Campo"],
        values="Frequencia",
        color="Frequencia",
        color_continuous_scale=["#CAF0F8", "#0077B6", "#03045E"],
    )
    fig.update_layout(height=600, plot_bgcolor="white")
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, width="stretch")

    #with col2:
    st.subheader("Nuvem de Palavras — Keywords")
    keywords_preenchidos = df["Keywords"].dropna()
    cobertura = len(keywords_preenchidos) / len(df) * 100
    st.caption(f"Cobertura: {cobertura:.1f}% dos artigos possuem keywords")

    todas_kw = []
    for kws in keywords_preenchidos:
        for kw in str(kws).split(";"):
            kw = kw.strip()
            if kw:
                todas_kw.append(kw)

    if todas_kw:
        freq_kw = dict(pd.Series(todas_kw).value_counts().head(100))

        # WordCloud: gera imagem com palavras proporcionais a frequencia.
        #   max_words: limite de palavras na nuvem
        #   colormap: paleta matplotlib ("ocean", "viridis", "plasma", etc.)
        #   generate_from_frequencies(): usa dicionario {palavra: contagem}
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",        # Paleta de cores (trocar por "viridis", "plasma", "ocean" etc.)
            max_words=80,            # Maximo de palavras exibidas
            prefer_horizontal=0.7,   # 70% horizontal, 30% vertical
            min_font_size=10,
            max_font_size=80,
            relative_scaling=0.5,
        ).generate_from_frequencies(freq_kw)

        # WordCloud gera imagem matplotlib, entao usamos st.pyplot() (nao st.plotly_chart)
        fig_wc, ax_wc = plt.subplots(figsize=(10, 6))
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig_wc)  # st.pyplot(): renderiza graficos matplotlib no Streamlit
        plt.close(fig_wc)  # Liberar memoria
    else:
        st.info("Nenhum keyword disponivel com os filtros atuais.")


# ============================================================
# ABA 5 — GEOGRAFIA
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Coluna usada: "Source Country"
# Graficos: mapa choropleth mundial + barras horizontais top 15 paises

def aba_geografia(df):
    """Mapa mundial colorido por numero de publicacoes e ranking de paises."""

    cobertura = df["Source Country"].notna().sum() / len(df) * 100
    st.caption(
        f"Cobertura: {cobertura:.1f}% dos artigos possuem informação de país. "
        "Preprints frequentemente não informam o país de origem."
    )

    # --- Mapa Choropleth ---
    st.subheader("Distribuição Geográfica das Publicações")
    contagem_pais = df["Source Country"].dropna().value_counts().reset_index()
    contagem_pais.columns = ["Pais", "Artigos"]

    # Mapear nomes de paises para ISO-3
    def pais_para_iso3(nome):
        try:
            return pycountry.countries.lookup(nome).alpha_3
        except LookupError:
            return None

    contagem_pais["ISO3"] = contagem_pais["Pais"].apply(pais_para_iso3)
    contagem_pais = contagem_pais.dropna(subset=["ISO3"])

    # px.choropleth(): mapa mundial onde cada pais e colorido conforme um valor.
    #   locations: coluna com codigos ISO-3 dos paises (ex: "BRA", "USA")
    #   color: coluna que define a intensidade da cor
    #   color_continuous_scale: gradiente de cores [menos → mais]
    #   Para mudar a projecao do mapa, altere projection_type abaixo
    #   (opcoes: "natural earth", "orthographic", "mercator", "equirectangular")
    fig_mapa = px.choropleth(
        contagem_pais,
        locations="ISO3",
        locationmode="ISO-3",
        color="Artigos",
        color_continuous_scale=["#CAF0F8", "#48CAE4", "#0077B6", "#023E8A", "#03045E"],
        labels={"Artigos": "Número de Artigos"},
    )
    fig_mapa.update_layout(
        height=500,
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    )
    st.plotly_chart(fig_mapa, width="stretch")

    # --- Top 15 paises ---
    st.subheader("Top 15 Países por Número de Publicações")
    top_paises = contagem_pais.head(15)
    fig_pais = px.bar(
        top_paises, x="Artigos", y="Pais",
        orientation="h",
        color_discrete_sequence=[CORES["secondary"]],
    )
    fig_pais.update_layout(
        height=450, plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
    )
    fig_pais.update_traces(text=top_paises["Artigos"], textposition="outside")
    st.plotly_chart(fig_pais, width="stretch")


# ============================================================
# ABA 6 — STRINGS DE BUSCA
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado) + docs/pesquisa_palavras_chave_tsp_quantico.xlsx
# A planilha Excel e usada apenas para exibir as strings completas na tabela de referencia.
# Graficos: barras por string, barras de sobreposicao, heatmap de coocorrencia

def aba_strings(df):
    """Analise das strings de busca: volume, sobreposicao e coocorrencia."""

    # --- Volume por String ---
    st.subheader("Volume de Artigos por String de Busca")

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
        color="Prioridade",
        color_discrete_map=COR_PRIORIDADE,
        hover_data=["Descrição"],
        labels={"Artigos": "Artigos Únicos"},
    )
    fig.update_layout(
        height=450, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_traces(texttemplate="%{y}", textposition="outside")
    st.plotly_chart(fig, width="stretch")

    # --- Sobreposicao + Heatmap ---
    #col1, col2 = st.columns(2)

    #with col1:
    st.subheader("Sobreposição entre Strings")
    contagem_overlap = df["qtd_strings"].value_counts().sort_index()
    fig_overlap = px.bar(
        x=contagem_overlap.index.astype(str),
        y=contagem_overlap.values,
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Aparece em N strings", "y": "Qtd Artigos"},
    )
    fig_overlap.update_layout(height=600, plot_bgcolor="white")
    fig_overlap.update_traces(
        text=[f"{v} ({v/len(df)*100:.1f}%)" for v in contagem_overlap.values],
        textposition="outside",
    )
    st.plotly_chart(fig_overlap, width="stretch")

    #with col2:
    # Heatmap de coocorrencia: mostra quantos artigos aparecem em AMBAS as strings.
    # go.Heatmap(): grafico de calor (matrix). Usado quando px nao tem o tipo.
    #   z: matriz 2D de valores | x, y: labels dos eixos
    #   colorscale: gradiente de cores [[posicao, cor], ...]
    #   text/texttemplate: exibe valores dentro das celulas
    st.subheader("Coocorrência entre Strings")
    st.caption("Quantos artigos compartilham cada par de strings")

    # Construir matriz de coocorrencia
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
        z=matriz,
        x=labels_str,
        y=labels_str,
        colorscale=[[0, "#FFFFFF"], [0.2, "#CAF0F8"], [0.5, "#48CAE4"], [1, "#03045E"]],
        text=matriz,
        texttemplate="%{text}",
        textfont={"size": 8},
    ))
    fig_heat.update_layout(
        height=600,
        xaxis=dict(tickangle=45),
    )
    st.plotly_chart(fig_heat, width="stretch")

    # --- Tabela de Referência das Strings de Busca ---
    st.divider()
    st.subheader("Referência — Strings de Busca Utilizadas")
    st.caption("Fonte: Levantamento bibliográfico no Lens.org (filtro: Scholarly Works)")

    dados_ref = []
    for num in sorted(STRINGS_BUSCA.keys()):
        dados_ref.append({
            "Código": f"String-{num:02d}",
            "Descrição Resumida": STRINGS_BUSCA[num],
            "Prioridade": PRIORIDADES.get(num, "Baixa"),
        })
    df_ref = pd.DataFrame(dados_ref)

    # Carregar strings completas da planilha
    try:
        caminho_xlsx = os.path.join(PASTA_PROJETO, "docs", "pesquisa_palavras_chave_tsp_quantico.xlsx")
        df_xlsx = pd.read_excel(caminho_xlsx, sheet_name="Palavras-Chave vs Artigos", header=None)
        strings_completas = {}
        totais = {}
        for _, row in df_xlsx.iterrows():
            try:
                num = int(row.iloc[0])
                if 1 <= num <= 26:
                    strings_completas[num] = str(row.iloc[1]).strip()
                    totais[num] = int(row.iloc[5]) if pd.notna(row.iloc[5]) else 0
            except (ValueError, TypeError):
                continue

        df_ref["String de Busca Completa"] = df_ref["Código"].apply(
            lambda x: strings_completas.get(int(x.replace("String-", "")), "")
        )
        df_ref["Total Bruto"] = df_ref["Código"].apply(
            lambda x: totais.get(int(x.replace("String-", "")), 0)
        )
    except Exception:
        df_ref["String de Busca Completa"] = df_ref["Descrição Resumida"]
        df_ref["Total Bruto"] = 0

    st.dataframe(
        df_ref[["Código", "String de Busca Completa", "Prioridade", "Total Bruto"]].reset_index(drop=True),
        height=600,
        width="stretch",
        column_config={
            "Código": st.column_config.TextColumn(width="small"),
            "String de Busca Completa": st.column_config.TextColumn(width="large"),
            "Prioridade": st.column_config.TextColumn(width="small"),
            "Total Bruto": st.column_config.NumberColumn(width="small")
        },
    )


# ============================================================
# ABA 7 — ALGORITMOS E ABORDAGENS
# ============================================================
# Fonte de dados: data/base_algoritmos_abordagens.csv (38 algoritmos catalogados)
#   → Esta aba usa uma fonte de dados DIFERENTE das demais abas.
#   → Possui seus PROPRIOS filtros (paradigma, abordagem, area, variante).
#   → Os filtros da sidebar NÃO afetam esta aba.
# Graficos: pizza (paradigma, abordagem), barras (timeline, hardware, variantes,
#           escala, criterios, formulacao, metricas), heatmap, radar, tabela

# Paleta de cores para paradigmas quanticos (aba Algoritmos)
PALETTE_PARADIGMA = {
    "QA": "#0077B6",           # Quantum Annealing — azul escuro
    "GBC": "#00B4D8",          # Gate-Based Computing — azul claro
    "QA e GBC": "#023E8A",     # Hibrido QA + GBC — azul marinho
    "CA": "#48CAE4",           # Computacao Adiabatica — ciano
    "QRNG": "#70AD47",         # Quantum Random Number Gen — verde
    "Generic": "#A5A5A5",      # Generico — cinza
    "QML": "#9B59B6",          # Quantum Machine Learning — roxo
}

# Paleta de cores para abordagens (full quantum vs hybrid)
PALETTE_ABORDAGEM = {
    "Hybrid": "#0077B6",           # Hibrida — azul
    "Full Quantum": "#00B4D8",     # Puramente quantica — ciano
    "Full e Hybrid": "#48CAE4",    # Ambas — azul claro
    "Não especificado": "#A5A5A5", # Nao informado — cinza
}

# Paleta de cores para topicos (Routing, Scheduling, etc.)
PALETTE_TOPICO = {
    "Routing": "#0077B6",
    "Network Design": "#ED7D31",
    "Scheduling": "#9B59B6",
    "Cargo": "#70AD47",
    "Fleet Optimization": "#48CAE4",
    "Prediction": "#FFC000",
}


@st.cache_data
def carregar_algoritmos():
    """Carrega a base compilada de algoritmos e abordagens.

    Fonte: data/base_algoritmos_abordagens.csv (129 trabalhos)
    Colunas: id, autores, paradigma, algoritmo_quantico, topico,
             problema, abordagem, ano, hardware, num_cidades, formulacao,
             contribuicao, escala_testada, qualidade_solucao, tempo_execucao,
             taxa_sucesso, sensibilidade_parametros, robustez_ruido,
             metricas_avaliadas, fonte
    """
    caminho = os.path.join(PASTA_PROJETO, "data", "base_algoritmos_abordagens.csv")
    df = pd.read_csv(caminho, dtype=str)
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype(int)
    # Converter ano para numerico (artigos sem ano ficam como NaN)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    # Converter ranking para numerico (coluna de pontuação ponderada 0-10)
    if "ranking" in df.columns:
        df["ranking"] = pd.to_numeric(df["ranking"], errors="coerce").fillna(0.0)
    return df


def aba_algoritmos():
    """Aba de exploracao de algoritmos e abordagens do artigo de referencia.

    # ABA 7 — ALGORITMOS E ABORDAGENS
    # Fonte de dados: data/base_algoritmos_abordagens.csv (129 trabalhos catalogados)
    #   → Extraido das 3 tabelas do artigo Phillipson (2025), paginas 50-52
    #   → Colunas: id, autores, paradigma, algoritmo_quantico, topico,
    #              problema, abordagem, ano, hardware, formulacao, etc.
    #   → Esta aba usa uma fonte de dados DIFERENTE das demais abas.
    #   → Possui seus PROPRIOS filtros (paradigma, algoritmo, topico, problema, abordagem, criterios).
    #   → Os filtros da sidebar NÃO afetam esta aba.
    """

    # Mapeamento de códigos de critérios para suas descrições completas.
    # Usado no filtro multiselect para exibir a descrição ao invés do código (C1, C2...).
    CRITERIOS_DESCRICAO = {
        "C1": "C1 — Qualidade da solução",
        "C2": "C2 — Escalabilidade",
        "C3": "C3 — Aplicação real",
        "C4": "C4 — Comparação com clássico",
        "C5": "C5 — Análise de limitações",
        "C6": "C6 — Taxa de sucesso",
    }
    # Mapeamento inverso: descrição → código (para aplicar filtro no DataFrame)
    DESCRICAO_CRITERIOS = {v: k for k, v in CRITERIOS_DESCRICAO.items()}

    df_algo = carregar_algoritmos()

    # --- Filtros especificos desta aba ---
    # st.markdown("##### ...") renderiza como titulo h5 (pequeno).
    st.markdown("##### Filtros de Algoritmos")
    # Primeira linha de filtros: paradigma, algoritmo, topico
    fc1, fc2, fc3 = st.columns(3)

    # Cada filtro usa st.multiselect() com key= unico.
    # O parametro key= e OBRIGATORIO quando ha multiplos widgets do mesmo tipo no dashboard.
    with fc1:
        paradigmas = sorted(df_algo["paradigma"].dropna().unique())
        paradigma_sel = st.multiselect(
            "Paradigma",
            options=paradigmas,
            default=None,
            placeholder="Todos",
            key="algo_paradigma",
        )

    with fc2:
        algoritmos = sorted(df_algo["algoritmo_quantico"].dropna().unique())
        algoritmo_sel = st.multiselect(
            "Algoritmo Quântico",
            options=algoritmos,
            default=None,
            placeholder="Todos",
            key="algo_algoritmo",
        )

    with fc3:
        topicos = sorted(df_algo["topico"].dropna().unique())
        topico_sel = st.multiselect(
            "Tópico",
            options=topicos,
            default=None,
            placeholder="Todos",
            key="algo_topico",
        )

    # Segunda linha de filtros: problema, abordagem, critérios de seleção
    fc4, fc5, fc6 = st.columns(3)

    with fc4:
        problemas = sorted(df_algo["problema"].dropna().unique())
        problema_sel = st.multiselect(
            "Problema",
            options=problemas,
            default=None,
            placeholder="Todos",
            key="algo_problema",
        )

    with fc5:
        abordagens = sorted(df_algo["abordagem"].dropna().unique())
        abordagem_sel = st.multiselect(
            "Abordagem",
            options=abordagens,
            default=None,
            placeholder="Todas",
            key="algo_abordagem",
        )

    with fc6:
        # Filtro de critérios de seleção — exibe a descrição completa (ex: "C1 — Qualidade da solução")
        # ao invés do código curto (C1). O filtro verifica se o critério selecionado
        # aparece na coluna "criterios" do CSV (que pode conter múltiplos valores: "C1, C3").
        criterio_opcoes = list(CRITERIOS_DESCRICAO.values())
        criterio_sel = st.multiselect(
            "Critério de Seleção",
            options=criterio_opcoes,
            default=None,
            placeholder="Todos",
            key="algo_criterio",
        )

    # Aplicar filtros — mesma logica de mascara booleana usada em criar_filtros().
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
        # Converter descrições selecionadas de volta para códigos (C1, C2...)
        codigos_sel = [DESCRICAO_CRITERIOS[d] for d in criterio_sel]
        # Filtrar linhas que contenham QUALQUER um dos critérios selecionados
        # A coluna "criterios" pode ter valores como "C1, C3", então usamos str.contains
        criterio_mask = pd.Series(False, index=df_algo.index)
        for codigo in codigos_sel:
            criterio_mask |= df_algo["criterios"].str.contains(codigo, na=False)
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

    st.divider()

    # ===============================
    # LINHA 1: Paradigma + Abordagem
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Paradigma Quântico")
        contagem_p = df_f["paradigma"].value_counts().reset_index()
        contagem_p.columns = ["Paradigma", "Trabalhos"]

        fig_p = px.pie(
            contagem_p, values="Trabalhos", names="Paradigma",
            color="Paradigma", color_discrete_map=PALETTE_PARADIGMA,
            hole=0.4,
        )
        fig_p.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_p.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_p, use_container_width=True)

    with col2:
        st.subheader("Distribuição por Abordagem")
        contagem_a = df_f["abordagem"].value_counts().reset_index()
        contagem_a.columns = ["Abordagem", "Trabalhos"]

        fig_a = px.pie(
            contagem_a, values="Trabalhos", names="Abordagem",
            color="Abordagem", color_discrete_map=PALETTE_ABORDAGEM,
            hole=0.4,
        )
        fig_a.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_a.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_a, use_container_width=True)

    # ===============================
    # LINHA 2: Tópico + Algoritmo Quântico
    # ===============================
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Distribuição por Tópico")
        contagem_t = df_f["topico"].value_counts().reset_index()
        contagem_t.columns = ["Tópico", "Trabalhos"]

        fig_t = px.bar(
            contagem_t, x="Trabalhos", y="Tópico",
            orientation="h",
            color="Tópico", color_discrete_map=PALETTE_TOPICO,
            text="Trabalhos",
        )
        fig_t.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            showlegend=False,
        )
        fig_t.update_traces(textposition="outside")
        st.plotly_chart(fig_t, use_container_width=True)

    with col4:
        st.subheader("Algoritmos Quânticos Mais Frequentes")
        contagem_alg = df_f["algoritmo_quantico"].value_counts().reset_index()
        contagem_alg.columns = ["Algoritmo", "Trabalhos"]

        fig_alg = px.bar(
            contagem_alg, x="Trabalhos", y="Algoritmo",
            orientation="h",
            color_discrete_sequence=[CORES["primary"]],
        )
        fig_alg.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_alg.update_traces(text=contagem_alg["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_alg, use_container_width=True)

    # ===============================
    # LINHA 3: Problemas (Top 15) + Paradigma por Tópico (Stacked Bar)
    # ===============================
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Problemas Mais Frequentes (Top 15)")
        contagem_sub = df_f["problema"].value_counts().head(15).reset_index()
        contagem_sub.columns = ["Problema", "Trabalhos"]

        fig_sub = px.bar(
            contagem_sub, x="Trabalhos", y="Problema",
            orientation="h",
            color_discrete_sequence=[CORES["accent"]],
        )
        fig_sub.update_layout(
            height=450, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_sub.update_traces(text=contagem_sub["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_sub, use_container_width=True)

    with col6:
        st.subheader("Paradigma por Tópico")
        contagem_pt = df_f.groupby(["topico", "paradigma"]).size().reset_index(name="Trabalhos")

        fig_pt = px.bar(
            contagem_pt, x="Trabalhos", y="topico",
            orientation="h",
            color="paradigma",
            color_discrete_map=PALETTE_PARADIGMA,
            labels={"topico": "Tópico", "paradigma": "Paradigma"},
        )
        fig_pt.update_layout(
            barmode="stack", height=450, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_pt, use_container_width=True)

    # ===============================
    # LINHA 4: Heatmap Tópico × Algoritmo
    # ===============================
    st.subheader("Heatmap: Tópico × Algoritmo Quântico")
    st.caption("Intensidade indica o número de trabalhos que combinam cada tópico com cada algoritmo")

    heat_data = df_f.groupby(["topico", "algoritmo_quantico"]).size().reset_index(name="Qtd")
    heat_pivot = heat_data.pivot_table(
        index="topico", columns="algoritmo_quantico", values="Qtd", fill_value=0
    )
    # Ordenar por total decrescente
    heat_pivot = heat_pivot.loc[heat_pivot.sum(axis=1).sort_values(ascending=False).index]

    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_pivot.values,
        x=heat_pivot.columns.tolist(),
        y=heat_pivot.index.tolist(),
        colorscale=[[0, "#FFFFFF"], [0.2, "#CAF0F8"], [0.5, "#48CAE4"], [1, "#03045E"]],
        text=heat_pivot.values,
        texttemplate="%{text}",
    ))
    fig_heat.update_layout(height=400, xaxis_title="Algoritmo Quântico", yaxis_title="Tópico")
    st.plotly_chart(fig_heat, use_container_width=True)

    # ===============================
    # LINHA 5: Treemap hierárquico
    # ===============================
    st.subheader("Treemap: Tópico → Problema → Paradigma")
    st.caption("Visualização hierárquica da distribuição dos trabalhos")

    df_tree = df_f[["topico", "problema", "paradigma"]].copy()
    df_tree["count"] = 1

    fig_tree = px.treemap(
        df_tree,
        path=["topico", "problema", "paradigma"],
        values="count",
        color="topico",
        color_discrete_map=PALETTE_TOPICO,
    )
    fig_tree.update_layout(height=500)
    fig_tree.update_traces(textinfo="label+value")
    st.plotly_chart(fig_tree, use_container_width=True)

    # ===============================
    # LINHA 6: Radar de critérios por autor
    # ===============================
    # Exibe um radar (spider chart) com os 6 critérios de seleção (C1-C6) por autor.
    # Cada eixo mostra o peso do critério se atendido, ou 0 caso contrário.
    # O usuário pode selecionar quais autores comparar via multiselect.
    st.subheader("Radar de Critérios por Autor")
    st.caption("Pontuação dos critérios de seleção aplicados por autor (peso do critério se atendido)")

    # Labels curtos para os 6 eixos do radar
    CRITERIOS_RADAR = {
        "C1": "Qualidade da Solução",
        "C2": "Escalabilidade",
        "C3": "Aplicação Real",
        "C4": "Comparação c/ Clássico",
        "C5": "Análise de Limitações",
        "C6": "Taxa de Sucesso",
    }
    # Pesos de cada critério na escala do radar (proporcionais aos pesos reais × 10)
    PESOS_RADAR = {"C1": 20, "C2": 15, "C3": 20, "C4": 15, "C5": 10, "C6": 20}
    codigos = list(CRITERIOS_RADAR.keys())
    labels_radar = list(CRITERIOS_RADAR.values())

    # Listar todos os autores ordenados: primeiro os que têm ranking > 0 (decrescente),
    # depois os demais em ordem alfabética.
    if "ranking" in df_f.columns:
        df_com_rank = df_f[df_f["ranking"] > 0].sort_values("ranking", ascending=False)
        df_sem_rank = df_f[df_f["ranking"] == 0].sort_values("autores")
        autores_com_rank = df_com_rank["autores"].unique().tolist()
        autores_sem_rank = df_sem_rank["autores"].unique().tolist()
        todos_autores = autores_com_rank + [a for a in autores_sem_rank if a not in autores_com_rank]
    else:
        todos_autores = sorted(df_f["autores"].unique().tolist())
        autores_com_rank = []

    # Default: top 5 autores com maior ranking (se houver)
    default_autores = autores_com_rank[:5] if autores_com_rank else todos_autores[:5]

    if todos_autores:
        autores_sel_radar = st.multiselect(
            "Selecione autores para comparar",
            options=todos_autores,
            default=default_autores,
            key="radar_autores_sel",
        )

        if autores_sel_radar:
            fig_radar = go.Figure()
            cores_radar = px.colors.qualitative.Set2

            for i, autor in enumerate(autores_sel_radar):
                row_autor = df_f[df_f["autores"] == autor].iloc[0]
                criterios_str = row_autor["criterios"] if pd.notna(row_autor["criterios"]) else ""
                # Ignorar "Nao Reportada" como critério
                if criterios_str.strip().lower() == "nao reportada":
                    criterios_presentes = set()
                else:
                    criterios_presentes = {c.strip() for c in criterios_str.split(",")}

                values = []
                for cod in codigos:
                    values.append(PESOS_RADAR[cod] if cod in criterios_presentes else 0)
                values.append(values[0])  # fechar polígono

                ranking_val = int(row_autor["ranking"]) if "ranking" in row_autor.index and pd.notna(row_autor["ranking"]) else 0
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
            st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Nenhum autor disponível nos dados filtrados.")

    # ===============================
    # LINHA 7: Tabela completa
    # ===============================
    st.subheader("Tabela Detalhada dos Trabalhos")

    colunas_exibir = [
        "autores", "ano", "paradigma", "algoritmo_quantico", "topico",
        "problema", "abordagem", "hardware", "num_cidades",
        "formulacao", "contribuicao", "escala_testada", "qualidade_solucao",
        "tempo_execucao", "taxa_sucesso", "sensibilidade_parametros",
        "robustez_ruido", "metricas_avaliadas", "criterios", "ranking",
    ]
    # Filtrar apenas colunas que existem no DataFrame carregado
    colunas_exibir = [c for c in colunas_exibir if c in df_f.columns]
    colunas_nomes = {
        "autores": "Autores",
        "ano": "Ano",
        "paradigma": "Paradigma",
        "algoritmo_quantico": "Algoritmo Quântico",
        "topico": "Tópico",
        "problema": "Problema",
        "abordagem": "Abordagem",
        "hardware": "Hardware",
        "num_cidades": "Nº Cidades",
        "formulacao": "Formulação",
        "contribuicao": "Contribuição",
        "escala_testada": "Escala",
        "qualidade_solucao": "Qualidade",
        "tempo_execucao": "Tempo Execução",
        "taxa_sucesso": "Taxa Sucesso",
        "sensibilidade_parametros": "Sensib. Parâmetros",
        "robustez_ruido": "Robustez Ruído",
        "metricas_avaliadas": "Métricas Avaliadas",
        "criterios": "Critérios",
        "ranking": "Score Geral",
    }

    # Ordenar por ranking decrescente (melhores no topo)
    df_tabela = df_f[colunas_exibir].copy()
    df_tabela = df_tabela.sort_values("ranking", ascending=False) if "ranking" in df_tabela.columns else df_tabela
    df_tabela = df_tabela.rename(columns=colunas_nomes)
    # Formatar ano como inteiro (sem decimal) onde disponível
    if "Ano" in df_tabela.columns:
        df_tabela["Ano"] = df_tabela["Ano"].apply(
            lambda x: str(int(x)) if pd.notna(x) and x != 0 else "N/D"
        )

    st.dataframe(
        df_tabela.reset_index(drop=True),
        height=500,
        use_container_width=True,
    )


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================
# Fluxo do Streamlit: o script inteiro e re-executado de cima para baixo
# toda vez que o usuario interage com qualquer widget (slider, multiselect, etc.).
# O @st.cache_data garante que os CSVs nao sejam relidos do disco a cada re-execucao.

def main():
    # st.title(): titulo grande da pagina (equivale a <h1> em HTML).
    st.title("Análise Bibliométrica — TSP Quântico")
    st.caption(
        "Exploração dos 3.696 artigos únicos identificados na pesquisa bibliográfica | "
        "Mestrado Profissional — SENAI CIMATEC"
    )

    # 1. Carregar dados do CSV (cacheado — so le do disco na primeira vez)
    df = carregar_dados()

    # 1b. Carregar estatisticas de deduplicacao (CSV com 1 linha de metricas)
    #     Fonte: data/resumo_deduplicacao.csv — gerado apos processo de limpeza
    try:
        df_dedup = pd.read_csv("data/resumo_deduplicacao.csv")
    except FileNotFoundError:
        df_dedup = None

    # 2. Montar filtros na sidebar e obter DataFrame filtrado
    df_filtrado = criar_filtros(df)

    # 3. Exibir KPIs no topo (metricas resumidas + metricas de deduplicacao)
    exibir_kpis(df_filtrado, df_dedup)

    st.divider()

    # 4. st.tabs(): cria abas de navegacao horizontais.
    #    Retorna N objetos, um por aba. Cada aba e preenchida com "with tabN:".
    #    IMPORTANTE: o numero de variaveis deve corresponder ao numero de nomes na lista.
    #    Para adicionar uma aba, inclua o nome na lista e crie uma nova variavel (tab8, etc.).
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Visão Geral",
        "Fontes e Autores",
        "Impacto e Citações",
        "Campos de Estudo",
        "Geografia",
        "Strings de Busca",
        "Algoritmos e Abordagens",
    ])

    # Abas 1-6 recebem df_filtrado (filtrado pela sidebar).
    # Aba 7 (Algoritmos) NAO recebe df_filtrado — usa sua propria fonte de dados e filtros.
    with tab1:
        aba_visao_geral(df_filtrado)

    with tab2:
        aba_fontes_autores(df_filtrado)

    with tab3:
        aba_impacto(df_filtrado)

    with tab4:
        aba_campos_estudo(df_filtrado)

    with tab5:
        aba_geografia(df_filtrado)

    with tab6:
        aba_strings(df_filtrado)

    with tab7:
        aba_algoritmos()


# Ponto de entrada: so executa quando o script e rodado diretamente
# (nao quando importado como modulo). O Streamlit chama este arquivo diretamente.
if __name__ == "__main__":
    main()
