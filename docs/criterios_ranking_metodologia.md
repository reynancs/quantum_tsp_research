# Metodologia de Critérios de Seleção e Ranking Ponderado

## 1. Visão Geral

O sistema de ranking ponderado avalia cada trabalho catalogado na base de algoritmos
quânticos (`data/base_algoritmos_abordagens.csv`) com base em **6 critérios de qualidade**.
Cada critério representa uma dimensão relevante para a análise da maturidade e
contribuição científica do trabalho no contexto de computação quântica aplicada
a problemas de otimização em logística.

O resultado é uma **pontuação normalizada de 0 a 100** na coluna `ranking`,
que permite ordenar e comparar trabalhos de forma objetiva.

### 1.1 Origem dos Dados e Processo de Avaliação

Os dados utilizados para a avaliação dos trabalhos foram extraídos exclusivamente do
artigo de referência **Phillipson (2025)** — *"Quantum Computing in Logistics and Supply
Chain Management: an Overview"* — que cataloga mais de 130 abordagens quânticas
aplicadas a problemas de logística e cadeia de suprimentos. **Os trabalhos individuais
não foram acessados diretamente**; toda a informação sobre métricas de qualidade,
escalabilidade, hardware utilizado, taxas de sucesso e demais atributos foi obtida a
partir das descrições, tabelas e análises presentes no artigo de revisão.

**Consequências metodológicas:**

- **Campos "Não Reportada"**: Muitos trabalhos possuem a maioria dos campos preenchidos
  como "Não Reportada", pois o artigo de revisão nem sempre detalha todas as dimensões
  de cada trabalho catalogado. Isso não significa que o trabalho original não contenha
  essas informações — apenas que elas não foram reportadas na fonte secundária utilizada.
- **Viés de fonte única**: Como a avaliação depende do que foi reportado por Phillipson
  (2025), existe um potencial viés de seleção e de profundidade de análise. Trabalhos
  descritos com mais detalhes no artigo de revisão tendem a receber mais critérios
  atendidos e, portanto, rankings mais altos.
- **Limitação de escopo**: Os critérios C1 a C5 foram atribuídos manualmente com base
  na interpretação das informações disponíveis no artigo de referência, enquanto o
  critério C6 (Taxa de Sucesso) é avaliado automaticamente a partir do campo
  `taxa_sucesso` do CSV. Em ambos os casos, a fonte primária é Phillipson (2025).

**Definição dos critérios**: Os seis critérios de avaliação (C1–C6) foram definidos
pelos autores desta pesquisa com o objetivo de capturar dimensões relevantes de
maturidade tecnológica (TRL) de soluções quânticas para otimização logística. Os pesos
foram calibrados de acordo com a relevância prática de cada dimensão para aplicações
reais em logística, priorizando qualidade da solução, aplicabilidade real e taxa de
sucesso reportada.

---

## 2. Critérios de Seleção

| Código | Critério                 | Peso  | Descrição                                                                                                     |
|--------|--------------------------|-------|---------------------------------------------------------------------------------------------------------------|
| C1     | Qualidade da solução     | 2.0   | O trabalho reporta métricas de qualidade com resultados positivos (próximo ao ótimo, superior, competitivo).   |
| C2     | Escalabilidade           | 1.5   | O trabalho testa instâncias de escala variável ou média/grande (não limitado a poucos qubits).                 |
| C3     | Aplicação real           | 2.0   | O trabalho aplica o algoritmo em cenário real ou com dados reais (não apenas benchmarks teóricos).             |
| C4     | Comparação com clássico  | 1.5   | O trabalho compara resultados com algoritmos clássicos de referência.                                          |
| C5     | Análise de limitações    | 1.0   | O trabalho analisa limitações do hardware, sensibilidade a parâmetros ou robustez a ruído.                     |
| C6     | Taxa de sucesso          | 2.0   | O trabalho reporta taxa de sucesso quantitativa (percentual, probabilidade ou avaliação explícita).            |

### 2.1 Justificativa dos Pesos

Os pesos foram definidos com base na relevância prática de cada dimensão para
a avaliação de maturidade tecnológica (TRL) de soluções quânticas:

- **Peso 2.0 (C1, C3, C6)**: Critérios de maior impacto — qualidade da solução,
  aplicabilidade real e taxa de sucesso são essenciais para validar a viabilidade
  de uma abordagem quântica.
- **Peso 1.5 (C2, C4)**: Critérios de relevância intermediária — escalabilidade e
  comparação com clássico são importantes para contextualizar os resultados, mas
  muitos trabalhos estão limitados pelo hardware atual (NISQ).
- **Peso 1.0 (C5)**: Critério complementar — análise de limitações é valorizada,
  mas é mais comum em trabalhos de revisão do que em contribuições experimentais.

---

## 3. Fórmula do Ranking

### 3.1 Cálculo

```
pontuacao_bruta = Σ (criterio_i × peso_i)   para i = C1, C2, ..., C6

onde criterio_i = 1 se o critério é atendido, 0 caso contrário
```

### 3.2 Normalização

```
pontuacao_maxima = Σ pesos = 2.0 + 1.5 + 2.0 + 1.5 + 1.0 + 2.0 = 10.0

ranking = (pontuacao_bruta / pontuacao_maxima) × 100
```

### 3.3 Escala

| Faixa         | Interpretação                                    |
|---------------|--------------------------------------------------|
| 0             | Nenhum critério atendido (dados insuficientes)   |
| 1 – 20        | Avaliação mínima (1 critério)                    |
| 21 – 40       | Avaliação parcial (2 critérios)                  |
| 41 – 60       | Avaliação moderada (3 critérios)                 |
| 61 – 80       | Avaliação boa (4-5 critérios)                    |
| 81 – 100      | Avaliação excelente (5-6 critérios)              |

---

## 4. Critério C6 — Avaliação Automática

O critério **C6 (Taxa de Sucesso)** é o único critério avaliado automaticamente
pelo script `scripts/gerar_base_algoritmos_v2.py`. A lógica é:

```python
def avaliar_c6_taxa_sucesso(taxa: str) -> bool:
    """Retorna True se o trabalho reporta taxa de sucesso."""
    if taxa é nula ou vazia:
        return False
    if taxa == "Nao Reportada" ou "Nao reportado":
        return False
    # Qualquer valor concreto (percentual, avaliação qualitativa, etc.)
    return True
```

**Exemplos de valores que atendem C6:**
- `"91%"` — percentual explícito
- `"94% F1"` — métrica com valor
- `"Baixa (quantico)"` — avaliação qualitativa (reportada, mesmo que baixa)
- `"QAOA baixa / VQE moderada"` — comparação entre algoritmos

**Exemplos de valores que NÃO atendem C6:**
- `"Nao Reportada"` — sem informação
- `"Nao reportado"` — variação sem informação
- `""` — vazio

Os demais critérios (C1–C5) são atribuídos manualmente na coluna `criterios`
do CSV antigo (`data/base_algoritmos_abordagens_OLD.csv`) e herdados via
mapeamento de autores.

---

## 5. Exemplo Prático

| Autor          | Critérios    | Cálculo                                       | Ranking |
|----------------|--------------|------------------------------------------------|---------|
| Azzaoui [13]   | C1, C3, C6   | (2.0 + 2.0 + 2.0) / 10.0 × 100 = 60          | 60      |
| Sales [129]    | C1, C2, C3   | (2.0 + 1.5 + 2.0) / 10.0 × 100 = 55          | 55      |
| Khumalo [75]   | C4, C5, C6   | (1.5 + 1.0 + 2.0) / 10.0 × 100 = 45          | 45      |
| Feld [49]      | C1, C2       | (2.0 + 1.5) / 10.0 × 100 = 35                | 35      |
| Azad [12]      | C4, C5       | (1.5 + 1.0) / 10.0 × 100 = 25                | 25      |
| Cattelan [29]  | (nenhum)     | 0.0 / 10.0 × 100 = 0                          | 0       |

---

## 6. Arquivos Relacionados

| Arquivo                                  | Descrição                                            |
|------------------------------------------|------------------------------------------------------|
| `scripts/gerar_base_algoritmos_v2.py`    | Script que gera o CSV, aplica C6 e calcula ranking   |
| `data/base_algoritmos_abordagens.csv`    | CSV final com coluna `criterios` e `ranking`         |
| `data/base_algoritmos_abordagens_OLD.csv`| CSV antigo com critérios C1-C5 originais             |
| `src/dashboard_bibliometrico.py`         | Dashboard com filtro de critérios e tabela ranking    |

---

## 7. Como Modificar

### Alterar pesos dos critérios

No arquivo `scripts/gerar_base_algoritmos_v2.py`, edite o dicionário `PESOS_CRITERIOS`:

```python
PESOS_CRITERIOS = {
    "C1": 2.0,  # Qualidade da solução
    "C2": 1.5,  # Escalabilidade
    "C3": 2.0,  # Aplicação real
    "C4": 1.5,  # Comparação com clássico
    "C5": 1.0,  # Análise de limitações
    "C6": 2.0,  # Taxa de sucesso
}
```

Após alterar, execute o script para regenerar o CSV:

```bash
python -X utf8 scripts/gerar_base_algoritmos_v2.py
```

### Adicionar novo critério (C7, C8...)

1. Adicione a entrada no dicionário `PESOS_CRITERIOS`
2. Implemente a lógica de avaliação (manual ou automática)
3. Atualize `CRITERIOS_DESCRICAO` em `src/dashboard_bibliometrico.py`
4. Regenere o CSV

### Atribuir critérios C1-C5 manualmente

Edite a coluna `criterios` no arquivo `data/base_algoritmos_abordagens_OLD.csv`
para os autores correspondentes. O script faz o merge automático.
