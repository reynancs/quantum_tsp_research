"""
Script para gerar a nova base_algoritmos_abordagens.csv
Fonte: 3 tabelas do PDF Phillipson (2025) páginas 50-52
       + dados enriquecidos do CSV anterior (38 linhas via git)

Colunas finais:
  id, autores, paradigma, algoritmo_quantico, topico, subtopico,
  problema, abordagem, ano, hardware, num_cidades, formulacao,
  contribuicao, escala_testada, qualidade_solucao, tempo_execucao,
  taxa_sucesso, sensibilidade_parametros, robustez_ruido,
  metricas_avaliadas, fonte
"""
import pandas as pd
import re
import os
import sys

# Forçar UTF-8 no stdout (Windows cp1252 workaround)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ============================================================
# 1. TODAS AS ENTRADAS DAS 3 TABELAS DO PDF (pages 50-52)
#    Colunas: autores, paradigma_raw, topico, problema, natureza
# ============================================================
PDF_ENTRIES = [
    # ---- TABLE 1 (page 50) - Routing ----
    ("Ajagekar [4]", "QA - QUBO", "Routing", "VRP", "hybrid"),
    ("Alsaiyari [6]", "GBC - QAOA/VQE", "Routing", "VRP", "hybrid"),
    ("Atchade-Adelomou [11]", "QA and GBC - QUBO", "Routing", "Picking", "hybrid"),
    ("Azad [12]", "GBC - QAOA", "Routing", "VRP", "hybrid"),
    ("Azzaoui [13]", "GBC - QAOA", "Routing", "TSP", "hybrid"),
    ("Bentley [16]", "GBC - QAOA", "Routing", "CVRP", "hybrid"),
    ("Borowski [19]", "QA - QUBO", "Routing", "VRP/CVRP", "full and hybrid"),
    ("Bourreau [20]", "GBC - QAOA", "Routing", "TSP", "hybrid"),
    ("Cattelan [29]", "QA - QUBO", "Routing", "RPP", "hybrid"),
    ("Correll [36]", "GBC - QML", "Routing", "VRP", "hybrid"),
    ("Dixit [46]", "QA - QUBO", "Routing", "STDSP", "full"),
    ("Feld [49]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Fitzek [50]", "GBC - QAOA", "Routing", "HVRP", "hybrid"),
    ("Fitzek [51]", "GBC - QAOA", "Routing", "HVRP", "hybrid"),
    ("Harikrishnakumar [62]", "QA - QUBO", "Routing", "(D-)MDCVRP", "full"),
    ("Herzog [65]", "GBC - QAOA", "Routing", "CVRP", "hybrid"),
    ("Harwood [63]", "GBC - QAOA", "Routing", "VRPTW", "hybrid"),
    ("Irie [67]", "QA - QUBO", "Routing", "CVRPTW", "hybrid"),
    ("Kanai [73]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Khan [74]", "GBC - Grover/QAOA", "Routing", "FRO", "hybrid"),
    ("Khumalo [75]", "GBC - QAOA/VQE", "Routing", "TSP", "hybrid"),
    ("Le [81]", "QA - QUBO", "Routing", "sTSP", "hybrid"),
    ("Leonidas [82]", "GBC - QAOA", "Routing", "VRPTW", "hybrid"),
    ("Li [83]", "GBC - VQA", "Routing", "VRP", "hybrid"),
    ("Liu [84]", "QA - QUBO", "Routing", "TSP", "hybrid"),
    ("Lo [85]", "QRNG", "Routing", "VRP", "hybrid"),
    ("Makhanov [87]", "GBC - Grover", "Routing", "SPP", "hybrid"),
    ("Makhanov [88]", "GBC - Grover", "Routing", "FRO", "hybrid"),
    ("Mario [91]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Marsoit [92]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Masuda [95]", "CA - QUBO", "Routing", "TDVRPTW", "full"),
    ("Mohanty [99]", "GBC - VQE", "Routing", "VRP", "hybrid"),
    ("Mohanty [100]", "GBC - QSVM", "Routing", "VRP", "hybrid"),
    ("Neukart [104]", "QA - QUBO", "Routing", "Flow opt.", "hybrid"),
    ("Osaba [106]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Palackal [108]", "GBC - QAOA/VQE", "Routing", "TSP", "hybrid"),
    ("Palmieri [109]", "QA and GBC - QUBO", "Routing", "CVRP", "hybrid"),
    ("Papalitsas [110]", "QA - QUBO", "Routing", "TSPTW", "full"),
    ("Phillipson [113]", "QA - QUBO", "Routing", "Flow opt.", "hybrid"),
    ("Poggel [117]", "Generic", "Routing", "CVRP", "hybrid"),
    ("Qiu [118]", "GBC - QACO", "Routing", "TSP", "hybrid"),
    ("Ramezani [120]", "GBC - QAOA", "Routing", "TSP", "hybrid"),
    ("Rana [121]", "QA and GBC - QUBO", "Routing", "CVRP", "hybrid"),
    ("Rosendo [125]", "QA and GBC - QUBO", "Routing", "CVRP", "hybrid"),
    ("Sadashivan [126]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Salehi [128]", "QA - QUBO", "Routing", "TSPTW", "full"),
    ("Sales [129]", "QA - QUBO", "Routing", "CVRP", "full and hybrid"),
    # ---- TABLE 2 (page 51) - Routing (cont.) + Network Design + Fleet + Cargo ----
    ("Salloum [130]", "QA - QUBO", "Routing", "TFO", "hybrid"),
    ("Salloum [131]", "QA - QUBO", "Routing", "TFO", "hybrid"),
    ("Sanches [132]", "GBC - RL", "Routing", "CVRP", "hybrid"),
    ("Sato [133]", "GBC - Quantum Search", "Routing", "TSP", "full"),
    ("Sinno [144]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Spyridis [146]", "GBC - QAOA", "Routing", "m-TSP", "hybrid"),
    ("Srinivasan [147]", "GBC - QPE", "Routing", "TSP", "hybrid"),
    ("Tejani [151]", "GBC - QPE", "Routing", "BTSP", "hybrid"),
    ("Warren [158]", "QA - QUBO", "Routing", "TSP", "full and hybrid"),
    ("Weinberg [159]", "QA - QUBO", "Routing", "CVRP", "hybrid"),
    ("Wesolowski [160]", "GBC", "Routing", "SPSP", "full"),
    ("Xie [163]", "GBC - QAOA", "Routing", "CVRP", "hybrid"),
    ("Xu [166]", "GBC - QML", "Routing", "CVRP", "hybrid"),
    ("Yarkoni [168]", "QA - QUBO", "Routing", "SRP", "hybrid"),
    # Network Design
    ("Buss [25]", "GBC - QAOA", "Network Design", "FLP", "hybrid"),
    ("Chiscop [33]", "QA - QUBO", "Network Design", "MSLSCP", "hybrid"),
    ("Choo [34]", "QA - QUBO", "Network Design", "FLP", "hybrid"),
    ("Ding [44]", "QA - QUBO", "Network Design", "NDP", "hybrid"),
    ("Ding [43]", "QA - QUBO", "Network Design", "NDP", "full"),
    ("Dixit [45]", "QA - QUBO", "Network Design", "NDP", "hybrid"),
    ("Gabbassov [52]", "QA - QUBO", "Network Design", "UTP", "hybrid"),
    ("Giraldo [54]", "QA and GBC - QUBO", "Network Design", "MCLP", "hybrid"),
    ("Guo [59]", "QA - QUBO", "Network Design", "FLP", "hybrid"),
    ("Khumalo [75]", "GBC - QAOA/VQE", "Network Design", "FLP", "hybrid"),
    ("Klar [76]", "QA - QUBO", "Network Design", "FLP", "hybrid"),
    ("Mahasinghe [86]", "QA - QUBO", "Network Design", "FLP", "-"),
    ("Malviya [90]", "QA - QUBO", "Network Design", "NDP", "hybrid"),
    ("Malviya [89]", "GBC - QAOA", "Network Design", "NDP", "full"),
    ("Radvand [119]", "GBC - Grover", "Network Design", "CSLP", "full"),
    ("Sakib [127]", "QA - QUBO", "Network Design", "CSLP", "hybrid"),
    ("Satori [134]", "QA - QUBO", "Network Design", "LAP", "hybrid"),
    ("Tosum [153]", "QA - QUBO", "Network Design", "QAP", "-"),
    ("Wang [157]", "GBC - QAOA", "Network Design", "FLP", "hybrid"),
    # Fleet opt.
    ("Martins [94]", "QA - QUBO", "Fleet Optimization", "TAP", "hybrid"),
    ("Vikstaal [156]", "GBC - QAOA", "Fleet Optimization", "TAP", "hybrid"),
    ("Willsch [161]", "QA - QUBO", "Fleet Optimization", "TAP", "hybrid"),
    # Cargo
    ("De Andoin [8]", "QA - QUBO", "Cargo", "BPP", "hybrid"),
    ("De Andoin [9]", "QA - QUBO", "Cargo", "BPP", "hybrid"),
    ("Ardelean [10]", "GBC - QML", "Cargo", "QKP", "hybrid"),
    ("Benson [15]", "QA - CQM", "Cargo", "KP", "hybrid"),
    ("Bontekoe [18]", "QA - QUBO", "Cargo", "QKP", "full"),
    ("Bozejko [21]", "QA - QUBO", "Cargo", "QKP", "hybrid"),
    ("Cellini [30]", "QA - QUBO", "Cargo", "BPP", "full"),
    ("Cellini [31]", "QA - QUBO", "Cargo", "BPP", "hybrid"),
    ("Christiansen [35]", "GBC - QAOA", "Cargo", "QKP", "hybrid"),
    ("Cui [38]", "GBC - Grover", "Cargo", "QKP", "hybrid"),
    ("Gatti [53]", "QA - QUBO", "Cargo", "BPP", "hybrid"),
    # ---- TABLE 3 (page 52) - Cargo (cont.) + Prediction + Scheduling ----
    ("Matt [96]", "GBC - QAOA", "Cargo", "BPP", "hybrid"),
    ("Nayak [103]", "QA - QUBO", "Cargo", "ALO", "hybrid"),
    ("Pilon [116]", "QA - QUBO", "Cargo", "ALO", "full"),
    ("Romero [123,124]", "QA - CQM", "Cargo", "BPP", "hybrid"),
    ("Shirai [141]", "GBC - VQA", "Cargo", "QKP", "hybrid"),
    ("Sotelo [64,145]", "GBC - VQE", "Cargo", "ALO", "hybrid"),
    ("Van Dam [40]", "GBC - QAOA", "Cargo", "KP", "hybrid"),
    # Prediction
    ("Gutta [60]", "GBC - QML", "Prediction", "Forecasting", "hybrid"),
    ("Jahin [69]", "GBC - QML", "Prediction", "Prediction", "hybrid"),
    ("Jiang [71]", "GBC - HHL/VQE", "Prediction", "Inventory", "hybrid"),
    ("Koushik [78]", "GBC - QML", "Prediction", "Maintenance", "hybrid"),
    ("Sehrawat [140]", "GBC - QML", "Prediction", "Forecasting", "hybrid"),
    # Scheduling
    ("Adelomou [2]", "GBC - VQE", "Scheduling", "Personnel", "hybrid"),
    ("Ajagekar [4]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Ajagekar [4]", "QA - QUBO", "Scheduling", "MCFP", "hybrid"),
    ("Amaro [7]", "GBC - VQE", "Scheduling", "JSP", "hybrid"),
    ("Bernreuther [17]", "GBC - QAOA", "Scheduling", "Scheduling", "hybrid"),
    ("Carugno [27]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Denkena [42]", "QA - QUBO", "Scheduling", "FJSP", "hybrid"),
    ("Grange [57]", "GBC - QAOA", "Scheduling", "Scheduling", "hybrid"),
    ("Huang [66]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Krol [79]", "GBC - Grover", "Scheduling", "Scheduling", "full"),
    ("Kurowski [80]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Mohammadbagherpoor [98]", "QA - VQE", "Scheduling", "QAP", "hybrid"),
    ("Mori [101]", "GBC and QA - QAOA", "Scheduling", "ARP", "hybrid"),
    ("Permin [111]", "GBC - Grover", "Scheduling", "JSP", "hybrid"),
    ("Riandari [122]", "GBC - QAOA", "Scheduling", "Production opt.", "hybrid"),
    ("Scherer [135]", "GBC - Grover", "Scheduling", "JSP", "full"),
    ("Streif [148]", "GBC - QAOA", "Scheduling", "JSP", "hybrid"),
    ("Schworm [137]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Schworm [138]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Schworm [139]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
    ("Venturelli [155]", "QA - QUBO", "Scheduling", "JSP", "full"),
    ("Windmann [162]", "GBC - QAOA", "Scheduling", "JSP", "hybrid"),
    ("Yarkoni [167]", "QA - QUBO", "Scheduling", "JSP", "hybrid"),
]

# ============================================================
# 1b. MAPEAMENTO DE ENRIQUECIMENTO (dados do CSV antigo, 38 linhas)
#     Chave: sobrenome normalizado do primeiro autor
#     Valor: dict com colunas extras
#     Fonte: data/base_algoritmos_abordagens_OLD.csv (recuperado do git)
# ============================================================
# Colunas extras que serão mescladas do CSV antigo:
COLUNAS_ENRIQUECIMENTO = [
    "ano", "hardware", "num_cidades", "formulacao", "contribuicao",
    "escala_testada", "qualidade_solucao", "tempo_execucao",
    "taxa_sucesso", "sensibilidade_parametros", "robustez_ruido",
    "metricas_avaliadas", "criterios",
]

# Mapeamento: nome do autor no PDF → nome do autor no CSV antigo
# (necessário porque os nomes diferem ligeiramente entre as fontes)
MAPA_AUTORES_OLD = {
    "Srinivasan [147]": "Srinivasan et al.",
    "Liu [84]": "Liu et al.",
    "Bourreau [20]": "Bourreau et al.",
    "Khumalo [75]": "Khumalo et al.",
    "Palackal [108]": "Palackal et al.",
    "Palmieri [109]": "Palmieri",
    "Sato [133]": "Sato et al.",
    "Ramezani [120]": "Ramezani et al.",
    "Warren [158]": "Warren",
    "Azzaoui [13]": "Azzaoui et al.",
    "Qiu [118]": "Qiu et al.",
    "Salehi [128]": "Salehi et al.",
    "Papalitsas [110]": "Papalitsas et al.",
    "Le [81]": "Le et al.",
    "Spyridis [146]": "Spyridis et al.",
    "Tejani [151]": "Tejani",
    "Matt [96]": "Matt et al.",
    "Sales [129]": "Sales et al.",
    "Bentley [16]": "Bentley et al.",
    "Feld [49]": "Feld et al.",
    "Borowski [19]": "Borowski et al.",
    "Weinberg [159]": "Weinberg et al.",
    "Osaba [106]": "Osaba et al.",
    "Marsoit [92]": "Marsoit et al.",
    "Yarkoni [168]": "Yarkoni et al.",
    "Mohanty [99]": "Mohanty et al.",
    "Azad [12]": "Azad et al.",
    "Phillipson [113]": "Phillipson e Chiscop",
    "Sanches [132]": "Sanches et al.",
    "Xu [166]": "Xu et al.",
    "Jahin [69]": "Jahin et al.",
    "Adelomou [2]": "Adelomou et al.",
    "Ardelean [10]": "Ardelean et al.",
    "Amaro [7]": "Amaro et al.",
}


def carregar_dados_antigos():
    """Carrega o CSV antigo e indexa por nome do autor para merge."""
    caminho = os.path.join(os.path.dirname(__file__), "..", "data", "base_algoritmos_abordagens_OLD.csv")
    if not os.path.exists(caminho):
        print("⚠ CSV antigo não encontrado. Todas as colunas extras serão 'Nao Reportada'.")
        return {}

    df_old = pd.read_csv(caminho, dtype=str)
    # Criar dicionário: nome_autor → dict de colunas extras
    lookup = {}
    for _, row in df_old.iterrows():
        autor = row["autores"].strip()
        dados = {}
        for col in COLUNAS_ENRIQUECIMENTO:
            val = row.get(col, pd.NA)
            dados[col] = val if pd.notna(val) else "Nao Reportada"
        lookup[autor] = dados
    return lookup


# ============================================================
# 2. FUNÇÕES DE LIMPEZA
# ============================================================

def separar_paradigma(raw: str):
    """Separa 'GBC - QAOA' em paradigma='GBC' e algoritmo='QAOA'."""
    raw = raw.strip()
    # Tratar "QA and GBC" / "GBC and QA"
    if "and" in raw.lower():
        parts = re.split(r"\s*-\s*", raw, maxsplit=1)
        if len(parts) == 2:
            para_raw, algo = parts
        else:
            para_raw, algo = raw, ""
        para_raw = para_raw.strip()
        para_raw = re.sub(r"(?i)\bQA\b", "QA", para_raw)
        para_raw = re.sub(r"(?i)\bGBC\b", "GBC", para_raw)
        para_raw = re.sub(r"\s*and\s*", " e ", para_raw)
        return para_raw.strip(), algo.strip()

    parts = re.split(r"\s*-\s*", raw, maxsplit=1)
    if len(parts) == 2:
        paradigma, algoritmo = parts[0].strip(), parts[1].strip()
    else:
        paradigma, algoritmo = raw.strip(), ""

    paradigma_map = {
        "QA": "QA", "GBC": "GBC", "CA": "CA",
        "QRNG": "QRNG", "Generic": "Generic", "QML": "QML",
        "QAOA": "GBC",
    }
    paradigma_norm = paradigma_map.get(paradigma, paradigma)
    if paradigma == "QAOA" and not algoritmo:
        algoritmo = "QAOA"
    return paradigma_norm, algoritmo


def normalizar_algoritmo(algo: str) -> str:
    """Agrupa algoritmos semelhantes."""
    algo = algo.strip()
    if not algo:
        return "Não especificado"

    if re.search(r"(?i)grover|quantum search", algo):
        return "Grover"
    if re.search(r"(?i)^QAOA$|^IQAOA|^QAOA\s*/\s*QOBA", algo):
        return "QAOA"
    if re.search(r"(?i)QAOA\s*/\s*VQE", algo):
        return "QAOA/VQE"
    if re.search(r"(?i)grover.*QAOA|QAOA.*grover", algo):
        return "Grover/QAOA"
    if re.search(r"(?i)^VQE$|^F-VQE|^VQA$", algo):
        return "VQE"
    if re.search(r"(?i)QPE|Quantum Phase", algo):
        return "QPE"
    if re.search(r"(?i)^QML$|^QSVM$|Q-Learning|QAmplify|QCBR|HQAGO", algo):
        return "QML"
    if re.search(r"(?i)^QUBO$", algo):
        return "QA"  # QUBO é formulação, não algoritmo — vai para coluna 'formulacao'
    if re.search(r"(?i)QACO", algo):
        return "QACO"
    if re.search(r"(?i)^RL$|reinforcement", algo):
        return "RL"
    if re.search(r"(?i)^CQM$", algo):
        return "CQM"
    if re.search(r"(?i)HHL", algo):
        return "HHL/VQE"
    return algo


def normalizar_natureza(nat: str) -> str:
    """Normaliza a natureza/abordagem."""
    nat = nat.strip().lower()
    if nat in ("full", "full quantum"):
        return "Full Quantum"
    if nat == "hybrid":
        return "Hybrid"
    if "full" in nat and "hybrid" in nat:
        return "Full e Hybrid"
    if nat == "-" or nat == "":
        return "Não especificado"
    return nat.title()


# ============================================================
# 3. CONSTRUIR O DATAFRAME
# ============================================================
dados_antigos = carregar_dados_antigos()
DEFAULT_EXTRA = {col: "Nao Reportada" for col in COLUNAS_ENRIQUECIMENTO}

rows = []
for i, (autores, paradigma_raw, topico, problema, natureza) in enumerate(PDF_ENTRIES, 1):
    paradigma, algoritmo_raw = separar_paradigma(paradigma_raw)
    algoritmo = normalizar_algoritmo(algoritmo_raw)
    abordagem = normalizar_natureza(natureza)

    # Normalizar GBC e QA → QA e GBC
    if paradigma == "GBC e QA":
        paradigma = "QA e GBC"

    # Buscar dados enriquecidos do CSV antigo
    autor_old = MAPA_AUTORES_OLD.get(autores, "")
    extras = dados_antigos.get(autor_old, DEFAULT_EXTRA)

    # Se algoritmo é "QA" (originalmente QUBO) e formulacao não tem valor,
    # preencher formulacao com "QUBO"
    formulacao = extras["formulacao"]
    if algoritmo == "QA" and formulacao == "Nao Reportada":
        formulacao = "QUBO"

    row = {
        "id": i,
        "autores": autores,
        "paradigma": paradigma,
        "algoritmo_quantico": algoritmo,
        "topico": topico,
        "problema": problema,
        "abordagem": abordagem,
        "ano": extras["ano"],
        "hardware": extras["hardware"],
        "num_cidades": extras["num_cidades"],
        "formulacao": formulacao,
        "contribuicao": extras["contribuicao"],
        "escala_testada": extras["escala_testada"],
        "qualidade_solucao": extras["qualidade_solucao"],
        "tempo_execucao": extras["tempo_execucao"],
        "taxa_sucesso": extras["taxa_sucesso"],
        "sensibilidade_parametros": extras["sensibilidade_parametros"],
        "robustez_ruido": extras["robustez_ruido"],
        "metricas_avaliadas": extras["metricas_avaliadas"],
        "criterios": extras["criterios"],
        "fonte": "Phillipson 2025",
    }
    rows.append(row)

df = pd.DataFrame(rows)

# ============================================================
# 4. CRITÉRIO C6 (TAXA DE SUCESSO) E RANKING PONDERADO
# ============================================================
#
# SISTEMA DE CRITÉRIOS E PONTUAÇÃO PONDERADA
# -------------------------------------------
# Cada critério avalia uma dimensão de qualidade do trabalho.
# O artigo recebe 1 ponto por critério atendido, multiplicado pelo peso.
# O ranking final é a soma ponderada normalizada em escala 0-100.
#
# Critérios (6 dimensões):
#   C1 — Qualidade da solução      (peso 2.0): o trabalho reporta métricas
#         de qualidade com resultados positivos (próximo ao ótimo, superior, etc.)
#   C2 — Escalabilidade            (peso 1.5): o trabalho testa instâncias de
#         escala variável ou média/grande (não limitado a <=5 qubits)
#   C3 — Aplicação real            (peso 2.0): o trabalho aplica o algoritmo
#         em cenário real ou com dados reais (não apenas benchmarks teóricos)
#   C4 — Comparação com clássico   (peso 1.5): o trabalho compara resultados
#         com algoritmos clássicos de referência
#   C5 — Análise de limitações     (peso 1.0): o trabalho analisa limitações
#         do hardware, sensibilidade a parâmetros ou robustez a ruído
#   C6 — Taxa de sucesso           (peso 2.0): o trabalho reporta taxa de
#         sucesso quantitativa (percentual, probabilidade, ou avaliação explícita)
#
# Fórmula:
#   pontuacao_bruta = Σ (criterio_i × peso_i)  para i = C1..C6
#   pontuacao_maxima = Σ pesos = 2.0 + 1.5 + 2.0 + 1.5 + 1.0 + 2.0 = 10.0
#   ranking = (pontuacao_bruta / pontuacao_maxima) × 100
#
# Resultado: escala de 0 a 100 onde:
#   0         = nenhum critério atendido (dados insuficientes)
#   100       = todos os 6 critérios atendidos (excelência completa)
#

PESOS_CRITERIOS = {
    "C1": 2.0,  # Qualidade da solução
    "C2": 1.5,  # Escalabilidade
    "C3": 2.0,  # Aplicação real
    "C4": 1.5,  # Comparação com clássico
    "C5": 1.0,  # Análise de limitações
    "C6": 2.0,  # Taxa de sucesso
}
PONTUACAO_MAXIMA = sum(PESOS_CRITERIOS.values())  # 10.0


def avaliar_c6_taxa_sucesso(taxa: str) -> bool:
    """Avalia se o trabalho atende ao critério C6 (Taxa de Sucesso).

    Retorna True se o trabalho reporta taxa de sucesso quantitativa
    ou avaliação explícita (não apenas 'Nao Reportada' ou 'Nao reportada').
    """
    if pd.isna(taxa):
        return False
    taxa_lower = taxa.strip().lower()
    # Não atende: valores genéricos sem informação útil
    if taxa_lower in ("nao reportada", "nao reportado", ""):
        return False
    # Atende: qualquer valor concreto (percentual, avaliação qualitativa, etc.)
    return True


def calcular_ranking(criterios_str: str, taxa_sucesso: str) -> float:
    """Calcula pontuação ponderada (0-100) com base nos critérios C1-C6.

    Args:
        criterios_str: string com critérios existentes, ex: "C1, C3, C6"
        taxa_sucesso: valor da coluna taxa_sucesso (para C6)

    Returns:
        Pontuação normalizada 0 a 100
    """
    pontuacao = 0.0
    if pd.isna(criterios_str) or criterios_str.strip().lower() == "nao reportada":
        criterios_presentes = set()
    else:
        criterios_presentes = {c.strip() for c in criterios_str.split(",")}

    for codigo, peso in PESOS_CRITERIOS.items():
        if codigo in criterios_presentes:
            pontuacao += peso

    return round((pontuacao / PONTUACAO_MAXIMA) * 100)


# --- Aplicar C6 e atualizar coluna 'criterios' ---
print("🔄 Avaliando critério C6 (Taxa de Sucesso)...")
c6_count = 0
for idx, row in df.iterrows():
    taxa = row["taxa_sucesso"]
    criterios = row["criterios"]

    if avaliar_c6_taxa_sucesso(taxa):
        c6_count += 1
        # Adicionar C6 à lista de critérios
        if pd.isna(criterios) or criterios.strip().lower() == "nao reportada":
            df.at[idx, "criterios"] = "C6"
        else:
            if "C6" not in criterios:
                df.at[idx, "criterios"] = criterios + ", C6"

print(f"   C6 atribuído a {c6_count} trabalhos")

# --- Calcular coluna Ranking ---
print("📊 Calculando ranking ponderado...")
df["ranking"] = df.apply(
    lambda r: calcular_ranking(r["criterios"], r["taxa_sucesso"]),
    axis=1,
)

# Estatísticas do ranking
ranking_com_pontos = (df["ranking"] > 0).sum()
print(f"   Trabalhos com ranking > 0: {ranking_com_pontos}/{len(df)}")
print(f"   Ranking médio (com pontos): {df[df['ranking'] > 0]['ranking'].mean():.1f}")
print(f"   Ranking máximo: {df['ranking'].max()}")
print(f"   Top 5 ranking:")
top5 = df.nlargest(5, "ranking")[["autores", "criterios", "ranking"]]
for _, r in top5.iterrows():
    print(f"      {r['autores']}: {r['ranking']} ({r['criterios']})")

# ============================================================
# 5. VERIFICAÇÕES E ESTATÍSTICAS
# ============================================================
print(f"\nTotal de entradas: {len(df)}")
print(f"Colunas: {list(df.columns)} ({len(df.columns)} colunas)")

print(f"\nParadigmas únicos:")
print(df["paradigma"].value_counts().to_string())
print(f"\nAlgoritmos únicos:")
print(df["algoritmo_quantico"].value_counts().to_string())
print(f"\nTópicos únicos:")
print(df["topico"].value_counts().to_string())
print(f"\nAbordagens únicas:")
print(df["abordagem"].value_counts().to_string())

# Estatísticas de enriquecimento
enriquecidos = (df["ano"] != "Nao Reportada").sum()
print(f"\n📊 Enriquecimento:")
print(f"   Artigos com dados completos: {enriquecidos}/{len(df)}")
print(f"   Artigos com 'Nao Reportada': {len(df) - enriquecidos}/{len(df)}")

# ============================================================
# 6. SALVAR CSV
# ============================================================
output_path = "data/base_algoritmos_abordagens.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n✅ Arquivo salvo: {output_path}")
print(f"   {len(df)} linhas x {len(df.columns)} colunas")
