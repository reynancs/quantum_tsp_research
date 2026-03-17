# Resumo da Etapa 1 — Pesquisa Bibliográfica por Palavras-Chave

**Projeto**: Computação Quântica Aplicada ao Problema do Caixeiro Viajante (TSP) em Logística
**Programa**: Mestrado Profissional em Gestão de Tecnologia e Inovação — SENAI CIMATEC
**Data da busca**: 10/03/2026
**Data da deduplicação**: 17/03/2026
**Base principal**: Lens.org (filtro: Scholarly Works)

---

## 1. Contexto e Objetivo

O presente levantamento bibliográfico constitui a Etapa 1 do projeto de pesquisa, cujo objetivo é construir um artigo técnico-científico sobre a aplicação de algoritmos de Computação Quântica ao Problema do Caixeiro Viajante (TSP) e suas variantes, com foco na área de Logística.

O objetivo específico desta etapa foi mapear o volume e a distribuição da produção acadêmica existente sobre o tema, por meio de buscas estruturadas por palavras-chave em bases acadêmicas. Este mapeamento permite:

- Dimensionar o corpus disponível de artigos relevantes
- Identificar quais algoritmos, paradigmas quânticos e problemas logísticos concentram mais pesquisas
- Detectar lacunas de pesquisa (temas pouco explorados)
- Fundamentar a justificativa de relevância do artigo proposto

---

## 2. Estrutura da Pesquisa

### 2.1 Sistema de Eixos

As strings de busca foram construídas combinando pelo menos 2 dos 3 eixos temáticos abaixo com o operador booleano AND:

| Eixo | Descrição | Exemplos de Termos |
|------|-----------|-------------------|
| **Eixo 1 — Problema** | TSP e variantes de otimização combinatória | "Traveling Salesman Problem", "TSP", "Vehicle Routing", "Combinatorial Optimization", "Hamiltonian Cycle", "Bin Packing", "Knapsack", "Job Shop Scheduling" |
| **Eixo 2 — Tecnologia** | Computação quântica, algoritmos e hardware | "Quantum Computing", "Quantum Annealing", "QAOA", "VQE", "Grover", "QUBO", "Ising Model", "D-Wave", "IBM Quantum", "Quantum-Inspired", "QML" |
| **Eixo 3 — Aplicação** | Logística e operações | "Logistics", "Supply Chain Management", "Route Optimization", "Facility Location", "Cargo Loading" |

### 2.2 Classificação de Prioridades

Cada string foi classificada em Alta, Média ou Baixa como prioridade antes da execução da busca, com base na **relevância semântica direta ao tema central da dissertação**. Os critérios foram:

| Prioridade | Critério | Padrão Típico |
|------------|----------|--------------|
| **Alta** | Ambos os termos apontam **diretamente** para o objeto de estudo (TSP/VRP + tecnologia quântica central) | "Traveling Salesman" + "Quantum Computing", "VRP" + "QAOA", "Quantum Computing" + "Supply Chain Management" |
| **Média** | Um dos termos é **mais amplo ou periférico**, capturando artigos relevantes mas com maior proporção de ruído | "Combinatorial Optimization" + "Quantum Annealing", "TSP" + "Grover", "Quantum-Inspired", "Job Shop Scheduling" |
| **Baixa** | Termos **complementares, muito específicos de hardware, formulações matemáticas**, ou problemas adjacentes que ampliam a cobertura | "TSP" + "IBM Quantum", "Ising Model", "Hamiltonian Cycle", "Knapsack", "Bin Packing" |

**Nota**: prioridade reflete **relevância temática**, não volume esperado de resultados. Strings mais específicas (Alta) tendem a retornar menos artigos, porém com maior aderência ao tema. Strings mais amplas (Média/Baixa) retornam mais volume, mas com maior proporção de artigos tangenciais.

### 2.3 Duas Fases de Strings

A pesquisa foi conduzida em duas fases:

- **Fase 1 (Strings #1–#16)**: 16 strings originais baseadas na taxonomia inicial do projeto, focadas em TSP, VRP e algoritmos quânticos principais
- **Fase 2 (Strings #17–#26)**: 10 strings adicionais derivadas da análise do artigo de referência (Phillipson, 2025), ampliando a cobertura para problemas logísticos adjacentes (scheduling, bin packing, knapsack, facility location) e abordagens emergentes (quantum-inspired, QRL, QML)

---

## 3. Contribuição do Artigo de Referência

O artigo "Quantum Computing in Logistics and Supply Chain Management — an Overview" (Phillipson, 2025, Maastricht University/TNO) foi utilizado como referência para esta pesquisa. Trata-se de uma revisão abrangente de mais de 80 artigos publicados, cobrindo seis áreas de aplicação: routing, network design, fleet maintenance, cargo loading, prediction e scheduling.

A contribuição do artigo de referência para a estruturação da pesquisa bibliográfica se deu em três frentes:

**a) Expansão da taxonomia de algoritmos**: O artigo revelou algoritmos não contemplados na taxonomia inicial do projeto, como IQAOA, Grover-Mixer QAOA, F-VQE, VarQITE, QACO, Quantum Q-Learning, entre outros. Esses algoritmos foram incorporados ao arquivo `algorithms_reference.md`, expandindo de ~20 para 40+ algoritmos catalogados.

**b) Identificação de novas strings de busca**: A cobertura de problemas logísticos além do TSP/VRP (JSP, BPP, KP, FLP) e de abordagens emergentes (Quantum-Inspired, QRL, QML para supply chain) motivou a criação das 10 strings adicionais (#17–#26), garantindo que a revisão exploratória capture a amplitude real do campo.

**c) Refinamento das métricas de comparação**: O artigo detalha métricas específicas por domínio (makespan para JSP, taxa de ocupação para BPP, cobertura de demanda para network design), ampliando de 6 para 14 métricas universais mais métricas específicas por problema.

---

## 4. Principais Resultados e Insights

### 4.1 Visão Geral Quantitativa

| Métrica | Valor |
|---------|-------|
| Total de strings de busca | 26 |
| Total bruto de artigos (com duplicatas) | **5.320**¹ |
| Total de artigos únicos (após deduplicação) | **3.696** |
| Duplicatas removidas | 1.624 (30,5%) |
| Artigos com DOI | 3.478 (94,1%) |
| Artigos sem DOI | 218 (5,9%) |
| Média por string | 204,6 |
| Strings originais (#1–#16) | 3.170 artigos |
| Strings novas (#17–#26) | 2.150 artigos |

¹ *Total original era 5.536. Reduzido para 5.320 após aplicação de filtro temporal (2020–2026) na string #7, que passou de 1.010 para 794 resultados.*

### 4.2 Distribuição por Prioridade

| Prioridade | Strings | Artigos | % do Total | Média/string |
|------------|---------|---------|-----------|-------------|
| **Alta** | 8 | 1.523 | 27,5% | 190 |
| **Média** | 10 | 2.262 | 40,9% | 226 |
| **Baixa** | 8 | 1.751 | 31,6% | 219 |

O volume maior em strings de prioridade Média e Baixa confirma a relação inversa entre especificidade e volume: strings mais focadas no tema central (Alta) retornam menos resultados, porém com maior aderência.

### 4.3 Distribuição por Volume

| Faixa | Quantidade de strings |
|-------|----------------------|
| >500 artigos | 2 (strings genéricas: "Combinatorial Optimization" e "Knapsack") |
| 200–500 artigos | 8 |
| 50–200 artigos | 9 |
| <50 artigos | 7 (nichos específicos) |

As 5 strings com maior volume concentram **53,2%** do total (2.943 artigos), indicando alta concentração em termos genéricos.

### 4.4 Ranking Completo por Volume

| # | String de Busca | Prioridade | Total | Fase |
|---|----------------|-----------|-------|------|
| 7 | "Combinatorial Optimization" AND "Quantum Annealing" | Média | 794² | Original |
| 25 | "Knapsack Problem" AND "Quantum" | Baixa | 814 | Nova |
| 1 | "Traveling Salesman Problem" AND "Quantum Computing" | Alta | 391 | Original |
| 18 | "Quantum Computing" AND "Supply Chain Management" | Alta | 386 | Nova |
| 22 | "Job Shop Scheduling" AND "Quantum" | Média | 342 | Nova |
| 9 | "Traveling Salesman" AND "Grover" | Média | 333 | Original |
| 14 | "Traveling Salesman" AND "Ising Model" | Baixa | 274 | Original |
| 2 | "Traveling Salesman" AND "Quantum Algorithms" | Alta | 264 | Original |
| 23 | "Bin Packing" AND "Quantum" | Baixa | 249 | Nova |
| 16 | "Hamiltonian Cycle" AND "Quantum" | Baixa | 246 | Original |
| 19 | "Traveling Salesman" AND "Quantum-Inspired" | Média | 182 | Nova |
| 6 | "Vehicle Routing" AND "Quantum Computing" | Alta | 179 | Original |
| 10 | "QUBO" AND "Traveling Salesman" | Média | 142 | Original |
| 3 | "TSP" AND "Quantum Annealing" | Alta | 124 | Original |
| 11 | "Route Optimization" AND "Quantum" AND "Logistics" | Média | 106 | Original |
| 12 | "TSP" AND "D-Wave" | Média | 88 | Original |
| 4 | "Traveling Salesman" AND "QAOA" | Alta | 82 | Original |
| 26 | "Quantum Machine Learning" AND "Supply Chain" | Baixa | 79 | Nova |
| 5 | "TSP" AND "Hybrid Quantum" | Alta | 68 | Original |
| 15 | "Vehicle Routing" AND "Quantum Annealing" AND "Logistics" | Baixa | 41 | Original |
| 24 | "Facility Location" AND "Quantum Computing" | Baixa | 30 | Nova |
| 17 | "Vehicle Routing Problem" AND "QAOA" | Alta | 29 | Nova |
| 20 | "Quantum Reinforcement Learning" AND "Routing" | Média | 21 | Nova |
| 8 | "TSP" AND "VQE" | Média | 20 | Original |
| 13 | "TSP" AND "IBM Quantum" | Baixa | 18 | Original |
| 21 | "CVRP" AND "Quantum Annealing" | Média | 18 | Nova |

² *String #7 refinada com filtro temporal 2020–2026 (originalmente 1.010 resultados) para viabilizar exportação no plano gratuito do Lens.org (limite de 1.000 registros).*

### 4.5 Insights Principais

**Insight 1 — Quantum Annealing domina a literatura de otimização combinatória quântica**

A string "Combinatorial Optimization" AND "Quantum Annealing" retorna 794 artigos (filtro 2020–2026), o maior volume absoluto. Somada a "TSP" AND "Quantum Annealing" (124) e "TSP" AND "D-Wave" (88), confirma que o paradigma de annealing (D-Wave) é o mais pesquisado para problemas de otimização, alinhado com as conclusões de Phillipson (2025).

**Insight 2 — Algoritmos variacionais gate-based (QAOA/VQE) são um nicho ainda pequeno**

- "Traveling Salesman" AND "QAOA" = 82 artigos
- "Vehicle Routing Problem" AND "QAOA" = 29 artigos
- "TSP" AND "VQE" = 20 artigos
- "TSP" AND "IBM Quantum" = 18 artigos

A disparidade entre QA (~1.200+ artigos) e gate-based (~150 artigos) representa um **gap de pesquisa significativo** e uma oportunidade para contribuição original no artigo proposto.

**Insight 3 — Supply Chain Management tem cobertura substancial, mas logística aplicada é escassa**

A string "Quantum Computing" AND "Supply Chain Management" retorna 386 artigos (nova, Alta prioridade), indicando interesse significativo no tema amplo. Porém, strings focadas em logística aplicada são modestas:
- "Route Optimization" AND "Quantum" AND "Logistics" = 106
- "Vehicle Routing" AND "Quantum Annealing" AND "Logistics" = 41

Há espaço para artigos que façam a ponte entre teoria quântica e aplicação logística real.

**Insight 4 — Problemas adjacentes expandem significativamente o corpus**

As novas strings adicionaram 2.150 artigos ao levantamento:
- "Knapsack Problem" AND "Quantum" = 814 (maior volume entre as novas)
- "Job Shop Scheduling" AND "Quantum" = 342
- "Bin Packing" AND "Quantum" = 249

Estes problemas são variantes ou subproblemas do TSP/VRP em contextos logísticos, e sua literatura contém algoritmos e formulações (QUBO, QAOA) diretamente transferíveis.

**Insight 5 — Abordagens emergentes ainda são incipientes**

- "Quantum Reinforcement Learning" AND "Routing" = 21 artigos
- "CVRP" AND "Quantum Annealing" = 18 artigos
- "Quantum Machine Learning" AND "Supply Chain" = 79 artigos
- "Facility Location" AND "Quantum Computing" = 30 artigos

Estes nichos com <100 artigos representam fronteiras de pesquisa onde contribuições originais são mais viáveis.

**Insight 6 — Quantum-Inspired é uma tendência relevante**

"Traveling Salesman" AND "Quantum-Inspired" retorna 182 artigos, revelando que algoritmos clássicos inspirados em computação quântica (Simulated Bifurcation, Digital Annealing, Coherent Ising Machines) formam uma categoria significativa e crescente que deve ser incluída na revisão como referência comparativa.

**Insight 7 — Sobreposição real menor que a estimada**

A deduplicação por DOI e título reduziu o total bruto de 5.320 para **3.696 artigos únicos** (taxa de sobreposição de 30,5%). Este valor ficou acima da estimativa inicial de 1.500–2.500, indicando que as 26 strings capturam conjuntos relativamente distintos de artigos. A análise de sobreposição revela que **81,1% dos artigos aparecem em apenas 1 string**, confirmando a complementaridade das buscas.

**Insight 8 — Crescimento acelerado nos últimos 5 anos**

A análise bibliométrica temporal mostra que **61,7% dos artigos únicos (2.228 de 3.610 com ano informado) foram publicados a partir de 2020**, com pico em 2022 e 2025. Este crescimento exponencial confirma que computação quântica aplicada a otimização combinatória é um campo em franca expansão.

**Insight 9 — Alta taxa de Open Access**

**82,8% dos artigos** (3.060 de 3.696) estão em Open Access, com predominância da modalidade Gold (38,8%) e Green (27,6%). Isto favorece o acesso e a reprodutibilidade da revisão bibliográfica, reduzindo barreiras de paywall para leitura completa dos artigos.

---

## 5. Resultados da Deduplicação e Análise Bibliométrica

### 5.1 Deduplicação

Os 5.320 resultados brutos foram exportados em formato CSV (26 arquivos) e processados pelo script `src/deduplicar_artigos.py`, que realizou deduplicação em duas etapas:

1. **Por DOI**: 5.055 artigos com DOI → 3.478 únicos (1.577 duplicatas removidas)
2. **Por título normalizado** (artigos sem DOI): 265 → 218 únicos (47 duplicatas removidas)

**Resultado**: 3.696 artigos únicos, armazenados em `data/artigos_unicos.csv`.

### 5.2 Análise Bibliométrica

A análise bibliométrica foi conduzida em duas frentes:

- **Script estático** (`src/analise_bibliometrica.py`): gerou 9 gráficos PNG e resumo estatístico em `data/resultados_bibliometria/`
- **Dashboard interativo** (`src/dashboard_bibliometrico.py`): aplicação Streamlit com 6 abas, 16 gráficos Plotly e filtros dinâmicos para exploração dos dados

### 5.3 Principais Métricas da Base Deduplicada

| Métrica | Valor |
|---------|-------|
| Artigos únicos | 3.696 |
| Período coberto | 1884–2026 |
| Artigos 2020+ | 2.228 (61,7%) |
| Total de citações | 136.407 |
| Média de citações/artigo | 36,9 |
| Artigos Open Access | 3.060 (82,8%) |
| Países de origem | 49 |
| Journals/fontes distintas | 1.409 |

---

## 6. Conclusão

O levantamento bibliográfico por palavras-chave cumpriu seus objetivos: mapeou um corpus de **3.696 artigos únicos** (após deduplicação de 5.320 brutos) distribuídos em 26 strings de busca, organizadas em 3 eixos temáticos e 3 níveis de prioridade.

Os resultados confirmam que:

1. **Existe literatura suficiente** para sustentar uma revisão exploratória robusta, com 3.696 artigos únicos cobrindo o período de 1884 a 2026
2. **O campo está em crescimento acelerado** — 61,7% dos artigos foram publicados a partir de 2020, com pico em 2022 e 2025
3. **Quantum Annealing é o paradigma dominante**, seguido por QAOA/VQE, com um gap significativo entre ambos
4. **Abordagens híbridas** (quântico + clássico) são o padrão na literatura, não a exceção
5. **Existem lacunas claras** em algoritmos gate-based para TSP, QML para previsão em logística, e aplicações de quantum reinforcement learning — oportunidades para contribuição original
6. **Alta acessibilidade** — 82,8% dos artigos são Open Access, facilitando a leitura completa
7. **O artigo de referência (Phillipson, 2025)** foi fundamental para ampliar a cobertura da pesquisa e identificar algoritmos e problemas que não constavam no escopo inicial

---

## 7. Recomendações e Próximos Passos

### 7.1 Itens Concluídos nesta Etapa

- [x] Deduplicação por DOI e título (5.320 → 3.696 artigos únicos)
- [x] Análise bibliométrica estática (9 gráficos PNG)
- [x] Dashboard interativo Streamlit (16 gráficos, 6 abas, filtros dinâmicos)
- [x] Filtro temporal na string #7 (1.010 → 794)

### 7.2 Itens Pendentes para a Fase 1

- **Refinar a string #25**: "Knapsack Problem" AND "Quantum" (814 artigos) é genérica — considerar adicionar termos de logística se o objetivo for capturar apenas KP aplicado a supply chain
- **Busca em bases complementares**: replicar as 8 strings de Alta prioridade em **IEEE Xplore** e **arXiv** para verificar cobertura além do Lens.org

### 7.3 Próximos Passos — Fase 2 (Fundamentação Teórica)

- **Seleção de artigos para leitura**: todos os artigos das strings #8 (VQE, 20), #13 (IBM Quantum, 18), #21 (CVRP+QA, 18), #17 (VRP+QAOA, 29) e #20 (QRL+Routing, 21) — nichos com volume gerenciável e alta relevância
- **Leitura por amostragem**: para strings com >100 artigos, selecionar os mais citados, mais recentes, e os que usam dados reais de logística
- **Priorizar artigos de review**: identificar outros artigos de revisão além de Phillipson (2025) para cruzar referências
- Iniciar a construção da **tabela-resumo por artigo** com os artigos selecionados
- Começar a redigir a **Fundamentação Teórica** usando os algoritmos catalogados em `algorithms_reference.md`
