# Resumo de Algoritmos Quânticos Aplicados a Problemas de Logística e TSP

> Baseado na taxonomia do projeto e no artigo de referência: Phillipson, F. (2025). "Quantum Computing in Logistics and Supply Chain Management - an Overview".

---

## 1. Algoritmos por Paradigma Quântico

### 1.1 Quantum Annealing (QA)

O paradigma dominante na literatura. Utiliza tunelamento quântico para encontrar o estado de menor energia de um sistema formulado como QUBO/Ising.

| Algoritmo | Descrição | Hardware | Escala Testada | Aplicações Principais |
|-----------|-----------|----------|---------------|----------------------|
| **D-Wave QA** | Annealing nativo em hardware quântico | D-Wave 2000Q, Advantage (5640 qubits, conectividade 15) | 10–30 cidades (direto); maiores com decomposição | TSP, VRP, CVRP, JSP, BPP, FLP, TAP |
| **D-Wave Hybrid Solver (Kerberos)** | Pipeline automático: decompõe problema + QA + clássico | D-Wave Leap / AWS Braket | Centenas de variáveis | VRP, NDP, KP |
| **D-Wave CQM Solver** | Aceita restrições diretamente (Constrained Quadratic Model) | D-Wave Leap | Variável | CVRP, BPP, KP |
| **Simulated Quantum Annealing** | Simulação clássica do processo de QA | CPU/GPU | Variável | Benchmark/comparação |
| **Reverse Annealing** | Parte de solução conhecida e refina | D-Wave Advantage | 10–30 cidades | JSP, TSP |
| **Column Generation + QA** | Geração de colunas assistida por annealing | D-Wave + Clássico | Variável | CVRP com restrições de desigualdade |

**Destaque**: QA é o paradigma mais utilizado por oferecer maior número de qubits e um stack completo (D-Wave Leap). A maioria dos trabalhos experimentais usa D-Wave.

---

### 1.2 Algoritmos Variacionais Gate-Based

Circuitos quânticos parametrizados otimizados por loop clássico. Adequados para era NISQ.

| Algoritmo | Descrição | Hardware | Escala | Aplicações |
|-----------|-----------|----------|--------|------------|
| **QAOA** | Circuito alternando operadores de custo e mixer | IBM Quantum, Google, Rigetti | 5–20 cidades | TSP, VRP, CVRP, HVRP, m-TSP, JSP, BPP, KP |
| **VQE** | Encontra autovalor mínimo via ansatz variacional | IBM Quantum | 5–15 cidades | TSP, VRP, CVRP, cargo loading, QAP |
| **QAOA+ / Warm-Start QAOA** | QAOA inicializado com solução clássica (greedy) | IBM Quantum | 5–25 cidades | KP, TSP |
| **IQAOA (Indirect QAOA)** | Meta-otimização clássica + Quantum Alternating Operator Ansatz | IBM Quantum | Até 8 cidades (TSP) | TSP |
| **Grover-Mixer QAOA** | Usa Grover como mixer para restringir espaço de busca factível | IBM Quantum | 5–15 cidades | CVRP, KP |
| **F-VQE (Filtering VQE)** | VQE com filtragem; convergência mais rápida | IBM Quantum | Até 23 qubits | JSP |
| **VarQITE** | Variational Quantum Imaginary Time Evolution | IBM Quantum | 5–15 cidades | JSP |
| **CVaR-QAOA** | QAOA com Conditional Value at Risk | Simuladores | 5–20 cidades | TSP |
| **AAM-QAOA** | Amplitude Amplification-Mixer + Quantum Tree Generator | Simuladores/IBM | Variável | KP |
| **VQA-PFS** | Preserving Feasible Space; supera QAOA e QAOA+ | IBM Quantum | Variável | FLP |
| **pVSQA** | Post-processing Variationally Scheduled QA | Simuladores/IBM | Variável | Graph Partitioning, QKP |

**Destaque**: QAOA e VQE são o segundo paradigma mais usado. F-VQE mostrou convergência superior a QAOA, VQE e VarQITE em benchmarks de JSP (Amaro et al., 2022). VQE tende a superar QAOA em qualidade de solução para TSP (Palackal et al.).

---

### 1.3 Algoritmos Gate-Based Exatos

| Algoritmo | Descrição | Complexidade | Status |
|-----------|-----------|-------------|--------|
| **Grover's Search** | Busca não-estruturada com speedup quadrático O(√N!) | Requer muitos qubits | Muito citado, pouco implementado para TSP |
| **Grover's Adaptive Search (GAS)** | Versão iterativa de Grover | Quadrático sobre brute-force | Usado em CSLP, QISS |
| **Quantum Phase Estimation (QPE)** | Codifica distâncias como fases para encontrar rota mínima | Circuitos profundos | Demonstrado para TSP com 4 cidades (Srinivasan et al.) |
| **HOBO Encoding + Grover** | Higher-Order Binary Optimization reduz qubits + Grover amplifica | Variável | Pequena escala |

---

### 1.4 Abordagens Híbridas (Clássica + Quântica)

A maioria das soluções na literatura são híbridas ("Horizontal Hybrid Quantum Computing").

| Abordagem | Descrição | Vantagem | Exemplos de Uso |
|-----------|-----------|----------|----------------|
| **Decomposição + QA** | Divide problema grande em sub-problemas para o QA | Escalabilidade | VRP, CVRP, JSP, tráfego (até 500 carros) |
| **2-Phase Heuristic** | Fase 1: clustering; Fase 2: roteamento como TSP | Reduz complexidade | CVRP (Feld et al., Borowski et al.) |
| **Path-Slicing + Quantum Local Search** | Fatia caminhos do TSP em subproblemas | Eficiência de recursos | TSP (Liu et al.) |
| **QAOA + Solver Clássico** | QAOA gera candidatos, solver refina | Qualidade | VRP, CVRP |
| **Hybrid QC-MILP Decomposition** | MILP clássico + QUBO no QA para sequenciamento | Escala industrial | JSP, MCFP (Ajagekar et al.) |
| **DFJ Adaptive** | Eliminação adaptativa de subtours, reduz qubits | Viabilidade em hardware atual | CVRP → TSP (Palmieri) |
| **Quantum-Inspired** | Algoritmos clássicos imitando comportamento quântico | Roda em hardware clássico | Digital Annealing, Simulated Bifurcation, Coherent Ising Machines |

---

### 1.5 Algoritmos de Machine Learning Quântico

Tendência emergente com poucos trabalhos, identificada como lacuna de pesquisa.

| Algoritmo | Descrição | Aplicação |
|-----------|-----------|-----------|
| **Quantum Reinforcement Learning (QRL)** | Circuitos quânticos substituem camadas de atenção em agentes RL | VRP (Sanches et al., Correll et al.) |
| **Quantum Q-Learning** | Circuitos parametrizados para Q-values | CVRP (Xu et al.) |
| **QACO (Quantum Ant Colony Optimization)** | Colônia de formigas quântica + K-means | TSP (Qiu et al.) |
| **QSVM (Quantum Support Vector Machine)** | SVM quântico para VRP | VRP 3-4 cidades (Mohanty et al.) |
| **QAmplifyNet** | Rede neural híbrida para previsão de backorder | Supply Chain (Jahin et al.) — F1: 94% |
| **QCBR (Quantum Cases-Based Reasoning)** | PQC + VQE para scheduling por analogia | Personnel scheduling (Adelomou et al.) |
| **HQAGO** | Busca quântica + otimização genética | Knapsack (Ardelean et al.) |

---

### 1.6 Algoritmos Clássicos (Baseline de Comparação)

| Algoritmo | Tipo | Uso Principal na Literatura |
|-----------|------|---------------------------|
| **Gurobi** | Solver exato (MILP/MIP) | Benchmark padrão para QUBO e VRP |
| **CPLEX** | Solver exato | Comparação com QA para STDSP |
| **Branch and Bound** | Exato | Até ~30 cidades |
| **Christofides** | Aproximação (1.5x ótimo) | TSP baseline |
| **LKH** | Heurística | Instâncias grandes de TSP |
| **Simulated Annealing** | Metaheurística | Comparação direta com QA |
| **Tabu Search** | Metaheurística | Baseline para JSP e NDP |
| **Genetic Algorithm** | Metaheurística | Instâncias grandes |
| **Greedy Heuristic** | Guloso | Baseline simples |
| **ADMM** | Decomposição | Otimização distribuída (Harwood et al.) |
| **Nelder-Mead / COBYLA** | Otimizadores clássicos | Otimizadores dentro do loop VQE |

---

## 2. Métricas de Comparação Detalhadas

### 2.1 Métricas Universais

| Métrica | Descrição | Importância |
|---------|-----------|-------------|
| **Qualidade da solução** | Razão solução/ótimo conhecido (approximation ratio) | Principal indicador de eficácia |
| **Tempo de execução** | Wall-clock time incluindo compilação/transpilação | Comparabilidade com clássicos |
| **Número de qubits** | Lógicos vs. físicos (N² para TSP com N cidades) | Determina viabilidade no hardware atual |
| **Profundidade do circuito** | Número de camadas de gates (gate-based) | Limita viabilidade em NISQ |
| **Taxa de sucesso** | Fração de execuções com solução factível | Confiabilidade |
| **Feasibility ratio** | Proporção de soluções que respeitam restrições | Qualidade prática |
| **Optimality gap** | % diferença do ótimo conhecido | Quantifica "quão bom" é o resultado |

### 2.2 Métricas Específicas de Hardware

| Métrica | Descrição | Relevância |
|---------|-----------|-----------|
| **Embedding overhead** | Qubits físicos para embedding (D-Wave: clique de n=177 máx.) | Limita escala no QA |
| **Chain strength** | Penalty para manter consistência de qubits encadeados | Sensibilidade alta; impacta qualidade |
| **Penalty λ (QUBO)** | Peso das restrições na função objetivo | Difícil de calibrar; pouco estudado sistematicamente |
| **Profundidade p (QAOA)** | Número de repetições dos operadores | Trade-off qualidade vs. ruído |
| **Robustez ao ruído** | Performance em hardware real vs. simulador ideal | Crítico para era NISQ |
| **Annealing time** | Tempo de evolução quântica (QA) | Determinado experimentalmente |
| **Connectivity (Pegasus/Chimera)** | Topologia do chip: Advantage (15 conexões/qubit) vs. 2000Q (6) | Advantage ~2x mais rápido que 2000Q |

### 2.3 Métricas por Domínio de Problema

| Problema | Métricas Específicas |
|----------|---------------------|
| **TSP/TSPTW** | Custo total da rota, violação de time windows, nº de cidades |
| **VRP/CVRP** | Nº de veículos, capacidade utilizada, janelas de tempo, nº de rotas |
| **HVRP** | Capacidades heterogêneas dos veículos |
| **Bin Packing** | Nº de bins, taxa de ocupação, dimensões (1D/2D/3D) |
| **Knapsack** | Valor total, violação de capacidade, convergence ratio |
| **JSP/FJSP** | Makespan, workload total, prioridade de jobs |
| **Network Design** | Custo de infraestrutura, cobertura de demanda, nº de facilities |
| **Fleet/TAP** | Custo de manutenção, utilização de aeronaves, nº de voos |
| **Traffic Flow** | Nº de estradas congestionadas após otimização |
| **Cargo Loading** | Payload maximizado, restrições de peso/volume/centro de gravidade |

---

## 3. Panorama Geral: Áreas de Aplicação × Algoritmos

Baseado na revisão de 80+ artigos (Phillipson, 2025):

| Área | QA | QAOA | VQE | Grover | Híbrido | QML/RL | Total Aprox. |
|------|:--:|:----:|:---:|:------:|:-------:|:------:|:----------:|
| **Routing (VRP/TSP)** | +++ | ++ | + | + | +++ | + | ~35 artigos |
| **Network Design** | ++ | + | — | + | ++ | — | ~12 artigos |
| **Fleet/Maintenance** | + | + | — | — | + | — | ~5 artigos |
| **Cargo/Bin Packing** | ++ | + | + | — | ++ | — | ~12 artigos |
| **Prediction** | — | — | — | — | — | + | ~3 artigos |
| **Scheduling** | ++ | ++ | + | + | ++ | — | ~15 artigos |

Legenda: +++ = muito usado, ++ = moderado, + = poucos trabalhos, — = não encontrado

---

## 4. Conclusões-Chave do Artigo de Referência

1. **Híbrido é o padrão**: a grande maioria das soluções publicadas combina QC + clássico
2. **QA domina**: D-Wave lidera por oferecer mais qubits e stack completo
3. **QAOA/VQE limitados**: segundo paradigma mais usado, mas ainda com performance inferior
4. **Hardware é o gargalo**: ruído, decoerência e número de qubits limitam aplicações reais
5. **Routing e Scheduling** são os tópicos mais pesquisados
6. **Prediction/QML** é a maior lacuna de pesquisa identificada
7. **Poucos artigos** demonstram vantagem clara sobre métodos clássicos — maioria indica "potencial"
8. **Sensibilidade a parâmetros** (penalty, chain strength, profundidade p) é desafio transversal pouco explorado
9. **Fluxo principal** de pesquisa começa em ~2020, com crescimento acelerado
10. **Metaheurísticas quânticas** (QACO, Quantum Genetic) são tendência emergente
