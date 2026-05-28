# Possíveis perguntas da banca avaliadora — Q&A

**Trabalho:** Aplicação de Quantum Annealing ao Problema do Caixeiro Viajante — revisão exploratória da literatura em logística
**Autor:** Renan Cardoso dos Santos
**Evento:** XI SAPCT — SENAI CIMATEC · 28 e 29 de Maio de 2026

Documento de apoio para a apresentação oral. Reúne perguntas prováveis da
banca avaliadora e respostas estruturadas, com foco especial na justificativa
do uso de Phillipson (2025) como referência analítica.

---

## 1. Sobre o uso de Phillipson (2025) como referência analítica

> **Phillipson, F.** *Quantum Computing in Logistics and Supply Chain
> Management: an overview.* Maastricht University / TNO, 2025.

### 1.1  Pergunta-chave

> **"Qual a justificativa de ter realizado a análise dos tipos de abordagens
> e algoritmos usando o artigo de Phillipson (2025) como referência?"**

### Resposta sugerida (versão "falada", ~1 minuto)

A escolha do artigo de Phillipson (2025) como referência analítica para a
classificação de algoritmos e abordagens não foi por autoridade, mas por
**quatro razões metodológicas convergentes**:

1. **Pertinência temática exata.** É um *overview* publicado em coautoria
   entre uma universidade (Maastricht) e um instituto de pesquisa aplicada
   de referência na Europa (TNO), e se posiciona precisamente na
   intersecção dos três eixos desta revisão: **problema combinatório**,
   **tecnologia quântica** e **aplicação logística**. Não é uma revisão
   genérica de computação quântica nem uma revisão genérica de logística —
   é o *crossover* exato do nosso recorte.

2. **Atualidade.** Em um campo que dobra de volume a cada dois anos, usar
   uma referência de **2025** garante que a taxonomia incorpore os avanços
   mais recentes — D-Wave Advantage com conectividade Pegasus, *hybrid
   solvers*, evolução do QAOA — que uma revisão anterior simplesmente não
   capturaria.

3. **Taxonomia citável e reprodutível.** Phillipson sistematiza os
   algoritmos em categorias já validadas por revisão por pares — paradigma,
   abordagem e problema. Ao adotá-la como lente, garantimos que nossa
   classificação seja **comparável** com a literatura corrente e
   **replicável** por terceiros — algo que uma taxonomia *ad-hoc*,
   construída só por nós, não asseguraria.

4. **Dupla função metodológica.** Phillipson cumpriu dois papéis no
   protocolo: (a) **baseline conceitual** para classificar os paradigmas e
   abordagens encontrados nos artigos; e (b) **fonte das 10 strings
   adicionais da segunda fase da busca** — ampliando a sensibilidade do
   levantamento para termos que a taxonomia inicial do projeto poderia não
   cobrir.

**Em síntese:** Phillipson combina atualidade, pertinência temática exata,
taxonomia validada e dupla função metodológica — características raramente
reunidas em um único artigo de revisão deste tema.

### Perguntas-derivadas e contra-argumentos

| Se a banca perguntar… | Você pode responder… |
|---|---|
| **"E se a taxonomia do Phillipson estiver enviesada?"** | "Justamente por isso a confrontamos com a taxonomia inicial do projeto e com o que emergiu dos próprios artigos classificados. É uma **triangulação**, não uma adoção cega — e a coincidência entre as duas fontes reforça a validade construtiva." |
| **"Por que não usar mais artigos de revisão como referência analítica?"** | "Foram considerados, mas nenhum outro reunia simultaneamente recorte de logística/SCM, cobertura ampla de paradigmas quânticos e publicação recente. Phillipson é tratado como **referência analítica**, não como fonte primária — os 3.696 artigos do corpus seguem sendo a base empírica." |
| **"Por que isso aparece só na segunda fase da metodologia?"** | "É deliberado. A primeira fase usou a taxonomia interna do projeto para evitar *anchoring*; a segunda fase incorporou Phillipson como instrumento de triangulação e como expansão lexical. Essa ordem reduz o risco de a revisão simplesmente espelhar o autor de referência." |
| **"Qual a limitação dessa escolha?"** | "Reconhecemos a dependência de um *overview* único como lente classificatória — é uma limitação metodológica explícita. Mitigamos com (a) a fase 1 independente, (b) a deduplicação rigorosa do corpus e (c) o caráter exploratório da revisão, que não pretende ser exaustiva, mas mapeadora." |

---

### 1.2  Pergunta de leitura crítica do texto de Phillipson

> **"Na página 4 Phillipson afirma 'an overview of over 80 published papers',
> mas as tabelas a partir da página 50 listam bem mais do que isso —
> e o CSV `base_algoritmos_abordagens.csv` tabula 129 entradas. Como
> vocês explicam essa discrepância?"**

Esta é uma **pergunta de leitura crítica** — testa se você leu o artigo
em profundidade ou apenas o resumo. Demonstrar que você notou a divergência
e tem uma explicação racional é altamente valorizado pela banca.

#### Fatos numéricos verificados

| Fonte | Quantidade | Observação |
|---|---|---|
| Texto de Phillipson (p. 4) | **"over 80"** | *claim* conservador / *lower bound* |
| Tabelas (apêndice, a partir da p. 50) | **≈ 128 papers únicos** | contagem real das referências |
| Nosso CSV (`base_algoritmos_abordagens.csv`) | **129 linhas / 131 citações** | granularidade *paper × tópico × problema* |

Verificação no nosso CSV (executável e reproduzível):

- **129 linhas** (entradas tabeladas);
- **131 citações** de referência (duas linhas agregam pares: `[123,124]` e
  `[64,145]`);
- **128 papers únicos** após deduplicação por número de referência;
- **3 papers reaparecem em múltiplos tópicos** (mesmo *paper*,
  aplicações diferentes):
  - **Ajagekar [4]** — Routing (VRP) + Scheduling (JSP) + Scheduling (MCFP)
  - **Khumalo [75]** — Routing (TSP) + Network Design (FLP)

#### Resposta sugerida (versão "falada", ~1 minuto)

> "É uma observação acurada — e que, longe de fragilizar, **fortalece** o
> uso de Phillipson como referência analítica. Nós verificamos: o texto
> diz 'mais de 80' (*over 80*), mas as tabelas listam cerca de **128 papers
> únicos**. O nosso CSV registra **129 entradas** porque três papers — como
> o Ajagekar [4] e o Khumalo [75] — aparecem em mais de um tópico,
> tratando problemas diferentes; e duas linhas agregam pares de referências
> citados em conjunto.
>
> A divergência tem três explicações plausíveis:
>
> Primeiro, defasagem editorial. É padrão em revisões de literatura que o
> resumo e a introdução sejam escritos numa fase inicial — quando o autor
> tinha um mapeamento parcial — e que as tabelas cresçam ao longo da
> revisão por pares. A frase '*over 80*' segue **tecnicamente verdadeira**
> (128 é mais que 80) sem precisar ser atualizada.
>
> Segundo, retórica conservadora. *Lower bounds* aproximados são preferidos
> em prosa acadêmica: 'mais de 80' é defensável e memorável; um número
> exato como '127' é mais frágil — basta uma citação esquecida para se
> tornar incorreto.
>
> Terceiro, granularidade. A nossa contagem de 129 entradas reflete
> deliberadamente combinações *paper × tópico × problema*, porque essa
> granularidade é necessária para a análise paradigma × algoritmo × tipo
> de problema que apresentamos.
>
> Em vez de invalidar a referência, a descoberta significa que a base
> catalogada é cerca de **60% maior do que o próprio autor anuncia** — o
> que aumenta o valor do *overview* como instrumento analítico."

#### Perguntas-derivadas

| Se a banca insistir… | Você pode responder… |
|---|---|
| **"Vocês não acharam isso preocupante / não consultaram o autor?"** | "Avaliamos se essa divergência configurava erro metodológico ou apenas conservadorismo retórico. A magnitude (128 ≈ 1,6× o claim) e o padrão de crescimento típico de revisões durante peer review apontam para a segunda hipótese. Considerou-se desnecessário contatar o autor — a auditoria das tabelas é reprodutível por qualquer revisor." |
| **"Por que vocês mantiveram as 3 entradas duplicadas no CSV?"** | "São deliberadas — não são duplicatas, são **registros multi-aplicação**. O paper do Ajagekar, por exemplo, propõe um framework de QA aplicado a três problemas distintos (VRP, JSP, MCFP). Eliminá-los descartaria informação relevante para a análise por *problema*. A deduplicação ocorre quando contamos *papers únicos* (128), não quando contamos *aplicações* (129)." |
| **"E se houver papers nas tabelas que não estão na revisão completa do texto?"** | "É possível — e nesse caso, as tabelas seriam o catálogo mais completo. Nossa análise se ancorou nas tabelas justamente por essa razão: são o registro estruturado mais exaustivo, padronizado por campos (paradigma, algoritmo, problema, hardware) — formato adequado para análise quantitativa." |
| **"Esse achado não deveria ser reportado no trabalho?"** | "Pode e deve ser. Em uma versão expandida (dissertação completa), é apropriado registrar como nota metodológica: a base analítica derivada das tabelas de Phillipson contém ~128 papers, mais do que o claim conservador de '*over 80*' do texto. Isso documenta a rigorosidade da extração." |

#### Pontos a comunicar à banca

1. **Demonstra leitura profunda** — não dependemos do resumo/introdução do
   autor; auditamos as tabelas.
2. **Demonstra rigor de extração** — nossa contagem (129 linhas, 128 papers)
   é reprodutível a partir do CSV publicado no repositório.
3. **Não fragiliza a referência** — pelo contrário, mostra que a base
   catalogada é mais robusta do que o texto sugere.
4. **Justifica a granularidade do nosso CSV** — preservar duplicidades
   intencionais (mesmo paper em tópicos diferentes) é metodologicamente
   correto para análises por aplicação.

---

## 2. Sobre o tema e a justificativa do trabalho

### 2.1  "Por que estudar TSP especificamente, e não outros problemas de roteamento?"

O TSP é o problema canônico de otimização combinatória NP-Hard usado como
**benchmark** na área. Resolver o TSP eficientemente abre caminho para
variantes mais complexas e realistas (TSPTW, VRP, CVRP). Além disso, o TSP
tem uma formulação QUBO bem estabelecida, o que o torna o caso de teste
natural para *quantum annealing*.

### 2.2  "Por que Quantum Annealing e não algoritmos gate-based (QAOA / VQE)?"

Três motivos:

1. **Maturidade do hardware.** O D-Wave Advantage já oferece 5.640 qubits
   com conectividade Pegasus, enquanto sistemas gate-based ainda operam na
   era NISQ com poucas dezenas de qubits úteis.
2. **Aplicabilidade direta.** O QA recebe diretamente formulações QUBO/Ising,
   sem necessidade de circuitos quânticos profundos.
3. **Evidência empírica.** A própria revisão confirma — mais de 1.200 artigos
   em QA contra ≈ 150 em QAOA/VQE aplicados ao TSP. O QA é hoje o paradigma
   mais utilizado, embora os gate-based representem uma fronteira promissora
   (e uma das lacunas identificadas).

### 2.3  "Qual é a relevância prática para a logística brasileira?"

A logística representa parcela significativa do custo operacional no Brasil
(setor estratégico para o SENAI CIMATEC e para a indústria nacional).
Avanços em otimização de rotas — mesmo incrementais — têm impacto direto em
eficiência, consumo de combustível e tempo de entrega. Mapear o estado da
arte em QA aplicado ao TSP é um passo necessário para futuras provas de
conceito em cenários brasileiros.

---

## 3. Sobre a metodologia

### 3.1  "Por que escolheram a base Lens.org e não Scopus, Web of Science ou Google Scholar?"

- **Cobertura ampla e gratuita.** Lens.org agrega Microsoft Academic, Crossref,
  PubMed, CORE e patentes, oferecendo cobertura comparável a bases pagas.
- **API e exportação estruturada** que permitiram automação da deduplicação.
- **Filtro Scholarly Works** que separa publicações acadêmicas de outros
  registros, garantindo qualidade da base.
- **Reprodutibilidade.** Por ser de acesso aberto, qualquer revisor pode
  replicar as 26 *strings* de busca.

### 3.2  "Como foi feita a deduplicação? Como garantir que não há artigos duplicados restantes?"

A deduplicação ocorreu em **duas etapas sequenciais**:

1. **Por DOI** — identificador único e canônico, elimina duplicatas exatas.
2. **Por título normalizado** — para artigos sem DOI (típicos de
   *preprints* arXiv ou *conference proceedings*); o título foi
   normalizado (minúsculas, sem pontuação, sem espaços extras) antes da
   comparação.

A taxa de duplicatas (**30,5%**, 1.624 registros) é coerente com a
literatura de bibliometria, indicando boa cobertura cruzada entre as 26
strings (complementaridade) e baixa taxa de falsos negativos.

### 3.3  "Por que 26 strings de busca? Como vocês definiram esse número?"

O número não é arbitrário — resulta de uma matriz combinatória dos três
eixos temáticos (problema × tecnologia × aplicação), priorizada por
relevância semântica direta ao tema central:

- **8 strings de prioridade Alta** — TSP/VRP diretamente combinados com QA,
  QAOA, VQE, Grover.
- **10 strings de prioridade Média** — variantes do problema combinadas com
  formulações QUBO/Ising e hardware específico (D-Wave, IBM).
- **8 strings de prioridade Baixa** — termos correlatos (Job Shop,
  Bin Packing, Facility Location, QML).

O número foi calibrado para **maximizar recall sem inflar ruído**.

### 3.4  "Como vocês validaram a qualidade da classificação dos algoritmos?"

A classificação foi feita em duas etapas:

1. **Categorização automática** com base nos termos das *strings* que
   originaram cada artigo (cada artigo carrega a *string* de origem).
2. **Refinamento manual** sobre a sub-amostra de 129 trabalhos
   catalogados em detalhe (paradigma, abordagem, algoritmo, problema),
   confrontada com a taxonomia de Phillipson (2025).

A próxima etapa da pesquisa (mestrado) inclui validação cruzada com
*inter-rater reliability* sobre uma amostra randomizada.

---

## 4. Sobre os resultados

### 4.1  "Como interpretar os 82,8% de Open Access?"

É um indicador positivo de **maturidade da ciência aberta** no campo. Reflete:

- Forte presença de *preprints* (arXiv) — característica de áreas próximas à
  física e ciência da computação.
- Adesão crescente de periódicos a modelos *Gold Open Access*.
- Favorece **reprodutibilidade** e replicação dos experimentos quânticos —
  fundamental para o avanço do campo.

### 4.2  "O pico em 2025 não pode ser viés de coleta (data corte)?"

Boa observação. A coleta foi realizada em **maio de 2025**, então o ano
2025 ainda está em curso e a contagem é parcial. Mesmo assim:

- O volume de 2025 já supera 2024 em número absoluto.
- A tendência de 2020–2024 é consistentemente crescente.
- A conclusão de "campo em expansão" não depende exclusivamente do dado de
  2025.

### 4.3  "Por que QA tem mais de 1.200 artigos, mas o gráfico de paradigma mostra só 63 QA?"

São duas visões complementares com cardinalidades diferentes:

- **>1.200 artigos** = corpus completo, classificado pelas *strings* de
  busca que diretamente mencionam QA.
- **63 QA no gráfico** = amostra de **129 trabalhos catalogados em
  profundidade** (paradigma, abordagem, algoritmo específico, problema
  específico) por análise detalhada de conteúdo.

Os gráficos de paradigma, abordagem e algoritmos mostram a **distribuição
relativa** dentro dessa amostra qualitativa; o "> 1.200" é a contagem
bruta do corpus quantitativo.

### 4.4  "Como vocês chegaram nas 4 lacunas? Esse número é resultado da análise ou foi pré-definido?"

As lacunas **emergiram do confronto** entre:

1. O que Phillipson (2025) aponta como áreas pouco exploradas.
2. O que os números do corpus efetivamente mostram (ex.: 21 artigos de QRL,
   18 de CVRP + QA).
3. A escassez de validação com dados logísticos reais (predominância de
   benchmarks acadêmicos como TSPLIB).

Não foi um número pré-definido — foram as quatro lacunas que se mostraram
**estatisticamente sub-representadas e tematicamente relevantes**.

---

## 5. Sobre conceitos técnicos

### 5.1  "Explique o que é QUBO em uma frase."

*Quadratic Unconstrained Binary Optimization* — é uma formulação matemática
que expressa um problema de otimização como a minimização de uma função
quadrática sobre variáveis binárias (0/1), **sem restrições explícitas**
(as restrições são incorporadas como penalidades na função objetivo). É a
forma canônica aceita pelos *annealers* da D-Wave.

### 5.2  "O que diferencia Quantum Annealing de Quantum Approximate Optimization Algorithm (QAOA)?"

| Aspecto | Quantum Annealing | QAOA |
|---|---|---|
| Hardware | Analógico (D-Wave) | Gate-based (IBM Q, Rigetti) |
| Operação | Evolução adiabática contínua | Circuito quântico com camadas $p$ |
| Maturidade | Mais maduro, milhares de qubits | NISQ, dezenas de qubits úteis |
| Input | QUBO/Ising | Hamiltoniano e ansatz $\beta, \gamma$ |
| Escalabilidade atual | Maior (problemas com milhares de variáveis) | Menor (limitada pela profundidade do circuito) |

### 5.3  "Por que o TSP é NP-Hard? E o que isso significa na prática?"

NP-Hard significa que **não existe algoritmo conhecido capaz de resolvê-lo
em tempo polinomial** no pior caso. Para o TSP, o número de rotas
possíveis cresce com $(n-1)!/2$ — para 20 cidades, são mais de $10^{17}$
combinações. Na prática, métodos exatos só resolvem instâncias pequenas;
para instâncias grandes, recorre-se a heurísticas — e é justamente aí que
métodos quânticos podem oferecer vantagem.

---

## 6. Sobre as próximas etapas e contribuição original

### 6.1  "Esta revisão é só um mapeamento — onde está a contribuição original?"

A revisão é a **fase exploratória** de uma pesquisa de mestrado mais ampla.
Sua contribuição original já se manifesta em:

1. **Mapeamento sistemático** de 3.696 artigos únicos sobre QA + TSP +
   logística — não há, até onde sabemos, levantamento publicado com esse
   recorte exato e essa magnitude.
2. **Identificação quantitativa** de lacunas (QRL, CVRP+QA, gate-based,
   dados reais) — base para priorizar as próximas etapas.
3. **Taxonomia cruzada** entre o projeto inicial e Phillipson (2025).

As contribuições experimentais virão nas próximas fases: reprodução em
simuladores quânticos e comparação clássico × quântico para instâncias do
TSP em contexto logístico.

### 6.2  "Qual será a contribuição experimental futura?"

Três frentes encadeadas:

1. **Fundamentação teórica aprofundada** — incluindo formulação QUBO para
   TSPTW e variantes brasileiras (CVRP urbano).
2. **Reprodução em simuladores quânticos** — D-Wave Leap, Qiskit, PennyLane
   — sobre instâncias de tamanho controlado.
3. **Comparação experimental** entre soluções clássicas (heurísticas,
   metaheurísticas) e quânticas (QA, abordagens híbridas) em instâncias do
   TSP com dados logísticos reais ou semi-realistas.

### 6.3  "Como vocês vão obter dados logísticos reais? Já têm parceiro industrial?"

A pesquisa está vinculada ao **QuIIN — Quantum Industrial Innovation**,
Centro de Competência EMBRAPII CIMATEC em Tecnologias Quânticas. Esse
arranjo institucional facilita acesso a dados de parceiros industriais já
articulados pela EMBRAPII e pelo SENAI CIMATEC. Em paralelo, datasets
públicos (ex.: TSPLIB, instâncias da SINTEF para VRP) servem como
*baseline* enquanto a parceria industrial é formalizada.

---

## 7. Limitações reconhecidas

Lista para apresentar proativamente (mostra maturidade científica):

- **Cobertura de bases.** A revisão usou apenas Lens.org; bases adicionais
  (Scopus, IEEE Xplore) poderiam ampliar o corpus marginalmente, mas com
  alto custo e ganho decrescente.
- **Idioma.** Strings em inglês — a produção em outros idiomas não foi
  capturada.
- **Recorte temporal.** Coleta em maio/2025; novas publicações posteriores
  não estão refletidas.
- **Dependência de Phillipson (2025)** como lente analítica — mitigada por
  triangulação com taxonomia interna (ver Seção 1).
- **Sub-amostra qualitativa de 129 trabalhos** — necessária para a análise
  de profundidade, mas representa uma fração do corpus total.

---

## 8. Encerramento — possíveis "perguntas-armadilha"

| Pergunta | Postura recomendada |
|---|---|
| **"Computação quântica realmente já supera o clássico no TSP?"** | Honestidade: "Hoje, não com vantagem prática demonstrada de forma generalizável. Há resultados pontuais em instâncias específicas (Salehi *et al.* 2022 para TSPTW). A literatura aponta *potencial*, não supremacia consolidada — e é exatamente essa lacuna que motiva a continuidade da pesquisa." |
| **"Vocês não estão apenas seguindo um modismo (hype)?"** | "A bibliometria mostra que o campo cresce de forma sustentada desde 2020, com investimento institucional sério (D-Wave, IBM, Google, governos). Reconhecemos o componente de *hype*, mas o crescimento da produção acadêmica revisada por pares e a maturação do hardware indicam uma trajetória de pesquisa legítima." |
| **"Por que não trabalhar diretamente com o problema brasileiro e pular a revisão?"** | "Sem o mapeamento da literatura corre-se o risco de duplicar esforço já feito, reinventar formulações QUBO já publicadas ou aplicar um algoritmo conhecidamente inferior. A revisão exploratória é o passo de menor custo e maior retorno informacional antes do investimento experimental." |

---

## 9. Lista de números para ter na ponta da língua

| Indicador | Valor |
|---|---|
| Strings de busca | **26** (8 Alta · 10 Média · 8 Baixa) |
| Registros brutos recuperados | **5.320** |
| Artigos únicos (após deduplicação) | **3.696** |
| Duplicatas removidas | **1.624** (30,5%) |
| Publicados a partir de 2020 | **61,7%** |
| Países representados | **49** |
| Periódicos e conferências distintos | **1.409** |
| Artigos em Open Access | **82,8%** |
| Artigos em Quantum Annealing | **> 1.200** |
| Artigos QAOA/VQE aplicados ao TSP | **≈ 150** |
| Algoritmos quânticos catalogados | **40+ em 6 categorias** |
| Abordagens híbridas (amostra classificada) | **83,7%** (108 de 129) |
| Hardware de referência | D-Wave Advantage — **5.640 qubits**, Pegasus |
| Artigos sobre QRL para roteamento | **21** |
| Artigos sobre CVRP com QA | **18** |
| Referência analítica principal | Phillipson (2025), Maastricht/TNO |
| Phillipson — claim no texto (p. 4) | "over 80 published papers" |
| Phillipson — papers únicos nas tabelas | **≈ 128** |
| Entradas no nosso CSV de algoritmos | **129** *(paper × tópico × problema)* |
| Papers em múltiplos tópicos | **3** (Ajagekar [4], Khumalo [75]) |

---

*Documento de preparação para defesa oral — XI SAPCT — SENAI CIMATEC 2026.*
