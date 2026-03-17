# Computação Quântica Aplicada ao TSP em Logística

Pesquisa acadêmica sobre a aplicação de algoritmos de Computação Quântica ao Problema do Caixeiro Viajante (Traveling Salesman Problem — TSP) e suas variantes, com foco em Logística.

**Programa**: Mestrado Profissional em Gestão de Tecnologia e Inovação — SENAI CIMATEC

---

## Contexto do Problema

O Problema do Caixeiro Viajante (TSP) é um dos problemas clássicos de otimização combinatória: dado um conjunto de cidades e as distâncias entre elas, encontrar a rota mais curta que visite todas as cidades exatamente uma vez e retorne à cidade de origem. O problema é NP-difícil, o que significa que o tempo de resolução cresce exponencialmente com o número de cidades em algoritmos clássicos exatos.

Na logística, o TSP e suas variantes (VRP — Vehicle Routing Problem, CVRP, TSPTW) são fundamentais para otimização de rotas de entrega, distribuição e transporte. Com o avanço da computação quântica, novos paradigmas computacionais — como Quantum Annealing (D-Wave), algoritmos variacionais gate-based (QAOA, VQE) e abordagens híbridas — oferecem potencial para resolver instâncias maiores do TSP de forma mais eficiente.

## Objetivo

Construir um artigo técnico-científico que mapeie, analise e compare os algoritmos quânticos aplicados ao TSP e variantes em contextos logísticos, identificando:

- O estado-da-arte dos algoritmos quânticos para otimização combinatória
- Gaps de pesquisa e oportunidades de contribuição original
- Tendências tecnológicas (hardware, simuladores, abordagens híbridas)
- Aplicabilidade prática em cenários logísticos reais

## Fases do Projeto

| Fase | Descrição | Status |
|------|-----------|--------|
| 1 | Exploração Bibliográfica | Concluída |
| 2 | Fundamentação Teórica | Pendente |
| 3 | Metodologia | Pendente |
| 4 | Resultados e Discussão | Pendente |
| 5 | Montagem Final do Artigo | Pendente |

## Fase 1 — Exploração Bibliográfica

### Como foi estruturada a revisão

A pesquisa bibliográfica foi estruturada em **3 eixos temáticos** combinados com operadores booleanos:

| Eixo | Foco | Exemplos |
|------|------|----------|
| Problema | TSP e variantes | "Traveling Salesman Problem", "Vehicle Routing", "Combinatorial Optimization" |
| Tecnologia | Computação quântica | "Quantum Computing", "Quantum Annealing", "QAOA", "VQE", "QUBO" |
| Aplicação | Logística | "Logistics", "Supply Chain Management", "Route Optimization" |

Foram construídas **26 strings de busca** classificadas em 3 níveis de prioridade (Alta, Média, Baixa) e executadas no Lens.org.

### Passo a passo da pesquisa

1. **Definição de eixos e strings**: 16 strings originais + 10 derivadas da análise do artigo de referência (Phillipson, 2025)
2. **Execução das buscas**: 26 strings no Lens.org com filtro "Scholarly Works" → 5.320 resultados brutos
3. **Exportação**: 26 arquivos CSV exportados para `data/exportacoes_lens/`
4. **Deduplicação**: Script Python removeu duplicatas por DOI e título → **3.696 artigos únicos**
5. **Análise bibliométrica**: Geração de 9 gráficos estáticos + dashboard interativo Streamlit

### Resultados

- **3.696 artigos únicos** após deduplicação (taxa de sobreposição: 30,5%)
- **61,7% publicados a partir de 2020** — campo em crescimento acelerado
- **82,8% em Open Access** — alta acessibilidade
- **49 países** representados, **1.409 fontes** distintas
- **136.407 citações** totais, média de 36,9 por artigo

### Principais Insights

1. **Quantum Annealing domina** a literatura (~800+ artigos), enquanto QAOA/VQE são nicho (~150 artigos) — gap de pesquisa significativo
2. **Abordagens híbridas** (quântico + clássico) são padrão, não exceção
3. **Áreas emergentes pouco publicadas**: QRL (21 artigos), CVRP+QA (18), QML+Supply Chain (79)
4. **Quantum-Inspired** é uma tendência relevante (182 artigos)
5. **81,1% dos artigos** aparecem em apenas 1 string — as buscas são complementares

> O relatório completo da Fase 1 está em [`artefatos/resumo_pesquisa_bibliografica.md`](artefatos/resumo_pesquisa_bibliografica.md)

---

## Estrutura do Projeto

```
quantum_tsp_research/
│
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── .gitignore                         # Arquivos ignorados pelo Git
│
├── .ai/                               # Configurações e guias de IA
│   ├── SKILL.md                       # Guia de workflow do projeto (privado)
│   ├── algorithms_reference.md        # Taxonomia de 40+ algoritmos quânticos
│   ├── keywords_guide.md              # 26 strings de busca validadas
│   └── writing_style.md              # Guia de estilo acadêmico ABNT/IEEE
│
├── src/                               # Scripts Python
│   ├── deduplicar_artigos.py          # Deduplicação dos CSVs do Lens.org
│   ├── analise_bibliometrica.py       # Análise estática (gera gráficos PNG)
│   ├── dashboard_bibliometrico.py     # Dashboard interativo Streamlit
│   └── analysis_template.py           # Template para Fase 4 (artigos classificados)
│
├── data/                              # Dados processados
│   ├── exportacoes_lens/              # 26 CSVs exportados do Lens.org
│   ├── artigos_unicos.csv             # 3.696 artigos após deduplicação
│   ├── resumo_deduplicacao.csv        # Estatísticas de deduplicação
│   ├── resumo_por_string.csv          # Contagem por string de busca
│   ├── base_algoritmos_abordagens.csv # 38 algoritmos/abordagens compilados
│   └── resultados_bibliometria/       # Gráficos PNG da análise estática
│
├── artefatos/                         # Entregas e relatórios
│   ├── resumo_pesquisa_bibliografica.md  # Relatório da Fase 1 (entrega)
│   └── resumo_algoritmos.md           # Resumo de ~80 artigos (Phillipson, 2025)
│
└── docs/                              # Documentos de apoio
    ├── selecao_artigos.txt            # Recomendações de implementação
    ├── pesquisa_palavras_chave_tsp_quantico.xlsx
    ├── selecao_abordagens_tsp_vrp.xlsx
    ├── tabela_resumo_tsp.xlsx
    └── referencia_bibliografica/       # Artigo de referência (Phillipson, 2025)
```

## Como Usar

### Pré-requisitos

- Python 3.10+
- Bibliotecas: `pandas`, `matplotlib`, `plotly`, `streamlit`, `wordcloud`

### Dashboard Interativo

```bash
streamlit run src/dashboard_bibliometrico.py
```

Acesse `http://localhost:8501` no navegador. O dashboard oferece:

- **7 abas**: Visão Geral, Fontes e Autores, Impacto e Citações, Campos de Estudo, Geografia, Strings de Busca, Algoritmos e Abordagens
- **Filtros dinâmicos**: Período, tipo de publicação, string de busca, prioridade, Open Access, citações mínimas
- **16+ gráficos interativos**: stacked bars, donut charts, bubble charts, treemaps, nuvem de palavras, mapa choropleth, heatmap de coocorrência

### Análise Estática (gráficos PNG)

```bash
python src/analise_bibliometrica.py
```

Gera 9 gráficos em `data/resultados_bibliometria/`.

### Reprocessar Deduplicação

```bash
python src/deduplicar_artigos.py
```

Lê os CSVs de `data/exportacoes_lens/` e gera `data/artigos_unicos.csv`.

## Referência Principal

> Phillipson, F. (2025). *Quantum Computing in Logistics and Supply Chain Management — An Overview*. Maastricht University / TNO.

Revisão abrangente de 80+ artigos cobrindo routing, network design, fleet maintenance, cargo loading, prediction e scheduling com abordagens quânticas.
