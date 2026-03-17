# Computacao Quantica Aplicada ao TSP em Logistica

Pesquisa academica sobre a aplicacao de algoritmos de Computacao Quantica ao Problema do Caixeiro Viajante (Traveling Salesman Problem — TSP) e suas variantes, com foco em Logistica.

**Programa**: Mestrado Profissional em Gestao de Tecnologia e Inovacao — SENAI CIMATEC

---

## Contexto do Problema

O Problema do Caixeiro Viajante (TSP) e um dos problemas classicos de otimizacao combinatoria: dado um conjunto de cidades e as distancias entre elas, encontrar a rota mais curta que visite todas as cidades exatamente uma vez e retorne a cidade de origem. O problema e NP-dificil, o que significa que o tempo de resolucao cresce exponencialmente com o numero de cidades em algoritmos classicos exatos.

Na logistica, o TSP e suas variantes (VRP — Vehicle Routing Problem, CVRP, TSPTW) sao fundamentais para otimizacao de rotas de entrega, distribuicao e transporte. Com o avanco da computacao quantica, novos paradigmas computacionais — como Quantum Annealing (D-Wave), algoritmos variacionais gate-based (QAOA, VQE) e abordagens hibridas — oferecem potencial para resolver instancias maiores do TSP de forma mais eficiente.

## Objetivo

Construir um artigo tecnico-cientifico que mapeie, analise e compare os algoritmos quanticos aplicados ao TSP e variantes em contextos logisticos, identificando:

- O estado-da-arte dos algoritmos quanticos para otimizacao combinatoria
- Gaps de pesquisa e oportunidades de contribuicao original
- Tendencias tecnologicas (hardware, simuladores, abordagens hibridas)
- Aplicabilidade pratica em cenarios logisticos reais

## Fases do Projeto

| Fase | Descricao | Status |
|------|-----------|--------|
| 1 | Exploracao Bibliografica | Concluida |
| 2 | Fundamentacao Teorica | Pendente |
| 3 | Metodologia | Pendente |
| 4 | Resultados e Discussao | Pendente |
| 5 | Montagem Final do Artigo | Pendente |

## Fase 1 — Exploracao Bibliografica

### Como foi estruturada a revisao

A pesquisa bibliografica foi estruturada em **3 eixos tematicos** combinados com operadores booleanos:

| Eixo | Foco | Exemplos |
|------|------|----------|
| Problema | TSP e variantes | "Traveling Salesman Problem", "Vehicle Routing", "Combinatorial Optimization" |
| Tecnologia | Computacao quantica | "Quantum Computing", "Quantum Annealing", "QAOA", "VQE", "QUBO" |
| Aplicacao | Logistica | "Logistics", "Supply Chain Management", "Route Optimization" |

Foram construidas **26 strings de busca** classificadas em 3 niveis de prioridade (Alta, Media, Baixa) e executadas no Lens.org.

### Passo a passo da pesquisa

1. **Definicao de eixos e strings**: 16 strings originais + 10 derivadas da analise do artigo de referencia (Phillipson, 2025)
2. **Execucao das buscas**: 26 strings no Lens.org com filtro "Scholarly Works" → 5.320 resultados brutos
3. **Exportacao**: 26 arquivos CSV exportados para `data/exportacoes_lens/`
4. **Deduplicacao**: Script Python removeu duplicatas por DOI e titulo → **3.696 artigos unicos**
5. **Analise bibliometrica**: Geracao de 9 graficos estaticos + dashboard interativo Streamlit

### Resultados

- **3.696 artigos unicos** apos deduplicacao (taxa de sobreposicao: 30,5%)
- **61,7% publicados a partir de 2020** — campo em crescimento acelerado
- **82,8% em Open Access** — alta acessibilidade
- **49 paises** representados, **1.409 fontes** distintas
- **136.407 citacoes** totais, media de 36,9 por artigo

### Principais Insights

1. **Quantum Annealing domina** a literatura (~800+ artigos), enquanto QAOA/VQE sao nicho (~150 artigos) — gap de pesquisa significativo
2. **Abordagens hibridas** (quantico + classico) sao padrao, nao excecao
3. **Areas emergentes pouco publicadas**: QRL (21 artigos), CVRP+QA (18), QML+Supply Chain (79)
4. **Quantum-Inspired** e uma tendencia relevante (182 artigos)
5. **81,1% dos artigos** aparecem em apenas 1 string — as buscas sao complementares

> O relatorio completo da Fase 1 esta em [`artefatos/resumo_pesquisa_bibliografica.md`](artefatos/resumo_pesquisa_bibliografica.md)

---

## Estrutura do Projeto

```
quantum_tsp_research/
│
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependencias Python
├── .gitignore                         # Arquivos ignorados pelo Git
│
├── .ai/                               # Configuracoes e guias de IA
│   ├── SKILL.md                       # Guia de workflow do projeto (privado)
│   ├── algorithms_reference.md        # Taxonomia de 40+ algoritmos quanticos
│   ├── keywords_guide.md              # 26 strings de busca validadas
│   └── writing_style.md              # Guia de estilo academico ABNT/IEEE
│
├── src/                               # Scripts Python
│   ├── deduplicar_artigos.py          # Deduplicacao dos CSVs do Lens.org
│   ├── analise_bibliometrica.py       # Analise estatica (gera graficos PNG)
│   ├── dashboard_bibliometrico.py     # Dashboard interativo Streamlit
│   └── analysis_template.py           # Template para Fase 4 (artigos classificados)
│
├── data/                              # Dados processados
│   ├── exportacoes_lens/              # 26 CSVs exportados do Lens.org
│   ├── artigos_unicos.csv             # 3.696 artigos apos deduplicacao
│   ├── resumo_deduplicacao.csv        # Estatisticas de deduplicacao
│   ├── resumo_por_string.csv          # Contagem por string de busca
│   ├── base_algoritmos_abordagens.csv # 38 algoritmos/abordagens compilados
│   └── resultados_bibliometria/       # Graficos PNG da analise estatica
│
├── artefatos/                         # Entregas e relatorios
│   ├── resumo_pesquisa_bibliografica.md  # Relatorio da Fase 1 (entrega)
│   └── resumo_algoritmos.md           # Resumo de ~80 artigos (Phillipson, 2025)
│
└── docs/                              # Documentos de apoio
    ├── selecao_artigos.txt            # Recomendacoes de implementacao
    ├── pesquisa_palavras_chave_tsp_quantico.xlsx
    ├── selecao_abordagens_tsp_vrp.xlsx
    ├── tabela_resumo_tsp.xlsx
    └── referencia_bibliografica/       # Artigo de referencia (Phillipson, 2025)
```

## Como Usar

### Pre-requisitos

- Python 3.10+
- Bibliotecas: `pandas`, `matplotlib`, `plotly`, `streamlit`, `wordcloud`

### Dashboard Interativo

```bash
streamlit run src/dashboard_bibliometrico.py
```

Acesse `http://localhost:8501` no navegador. O dashboard oferece:

- **6 abas**: Visao Geral, Fontes e Autores, Impacto e Citacoes, Campos de Estudo, Geografia, Strings de Busca
- **Filtros dinamicos**: Periodo, tipo de publicacao, prioridade, Open Access, citacoes minimas
- **16 graficos interativos**: stacked bars, donut charts, bubble charts, treemaps, nuvem de palavras, mapa choropleth, heatmap de coocorrencia

### Analise Estatica (graficos PNG)

```bash
python src/analise_bibliometrica.py
```

Gera 9 graficos em `data/resultados_bibliometria/`.

### Reprocessar Deduplicacao

```bash
python src/deduplicar_artigos.py
```

Le os CSVs de `data/exportacoes_lens/` e gera `data/artigos_unicos.csv`.

## Referencia Principal

> Phillipson, F. (2025). *Quantum Computing in Logistics and Supply Chain Management — An Overview*. Maastricht University / TNO.

Revisao abrangente de 80+ artigos cobrindo routing, network design, fleet maintenance, cargo loading, prediction e scheduling com abordagens quanticas.
