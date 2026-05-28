# -*- coding: utf-8 -*-
"""
Adiciona a coluna `categoria_algoritmo` em data/base_algoritmos_abordagens.csv.

Mapeia os 12 valores unicos de `algoritmo_quantico` para uma das 6 categorias
principais listadas em artefatos/resumo_algoritmos.md (Seções 1.1 a 1.6),
adaptadas ao subconjunto de algoritmos efetivamente presentes nos 129
trabalhos catalogados a partir de Phillipson (2025).

Distribuicao esperada apos a classificacao:
  Quantum Annealing            68 (52.7%) — QA, CQM
  Variacional (Gate-Based)     36 (27.9%) — QAOA, VQE, F-VQE, QAOA/VQE
  Exato (Gate-Based)           11 ( 8.5%) — Grover, QPE
  Aprendizado Quântico (QML)   11 ( 8.5%) — QML, QACO, RL, HHL/VQE
  Não especificado              3 ( 2.3%) — "Não especificado"
  ----------------------------------------
  Total                       129

Observacao sobre as 6 categorias do resumo_algoritmos.md:
  - 1.1 QA, 1.2 Variacionais, 1.3 Exatos, 1.5 QML mapeiam diretamente.
  - 1.4 "Abordagens Hibridas" e 1.6 "Classicos (baseline)" nao se aplicam
    como CATEGORIAS DE ALGORITMO porque (a) hibridismo e uma DIMENSAO ja
    capturada na coluna `abordagem` (Hybrid/Full Quantum) e (b) nenhum dos
    129 trabalhos tem algoritmo classico como tecnica primaria — todos sao
    quanticos por construcao.

Execucao:
    python scripts/classificar_categoria_algoritmo.py

Idempotente: ao rodar de novo, sobrescreve a coluna existente com o mesmo
mapeamento — nao duplica nem corrompe o CSV.
"""
import os
import sys

import pandas as pd


# Forcar UTF-8 no stdout (Windows cp1252 workaround)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_CSV = os.path.join(ROOT, "data", "base_algoritmos_abordagens.csv")


# ============================================================
# MAPEAMENTO ALGORITMO -> CATEGORIA
# ============================================================
# Chaves devem casar EXATAMENTE com os valores da coluna `algoritmo_quantico`.
# Para adicionar um novo algoritmo, basta inserir aqui a chave + categoria.
CATEGORIA_POR_ALGORITMO = {
    # 1. Quantum Annealing — paradigma dominante na literatura TSP/VRP
    "QA":               "Quantum Annealing",
    "CQM":              "Quantum Annealing",   # D-Wave Constrained Quadratic Model
    # 2. Variacionais (Gate-Based) — segundo paradigma mais frequente
    "QAOA":             "Variacional (Gate-Based)",
    "VQE":              "Variacional (Gate-Based)",
    "F-VQE":            "Variacional (Gate-Based)",
    "QAOA/VQE":         "Variacional (Gate-Based)",
    # 3. Exatos (Gate-Based)
    "Grover":           "Exato (Gate-Based)",
    "QPE":              "Exato (Gate-Based)",
    # 4. Aprendizado Quantico (QML)
    "QML":              "Aprendizado Quântico (QML)",
    "RL":               "Aprendizado Quântico (QML)",
    "QACO":             "Aprendizado Quântico (QML)",
    "HHL/VQE":          "Aprendizado Quântico (QML)",
    # 5. Catch-all
    "Não especificado": "Não especificado",
}

# Ordem canonica para apresentacao (graficos, tabelas) — segue a sequencia
# do resumo_algoritmos.md (1.1 -> 1.5) com "Nao especificado" sempre por ultimo.
ORDEM_CATEGORIAS = [
    "Quantum Annealing",
    "Variacional (Gate-Based)",
    "Exato (Gate-Based)",
    "Aprendizado Quântico (QML)",
    "Não especificado",
]


def classificar(algoritmo):
    """Retorna a categoria para um valor de `algoritmo_quantico`.

    Valores fora do mapeamento caem em "Não especificado" e sao reportados
    no log para revisao manual (ex: novo algoritmo adicionado ao CSV sem
    atualizar este script).
    """
    if pd.isna(algoritmo):
        return "Não especificado"
    chave = str(algoritmo).strip()
    return CATEGORIA_POR_ALGORITMO.get(chave, "Não especificado")


def main():
    if not os.path.exists(PATH_CSV):
        print(f"[ERRO] CSV nao encontrado: {PATH_CSV}")
        sys.exit(1)

    print(f"Lendo: {PATH_CSV}")
    df = pd.read_csv(PATH_CSV, dtype=str)
    print(f"  {len(df)} linhas, {len(df.columns)} colunas")

    # Aviso se algum algoritmo nao mapeado
    valores_unicos = set(df["algoritmo_quantico"].dropna().astype(str).str.strip())
    nao_mapeados = valores_unicos - set(CATEGORIA_POR_ALGORITMO.keys())
    if nao_mapeados:
        print(f"\n[AVISO] Algoritmos sem mapeamento explicito (caem em 'Não especificado'):")
        for v in sorted(nao_mapeados):
            n = (df["algoritmo_quantico"] == v).sum()
            print(f"  - {v!r}  ({n} linhas)")

    # Aplicar classificacao (sobrescreve se ja existir)
    df["categoria_algoritmo"] = df["algoritmo_quantico"].apply(classificar)

    # Reordenar colunas: categoria_algoritmo ao lado direito de algoritmo_quantico
    cols = list(df.columns)
    if "categoria_algoritmo" in cols:
        cols.remove("categoria_algoritmo")
    idx = cols.index("algoritmo_quantico") + 1
    cols.insert(idx, "categoria_algoritmo")
    df = df[cols]

    # Log da distribuicao
    print(f"\nDistribuicao por categoria:")
    contagem = df["categoria_algoritmo"].value_counts()
    total = len(df)
    for cat in ORDEM_CATEGORIAS:
        n = int(contagem.get(cat, 0))
        pct = 100 * n / max(total, 1)
        print(f"  {cat:35s} {n:4d}  ({pct:5.1f}%)")
    print(f"  {'-'*35} {'-'*4}")
    print(f"  {'TOTAL':35s} {total:4d}")

    df.to_csv(PATH_CSV, index=False, encoding="utf-8-sig")
    print(f"\nSalvo: {PATH_CSV}")


if __name__ == "__main__":
    main()
