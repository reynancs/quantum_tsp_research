# Justificativa Metodológica — Adoção de Phillipson (2025) como *Anchor Paper*

**Projeto:** Computação Quântica Aplicada ao TSP em Logística
**Programa:** Mestrado Profissional — SENAI CIMATEC
**Fase:** 1 — Exploração Bibliográfica
**Data:** 2026-05-26

---

## Contexto

A busca bibliométrica estruturada na Fase 1 retornou **3.696 artigos únicos** (5.320 registros brutos, 26 *strings* booleanas no Lens.org). A revisão narrativa adotou como artigo de referência **Phillipson (2025) — *Quantum Computing in Logistics and Supply Chain Management: An Overview***, embora esse trabalho não figure no ranking de artigos por citações totais nem por citações/ano. Este documento registra a justificativa metodológica para a escolha, alinhada a boas práticas reconhecidas de revisão bibliográfica.

## Tese central

A análise bibliométrica e o *anchor paper* cumprem **papéis epistemológicos distintos e complementares** em uma revisão exploratória — não competem entre si. Citações são apenas **um** dos critérios de seleção de literatura, e em campos emergentes como Computação Quântica aplicada elas embutem um forte **viés temporal** que justifica adotar critérios alternativos como dominantes.

---

## Cinco argumentos metodológicos

### 1. Distinção entre fontes primárias e secundárias

Em revisões estruturadas (KITCHENHAM; CHARTERS, 2007; PARÉ et al., 2015), **estudos secundários** — *reviews*, *surveys*, *mapping studies* — têm função epistemológica distinta de estudos primários: mapeiam o território e agregam evidência dispersa. Phillipson (2025) cobre aproximadamente 80 trabalhos primários organizados em uma taxonomia funcional (*routing*, *network design*, *fleet maintenance*, *cargo loading*, *prediction*, *scheduling*), o que nenhum artigo individual altamente citado oferece. O ranking de citações lista *primary studies* sobre TSP/QAOA/QA específicos; Phillipson é o *map of the territory* que dá estrutura à revisão.

### 2. Viés temporal sistemático das citações em campos emergentes

Citações apresentam *time lag* de dois a quatro anos para maturar. O ranking "Top 10 por citações/ano" do dashboard bibliométrico compensa parcialmente esse viés, mas mesmo a métrica normalizada subrepresenta trabalhos de 2024–2025. Em Quantum Computing, o estado-da-arte muda em escala anual:

| Período de citações altas | Tecnologia disponível | Status hoje |
|---|---|---|
| 2014–2017 (QAOA original) | D-Wave 2X (~1000 qubits), IBM Q simuladores | Defasado |
| 2018–2020 (Preskill NISQ) | D-Wave Advantage (5000+), IBM Eagle (127) | Parcialmente vigente |
| 2024–2025 | IBM Heron, D-Wave Advantage2, Quantinuum H2 | **Estado-da-arte** |

Phillipson (2025) reflete o terceiro *tier* — invisível no ranking de citações por *design* temporal.

### 3. Estratégia de *anchor paper* + *snowballing* é metodologicamente reconhecida

Wohlin (2014) formaliza o **snowballing** como alternativa ou complemento à busca por base bibliográfica: parte-se de um conjunto inicial de artigos-âncora — selecionados por relevância temática, não por citações — e aplica-se *backward citation tracking* (leitura das referências do âncora) e *forward citation tracking* (leitura de quem cita o âncora). Webster & Watson (2002) — referência clássica da área — defende explicitamente a abordagem *concept-centric* com *seed papers*. O pipeline real da Fase 1 é:

```
Busca bibliométrica (26 strings, Lens.org) → caracterização do campo (3.696 artigos)
                                       ↓
                  Anchor paper (Phillipson 2025) → taxonomia + ~80 referências primárias
                                       ↓
              Backward citation tracking → leitura crítica dos trabalhos referenciados
                                       ↓
              Forward citation tracking  → quem cita Phillipson (leitores recentes)
                                       ↓
                              CORPUS DE SÍNTESE
```

### 4. Critérios de seleção do *anchor paper* documentáveis e defensáveis

Em vez de "alto número de citações", os critérios aplicados a Phillipson (2025) são:

| Critério | Phillipson (2025) atende |
|---|---|
| Atualidade (≤ 12 meses do início da pesquisa) | ✓ |
| Cobertura temática direta (Quantum Computing + Logistics & SCM) | ✓ — mesmo escopo aplicado |
| Escopo abrangente (≥ 50 trabalhos cobertos) | ✓ — ~80 referências |
| Taxonomia funcional reusável | ✓ — 6 subáreas estruturadas |
| Filiação institucional reconhecida | ✓ — TNO / Maastricht University |
| Tipologia: *review* / *survey* / *mapping study* | ✓ — *review* abrangente |

Estes são critérios objetivos de **qualidade de fonte**, não de impacto retroativo. Snyder (2019) os endossa explicitamente para revisões em campos jovens.

### 5. PRISMA-ScR permite fontes adicionais documentadas

A extensão PRISMA para *scoping reviews* (TRICCO et al., 2018) prevê o item *"Sources of evidence"* incluindo *grey literature* e fontes identificadas por busca manual ou recomendação. Phillipson (2025) entra como **fonte adicional documentada** no fluxograma — não compete com os 3.696 da busca; coexiste com eles. Isto é prática-padrão de *scoping reviews*.

---

## Parágrafo redacional para a Seção Metodologia (ABNT, voz passiva)

> A revisão exploratória adotou uma estratégia complementar de duas frentes. A primeira consistiu em uma busca bibliométrica estruturada na base Lens.org (filtro *Scholarly Works*), executada por meio de 26 *strings* booleanas que cruzaram os eixos *Problema* (TSP, VRP e variantes), *Tecnologia* (Computação Quântica, *Quantum Annealing*, QAOA, VQE, abordagens híbridas) e *Aplicação* (Logística, *Supply Chain*, *Route Optimization*), resultando em 5.320 registros brutos consolidados em 3.696 artigos únicos após deduplicação por DOI e título normalizado. A segunda frente seguiu a estratégia de *anchor paper* combinada com *snowballing* (WOHLIN, 2014; WEBSTER; WATSON, 2002), adotando-se Phillipson (2025) — *Quantum Computing in Logistics and Supply Chain Management: An Overview* — como artigo-âncora da síntese narrativa. A escolha do âncora não se baseou em métricas retrospectivas de impacto (citações totais ou citações por ano), uma vez que o trabalho é recente e os indicadores bibliométricos apresentam *time lag* de dois a quatro anos para maturação; aplicaram-se, em substituição, critérios de qualidade de fonte: atualidade (publicação em 2025), aderência temática direta ao escopo Logística/*Supply Chain*, escopo abrangente (cobertura de aproximadamente 80 trabalhos primários), oferta de taxonomia funcional reusável (*routing*, *network design*, *fleet maintenance*, *cargo loading*, *prediction*, *scheduling*) e filiação institucional reconhecida (TNO / Maastricht University). Procederam-se então o *backward citation tracking* sobre as referências do âncora e o *forward citation tracking* sobre os trabalhos que o citam, integrando-se os resultados ao corpus bibliométrico — abordagem alinhada às diretrizes PRISMA-ScR (TRICCO et al., 2018) para *scoping reviews*, que admitem explicitamente a incorporação documentada de fontes complementares.

---

## Referências bibliográficas

KITCHENHAM, B.; CHARTERS, S. **Guidelines for performing Systematic Literature Reviews in Software Engineering**. Keele University Technical Report EBSE-2007-01, 2007.

PARÉ, G.; TRUDEL, M.-C.; JAANA, M.; KITSIOU, S. Synthesizing information systems knowledge: A typology of literature reviews. **Information & Management**, v. 52, n. 2, p. 183–199, 2015.

PHILLIPSON, F. **Quantum Computing in Logistics and Supply Chain Management — An Overview**. Maastricht University / TNO, 2025.

SNYDER, H. Literature review as a research methodology: An overview and guidelines. **Journal of Business Research**, v. 104, p. 333–339, 2019.

TRICCO, A. C. et al. PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. **Annals of Internal Medicine**, v. 169, n. 7, p. 467–473, 2018.

WEBSTER, J.; WATSON, R. T. Analyzing the past to prepare for the future: Writing a literature review. **MIS Quarterly**, v. 26, n. 2, p. xiii–xxiii, 2002.

WOHLIN, C. Guidelines for snowballing in systematic literature studies and a replication in software engineering. In: **Proceedings of the 18th International Conference on Evaluation and Assessment in Software Engineering (EASE)**, 2014.

---

## Notas de uso

- O parágrafo redacional pode ser inserido na Seção 3 (Metodologia) do artigo, idealmente após a descrição da busca bibliométrica e antes da apresentação dos critérios de inclusão/exclusão.
- As referências devem ser incorporadas à lista bibliográfica final, mantendo o padrão de formatação ABNT adotado no artigo.
- Em caso de adoção do padrão IEEE em vez de ABNT, converter as citações no texto para o formato `[número]` e reformatar as entradas bibliográficas.
- A tabela de critérios (Argumento 4) pode ser reaproveitada como Quadro X no corpo do artigo, ilustrando a operacionalização dos critérios de seleção do *anchor paper*.
