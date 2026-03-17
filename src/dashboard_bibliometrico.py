"""
Dashboard Bibliometrico — Fase 1 (Exploracao Bibliografica)

Dashboard interativo em Streamlit para explorar os 3.696 artigos
unicos identificados na pesquisa bibliografica sobre TSP + Computacao Quantica.

Como usar:
    streamlit run src/dashboard_bibliometrico.py
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
    page_title="Análise Bibliométrica - TSP Quântico",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PALETA DE CORES
# ============================================================

CORES = {
    "primary": "#0077B6",
    "secondary": "#00B4D8",
    "accent": "#90E0EF",
    "highlight": "#CAF0F8",
    "dark": "#03045E",
    "success": "#70AD47",
    "warning": "#FFC000",
    "danger": "#ED7D31",
}

# Sequencia para graficos categoricos (inspirada nos tons do Lens.org)
PALETTE = ["#0077B6", "#00B4D8", "#48CAE4", "#90E0EF", "#023E8A",
           "#0096C7", "#ADE8F4", "#70AD47", "#FFC000", "#ED7D31"]

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

PRIORIDADES = {
    1: "Alta", 2: "Alta", 3: "Alta", 4: "Alta", 5: "Alta",
    6: "Alta", 17: "Alta", 18: "Alta",
    7: "Media", 8: "Media", 9: "Media", 10: "Media", 11: "Media",
    12: "Media", 19: "Media", 20: "Media", 21: "Media", 22: "Media",
    13: "Baixa", 14: "Baixa", 15: "Baixa", 16: "Baixa",
    23: "Baixa", 24: "Baixa", 25: "Baixa", 26: "Baixa",
}

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


# ============================================================
# CARREGAMENTO DE DADOS
# ============================================================

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@st.cache_data
def carregar_dados():
    """Carrega e prepara o dataset principal."""
    caminho = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
    df = pd.read_csv(caminho, dtype=str)

    # Conversoes numericas
    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    df["Citing Patents Count"] = pd.to_numeric(df["Citing Patents Count"], errors="coerce").fillna(0).astype(int)
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce").fillna(1).astype(int)

    # Converter Data Published
    df["Date Published"] = pd.to_datetime(df["Date Published"], errors="coerce")

    # Lista de strings de origem
    df["strings_lista"] = df["strings_origem"].fillna("").apply(
        lambda x: [int(float(s.strip())) for s in x.split(";") if s.strip() and s.strip() != "nan"]
    )

    # Prioridade (baseada na primeira string)
    df["prioridade"] = df["strings_lista"].apply(
        lambda lst: PRIORIDADES.get(lst[0], "Baixa") if lst else "Baixa"
    )

    # Normalizar Publication Type
    df["Publication Type"] = df["Publication Type"].fillna("other").str.lower().str.strip()

    return df


# ============================================================
# FILTROS (SIDEBAR)
# ============================================================

def criar_filtros(df):
    """Cria os filtros na sidebar e retorna o DataFrame filtrado."""
    st.sidebar.header("Filtros")

    # 1. Periodo
    anos_validos = df["Publication Year"].dropna()
    ano_min = int(anos_validos.min())
    ano_max = int(anos_validos.max())
    ano_range = st.sidebar.slider(
        "Periodo (Ano)",
        min_value=ano_min, max_value=ano_max,
        value=(2018, ano_max),
    )

    # 2. Tipo de publicacao
    tipos = sorted(df["Publication Type"].unique())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de Publicação",
        options=tipos,
        default=None,
        placeholder="Todos os tipos",
    )

    # 3. String de Busca
    strings_opcoes = [f"String-{num:02d}" for num in sorted(STRINGS_BUSCA.keys())]
    strings_selecionadas = st.sidebar.multiselect(
        "String de Busca",
        options=strings_opcoes,
        default=None,
        placeholder="Todas",
    )

    # 5. Prioridade da string
    prioridades_sel = st.sidebar.multiselect(
        "Prioridade da String",
        options=["Alta", "Media", "Baixa"],
        default=None,
        placeholder="Todas",
    )

    # 4. Open Access
    oa_opcao = st.sidebar.radio(
        "Open Access",
        options=["Todos", "Sim", "Não"],
        horizontal=True,
    )

    # 5. Minimo de citacoes
    cit_max = min(int(df["Citing Works Count"].max()), 500)
    cit_min = st.sidebar.slider(
        "Minimo de Citações",
        min_value=0, max_value=cit_max, value=0,
    )

    # Aplicar filtros
    mask = pd.Series(True, index=df.index)

    # Periodo
    mask &= df["Publication Year"].between(ano_range[0], ano_range[1]) | df["Publication Year"].isna()

    # Tipo
    if tipos_selecionados:
        mask &= df["Publication Type"].isin(tipos_selecionados)

    # String de Busca
    if strings_selecionadas:
        nums_sel = [int(s.replace("String-", "")) for s in strings_selecionadas]
        mask &= df["strings_lista"].apply(
            lambda lst: any(n in lst for n in nums_sel)
        )

    # Prioridade
    if prioridades_sel:
        mask &= df["prioridade"].isin(prioridades_sel)

    # Open Access
    if oa_opcao == "Sim":
        mask &= df["Is Open Access"].astype(str).str.lower() == "true"
    elif oa_opcao == "Não":
        mask &= df["Is Open Access"].astype(str).str.lower() == "false"

    # Citacoes
    if cit_min > 0:
        mask &= df["Citing Works Count"] >= cit_min

    return df[mask].copy()


# ============================================================
# METRICAS KPI
# ============================================================

def exibir_kpis(df):
    """Exibe metricas KPI no topo da pagina."""
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    total = len(df)
    anos = df["Publication Year"].dropna()
    citacoes = df["Citing Works Count"].sum()
    media_cit = df["Citing Works Count"].mean()
    oa_pct = (df["Is Open Access"].astype(str).str.lower() == "true").sum() / max(total, 1) * 100
    paises = df["Source Country"].dropna().nunique()

    col1.metric("Total de Artigos", f"{total:,}")
    col2.metric("Periodo", f"{int(anos.min())}-{int(anos.max())}" if len(anos) > 0 else "N/A")
    col3.metric("Total de Citações", f"{citacoes:,}")
    col4.metric("Media Citações", f"{media_cit:.1f}")
    col5.metric("Open Access", f"{oa_pct:.1f}%")
    col6.metric("Paises", f"{paises}")


# ============================================================
# ABA 1 — VISAO GERAL
# ============================================================

def aba_visao_geral(df):
    """Graficos de visao geral: temporal, tipos de publicacao, open access."""

    # --- Grafico 1: Scholarly Works Over Time (stacked bar) ---
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

    fig = px.bar(
        contagem, x="Ano", y="Contagem", color="Tipo",
        color_discrete_map=PALETTE_PUB_TYPE,
        labels={"Contagem": "Número de Artigos", "Ano": "Ano de Publicação", "Tipo": "Tipo"},
    )
    fig.update_layout(
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
        plot_bgcolor="white",
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, width="stretch")

    # --- Graficos 2 e 3: Tipos de publicacao + Open Access ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tipos de Publicação")
        contagem_tipo = df["Publication Type"].value_counts().head(8)
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

def aba_fontes_autores(df):
    """Graficos de journals, autores e publishers."""

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

def aba_impacto(df):
    """Graficos de citacoes e impacto."""

    # --- Bubble chart: Top Cited Works Over Time ---
    st.subheader("Artigos Mais Citados ao Longo do Tempo")

    df_bubble = df.dropna(subset=["Date Published"]).copy()
    df_bubble = df_bubble[df_bubble["Citing Works Count"] > 0]

    # Limitar para nao poluir o grafico
    df_bubble_top = df_bubble.nlargest(200, "Citing Works Count")

    df_bubble_top["OA"] = df_bubble_top["Is Open Access"].astype(str).str.lower().apply(
        lambda x: "Open Access" if x == "true" else "Restrito"
    )

    # Criar label de hover
    df_bubble_top["hover"] = (
        df_bubble_top["Title"].str[:80] + "<br>" +
        df_bubble_top["Author/s"].fillna("").str.split(";").str[0] +
        " (" + df_bubble_top["Publication Year"].astype(int).astype(str) + ")" +
        "<br>Citacoes: " + df_bubble_top["Citing Works Count"].astype(str)
    )

    fig = px.scatter(
        df_bubble_top,
        x="Date Published",
        y="Citing Works Count",
        size="Citing Works Count",
        color="OA",
        color_discrete_map={"Open Access": CORES["secondary"], "Restrito": "#A5A5A5"},
        hover_name="hover",
        size_max=40,
        labels={"Date Published": "Data de Publicacao", "Citing Works Count": "Citacoes"},
    )
    fig.update_layout(
        height=500, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, width="stretch")

    # --- Histograma de citacoes + Top 20 ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição de Citações")
        df_cit = df[df["Citing Works Count"] > 0].copy()
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

    with col2:
        st.subheader("Top 20 Artigos Mais Citados")
        df_top = df.nlargest(20, "Citing Works Count")[
            ["Title", "Author/s", "Publication Year", "Citing Works Count", "DOI"]
        ].copy()
        df_top.columns = ["Titulo", "Autores", "Ano", "Citacoes", "DOI"]
        df_top["Autores"] = df_top["Autores"].fillna("").str.split(";").str[0]
        df_top["Titulo"] = df_top["Titulo"].str[:80]
        df_top["Ano"] = df_top["Ano"].fillna(0).astype(int)
        st.dataframe(
            df_top.reset_index(drop=True),
            height=400,
            width="stretch",
        )


# ============================================================
# ABA 4 — CAMPOS DE ESTUDO
# ============================================================

def aba_campos_estudo(df):
    """Treemaps de campos de estudo e keywords."""

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 30 Campos de Estudo (Fields of Study)")
        todos_campos = []
        for campos in df["Fields of Study"].dropna():
            for campo in str(campos).split(";"):
                campo = campo.strip()
                if campo:
                    todos_campos.append(campo)

        contagem = pd.Series(todos_campos).value_counts().head(30).reset_index()
        contagem.columns = ["Campo", "Frequencia"]

        fig = px.treemap(
            contagem,
            path=["Campo"],
            values="Frequencia",
            color="Frequencia",
            color_continuous_scale=["#CAF0F8", "#0077B6", "#03045E"],
        )
        fig.update_layout(height=500)
        fig.update_traces(textinfo="label+value")
        st.plotly_chart(fig, width="stretch")

    with col2:
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

            wc = WordCloud(
                width=800,
                height=500,
                background_color="white",
                colormap="ocean",
                max_words=80,
                prefer_horizontal=0.7,
                min_font_size=10,
                max_font_size=80,
                relative_scaling=0.5,
            ).generate_from_frequencies(freq_kw)

            fig_wc, ax_wc = plt.subplots(figsize=(10, 6))
            ax_wc.imshow(wc, interpolation="bilinear")
            ax_wc.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig_wc)
            plt.close(fig_wc)
        else:
            st.info("Nenhum keyword disponivel com os filtros atuais.")


# ============================================================
# ABA 5 — GEOGRAFIA
# ============================================================

def aba_geografia(df):
    """Mapa e graficos geograficos."""

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

def aba_strings(df):
    """Analise das strings de busca: volume, sobreposicao, coocorrencia."""

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
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sobreposição entre Strings")
        contagem_overlap = df["qtd_strings"].value_counts().sort_index()
        fig_overlap = px.bar(
            x=contagem_overlap.index.astype(str),
            y=contagem_overlap.values,
            color_discrete_sequence=[CORES["primary"]],
            labels={"x": "Aparece em N strings", "y": "Qtd Artigos"},
        )
        fig_overlap.update_layout(height=400, plot_bgcolor="white")
        fig_overlap.update_traces(
            text=[f"{v} ({v/len(df)*100:.1f}%)" for v in contagem_overlap.values],
            textposition="outside",
        )
        st.plotly_chart(fig_overlap, width="stretch")

    with col2:
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
            textfont={"size": 7},
        ))
        fig_heat.update_layout(
            height=500,
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
            "Total Bruto": st.column_config.NumberColumn(width="small"),
        },
    )


# ============================================================
# ABA 7 — ALGORITMOS E ABORDAGENS
# ============================================================

PALETTE_PARADIGMA = {
    "Quantum Annealing": "#0077B6",
    "Gate-Based Variacional": "#00B4D8",
    "Gate-Based Exato": "#48CAE4",
    "QA e Gate-Based": "#023E8A",
    "QML": "#70AD47",
    "QML / Hibrido": "#90E0EF",
    "Revisao": "#A5A5A5",
}

PALETTE_ABORDAGEM = {
    "Hibrida": "#0077B6",
    "Quantica": "#00B4D8",
    "Full e Hibrida": "#48CAE4",
    "Revisao": "#A5A5A5",
    "Variavel": "#FFC000",
}


@st.cache_data
def carregar_algoritmos():
    """Carrega a base compilada de algoritmos e abordagens."""
    caminho = os.path.join(PASTA_PROJETO, "data", "base_algoritmos_abordagens.csv")
    df = pd.read_csv(caminho, dtype=str)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype(int)
    return df


def aba_algoritmos():
    """Aba de exploracao de algoritmos e abordagens do artigo de referencia."""

    df_algo = carregar_algoritmos()

    # --- Filtros especificos desta aba ---
    st.markdown("##### Filtros de Algoritmos")
    fc1, fc2, fc3, fc4 = st.columns(4)

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
        abordagens = sorted(df_algo["abordagem"].dropna().unique())
        abordagem_sel = st.multiselect(
            "Abordagem",
            options=abordagens,
            default=None,
            placeholder="Todas",
            key="algo_abordagem",
        )

    with fc3:
        areas = sorted(df_algo["area_aplicacao"].dropna().unique())
        area_sel = st.multiselect(
            "Area de Aplicação",
            options=areas,
            default=None,
            placeholder="Todas",
            key="algo_area",
        )

    with fc4:
        variantes = sorted(df_algo["variante_tsp"].dropna().unique())
        variante_sel = st.multiselect(
            "Variante do Problema",
            options=variantes,
            default=None,
            placeholder="Todas",
            key="algo_variante",
        )

    # Aplicar filtros
    mask = pd.Series(True, index=df_algo.index)
    if paradigma_sel:
        mask &= df_algo["paradigma"].isin(paradigma_sel)
    if abordagem_sel:
        mask &= df_algo["abordagem"].isin(abordagem_sel)
    if area_sel:
        mask &= df_algo["area_aplicacao"].isin(area_sel)
    if variante_sel:
        mask &= df_algo["variante_tsp"].isin(variante_sel)
    df_f = df_algo[mask].copy()

    # Excluir linhas de plataformas genericas e revisoes para graficos de trabalhos
    df_trabalhos = df_f[~df_f["fonte"].isin(["Taxonomia"])].copy()
    df_todos = df_f.copy()

    st.divider()

    # --- KPIs ---
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Trabalhos", len(df_trabalhos))
    k2.metric("Algoritmos Distintos", df_todos["algoritmo"].nunique())
    k3.metric("Paradigmas", df_todos["paradigma"].nunique())

    # Contar criterios
    todos_criterios = []
    for c in df_todos["criterios"].dropna():
        for item in str(c).split(","):
            item = item.strip()
            if item:
                todos_criterios.append(item)
    k4.metric("Avaliações por Critério", len(todos_criterios))

    hardwares = df_todos["hardware"].dropna()
    hardwares = hardwares[~hardwares.isin(["Revisao", "Nao especificado", "Simulador"])]
    k5.metric("Plataformas HW", hardwares.nunique())

    st.divider()

    # ===============================
    # LINHA 1: Paradigma + Abordagem
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Paradigma Quântico")
        contagem_p = df_trabalhos["paradigma"].value_counts().reset_index()
        contagem_p.columns = ["Paradigma", "Trabalhos"]

        fig_p = px.pie(
            contagem_p, values="Trabalhos", names="Paradigma",
            color="Paradigma", color_discrete_map=PALETTE_PARADIGMA,
            hole=0.4,
        )
        fig_p.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_p.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_p, width="stretch")

    with col2:
        st.subheader("Distribuição por Abordagem")
        contagem_a = df_trabalhos["abordagem"].value_counts().reset_index()
        contagem_a.columns = ["Abordagem", "Trabalhos"]

        fig_a = px.pie(
            contagem_a, values="Trabalhos", names="Abordagem",
            color="Abordagem", color_discrete_map=PALETTE_ABORDAGEM,
            hole=0.4,
        )
        fig_a.update_traces(textposition="inside", textinfo="percent+label+value")
        fig_a.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_a, width="stretch")

    # ===============================
    # LINHA 2: Timeline + Hardware
    # ===============================
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Evolução Temporal dos Trabalhos")
        df_timeline = df_trabalhos.dropna(subset=["ano"]).copy()
        df_timeline["Ano"] = df_timeline["ano"].astype(int)
        contagem_t = df_timeline.groupby(["Ano", "paradigma"]).size().reset_index(name="Trabalhos")

        fig_t = px.bar(
            contagem_t, x="Ano", y="Trabalhos", color="paradigma",
            color_discrete_map=PALETTE_PARADIGMA,
            labels={"paradigma": "Paradigma"},
        )
        fig_t.update_layout(
            barmode="stack", height=400, plot_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig_t.update_xaxes(dtick=1)
        st.plotly_chart(fig_t, width="stretch")

    with col4:
        st.subheader("Plataformas de Hardware / Simulador")
        contagem_hw = df_trabalhos["hardware"].fillna("Nao especificado").value_counts().reset_index()
        contagem_hw.columns = ["Hardware", "Trabalhos"]

        fig_hw = px.bar(
            contagem_hw, x="Trabalhos", y="Hardware",
            orientation="h",
            color_discrete_sequence=[CORES["secondary"]],
        )
        fig_hw.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_hw.update_traces(text=contagem_hw["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_hw, width="stretch")

    # ===============================
    # LINHA 3: Variantes + Escala
    # ===============================
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Variantes do Problema Abordadas")
        contagem_v = df_trabalhos["variante_tsp"].value_counts().reset_index()
        contagem_v.columns = ["Variante", "Trabalhos"]

        fig_v = px.bar(
            contagem_v, x="Trabalhos", y="Variante",
            orientation="h",
            color_discrete_sequence=[CORES["primary"]],
        )
        fig_v.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_v.update_traces(text=contagem_v["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_v, width="stretch")

    with col6:
        st.subheader("Escala Testada (N. de Cidades)")
        contagem_e = df_trabalhos["escala_testada"].fillna("Nao informada").value_counts().reset_index()
        contagem_e.columns = ["Escala", "Trabalhos"]

        fig_e = px.bar(
            contagem_e, x="Trabalhos", y="Escala",
            orientation="h",
            color_discrete_sequence=[CORES["accent"]],
        )
        fig_e.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_e.update_traces(text=contagem_e["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_e, width="stretch")

    # ===============================
    # LINHA 4: Critérios de Seleção
    # ===============================
    st.subheader("Critérios de Seleção por Trabalho")
    st.caption(
        "C1: Híbrida superior ao clássico | "
        "C2: Melhor meta-heurística quântico-clássica | "
        "C3: Formulações avançadas / cenários realistas | "
        "C4: Limitações de hardware (ruído e decoerência) | "
        "C5: Sensibilidade a parâmetros e QUBO"
    )

    # Contagem de criterios
    criterio_list = []
    for _, row in df_trabalhos.iterrows():
        if pd.notna(row["criterios"]) and str(row["criterios"]).strip():
            for c in str(row["criterios"]).split(","):
                c = c.strip()
                if c:
                    criterio_list.append({"Criterio": c, "Autor": row["autores"], "Paradigma": row["paradigma"]})

    col7, col8 = st.columns(2)

    with col7:
        if criterio_list:
            df_crit = pd.DataFrame(criterio_list)
            contagem_c = df_crit["Criterio"].value_counts().reset_index()
            contagem_c.columns = ["Criterio", "Trabalhos"]

            nomes_criterio = {
                "C1": "C1 — Hibrida > Classico",
                "C2": "C2 — Melhor Meta-heuristica",
                "C3": "C3 — Cenarios Realistas",
                "C4": "C4 — Limitacoes HW",
                "C5": "C5 — Sensib. Parametros",
            }
            contagem_c["Label"] = contagem_c["Criterio"].map(nomes_criterio).fillna(contagem_c["Criterio"])

            fig_c = px.bar(
                contagem_c, x="Trabalhos", y="Label",
                orientation="h",
                color_discrete_sequence=[CORES["warning"]],
            )
            fig_c.update_layout(
                height=350, plot_bgcolor="white",
                yaxis=dict(autorange="reversed", title=""),
            )
            fig_c.update_traces(text=contagem_c["Trabalhos"], textposition="outside")
            st.plotly_chart(fig_c, width="stretch")
        else:
            st.info("Nenhum trabalho com critério de seleção atribuído nos filtros atuais.")

    with col8:
        # Heatmap criterio x paradigma
        if criterio_list:
            df_crit_heat = pd.DataFrame(criterio_list)
            heat = df_crit_heat.groupby(["Criterio", "Paradigma"]).size().reset_index(name="Qtd")
            heat_pivot = heat.pivot_table(index="Paradigma", columns="Criterio", values="Qtd", fill_value=0)

            fig_ch = go.Figure(data=go.Heatmap(
                z=heat_pivot.values,
                x=heat_pivot.columns.tolist(),
                y=heat_pivot.index.tolist(),
                colorscale=[[0, "#FFFFFF"], [0.3, "#CAF0F8"], [0.6, "#48CAE4"], [1, "#03045E"]],
                text=heat_pivot.values,
                texttemplate="%{text}",
            ))
            fig_ch.update_layout(height=350, title="Critérios × Paradigma")
            st.plotly_chart(fig_ch, width="stretch")

    # ===============================
    # LINHA 5: Formulação QUBO + Métricas
    # ===============================
    col9, col10 = st.columns(2)

    with col9:
        st.subheader("Formulação Utilizada")
        contagem_form = df_trabalhos["formulacao"].fillna("Nao informada").value_counts().reset_index()
        contagem_form.columns = ["Formulacao", "Trabalhos"]

        fig_form = px.bar(
            contagem_form, x="Trabalhos", y="Formulacao",
            orientation="h",
            color_discrete_sequence=[CORES["dark"]],
        )
        fig_form.update_layout(
            height=400, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
        )
        fig_form.update_traces(text=contagem_form["Trabalhos"], textposition="outside")
        st.plotly_chart(fig_form, width="stretch")

    with col10:
        st.subheader("Métricas de Avaliação Utilizadas")
        todas_metricas = []
        for m in df_trabalhos["metricas_avaliadas"].dropna():
            for item in str(m).split(","):
                item = item.strip()
                if item:
                    todas_metricas.append(item)

        if todas_metricas:
            contagem_m = pd.Series(todas_metricas).value_counts().head(15).reset_index()
            contagem_m.columns = ["Metrica", "Frequencia"]

            fig_m = px.bar(
                contagem_m, x="Frequencia", y="Metrica",
                orientation="h",
                color_discrete_sequence=[CORES["success"]],
            )
            fig_m.update_layout(
                height=400, plot_bgcolor="white",
                yaxis=dict(autorange="reversed"),
            )
            fig_m.update_traces(text=contagem_m["Frequencia"], textposition="outside")
            st.plotly_chart(fig_m, width="stretch")

    # ===============================
    # LINHA 6: Radar de maturidade
    # ===============================
    st.subheader("Radar de Maturidade por Paradigma")
    st.caption("Avaliação qualitativa baseada na análise dos trabalhos catalogados")

    # Calcular metricas de maturidade por paradigma
    paradigmas_radar = df_trabalhos[~df_trabalhos["paradigma"].isin(["Revisao"])]["paradigma"].unique()
    radar_data = []

    for par in paradigmas_radar:
        df_par = df_trabalhos[df_trabalhos["paradigma"] == par]
        n = len(df_par)
        if n == 0:
            continue

        # Dimensoes de maturidade (0-5 escala)
        # 1. Volume de publicacoes
        vol = min(n / 3, 5)  # normalizar: 15+ trabalhos = 5

        # 2. Variedade de problemas
        var = min(df_par["variante_tsp"].nunique() / 2, 5)

        # 3. Uso de hardware real
        hw_real = df_par["hardware"].fillna("").str.contains("D-Wave|IBM Quantum|Amazon", case=False).sum()
        hw_score = min(hw_real / max(n * 0.3, 1) * 5, 5)

        # 4. Cenarios realistas (C3)
        c3 = df_par["criterios"].fillna("").str.contains("C3").sum()
        c3_score = min(c3 / max(n * 0.2, 1) * 5, 5)

        # 5. Escala (instancias maiores)
        escala_media = df_par["escala_testada"].fillna("").str.contains("Media|Variavel").sum()
        escala_score = min(escala_media / max(n * 0.3, 1) * 5, 5)

        radar_data.append({
            "Paradigma": par,
            "Volume": round(vol, 1),
            "Variedade": round(var, 1),
            "Hardware Real": round(hw_score, 1),
            "Cenários Reais": round(c3_score, 1),
            "Escalabilidade": round(escala_score, 1),
        })

    if radar_data:
        dims = ["Volume", "Variedade", "Hardware Real", "Cenários Reais", "Escalabilidade"]

        fig_radar = go.Figure()
        cores_radar = list(PALETTE_PARADIGMA.values())

        for i, row in enumerate(radar_data):
            values = [row[d] for d in dims]
            values.append(values[0])  # fechar o poligono

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=dims + [dims[0]],
                fill="toself",
                name=row["Paradigma"],
                line_color=cores_radar[i % len(cores_radar)],
                opacity=0.6,
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        )
        st.plotly_chart(fig_radar, width="stretch")

    # ===============================
    # LINHA 7: Tabela completa
    # ===============================
    st.subheader("Tabela Detalhada dos Trabalhos")

    colunas_exibir = [
        "autores", "ano", "problema", "variante_tsp", "algoritmo",
        "paradigma", "hardware", "abordagem", "escala_testada",
        "qualidade_solucao", "criterios", "contribuicao",
    ]
    colunas_nomes = {
        "autores": "Autores",
        "ano": "Ano",
        "problema": "Problema",
        "variante_tsp": "Variante",
        "algoritmo": "Algoritmo",
        "paradigma": "Paradigma",
        "hardware": "Hardware",
        "abordagem": "Abordagem",
        "escala_testada": "Escala",
        "qualidade_solucao": "Qualidade",
        "criterios": "Critérios",
        "contribuicao": "Contribuição",
    }

    df_tabela = df_todos[colunas_exibir].copy()
    df_tabela = df_tabela.rename(columns=colunas_nomes)
    df_tabela["Ano"] = df_tabela["Ano"].apply(
        lambda x: str(int(x)) if pd.notna(x) and x != 0 else ""
    )

    st.dataframe(
        df_tabela.reset_index(drop=True),
        height=500,
        width="stretch",
    )


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================

def main():
    # Titulo
    st.title("Análise Bibliométrica — TSP Quântico")
    st.caption(
        "Exploração dos 3.696 artigos únicos identificados na pesquisa bibliográfica | "
        "Mestrado Profissional — SENAI CIMATEC"
    )

    # Carregar dados
    df = carregar_dados()

    # Filtros
    df_filtrado = criar_filtros(df)

    # KPIs
    exibir_kpis(df_filtrado)

    st.divider()

    # Abas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Visão Geral",
        "Fontes e Autores",
        "Impacto e Citações",
        "Campos de Estudo",
        "Geografia",
        "Strings de Busca",
        "Algoritmos e Abordagens",
    ])

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


if __name__ == "__main__":
    main()
