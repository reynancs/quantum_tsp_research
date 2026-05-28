# Guia Completo — Dashboard Bibliometrico

Documentacao completa do dashboard interativo em Streamlit localizado em
`src/dashboard_bibliometrico.py`.

---

## 1. Visao Geral

O **Dashboard Bibliometrico** e uma aplicacao web interativa que permite explorar
visualmente os **3.696 artigos unicos** identificados na pesquisa bibliografica sobre
**TSP (Travelling Salesman Problem) + Computacao Quantica**, parte do Mestrado
Profissional do SENAI CIMATEC.

O dashboard roda no navegador (Chrome, Firefox, Edge, etc.) e oferece:

- Filtros interativos na barra lateral (periodo, tipo de publicacao, string de busca, etc.)
- KPIs resumidos no topo (total de artigos, citacoes, paises, etc.)
- 7 abas tematicas com graficos interativos (passar o mouse mostra detalhes, zoom, download)
- Tabelas interativas com ordenacao e busca

### Como executar

Abra o terminal na pasta raiz do projeto e rode:

```bash
streamlit run src/dashboard_bibliometrico.py
```

O Streamlit abre automaticamente o navegador em `http://localhost:8501`. Toda vez que
voce salva o arquivo `.py`, o dashboard atualiza automaticamente (basta clicar em
"Rerun" no canto superior direito).

### O que e Streamlit?

Streamlit e uma biblioteca Python que transforma scripts Python em aplicacoes web
interativas. Voce nao precisa saber HTML, CSS ou JavaScript. Cada chamada `st.algo()`
renderiza um elemento na pagina (texto, grafico, tabela, filtro). O Streamlit re-executa
o script inteiro de cima para baixo toda vez que o usuario interage com um widget
(slider, checkbox, etc.).

---

## 2. Fontes de Dados e Uso por Aba

O dashboard carrega **3 fontes de dados**:

| # | Arquivo | Descricao | Onde e usado |
|---|---------|-----------|--------------|
| 1 | `data/artigos_unicos.csv` | 3.696 artigos unicos da pesquisa bibliografica (Lens.org) | Abas 1-6, KPIs, filtros da sidebar |
| 2 | `data/base_algoritmos_abordagens.csv` | 38 algoritmos/abordagens catalogados manualmente | Aba 7 (Algoritmos e Abordagens) |
| 3 | `docs/pesquisa_palavras_chave_tsp_quantico.xlsx` | Planilha com strings de busca completas e totais brutos | Aba 6 (Strings de Busca) — tabela de referencia |

### Uso por aba

| Aba | Fonte de dados | Observacao |
|-----|---------------|------------|
| 1. Visao Geral | `artigos_unicos.csv` (filtrado pela sidebar) | Usa colunas: Publication Year, Publication Type, Is Open Access |
| 2. Fontes e Autores | `artigos_unicos.csv` (filtrado pela sidebar) | Usa colunas: Source Title, Author/s, Publisher |
| 3. Impacto e Citacoes | `artigos_unicos.csv` (filtrado pela sidebar) | Usa colunas: Citing Works Count, Date Published, Title, DOI, strings_origem (para area de aplicacao) |
| 4. Campos de Estudo | `artigos_unicos.csv` (filtrado pela sidebar) | Usa colunas: Fields of Study, Keywords |
| 5. Geografia | `artigos_unicos.csv` (filtrado pela sidebar) | Usa colunas: Source Country (convertido para ISO-3 via pycountry) |
| 6. Strings de Busca | `artigos_unicos.csv` (filtrado) + `pesquisa_palavras_chave_tsp_quantico.xlsx` | O CSV fornece artigos por string; a planilha Excel fornece as strings completas |
| 7. Algoritmos e Abordagens | `base_algoritmos_abordagens.csv` | **Fonte independente** — NAO usa os filtros da sidebar. Tem seus proprios filtros internos |

---

## 3. Arquitetura

O fluxo de dados do dashboard segue 4 camadas:

```
CSV (dados brutos)
    |
    v
pandas DataFrame (limpeza, conversoes, colunas calculadas)
    |
    v
Plotly / matplotlib (criacao dos graficos)
    |
    v
Streamlit (renderiza tudo no navegador)
```

### Camada 1 — Dados (CSV)

O arquivo `data/artigos_unicos.csv` contem os 3.696 artigos. Cada linha e um artigo
com colunas como `Title`, `Author/s`, `Publication Year`, `Citing Works Count`,
`Source Country`, `Is Open Access`, `Fields of Study`, `Keywords`, `strings_origem`
(quais strings de busca encontraram esse artigo), entre outras.

Ha tambem `data/base_algoritmos_abordagens.csv` usado exclusivamente na aba
"Algoritmos e Abordagens".

### Camada 2 — pandas

O pandas le o CSV e faz transformacoes: converte tipos (ano para numerico, data para
datetime), cria colunas calculadas (`strings_lista`, `prioridade`, `qtd_strings`),
e aplica os filtros da sidebar produzindo um DataFrame filtrado.

### Camada 3 — Plotly / matplotlib

O Plotly Express (`px`) e o Plotly Graph Objects (`go`) criam graficos interativos
(barras, pizza, scatter, mapa, heatmap, radar). O matplotlib e usado apenas para a
nuvem de palavras (wordcloud).

### Camada 4 — Streamlit

O Streamlit recebe os graficos e os renderiza no navegador junto com textos, metricas,
filtros e tabelas. Ele cuida de todo o frontend automaticamente.

---

## 4. Referencia Streamlit — Funcoes Usadas

Abaixo estao todas as funcoes do Streamlit utilizadas no dashboard, com explicacao
e exemplo simples.

### Configuracao da Pagina

#### `st.set_page_config()`

Configura titulo, icone, layout e estado da sidebar. **Deve ser a primeira chamada
Streamlit do script.**

```python
st.set_page_config(
    page_title="Meu Dashboard",     # titulo da aba do navegador
    page_icon=":bar_chart:",         # icone da aba (aceita emojis)
    layout="wide",                   # "wide" usa a tela toda, "centered" fica estreito
    initial_sidebar_state="expanded" # sidebar aberta ao carregar
)
```

### Elementos de Texto

#### `st.title()`

Titulo grande no topo da pagina (equivale a `<h1>` em HTML).

```python
st.title("Meu Dashboard")
```

#### `st.subheader()`

Subtitulo menor (equivale a `<h3>`). Usado para nomear secoes e graficos.

```python
st.subheader("Publicacoes ao Longo do Tempo")
```

#### `st.caption()`

Texto pequeno e cinza, usado para notas explicativas e contexto.

```python
st.caption("Fonte: Levantamento bibliografico no Lens.org")
```

#### `st.markdown()`

Renderiza texto em formato Markdown. Suporta negrito, italico, listas, links, etc.

```python
st.markdown("##### Filtros de Algoritmos")   # titulo nivel 5
st.markdown("Texto em **negrito** e *italico*")
```

#### `st.info()`

Caixa de mensagem azul informativa. Usada quando nao ha dados para exibir.

```python
st.info("Nenhum keyword disponivel com os filtros atuais.")
```

#### `st.divider()`

Linha horizontal separadora entre secoes.

```python
st.divider()
```

### Sidebar (Barra Lateral)

#### `st.sidebar`

Tudo que voce chamar via `st.sidebar.algo()` aparece na barra lateral esquerda,
em vez do corpo principal da pagina. A sidebar e usada para filtros.

```python
st.sidebar.header("Filtros")
```

#### `st.sidebar.slider()`

Controle deslizante para selecionar um valor ou intervalo numerico.

```python
ano_range = st.sidebar.slider(
    "Periodo (Ano)",          # label exibido
    min_value=1990,           # valor minimo possivel
    max_value=2025,           # valor maximo possivel
    value=(2018, 2025),       # valor padrao (tupla = range, int = valor unico)
)
# ano_range retorna uma tupla, ex: (2018, 2025)
```

#### `st.sidebar.multiselect()`

Dropdown que permite selecionar multiplas opcoes. Retorna uma lista.

```python
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de Publicacao",           # label
    options=["journal", "preprint"], # opcoes disponiveis
    default=None,                   # nenhuma selecionada inicialmente
    placeholder="Todos os tipos",   # texto quando vazio
)
# tipos_selecionados retorna lista, ex: ["journal"] ou []
```

#### `st.sidebar.radio()`

Botoes de radio — o usuario escolhe apenas UMA opcao.

```python
oa_opcao = st.sidebar.radio(
    "Open Access",
    options=["Todos", "Sim", "Nao"],
    horizontal=True,    # botoes lado a lado (False = vertical)
)
# oa_opcao retorna string, ex: "Todos"
```

### Layout

#### `st.columns()`

Divide a pagina em colunas lado a lado. Retorna objetos de coluna que voce usa
com `with`.

```python
col1, col2 = st.columns(2)    # 2 colunas de largura igual

with col1:
    st.subheader("Coluna Esquerda")
    st.plotly_chart(fig1)

with col2:
    st.subheader("Coluna Direita")
    st.plotly_chart(fig2)
```

Pode receber lista de pesos para colunas desiguais: `st.columns([2, 1])` cria uma
coluna com o dobro da largura da outra.

#### `st.tabs()`

Cria abas de navegacao. Retorna objetos de aba que voce usa com `with`.

```python
tab1, tab2, tab3 = st.tabs(["Visao Geral", "Autores", "Impacto"])

with tab1:
    st.write("Conteudo da primeira aba")

with tab2:
    st.write("Conteudo da segunda aba")
```

### Dados e Graficos

#### `st.metric()`

Exibe um "cartao KPI" com rotulo, valor grande e delta opcional.

```python
st.metric("Total de Artigos", "3.696")
st.metric("Media Citacoes", "12.5", delta="+2.1")   # delta mostra variacao
```

#### `st.plotly_chart()`

Renderiza um grafico Plotly interativo (com hover, zoom, download PNG).

```python
fig = px.bar(df, x="Ano", y="Contagem")
st.plotly_chart(fig, width="stretch")   # width="stretch" ocupa toda a largura
```

#### `st.dataframe()`

Renderiza um DataFrame pandas como tabela interativa (ordenavel, pesquisavel).

```python
st.dataframe(
    df,
    height=400,           # altura em pixels
    width="stretch",      # largura total
    column_config={       # configuracao opcional de colunas
        "DOI": st.column_config.TextColumn(width="large"),
    },
)
```

#### `st.pyplot()`

Renderiza uma figura matplotlib (usado para a nuvem de palavras).

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
st.pyplot(fig)
```

### Cache

#### `@st.cache_data`

Decorador que faz a funcao ser executada apenas uma vez. Nas re-execucoes seguintes
do script (quando o usuario interage com um widget), o resultado e reutilizado da
memoria. Essencial para funcoes que carregam dados de arquivos.

```python
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/artigos.csv")
    return df

# Primeira chamada: le o CSV do disco (lento)
# Chamadas seguintes: retorna da cache (instantaneo)
df = carregar_dados()
```

---

## 5. Referencia Plotly — Tipos de Grafico Usados

O dashboard usa dois modulos do Plotly:
- **`plotly.express` (px)** — API de alto nivel, cria graficos com uma unica chamada
- **`plotly.graph_objects` (go)** — API de baixo nivel, mais controle sobre cada elemento

### `px.bar()` — Grafico de Barras

Barras verticais ou horizontais. Suporta empilhamento (stacked).

```python
# Barras verticais empilhadas
fig = px.bar(df, x="Ano", y="Contagem", color="Tipo")
fig.update_layout(barmode="stack")

# Barras horizontais
fig = px.bar(df, x="Artigos", y="Journal", orientation="h")
```

Parametros-chave:
- `orientation="h"` — barras horizontais
- `color` — coluna para colorir por categoria
- `color_discrete_map` — dicionario de cores por categoria
- `color_discrete_sequence` — lista de cores a usar
- `labels` — renomear eixos: `labels={"x": "Ano", "y": "Artigos"}`
- `hover_data` — colunas extras a mostrar no hover

### `px.scatter()` — Grafico de Dispersao / Bolhas

Pontos no plano cartesiano. Com o parametro `size`, vira grafico de bolhas.

```python
fig = px.scatter(
    df,
    x="Data",
    y="Citacoes",
    size="Citacoes",          # tamanho da bolha proporcional ao valor
    color="Categoria",        # cor por categoria
    size_max=40,              # tamanho maximo das bolhas em pixels
    hover_name="titulo",      # texto principal do hover
)
```

### `px.pie()` — Grafico de Pizza / Donut

Grafico circular de proporcoes. Com `hole`, vira donut.

```python
fig = px.pie(
    values=[60, 30, 10],
    names=["A", "B", "C"],
    hole=0.4,                 # 0 = pizza cheia, 0.4 = donut com furo de 40%
)
fig.update_traces(textposition="inside", textinfo="percent+label")
```

### `px.histogram()` — Histograma

Distribucao de frequencia de uma variavel continua.

```python
fig = px.histogram(
    df, x="Citacoes",
    nbins=50,                 # numero de barras/intervalos
    log_y=True,               # eixo Y em escala logaritmica
)
```

### `px.treemap()` — Treemap

Retangulos aninhados com tamanho proporcional ao valor. Bom para hierarquias.

```python
fig = px.treemap(
    df,
    path=["Campo"],           # coluna de categorias
    values="Frequencia",      # tamanho dos retangulos
    color="Frequencia",       # cor proporcional ao valor
    color_continuous_scale=["#CAF0F8", "#0077B6", "#03045E"],
)
fig.update_traces(textinfo="label+value")
```

### `px.choropleth()` — Mapa Coropletico

Mapa-mundi com paises coloridos por valor.

```python
fig = px.choropleth(
    df,
    locations="ISO3",                  # coluna com codigo ISO-3 do pais
    locationmode="ISO-3",
    color="Artigos",                   # coluna para a intensidade da cor
    color_continuous_scale=["#CAF0F8", "#48CAE4", "#0077B6", "#03045E"],
)
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
)
```

### `go.Heatmap()` — Mapa de Calor

Matriz de valores com cores proporcionais. Usado para coocorrencia de strings e
criterios vs paradigma.

```python
fig = go.Figure(data=go.Heatmap(
    z=matriz,                     # matriz 2D de valores (numpy array ou lista de listas)
    x=labels_colunas,             # rotulos do eixo X
    y=labels_linhas,              # rotulos do eixo Y
    colorscale=[[0, "#FFFFFF"], [0.5, "#48CAE4"], [1, "#03045E"]],
    text=matriz,                  # valores a exibir nas celulas
    texttemplate="%{text}",       # formato do texto
))
```

### `go.Scatterpolar()` — Grafico Radar / Spider

Grafico de radar com eixos radiais. Usado para maturidade por paradigma.

```python
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[4, 3, 5, 2, 4, 4],           # valores (ultimo repete o primeiro para fechar)
    theta=["Vol", "Var", "HW", "Cenarios", "Escala", "Vol"],
    fill="toself",                   # preenche a area do poligono
    name="Quantum Annealing",
    opacity=0.6,
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
)
```

### Opcoes Comuns de Layout

Todos os graficos Plotly aceitam `fig.update_layout()` para ajustar aparencia:

```python
fig.update_layout(
    height=450,                    # altura em pixels
    plot_bgcolor="white",          # fundo branco (padrao e cinza claro)
    showlegend=False,              # ocultar legenda
    barmode="stack",               # empilhar barras
    legend=dict(                   # posicionar legenda
        orientation="h",           # horizontal
        yanchor="bottom", y=1.02,  # acima do grafico
        xanchor="right", x=1,
    ),
    yaxis=dict(autorange="reversed"),  # inverter eixo Y (para bar horizontal)
)

# Personalizar aparencia dos dados (traces)
fig.update_traces(
    text=valores,                  # texto a exibir nas barras
    textposition="outside",        # texto fora da barra
    textinfo="percent+label",      # para graficos de pizza
)

# Configurar eixo X
fig.update_xaxes(dtick=1)         # intervalo de 1 entre marcas no eixo X
```

---

## 6. Estrutura do Codigo

O arquivo `src/dashboard_bibliometrico.py` tem ~1.320 linhas e segue a estrutura:

```
Imports e configuracao de pagina
    |
Constantes (CORES, PALETTE, STRINGS_BUSCA, PRIORIDADES, etc.)
    |
carregar_dados()          --> le CSV, converte tipos, cria colunas calculadas
carregar_algoritmos()     --> le CSV de algoritmos (aba 7)
    |
criar_filtros()           --> sidebar com widgets, retorna DataFrame filtrado
    |
exibir_kpis()             --> linha de metricas KPI no topo
    |
aba_visao_geral()         --> aba 1: temporal, tipos, OA
aba_fontes_autores()      --> aba 2: journals, autores, editoras
aba_impacto()             --> aba 3: bolhas de citacao, histograma, top 20
aba_campos_estudo()       --> aba 4: treemap, wordcloud
aba_geografia()           --> aba 5: mapa mundial, top paises
aba_strings()             --> aba 6: volume por string, sobreposicao, coocorrencia
aba_algoritmos()          --> aba 7: paradigmas, hardware, radar, tabela
    |
main()                    --> ponto de entrada, orquestra tudo
```

### Detalhamento das Funcoes

#### `carregar_dados()`

- Decorada com `@st.cache_data` (carrega uma unica vez)
- Le `data/artigos_unicos.csv` como strings (`dtype=str`)
- Converte `Publication Year`, `Citing Works Count`, `Citing Patents Count`, `qtd_strings`
  para numerico
- Converte `Date Published` para datetime
- Cria `strings_lista` — lista de inteiros com os numeros das strings que encontraram
  o artigo (parseando a coluna `strings_origem` separada por `;`)
- Cria `prioridade` — classifica como Alta/Media/Baixa baseado na primeira string

#### `criar_filtros(df)`

- Exibe widgets na sidebar: slider de periodo, multiselect de tipo/string/prioridade,
  radio de Open Access, slider de citacoes minimas
- Cria uma mascara booleana (`mask`) combinando todos os filtros com `&=`
- Retorna `df[mask].copy()` — o DataFrame filtrado

#### `exibir_kpis(df)`

- Cria 6 colunas com `st.columns(6)`
- Exibe metricas: Total de Artigos, Periodo, Total de Citacoes, Media de Citacoes,
  % Open Access, Numero de Paises

#### `aba_visao_geral(df)`

- Grafico de barras empilhadas: publicacoes por ano, coloridas por tipo
- Grafico de pizza (donut): distribuicao de tipos de publicacao
- Grafico de pizza (donut): Open Access vs Acesso Restrito
- Grafico de barras: tipos de Open Access (gold, green, bronze, hybrid)

#### `aba_fontes_autores(df)`

- Barras horizontais: Top 15 journals/fontes
- Barras horizontais: Top 20 autores mais ativos (conta aparicoes em `Author/s`,
  separados por `;`)
- Barras horizontais: Top 10 editoras (publishers)

#### `aba_impacto(df)`

- Bubble chart: Top 200 artigos mais citados ao longo do tempo
  (eixo X = data, Y = citacoes, tamanho = citacoes, cor = area de aplicacao)
- Histograma: distribuicao de citacoes (escala log no eixo Y)
- Tabela interativa: Top 20 artigos mais citados (titulo, autores, ano, citacoes, DOI)

#### `aba_campos_estudo(df)`

- Treemap: Top 30 campos de estudo (Fields of Study), parseados de coluna separada
  por `;`
- Nuvem de palavras (wordcloud): Top 80 keywords, usando `WordCloud` do matplotlib

#### `aba_geografia(df)`

- Mapa coropletico: distribuicao mundial das publicacoes por pais
  (usa `pycountry` para converter nomes de pais em ISO-3)
- Barras horizontais: Top 15 paises por numero de publicacoes

#### `aba_strings(df)`

- Barras verticais: volume de artigos por string de busca, coloridas por prioridade
- Barras verticais: sobreposicao (quantos artigos aparecem em N strings)
- Heatmap: matriz de coocorrencia entre pares de strings
- Tabela de referencia: lista completa das 26 strings de busca com descricao

#### `aba_algoritmos()`

- **Nota:** esta aba tem seus proprios filtros (paradigma, abordagem, area, variante)
  e carrega um CSV separado (`data/base_algoritmos_abordagens.csv`)
- KPIs: trabalhos, algoritmos distintos, paradigmas, avaliacoes, plataformas HW
- Donuts: distribuicao por paradigma quantico e por abordagem
- Barras empilhadas: evolucao temporal por paradigma
- Barras horizontais: plataformas de hardware, variantes do problema, escala testada,
  formulacao, metricas de avaliacao
- Heatmap: criterios de selecao vs paradigma
- Grafico radar: maturidade por paradigma (5 dimensoes: Volume, Variedade,
  Hardware Real, Cenarios Reais, Escalabilidade)
- Tabela completa: todos os trabalhos catalogados

#### `main()`

- Exibe titulo e caption
- Chama `carregar_dados()` e `criar_filtros()` para obter o DataFrame filtrado
- Chama `exibir_kpis()`
- Cria 7 abas com `st.tabs()` e chama a funcao de cada aba dentro do bloco `with`

---

## 7. Como Modificar — Guia Pratico

### Alterar cores

As cores sao definidas em constantes globais no topo do arquivo.

Para alterar a paleta principal, edite o dicionario `CORES`:

```python
CORES = {
    "primary": "#0077B6",     # azul principal
    "secondary": "#00B4D8",   # azul claro
    "accent": "#90E0EF",      # azul muito claro
    "highlight": "#CAF0F8",   # azul palido
    "dark": "#03045E",        # azul escuro
    "success": "#70AD47",     # verde
    "warning": "#FFC000",     # amarelo
    "danger": "#ED7D31",      # laranja
}
```

Para alterar cores de categorias especificas (ex: tipos de publicacao), edite
`PALETTE_PUB_TYPE`, `PALETTE_PARADIGMA`, `PALETTE_ABORDAGEM`, `COR_PRIORIDADE`
ou `COR_AREA`.

Para alterar a cor de um grafico individual, procure o `color_discrete_sequence`
ou `color_discrete_map` na chamada `px.bar()` / `px.pie()` correspondente.

### Adicionar novo filtro na sidebar

1. Na funcao `criar_filtros()`, adicione o widget desejado:

```python
# Exemplo: filtro por editora
editoras = sorted(df["Publisher"].dropna().unique())
editora_sel = st.sidebar.multiselect(
    "Editora",
    options=editoras,
    default=None,
    placeholder="Todas",
)
```

2. Adicione a logica de filtragem na mascara:

```python
if editora_sel:
    mask &= df["Publisher"].isin(editora_sel)
```

3. O `return df[mask].copy()` ja existente aplica o novo filtro automaticamente.

### Adicionar novo grafico em aba existente

1. Escolha a funcao da aba onde quer adicionar (ex: `aba_visao_geral`)
2. Crie o grafico com Plotly Express:

```python
st.subheader("Meu Novo Grafico")
fig = px.bar(
    df, x="coluna_x", y="coluna_y",
    color_discrete_sequence=[CORES["primary"]],
)
fig.update_layout(height=400, plot_bgcolor="white")
st.plotly_chart(fig, width="stretch")
```

3. Para colocar em colunas lado a lado:

```python
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, width="stretch")
with col2:
    st.plotly_chart(fig2, width="stretch")
```

### Adicionar nova aba

1. Na funcao `main()`, adicione o nome da aba na lista de `st.tabs()`:

```python
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Visao Geral",
    "Fontes e Autores",
    "Impacto e Citacoes",
    "Campos de Estudo",
    "Geografia",
    "Strings de Busca",
    "Algoritmos e Abordagens",
    "Minha Nova Aba",           # <-- adicionado
])
```

2. Crie a funcao da aba:

```python
def aba_minha_nova(df):
    st.subheader("Titulo da Secao")
    # ... seus graficos e tabelas aqui ...
```

3. Conecte a aba na `main()`:

```python
with tab8:
    aba_minha_nova(df_filtrado)
```

### Alterar tamanho de grafico

Procure o `update_layout(height=...)` do grafico e altere o valor em pixels:

```python
fig.update_layout(height=600)   # mais alto
fig.update_layout(height=300)   # mais baixo
```

A largura e controlada pelo `width="stretch"` em `st.plotly_chart()`, que faz o
grafico ocupar toda a largura disponivel.

### Alterar numero de items em ranking

Procure `.head(N)` ou `.nlargest(N, ...)` na funcao da aba e altere o numero:

```python
# Mudar de Top 15 para Top 25 journals
contagem = df["Source Title"].value_counts().head(25)   # era .head(15)

# Mudar de Top 200 para Top 100 artigos no bubble chart
df_bubble_top = df_bubble.nlargest(100, "Citing Works Count")   # era 200
```

---

## 8. Constantes Importantes

Todas definidas no topo do arquivo, antes das funcoes.

### `CORES`

Dicionario com as 8 cores base do dashboard. Todas as cores dos graficos derivam
daqui ou das paletas abaixo. Valores em hexadecimal.

### `PALETTE`

Lista de 10 cores usada como sequencia padrao para graficos categoricos. Inspirada
nos tons do Lens.org.

### `PALETTE_PUB_TYPE`

Mapeamento de tipo de publicacao para cor. Chaves em minusculo
(`"journal article"`, `"preprint"`, etc.).

### `STRINGS_BUSCA`

Dicionario `{numero: descricao}` com as 26 strings de busca usadas no levantamento
bibliografico. Exemplo: `1: "TSP + Quantum Computing"`, `6: "VRP + Quantum Computing"`.

### `PRIORIDADES`

Dicionario `{numero_string: "Alta"/"Media"/"Baixa"}`. Classifica cada string de busca
por prioridade de relevancia para a pesquisa.

### `AREA_APLICACAO`

Dicionario `{numero_string: area}`. Agrupa as 26 strings em 4 areas:
- **TSP** — strings diretamente sobre o Travelling Salesman Problem
- **VRP/Logistica** — Vehicle Routing Problem e logistica
- **Supply Chain/QML** — cadeia de suprimentos e machine learning quantico
- **Otim. Combinatoria** — outros problemas de otimizacao combinatoria

### `COR_AREA`

Dicionario `{area: cor_hex}`. Cores associadas a cada area de aplicacao, usadas
no bubble chart da aba de Impacto.

### `COR_PRIORIDADE`

Dicionario `{prioridade: cor_hex}`. Cores para Alta (laranja), Media (azul), Baixa (cinza).

### `PALETTE_PARADIGMA` e `PALETTE_ABORDAGEM`

Cores para categorias da aba de Algoritmos: paradigma quantico (Quantum Annealing,
Gate-Based, etc.) e abordagem (Hibrida, Quantica, etc.).

---

## 9. Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

As dependencias nao estao instaladas. Rode:

```bash
pip install -r requirements.txt
```

Ou instale individualmente:

```bash
pip install streamlit pandas plotly wordcloud matplotlib pycountry numpy openpyxl
```

### Dashboard demora para carregar

O decorator `@st.cache_data` ja esta aplicado nas funcoes `carregar_dados()` e
`carregar_algoritmos()`. O CSV e lido do disco apenas na primeira execucao; nas
interacoes seguintes, os dados vem da cache.

Se ainda estiver lento, pode ser que os filtros estejam gerando DataFrames muito
grandes. Tente restringir o periodo ou selecionar menos strings de busca.

### Graficos nao aparecem

Verifique se o DataFrame nao esta vazio apos aplicar os filtros. Selecione filtros
menos restritivos. Alguns graficos dependem de colunas que podem ter muitos valores
nulos (ex: `Source Country` para preprints, `Keywords` tem cobertura parcial).

### Porta ja em uso ("Address already in use")

Outro processo Streamlit (ou outra aplicacao) ja esta usando a porta 8501. Rode em
outra porta:

```bash
streamlit run src/dashboard_bibliometrico.py --server.port 8502
```

### Nuvem de palavras nao aparece

A wordcloud depende da coluna `Keywords`. Se os filtros selecionados retornarem
artigos sem keywords preenchidos, a nuvem nao sera gerada e uma mensagem azul
`st.info()` aparecera no lugar.

### Aba "Algoritmos e Abordagens" nao carrega

Esta aba usa um CSV separado (`data/base_algoritmos_abordagens.csv`). Verifique se
o arquivo existe. Note que esta aba tem seus proprios filtros internos (paradigma,
abordagem, area, variante) independentes da sidebar.

### Mapa geografico sem dados

O mapa usa `pycountry` para converter nomes de paises em codigos ISO-3. Paises com
nomes nao reconhecidos pelo `pycountry` sao descartados. A coluna `Source Country`
tambem pode estar vazia para muitos artigos (especialmente preprints).
