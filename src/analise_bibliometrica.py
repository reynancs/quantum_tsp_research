"""
Analise Bibliometrica — Fase 1 (Exploracao Bibliografica)

Gera graficos e estatisticas a partir dos dados exportados do Lens.org
apos a deduplicacao.

Como usar:
    python src/analise_bibliometrica.py

Entrada: data/artigos_unicos.csv (gerado pelo script de deduplicacao)
Saida:   data/resultados_bibliometria/ (graficos PNG + resumos CSV)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Gerar graficos sem abrir janela

# ============================================================
# CONFIGURACAO
# ============================================================

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_ENTRADA = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "data", "resultados_bibliometria")

# Cores padrao para os graficos
COR_PRINCIPAL = "#2E75B6"
COR_DESTAQUE = "#ED7D31"
COR_VERDE = "#70AD47"
CORES_CATEGORIAS = ["#2E75B6", "#ED7D31", "#70AD47", "#FFC000", "#5B9BD5", "#A5A5A5"]

# Mapeamento das strings de busca
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
    11: "Route Opt. + Quantum + Logistics",
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

PRIORIDADES = {
    1: "Alta", 2: "Alta", 3: "Alta", 4: "Alta", 5: "Alta",
    6: "Alta", 17: "Alta", 18: "Alta",
    7: "Media", 8: "Media", 9: "Media", 10: "Media", 11: "Media",
    12: "Media", 19: "Media", 20: "Media", 21: "Media", 22: "Media",
    13: "Baixa", 14: "Baixa", 15: "Baixa", 16: "Baixa",
    23: "Baixa", 24: "Baixa", 25: "Baixa", 26: "Baixa",
}


# ============================================================
# FUNCOES DE GRAFICOS
# ============================================================

def grafico_distribuicao_temporal(df):
    """
    Grafico 1: Distribuicao de artigos por ano de publicacao.
    Mostra o crescimento do campo ao longo do tempo.
    """
    contagem = df["Publication Year"].dropna().astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(contagem.index.astype(str), contagem.values,
                  color=COR_PRINCIPAL, edgecolor="white", linewidth=0.5)

    # Destacar ultimos 5 anos
    for i, (ano, _) in enumerate(contagem.items()):
        if ano >= 2020:
            bars[i].set_color(COR_DESTAQUE)

    ax.set_xlabel("Ano de Publicacao", fontsize=11)
    ax.set_ylabel("Numero de Artigos", fontsize=11)
    ax.set_title("Distribuicao Temporal dos Artigos (Azul: antes de 2020 | Laranja: 2020+)",
                 fontsize=12, fontweight="bold")
    ax.tick_params(axis="x", rotation=45)

    # Adicionar total no canto
    total = contagem.sum()
    recentes = contagem[contagem.index >= 2020].sum() if any(contagem.index >= 2020) else 0
    ax.text(0.98, 0.95, f"Total: {total}\n2020+: {recentes} ({recentes/total*100:.0f}%)",
            transform=ax.transAxes, ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "01_distribuicao_temporal.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_tipo_publicacao(df):
    """
    Grafico 2: Tipos de publicacao (journal article, conference, preprint, etc.)
    """
    contagem = df["Publication Type"].fillna("Nao informado").value_counts().head(8)

    fig, ax = plt.subplots(figsize=(10, 5))
    contagem.plot(kind="barh", ax=ax, color=COR_PRINCIPAL, edgecolor="white")
    ax.set_xlabel("Numero de Artigos", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Tipos de Publicacao", fontsize=12, fontweight="bold")

    # Adicionar valores nas barras
    for i, v in enumerate(contagem.values):
        ax.text(v + 5, i, f"{v} ({v/len(df)*100:.1f}%)", va="center", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "02_tipo_publicacao.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_top_fontes(df):
    """
    Grafico 3: Top 15 journals/conferencias que mais publicam sobre o tema.
    """
    contagem = df["Source Title"].fillna("Nao informado").value_counts().head(15)

    fig, ax = plt.subplots(figsize=(12, 6))
    contagem.plot(kind="barh", ax=ax, color=COR_PRINCIPAL, edgecolor="white")
    ax.set_xlabel("Numero de Artigos", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Top 15 Fontes de Publicacao (Journals/Conferencias)", fontsize=12, fontweight="bold")
    ax.invert_yaxis()

    for i, v in enumerate(contagem.values):
        ax.text(v + 0.5, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "03_top_fontes.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_open_access(df):
    """
    Grafico 4: Proporcao de artigos em Open Access.
    """
    # Open Access sim/nao
    oa = df["Is Open Access"].fillna("False").astype(str).str.lower()
    oa_counts = oa.value_counts()
    labels = ["Open Access" if "true" in k else "Acesso Restrito" for k in oa_counts.index]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Pie chart
    cores_oa = [COR_VERDE, COR_PRINCIPAL]
    ax1.pie(oa_counts.values, labels=labels, autopct="%1.1f%%",
            colors=cores_oa, startangle=90)
    ax1.set_title("Open Access vs Restrito", fontsize=12, fontweight="bold")

    # Open Access por cor (gold, green, bronze, hybrid)
    oa_cor = df[oa == "true"]["Open Access Colour"].fillna("nao informado").value_counts()
    if len(oa_cor) > 0:
        cores_mapa = {"gold": "#FFC000", "green": "#70AD47", "bronze": "#C65911",
                      "hybrid": "#5B9BD5", "nao informado": "#A5A5A5"}
        cores_barras = [cores_mapa.get(c, "#A5A5A5") for c in oa_cor.index]
        oa_cor.plot(kind="bar", ax=ax2, color=cores_barras, edgecolor="white")
        ax2.set_title("Tipos de Open Access", fontsize=12, fontweight="bold")
        ax2.set_xlabel("")
        ax2.set_ylabel("Numero de Artigos", fontsize=11)
        ax2.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "04_open_access.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_volume_por_string(df):
    """
    Grafico 5: Volume de artigos unicos por string de busca.
    Mostra quais strings capturaram mais artigos.
    """
    # Contar artigos por string (um artigo pode pertencer a varias strings)
    contagem = {}
    for _, row in df.iterrows():
        strings = str(row.get("strings_origem", "")).split("; ")
        for s in strings:
            s = s.strip()
            if s and s != "nan":
                try:
                    num = int(float(s))
                    contagem[num] = contagem.get(num, 0) + 1
                except ValueError:
                    pass

    # Ordenar por numero da string
    nums = sorted(contagem.keys())
    valores = [contagem[n] for n in nums]
    labels = [f"#{n}" for n in nums]

    # Cores por prioridade
    cores = []
    for n in nums:
        prio = PRIORIDADES.get(n, "Baixa")
        if prio == "Alta":
            cores.append(COR_DESTAQUE)
        elif prio == "Media":
            cores.append(COR_PRINCIPAL)
        else:
            cores.append("#A5A5A5")

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(labels, valores, color=cores, edgecolor="white", linewidth=0.5)

    ax.set_xlabel("String de Busca", fontsize=11)
    ax.set_ylabel("Artigos Unicos", fontsize=11)
    ax.set_title("Volume de Artigos por String de Busca (Laranja=Alta | Azul=Media | Cinza=Baixa)",
                 fontsize=12, fontweight="bold")
    ax.tick_params(axis="x", rotation=45)

    # Valores acima das barras
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(val), ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "05_volume_por_string.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_sobreposicao(df):
    """
    Grafico 6: Distribuicao de sobreposicao — em quantas strings cada artigo aparece.
    """
    contagem = df["qtd_strings"].fillna(1).astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    contagem.plot(kind="bar", ax=ax, color=COR_PRINCIPAL, edgecolor="white")
    ax.set_xlabel("Numero de Strings em que o Artigo Aparece", fontsize=11)
    ax.set_ylabel("Quantidade de Artigos", fontsize=11)
    ax.set_title("Sobreposicao entre Strings de Busca", fontsize=12, fontweight="bold")
    ax.tick_params(axis="x", rotation=0)

    # Adicionar valores
    for i, (idx, val) in enumerate(contagem.items()):
        ax.text(i, val + 5, f"{val}\n({val/len(df)*100:.1f}%)",
                ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "06_sobreposicao.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_top_citados(df):
    """
    Grafico 7: Top 20 artigos mais citados.
    """
    if "Citing Works Count" not in df.columns:
        print("  [AVISO] Coluna 'Citing Works Count' nao encontrada. Pulando grafico.")
        return

    df_cite = df.copy()
    df_cite["Citing Works Count"] = pd.to_numeric(df_cite["Citing Works Count"], errors="coerce")
    df_cite = df_cite.dropna(subset=["Citing Works Count"])
    df_cite = df_cite.nlargest(20, "Citing Works Count")

    # Criar label curto: "Primeiro Autor (Ano)"
    labels = []
    for _, row in df_cite.iterrows():
        autores = str(row.get("Author/s", ""))
        primeiro = autores.split(";")[0].split(",")[0].strip()[:25]
        ano = str(row.get("Publication Year", ""))[:4]
        labels.append(f"{primeiro} ({ano})")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(range(len(df_cite)), df_cite["Citing Works Count"].values,
            color=COR_PRINCIPAL, edgecolor="white")
    ax.set_yticks(range(len(df_cite)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Numero de Citacoes", fontsize=11)
    ax.set_title("Top 20 Artigos Mais Citados", fontsize=12, fontweight="bold")
    ax.invert_yaxis()

    for i, v in enumerate(df_cite["Citing Works Count"].values):
        ax.text(v + 1, i, str(int(v)), va="center", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "07_top_citados.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_campos_estudo(df):
    """
    Grafico 8: Top 20 campos de estudo (Fields of Study) mais frequentes.
    """
    if "Fields of Study" not in df.columns:
        print("  [AVISO] Coluna 'Fields of Study' nao encontrada. Pulando grafico.")
        return

    # Cada artigo pode ter varios campos separados por ;
    todos_campos = []
    for campos in df["Fields of Study"].dropna():
        for campo in str(campos).split(";"):
            campo = campo.strip()
            if campo:
                todos_campos.append(campo)

    contagem = pd.Series(todos_campos).value_counts().head(20)

    fig, ax = plt.subplots(figsize=(12, 7))
    contagem.plot(kind="barh", ax=ax, color=COR_PRINCIPAL, edgecolor="white")
    ax.set_xlabel("Frequencia nos Artigos", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Top 20 Campos de Estudo (Fields of Study)", fontsize=12, fontweight="bold")
    ax.invert_yaxis()

    for i, v in enumerate(contagem.values):
        ax.text(v + 1, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "08_campos_estudo.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


def grafico_paises(df):
    """
    Grafico 9: Top 15 paises de origem das publicacoes.
    """
    if "Source Country" not in df.columns:
        print("  [AVISO] Coluna 'Source Country' nao encontrada. Pulando grafico.")
        return

    contagem = df["Source Country"].fillna("Nao informado").value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    contagem.plot(kind="barh", ax=ax, color=COR_PRINCIPAL, edgecolor="white")
    ax.set_xlabel("Numero de Artigos", fontsize=11)
    ax.set_ylabel("")
    ax.set_title("Top 15 Paises de Origem das Publicacoes", fontsize=12, fontweight="bold")
    ax.invert_yaxis()

    for i, v in enumerate(contagem.values):
        ax.text(v + 0.5, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "09_paises.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  Salvo: {caminho}")


# ============================================================
# RESUMO ESTATISTICO
# ============================================================

def gerar_resumo_estatistico(df):
    """
    Gera um resumo estatistico completo em texto e CSV.
    """
    df_cite = pd.to_numeric(df.get("Citing Works Count", pd.Series()), errors="coerce")
    anos = df["Publication Year"].dropna().astype(int)

    resumo = {
        "Total de artigos unicos": len(df),
        "Periodo coberto": f"{anos.min()} - {anos.max()}" if len(anos) > 0 else "N/A",
        "Ano com mais publicacoes": int(anos.value_counts().idxmax()) if len(anos) > 0 else "N/A",
        "Artigos a partir de 2020": int((anos >= 2020).sum()) if len(anos) > 0 else 0,
        "Percentual 2020+": f"{(anos >= 2020).sum() / len(anos) * 100:.1f}%" if len(anos) > 0 else "N/A",
        "Tipos de publicacao distintos": df["Publication Type"].nunique(),
        "Fontes (journals/conf) distintas": df["Source Title"].nunique(),
        "Paises distintos": df["Source Country"].nunique(),
        "Total de citacoes": int(df_cite.sum()) if len(df_cite) > 0 else 0,
        "Media de citacoes por artigo": f"{df_cite.mean():.1f}" if len(df_cite) > 0 else "N/A",
        "Artigo mais citado (citacoes)": int(df_cite.max()) if len(df_cite) > 0 else "N/A",
        "Artigos Open Access": int(df["Is Open Access"].astype(str).str.lower().eq("true").sum()),
        "Percentual Open Access": f"{df['Is Open Access'].astype(str).str.lower().eq('true').sum() / len(df) * 100:.1f}%",
    }

    # Imprimir
    print("\n" + "=" * 60)
    print("  RESUMO ESTATISTICO DA BASE BIBLIOGRAFICA")
    print("=" * 60)
    for chave, valor in resumo.items():
        print(f"  {chave:40s}  {valor}")
    print("=" * 60)

    # Salvar como CSV
    caminho = os.path.join(PASTA_SAIDA, "resumo_estatistico.csv")
    pd.DataFrame([resumo]).T.reset_index().rename(
        columns={"index": "Metrica", 0: "Valor"}
    ).to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"\n  Resumo salvo em: {caminho}")


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================

def main():
    print("=" * 60)
    print("  ANALISE BIBLIOMETRICA — Fase 1")
    print("=" * 60)

    # Verificar arquivo de entrada
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"\n[ERRO] Arquivo nao encontrado: {ARQUIVO_ENTRADA}")
        print("       Rode primeiro o script de deduplicacao (deduplicar_artigos.py)")
        return

    # Criar pasta de saida
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Carregar dados
    print(f"\nCarregando dados de: {ARQUIVO_ENTRADA}")
    df = pd.read_csv(ARQUIVO_ENTRADA, dtype=str)
    print(f"Total de artigos: {len(df)}")

    # Converter colunas numericas
    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce")
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce")

    # Gerar graficos
    print("\nGerando graficos...")
    grafico_distribuicao_temporal(df)
    grafico_tipo_publicacao(df)
    grafico_top_fontes(df)
    grafico_open_access(df)
    grafico_volume_por_string(df)
    grafico_sobreposicao(df)
    grafico_top_citados(df)
    grafico_campos_estudo(df)
    grafico_paises(df)

    # Resumo estatistico
    gerar_resumo_estatistico(df)

    print(f"\nTodos os graficos salvos em: {PASTA_SAIDA}/")
    print("Processo concluido com sucesso!")


if __name__ == "__main__":
    main()
