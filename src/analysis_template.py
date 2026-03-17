"""
Template de Análise Bibliométrica — TSP + Computação Quântica
Uso: Preencha o CSV de entrada com os dados dos artigos e rode o script.
Gera tabelas e gráficos para incluir no artigo.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# CONFIGURAÇÃO - Ajuste o caminho do seu CSV de artigos
# ============================================================
INPUT_CSV = "artigos_revisao.csv"
OUTPUT_DIR = "resultados_bibliometria"

# Colunas esperadas no CSV:
# id, autores, ano, titulo, algoritmo, hardware, qubits, num_cidades, abordagem, base_dados

def carregar_dados(caminho_csv):
    """Carrega o CSV com os artigos da revisão."""
    if not os.path.exists(caminho_csv):
        print(f"Arquivo '{caminho_csv}' não encontrado.")
        print("Criando CSV de exemplo...")
        criar_csv_exemplo(caminho_csv)
    
    df = pd.read_csv(caminho_csv)
    print(f"Total de artigos carregados: {len(df)}")
    return df


def criar_csv_exemplo(caminho):
    """Cria um CSV de exemplo para o pesquisador preencher."""
    colunas = [
        "id", "autores", "ano", "titulo", "algoritmo",
        "hardware", "qubits", "num_cidades", "abordagem", "base_dados"
    ]
    exemplo = pd.DataFrame({
        "id": [1, 2, 3],
        "autores": ["Silva et al.", "Wang et al.", "Mueller et al."],
        "ano": [2022, 2023, 2021],
        "titulo": ["Quantum TSP example 1", "Hybrid QAOA for routing", "D-Wave TSP logistics"],
        "algoritmo": ["QAOA", "QAOA + Clássico", "Quantum Annealing"],
        "hardware": ["IBM Quantum", "Simulador", "D-Wave Advantage"],
        "qubits": [16, 20, 5000],
        "num_cidades": [8, 12, 20],
        "abordagem": ["Quântica", "Híbrida", "Quântica"],
        "base_dados": ["Lens.org", "IEEE", "Lens.org"]
    })
    exemplo.to_csv(caminho, index=False)
    print(f"CSV de exemplo criado em '{caminho}'. Preencha com seus dados reais.")


def distribuicao_por_ano(df):
    """Gráfico: distribuição de artigos por ano de publicação."""
    contagem = df["ano"].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    contagem.plot(kind="bar", ax=ax, color="#2E75B6", edgecolor="black")
    ax.set_xlabel("Ano de Publicação", fontsize=12)
    ax.set_ylabel("Número de Artigos", fontsize=12)
    ax.set_title("Distribuição Temporal dos Artigos", fontsize=14)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    
    caminho = os.path.join(OUTPUT_DIR, "distribuicao_por_ano.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"Salvo: {caminho}")


def distribuicao_por_algoritmo(df):
    """Gráfico: frequência de cada algoritmo nos artigos."""
    contagem = df["algoritmo"].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    contagem.plot(kind="barh", ax=ax, color="#4472C4", edgecolor="black")
    ax.set_xlabel("Número de Artigos", fontsize=12)
    ax.set_ylabel("Algoritmo", fontsize=12)
    ax.set_title("Algoritmos Mais Utilizados para TSP Quântico", fontsize=14)
    plt.tight_layout()
    
    caminho = os.path.join(OUTPUT_DIR, "distribuicao_por_algoritmo.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"Salvo: {caminho}")


def distribuicao_por_hardware(df):
    """Gráfico: hardware/simuladores utilizados."""
    contagem = df["hardware"].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    contagem.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
    ax.set_ylabel("")
    ax.set_title("Hardware e Simuladores Quânticos Utilizados", fontsize=14)
    plt.tight_layout()
    
    caminho = os.path.join(OUTPUT_DIR, "distribuicao_por_hardware.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"Salvo: {caminho}")


def distribuicao_por_abordagem(df):
    """Gráfico: quântica vs híbrida vs clássica."""
    contagem = df["abordagem"].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    cores = {"Quântica": "#2E75B6", "Híbrida": "#ED7D31", "Clássica": "#70AD47"}
    contagem.plot(kind="bar", ax=ax, color=[cores.get(x, "#999999") for x in contagem.index])
    ax.set_xlabel("Abordagem", fontsize=12)
    ax.set_ylabel("Número de Artigos", fontsize=12)
    ax.set_title("Distribuição por Tipo de Abordagem", fontsize=14)
    plt.tight_layout()
    
    caminho = os.path.join(OUTPUT_DIR, "distribuicao_por_abordagem.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"Salvo: {caminho}")


def tabela_resumo(df):
    """Gera tabela-resumo em formato CSV e Markdown."""
    # CSV
    caminho_csv = os.path.join(OUTPUT_DIR, "tabela_resumo.csv")
    df.to_csv(caminho_csv, index=False)
    print(f"Salvo: {caminho_csv}")
    
    # Markdown
    caminho_md = os.path.join(OUTPUT_DIR, "tabela_resumo.md")
    with open(caminho_md, "w") as f:
        f.write("# Tabela-Resumo da Revisão Bibliográfica\n\n")
        f.write(df.to_markdown(index=False))
    print(f"Salvo: {caminho_md}")


def estatisticas_gerais(df):
    """Imprime estatísticas gerais da revisão."""
    print("\n" + "=" * 50)
    print("ESTATÍSTICAS GERAIS DA REVISÃO")
    print("=" * 50)
    print(f"Total de artigos: {len(df)}")
    print(f"Período: {df['ano'].min()} - {df['ano'].max()}")
    print(f"Algoritmos distintos: {df['algoritmo'].nunique()}")
    print(f"Hardware distintos: {df['hardware'].nunique()}")
    print(f"Bases de dados: {df['base_dados'].nunique()}")
    
    if "qubits" in df.columns:
        print(f"Qubits (min-max): {df['qubits'].min()} - {df['qubits'].max()}")
    if "num_cidades" in df.columns:
        print(f"Cidades TSP (min-max): {df['num_cidades'].min()} - {df['num_cidades'].max()}")
    print("=" * 50)


def main():
    """Executa toda a análise bibliométrica."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    df = carregar_dados(INPUT_CSV)
    
    estatisticas_gerais(df)
    distribuicao_por_ano(df)
    distribuicao_por_algoritmo(df)
    distribuicao_por_hardware(df)
    distribuicao_por_abordagem(df)
    tabela_resumo(df)
    
    print(f"\nTodos os resultados salvos em '{OUTPUT_DIR}/'")
    print("Use esses gráficos e tabelas no artigo.")


if __name__ == "__main__":
    main()
