# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Pesquisa acadêmica de Mestrado Profissional (SENAI CIMATEC) sobre Computação Quântica aplicada ao **Traveling Salesman Problem (TSP)** e variantes (VRP, CVRP, TSPTW) em Logística. O entregável final é um artigo técnico-científico; o código nesta repo dá suporte à revisão bibliográfica (Fase 1) e à preparação de entregas (resumo expandido, apresentação SAPCT 2026).

Estado atual: **Fase 1 — Exploração Bibliográfica concluída**. 3.696 artigos únicos consolidados a partir de 26 strings de busca executadas no Lens.org.

## Comandos

Os scripts executáveis estão em `src/`. Dependências em `requirements.txt`.

```powershell
# Setup (a partir de PowerShell, na raiz do projeto)
.venv\Scripts\Activate.ps1   # ou: python -m venv .venv ; .venv\Scripts\Activate.ps1 ; pip install -r requirements.txt

# Pipeline da Fase 1 — executar em ordem
python src/deduplicar_artigos.py        # CSVs em data/exportacoes_lens/ → data/artigos_unicos.csv (3.696 linhas)
python src/analise_bibliometrica.py     # data/artigos_unicos.csv → data/resultados_bibliometria/ (9 PNGs)

# Dashboard interativo (7 abas, ~16 gráficos Plotly)
streamlit run src/dashboard_bibliometrico.py
# Acessar em http://localhost:8501

# Geração de entregas
python -X utf8 scripts/gerar_base_algoritmos_v2.py   # Recompila data/base_algoritmos_abordagens.csv
python src/gerar_apresentacao_v2.py                  # Gera docs/Apresentacao_SAPCT_CIMATEC_2026_*.pptx
python src/exportar_imagens.py                       # Exporta gráficos do dashboard como PNG estáticos
```

**Encoding no Windows**: o terminal padrão é cp1252 e quebra com caracteres acentuados. Use `PYTHONIOENCODING=utf-8` ou `python -X utf8` ao rodar scripts que imprimem texto em português. `scripts/gerar_base_algoritmos_v2.py` já força UTF-8 no stdout internamente.

**Não há suíte de testes** — validação se faz rodando o pipeline e inspecionando os artefatos gerados (CSVs, PNGs, dashboard).

## Arquitetura

A repo é organizada por **artefato**, não por camada de código. Os scripts em `src/` são independentes (não há módulos compartilhados) e cada um consome/produz arquivos em `data/`.

### Fluxo de dados (Fase 1)

```
Lens.org (busca manual) → data/exportacoes_lens/string_NN.csv (26 arquivos)
                       → src/deduplicar_artigos.py
                       → data/artigos_unicos.csv (3.696 artigos, fonte única de verdade)
                       → src/analise_bibliometrica.py        → data/resultados_bibliometria/*.png
                       → src/dashboard_bibliometrico.py      → Streamlit (UI interativa)
```

**Pontos de verdade**:
- `data/artigos_unicos.csv` — base completa pós-deduplicação (chaves: DOI normalizado, título normalizado)
- `data/base_algoritmos_abordagens.csv` — taxonomia curada de algoritmos extraídos de Phillipson (2025) + outros artigos
- `data/resumo_por_string.csv` / `data/resumo_deduplicacao.csv` — estatísticas agregadas

### Scripts em `src/`

| Script | Papel | Lê | Escreve |
|--------|-------|----|---------|
| `deduplicar_artigos.py` | Consolida 26 CSVs do Lens.org, deduplica por DOI/título | `data/exportacoes_lens/` | `data/artigos_unicos.csv`, `data/resumo_*.csv` |
| `analise_bibliometrica.py` | Gera 9 gráficos PNG estáticos | `data/artigos_unicos.csv` | `data/resultados_bibliometria/` |
| `dashboard_bibliometrico.py` | Dashboard Streamlit (7 abas, filtros, ~16 gráficos Plotly + WordCloud + choropleth) | `data/artigos_unicos.csv`, `data/base_algoritmos_abordagens.csv` | UI interativa |
| `dashboard_bibliometrico_QML_reference.py` | Variante de referência (QML/Supply Chain) — não usar como base; preferir o principal | idem | idem |
| `analysis_template.py` | Template para Fase 4 (análise de artigos classificados) — ainda não usado em produção | — | — |
| `gerar_apresentacao.py` / `gerar_apresentacao_v2.py` | Constrói .pptx via python-pptx a partir do template `docs/Template_Apresentacao_Oral_SAPCTSLIDES2026B.pptx` e do PDF do resumo expandido | `docs/resumo_final_expandido_SAPCT_CIMATEC_2026.pdf`, `docs/images/` | `docs/Apresentacao_SAPCT_*.pptx` |
| `exportar_imagens.py` | Exporta versões PNG dos gráficos do dashboard para uso em docx/pptx | dataframes do dashboard | `docs/images/` |

`scripts/gerar_base_algoritmos_v2.py` (note: pasta `scripts/`, não `src/`) reconstrói `data/base_algoritmos_abordagens.csv` a partir das 3 tabelas extraídas de Phillipson (2025) páginas 50-52.

### Tema visual do dashboard

Paleta fixa no topo de `src/dashboard_bibliometrico.py` (dict `CORES`, ~linha 70) — qualquer ajuste cromático passa por lá. O tema do Streamlit (`.streamlit/config.toml`) usa `#0077B6` como `primaryColor` para manter consistência. WordCloud renderiza via matplotlib com backend `Agg` (sem GUI). Mapas choropleth dependem de `pycountry` para conversão nome→ISO-3.

### Entregas em `artefatos/` e `docs/`

- `artefatos/` — relatórios markdown (entregas ao orientador): `resumo_pesquisa_bibliografica.md`, `resumo_algoritmos.md`, `criterios_ranking_metodologia.md`, `guia_dashboard_bibliometrico.md`, `perguntas_respostas_banca.md`.
- `docs/referencia_bibliografica/` — PDFs das referências centrais. A principal é **Phillipson (2025) — Quantum Computing in Logistics and Supply Chain Management** (revisão de ~80 artigos; é a fonte da taxonomia em `base_algoritmos_abordagens.csv`).
- `docs/Template_Apresentacao_Oral_SAPCTSLIDES2026B.pptx` — template oficial do evento; os scripts `gerar_apresentacao*.py` o usam como base.
- `docs/tmpl_unpacked/` e `docs/_pdf_extract.txt` — artefatos intermediários do skill `docx` (não editar manualmente; serão regerados).

### `.ai/` — Guias de domínio

Arquivos lidos por skills/agentes ao apoiar a redação do artigo. Tratá-los como **referência de domínio**, não como código:

- `.ai/SKILL.md` — workflow das 5 fases do projeto (Revisão → Fundamentação → Metodologia → Resultados → Artigo). Use como roteiro quando o usuário pedir ajuda em uma fase específica.
- `.ai/keywords_guide.md` — as 26 strings de busca validadas.
- `.ai/algorithms_reference.md` — taxonomia de 40+ algoritmos quânticos (QAOA, VQE, Quantum Annealing, Grover, HHL, híbridos etc.).
- `.ai/writing_style.md` — guia ABNT/IEEE: terceira pessoa, voz passiva, definição de siglas, citações.

## Convenções

- **Idioma**: arquivos de pesquisa (markdown, docstrings, comentários) em **português**; strings de busca e termos técnicos preservados em inglês. Não traduza nomes de algoritmos (QAOA, VQE, etc.).
- **Estilo acadêmico**: ao redigir em `artefatos/` ou `docs/`, seguir `.ai/writing_style.md` (terceira pessoa, voz passiva, sigla expandida na primeira ocorrência).
- **Não há lint/format configurado**. Não introduza black/ruff/mypy sem pedido explícito.
- **Caminhos**: scripts usam `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` para localizar a raiz — preserve esse padrão se criar novos scripts em `src/` ou `scripts/`.
- **Branch**: trabalha-se direto em `main`. Não criar branches sem solicitação.
