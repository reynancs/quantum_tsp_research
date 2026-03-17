"""
Script de Deduplicacao de Artigos — Fase 1 (Exploracao Bibliografica)

Este script faz o seguinte:
1. Le todos os arquivos CSV exportados do Lens.org (pasta dados/exportacoes_lens/)
2. Junta tudo em uma tabela unica
3. Remove artigos duplicados (mesmo artigo que apareceu em varias buscas)
4. Gera estatisticas e exporta o resultado limpo

Como usar:
    python src/deduplicar_artigos.py

Antes de rodar:
    - Exporte os resultados de cada string do Lens.org como CSV
    - Salve os arquivos na pasta dados/exportacoes_lens/
    - Nomeie como: string_01.csv, string_02.csv, ..., string_26.csv
"""

import os
import glob
import pandas as pd
import re
from datetime import datetime


# ============================================================
# CONFIGURACAO — Caminhos dos arquivos
# ============================================================

# Pasta raiz do projeto (um nivel acima de src/)
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta onde estao os CSVs exportados do Lens.org
PASTA_CSV = os.path.join(PASTA_PROJETO, "data", "exportacoes_lens")

# Pasta onde os resultados serao salvos
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "data")

# Mapeamento: numero da string -> descricao da busca
# (para facilitar a leitura dos resultados)
STRINGS_BUSCA = {
    1:  '"Traveling Salesman Problem" AND "Quantum Computing"',
    2:  '"Traveling Salesman" AND "Quantum Algorithms"',
    3:  '"TSP" AND "Quantum Annealing"',
    4:  '"Traveling Salesman" AND "QAOA"',
    5:  '"TSP" AND "Hybrid Quantum"',
    6:  '"Vehicle Routing" AND "Quantum Computing"',
    7:  '"Combinatorial Optimization" AND "Quantum Annealing"',
    8:  '"TSP" AND "VQE"',
    9:  '"Traveling Salesman" AND "Grover"',
    10: '"QUBO" AND "Traveling Salesman"',
    11: '"Route Optimization" AND "Quantum" AND "Logistics"',
    12: '"TSP" AND "D-Wave"',
    13: '"TSP" AND "IBM Quantum"',
    14: '"Traveling Salesman" AND "Ising Model"',
    15: '"Vehicle Routing" AND "Quantum Annealing" AND "Logistics"',
    16: '"Hamiltonian Cycle" AND "Quantum"',
    17: '"Vehicle Routing Problem" AND "QAOA"',
    18: '"Quantum Computing" AND "Supply Chain Management"',
    19: '"Traveling Salesman" AND "Quantum-Inspired"',
    20: '"Quantum Reinforcement Learning" AND "Routing"',
    21: '"CVRP" AND "Quantum Annealing"',
    22: '"Job Shop Scheduling" AND "Quantum"',
    23: '"Bin Packing" AND "Quantum"',
    24: '"Facility Location" AND "Quantum Computing"',
    25: '"Knapsack Problem" AND "Quantum"',
    26: '"Quantum Machine Learning" AND "Supply Chain"',
}


# ============================================================
# FUNCOES
# ============================================================

def extrair_numero_string(nome_arquivo):
    """
    Extrai o numero da string a partir do nome do arquivo.
    Exemplo: 'string_01.csv' -> 1, 'string_14.csv' -> 14
    Tambem aceita: '01.csv', 'busca_01.csv', etc.
    """
    # Procura por numeros no nome do arquivo
    numeros = re.findall(r'(\d+)', os.path.basename(nome_arquivo))
    if numeros:
        return int(numeros[0])
    return None


def carregar_csvs(pasta):
    """
    Le todos os arquivos CSV de uma pasta e junta em um unico DataFrame.
    Adiciona uma coluna 'string_numero' indicando de qual busca veio cada artigo.
    """
    # Encontrar todos os CSVs na pasta
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.csv")))

    if not arquivos:
        print(f"\n[ERRO] Nenhum arquivo CSV encontrado em: {pasta}")
        print(f"       Certifique-se de exportar os CSVs do Lens.org para esta pasta.")
        return None

    print(f"\nEncontrados {len(arquivos)} arquivo(s) CSV:")
    print("-" * 50)

    tabelas = []

    for arquivo in arquivos:
        # Extrair o numero da string do nome do arquivo
        numero = extrair_numero_string(arquivo)
        nome = os.path.basename(arquivo)

        try:
            # Ler o CSV (Lens.org usa virgula como separador)
            df = pd.read_csv(arquivo, dtype=str)
            df["string_numero"] = numero
            df["arquivo_origem"] = nome

            descricao = STRINGS_BUSCA.get(numero, "descricao nao mapeada")
            print(f"  {nome:30s} -> {len(df):5d} artigos  (String #{numero}: {descricao})")

            tabelas.append(df)
        except Exception as e:
            print(f"  {nome:30s} -> ERRO ao ler: {e}")

    if not tabelas:
        print("\n[ERRO] Nenhum CSV foi carregado com sucesso.")
        return None

    # Juntar todas as tabelas em uma so
    df_completo = pd.concat(tabelas, ignore_index=True)
    print("-" * 50)
    print(f"  TOTAL BRUTO: {len(df_completo)} artigos")

    return df_completo


def identificar_coluna_doi(df):
    """
    Identifica o nome da coluna de DOI no DataFrame.
    O Lens.org pode usar 'DOI', 'doi', 'Digital Object Identifier', etc.
    """
    possiveis = ["DOI", "doi", "Digital Object Identifier", "Lens ID"]
    for col in possiveis:
        if col in df.columns:
            return col

    # Procurar por coluna que contenha 'doi' no nome (case insensitive)
    for col in df.columns:
        if "doi" in col.lower():
            return col

    return None


def identificar_coluna_titulo(df):
    """
    Identifica o nome da coluna de titulo no DataFrame.
    """
    possiveis = ["Title", "title", "Document Title", "Article Title"]
    for col in possiveis:
        if col in df.columns:
            return col

    for col in df.columns:
        if "title" in col.lower():
            return col

    return None


def deduplicar(df):
    """
    Remove artigos duplicados em duas etapas:
    1. Primeiro, deduplica por DOI (identificador unico mais confiavel)
    2. Depois, para artigos sem DOI, deduplica por titulo normalizado

    Retorna o DataFrame limpo e estatisticas.
    """
    total_bruto = len(df)

    # Identificar colunas
    col_doi = identificar_coluna_doi(df)
    col_titulo = identificar_coluna_titulo(df)

    print(f"\n--- Deduplicacao ---")
    print(f"Coluna de DOI encontrada: '{col_doi}'")
    print(f"Coluna de titulo encontrada: '{col_titulo}'")

    if col_doi is None and col_titulo is None:
        print("[ERRO] Nao foi possivel encontrar colunas de DOI ou titulo.")
        print(f"       Colunas disponiveis: {list(df.columns)}")
        return df, {}

    # Registrar de quais strings cada artigo veio (antes de deduplicar)
    if col_doi:
        # Agrupar strings por DOI
        strings_por_doi = (
            df[df[col_doi].notna() & (df[col_doi] != "")]
            .groupby(col_doi)["string_numero"]
            .apply(lambda x: sorted(set(x.dropna().astype(int))))
            .to_dict()
        )

    # --- Etapa 1: Separar artigos COM e SEM DOI ---
    if col_doi:
        tem_doi = df[col_doi].notna() & (df[col_doi].str.strip() != "")
        df_com_doi = df[tem_doi].copy()
        df_sem_doi = df[~tem_doi].copy()
        print(f"\nArtigos com DOI: {len(df_com_doi)}")
        print(f"Artigos sem DOI: {len(df_sem_doi)}")
    else:
        df_com_doi = pd.DataFrame()
        df_sem_doi = df.copy()
        print(f"\nSem coluna DOI — todos os {len(df)} artigos serao deduplicados por titulo")

    # --- Etapa 2: Deduplicar por DOI ---
    if len(df_com_doi) > 0:
        antes_doi = len(df_com_doi)
        df_com_doi = df_com_doi.drop_duplicates(subset=[col_doi], keep="first")
        removidos_doi = antes_doi - len(df_com_doi)
        print(f"\nDeduplicacao por DOI: {antes_doi} -> {len(df_com_doi)} ({removidos_doi} duplicatas removidas)")

        # Adicionar coluna com todas as strings de origem
        df_com_doi["strings_origem"] = df_com_doi[col_doi].map(
            lambda doi: strings_por_doi.get(doi, [])
        )
        df_com_doi["qtd_strings"] = df_com_doi["strings_origem"].apply(len)
    else:
        removidos_doi = 0

    # --- Etapa 3: Deduplicar sem DOI por titulo ---
    removidos_titulo = 0
    if len(df_sem_doi) > 0 and col_titulo:
        antes_titulo = len(df_sem_doi)
        # Normalizar titulo: minusculas, sem espacos extras
        df_sem_doi["titulo_normalizado"] = (
            df_sem_doi[col_titulo]
            .fillna("")
            .str.lower()
            .str.strip()
            .str.replace(r'\s+', ' ', regex=True)
        )
        df_sem_doi = df_sem_doi.drop_duplicates(subset=["titulo_normalizado"], keep="first")
        df_sem_doi = df_sem_doi.drop(columns=["titulo_normalizado"])
        removidos_titulo = antes_titulo - len(df_sem_doi)
        print(f"Deduplicacao por titulo (sem DOI): {antes_titulo} -> {len(df_sem_doi)} ({removidos_titulo} duplicatas removidas)")

        # Para artigos sem DOI, strings_origem fica so com a propria
        if "strings_origem" not in df_sem_doi.columns:
            df_sem_doi["strings_origem"] = df_sem_doi["string_numero"].apply(
                lambda x: [int(x)] if pd.notna(x) else []
            )
            df_sem_doi["qtd_strings"] = 1

    # --- Etapa 4: Juntar resultado final ---
    if len(df_com_doi) > 0 and len(df_sem_doi) > 0:
        df_final = pd.concat([df_com_doi, df_sem_doi], ignore_index=True)
    elif len(df_com_doi) > 0:
        df_final = df_com_doi
    else:
        df_final = df_sem_doi

    total_unico = len(df_final)
    total_removido = total_bruto - total_unico
    taxa_sobreposicao = (total_removido / total_bruto * 100) if total_bruto > 0 else 0

    # Estatisticas
    stats = {
        "total_bruto": total_bruto,
        "total_unico": total_unico,
        "total_removido": total_removido,
        "removidos_por_doi": removidos_doi,
        "removidos_por_titulo": removidos_titulo,
        "taxa_sobreposicao_pct": round(taxa_sobreposicao, 1),
        "artigos_com_doi": len(df_com_doi) if len(df_com_doi) > 0 else 0,
        "artigos_sem_doi": len(df_sem_doi) if len(df_sem_doi) > 0 else 0,
    }

    return df_final, stats


def gerar_resumo_por_string(df):
    """
    Gera um resumo mostrando quantos artigos unicos vieram de cada string.
    """
    resumo = []
    for numero, descricao in sorted(STRINGS_BUSCA.items()):
        # Contar artigos que tem este numero nas strings_origem
        if "strings_origem" in df.columns:
            count = df["strings_origem"].apply(lambda x: numero in x if isinstance(x, list) else False).sum()
        else:
            count = len(df[df["string_numero"] == numero])
        resumo.append({
            "string_numero": numero,
            "descricao": descricao,
            "artigos_unicos": count,
        })
    return pd.DataFrame(resumo)


def salvar_resultados(df_final, stats, resumo_strings, pasta_saida):
    """
    Salva os resultados em arquivos CSV.
    """
    # 1. Artigos unicos
    arquivo_artigos = os.path.join(pasta_saida, "artigos_unicos.csv")
    # Converter listas para string antes de salvar
    df_salvar = df_final.copy()
    if "strings_origem" in df_salvar.columns:
        df_salvar["strings_origem"] = df_salvar["strings_origem"].apply(
            lambda x: "; ".join(map(str, x)) if isinstance(x, list) else str(x)
        )
    df_salvar.to_csv(arquivo_artigos, index=False, encoding="utf-8-sig")
    print(f"\nArtigos unicos salvos em: {arquivo_artigos}")

    # 2. Resumo estatistico
    arquivo_resumo = os.path.join(pasta_saida, "resumo_deduplicacao.csv")
    df_stats = pd.DataFrame([stats])
    df_stats.to_csv(arquivo_resumo, index=False, encoding="utf-8-sig")
    print(f"Resumo estatistico salvo em: {arquivo_resumo}")

    # 3. Resumo por string
    arquivo_strings = os.path.join(pasta_saida, "resumo_por_string.csv")
    resumo_strings.to_csv(arquivo_strings, index=False, encoding="utf-8-sig")
    print(f"Resumo por string salvo em: {arquivo_strings}")


def imprimir_resultado_final(stats, resumo_strings):
    """
    Imprime um resumo bonito no terminal.
    """
    print("\n" + "=" * 60)
    print("  RESULTADO FINAL DA DEDUPLICACAO")
    print("=" * 60)
    print(f"  Total bruto (com duplicatas):  {stats['total_bruto']:>6}")
    print(f"  Total unico (sem duplicatas):  {stats['total_unico']:>6}")
    print(f"  Duplicatas removidas:          {stats['total_removido']:>6}")
    print(f"    - por DOI:                   {stats['removidos_por_doi']:>6}")
    print(f"    - por titulo (sem DOI):      {stats['removidos_por_titulo']:>6}")
    print(f"  Taxa de sobreposicao:          {stats['taxa_sobreposicao_pct']:>5}%")
    print(f"  Artigos com DOI:               {stats['artigos_com_doi']:>6}")
    print(f"  Artigos sem DOI:               {stats['artigos_sem_doi']:>6}")
    print("=" * 60)

    print(f"\n  Distribuicao por string de busca:")
    print(f"  {'#':>3}  {'Artigos':>8}  Descricao")
    print(f"  {'-'*3}  {'-'*8}  {'-'*40}")
    for _, row in resumo_strings.iterrows():
        print(f"  {int(row['string_numero']):>3}  {int(row['artigos_unicos']):>8}  {row['descricao'][:50]}")
    print()


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================

def main():
    print("=" * 60)
    print("  DEDUPLICACAO DE ARTIGOS — Fase 1")
    print(f"  Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    # Verificar se a pasta existe
    if not os.path.exists(PASTA_CSV):
        print(f"\n[ERRO] Pasta nao encontrada: {PASTA_CSV}")
        print(f"       Crie a pasta e coloque os CSVs do Lens.org nela.")
        return

    # 1. Carregar todos os CSVs
    df = carregar_csvs(PASTA_CSV)
    if df is None:
        return

    # 2. Mostrar colunas disponiveis (util para debug)
    print(f"\nColunas encontradas nos CSVs ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  {i+1:2}. {col}")

    # 3. Deduplicar
    df_final, stats = deduplicar(df)

    # 4. Gerar resumo por string
    resumo_strings = gerar_resumo_por_string(df_final)

    # 5. Salvar resultados
    salvar_resultados(df_final, stats, resumo_strings, PASTA_SAIDA)

    # 6. Imprimir resultado final
    imprimir_resultado_final(stats, resumo_strings)

    print("Processo concluido com sucesso!")
    print(f"Proximo passo: abrir 'dados/artigos_unicos.csv' para revisar os artigos.\n")


if __name__ == "__main__":
    main()
