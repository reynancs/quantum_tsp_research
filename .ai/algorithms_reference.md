# Referência de Algoritmos — Computação Quântica para TSP

## Taxonomia dos Algoritmos

### 1. Quantum Annealing (QA)

**Princípio**: Explora o estado de menor energia de um sistema quântico via tunelamento quântico. O TSP é formulado como QUBO (Quadratic Unconstrained Binary Optimization) ou modelo de Ising.

| Algoritmo | Descrição | Hardware Típico | Escala (cidades) |
|-----------|-----------|----------------|-----------------|
| D-Wave Quantum Annealing | Annealing nativo em hardware D-Wave | D-Wave 2000Q, Advantage (5640 qubits) | 10–30 (direto), mais com embedding |
| Simulated Quantum Annealing | Simulação clássica do processo de annealing | CPU/GPU clássico | Variável |
| Reverse Annealing | Annealing reverso partindo de solução conhecida | D-Wave Advantage | 10–30 |
| D-Wave Hybrid Solver (Kerberos) | Pipeline híbrido com decomposição automática QA + clássico | D-Wave Leap / AWS Braket | Problemas maiores que o chip |
| D-Wave CQM Solver | Solver para Constrained Quadratic Model, aceita restrições diretamente | D-Wave Leap | Variável (centenas de variáveis) |
| Column Generation + QA | Geração de colunas assistida por annealing para problemas com restrições de desigualdade | D-Wave + Clássico | Variável |

**Formulação QUBO para TSP**: O TSP com N cidades requer N² variáveis binárias. A função objetivo combina a distância total com penalidades por violação de restrições (cada cidade visitada exatamente uma vez, em exatamente uma posição da rota).

### 2. Algoritmos Variacionais (Gate-Based)

**Princípio**: Circuitos quânticos parametrizados otimizados por um loop clássico. Adequados para hardware NISQ (Noisy Intermediate-Scale Quantum).

| Algoritmo | Descrição | Hardware Típico | Escala |
|-----------|-----------|----------------|--------|
| QAOA (Quantum Approximate Optimization Algorithm) | Circuito alternando operadores de custo e mixer | IBM Quantum, Google, Rigetti | 5–20 cidades |
| VQE (Variational Quantum Eigensolver) | Encontra autovalor mínimo via ansatz variacional | IBM Quantum | 5–15 cidades |
| QAOA+ / Warm-Start QAOA | QAOA inicializado com solução clássica | IBM Quantum | 5–25 cidades |
| CVaR-QAOA | QAOA com Conditional Value at Risk | Simuladores | 5–20 cidades |
| IQAOA (Indirect QAOA) | QAOA indireto com meta-otimização clássica e Quantum Alternating Operator Ansatz | IBM Quantum | Até 8 cidades (TSP) |
| Grover-Mixer QAOA | Variante do QAOA que usa Grover como mixer para restringir espaço de busca | IBM Quantum | 5–15 cidades |
| F-VQE (Filtering VQE) | VQE com filtragem, convergência mais rápida que QAOA e VQE padrão | IBM Quantum | Até 23 qubits |
| VarQITE | Variational Quantum Imaginary Time Evolution | IBM Quantum | 5–15 cidades |
| AAM-QAOA (Amplitude Amplification-Mixer QAOA) | Combina Quantum Tree Generator com Grover-mixer QAOA | Simuladores / IBM | Variável |
| VQA-PFS (Variational Quantum Algorithm - Preserving Feasible Space) | Operadores mistos + Hardware-Efficient Ansatz, supera QAOA/QAOA+ | IBM Quantum | Variável |
| pVSQA (Post-processing Variationally Scheduled QA) | Combina métodos variacionais com pós-processamento | Simuladores / IBM | Variável |

### 3. Algoritmos Gate-Based Exatos

| Algoritmo | Descrição | Complexidade | Escala |
|-----------|-----------|-------------|--------|
| Grover's Search | Busca não-estruturada com speedup quadrático | O(√N!) | Teórico (requer muitos qubits) |
| Grover's Adaptive Search (GAS) | Versão adaptativa de Grover com busca iterativa | IBM Quantum / Simuladores | Teórico / Pequena escala |
| HHL (Harrow-Hassidim-Lloyd) | Resolução de sistemas lineares | Exponencial em precisão | Teórico |
| Quantum Phase Estimation (QPE) | Estimativa de fase para encontrar autovalores; usado para codificar distâncias como fases no TSP | Requer circuitos profundos | Teórico |
| HOBO Encoding + Grover | Higher-Order Unconstrained Binary Optimization com Grover para reduzir qubits | IBM Quantum | Pequena escala |

### 4. Abordagens Híbridas (Clássica + Quântica)

| Abordagem | Descrição | Vantagem |
|-----------|-----------|---------|
| Decomposição + QA | Divide TSP/VRP grande em sub-problemas, resolve cada um no quantum | Escalabilidade |
| QAOA + Solver Clássico | QAOA gera soluções parciais, solver clássico refina | Qualidade da solução |
| Quantum-Inspired Clássico | Algoritmos clássicos que imitam comportamento quântico (ex: Simulated Bifurcation, Digital Annealing) | Roda em hardware clássico |
| GNN + Quantum | Graph Neural Networks combinadas com processamento quântico | Generalização |
| Quantum Reinforcement Learning (QRL) | Circuitos quânticos substituem camadas de atenção em agentes de RL para VRP | IBM Quantum / Simuladores | Prova de conceito |
| Quantum Q-Learning | Circuitos parametrizados para aproximar Q-values em CVRP | Simuladores NISQ | 3–6 cidades |
| QACO (Quantum Ant Colony Optimization) | Algoritmo quântico de colônia de formigas combinado com K-means | IBM Quantum / Simuladores | Variável |
| QAmplifyNet | Rede neural híbrida quântica-clássica para previsão de demanda em supply chain | IBM Quantum | Previsão (não roteamento) |
| QSVM (Quantum Support Vector Machine) | SVM quântico aplicado a problemas de VRP | IBM Qiskit | 3–4 cidades |
| HQAGO (Hybrid Quantum Search + Genetic Optimization) | Busca quântica com otimização genética, fixa qubits como bits clássicos | Simuladores | Variável |
| Hybrid QC-MILP/MIQP Decomposition | Decomposição em MILP/MIQP resolvido classicamente + QUBO no QA | D-Wave + Gurobi | Escala industrial |
| Path-Slicing + Quantum Local Search | Divide TSP em subproblemas via fatiamento de caminhos, resolve com QA | D-Wave | Variável |
| 2-Phase Heuristic (Clustering + Routing) | Fase 1: clustering clássico/quântico; Fase 2: roteamento como TSP | D-Wave / IBM | 10–30 cidades |
| DFJ Adaptive (Dantzig-Fulkerson-Johnson) | Eliminação adaptativa de subtours, reduz qubits necessários | D-Wave / IBM | Variável |
| QISS (Quantum Industrial Shift Scheduling) | Grover's Adaptive Search para scheduling industrial | IBM Quantum | Pequena escala |
| QCBR (Quantum Cases-Based Reasoning) | PQC + VQE para raciocínio baseado em casos em scheduling | IBM Quantum | Pequena escala |

### 5. Algoritmos Clássicos (Baseline de Comparação)

| Algoritmo | Tipo | Complexidade | Uso |
|-----------|------|-------------|-----|
| Força Bruta | Exato | O(N!) | Até ~15 cidades |
| Branch and Bound | Exato | Exponencial (podada) | Até ~30 cidades |
| Christofides | Aproximação | O(N³) | Garantia de 1.5x ótimo |
| LKH (Lin-Kernighan-Helsgott) | Heurística | Variável | Instâncias grandes |
| Nearest Neighbor | Heurística gulosa | O(N²) | Baseline simples |
| Genetic Algorithm | Metaheurística | Variável | Instâncias grandes |
| Simulated Annealing (Clássico) | Metaheurística | Variável | Comparação com QA |
| Tabu Search | Metaheurística | Variável | Baseline para JSP e NDP |
| Gurobi (MILP/MIP Solver) | Solver exato comercial | CPU clássico | Benchmark padrão para problemas QUBO |
| CPLEX | Solver exato comercial | CPU clássico | Comparação com soluções quânticas |
| Greedy Heuristic | Heurística gulosa | O(N²) | Baseline simples |
| ADMM (Alternating Direction Method of Multipliers) | Decomposição para otimização distribuída | CPU / híbrido | Variável |

## Métricas de Comparação

Ao comparar algoritmos nos artigos, registre:

1. **Qualidade da solução**: Razão entre solução encontrada e solução ótima conhecida (approximation ratio)
2. **Tempo de execução**: Wall-clock time (incluir tempo de compilação/transpilação para quânticos)
3. **Número de qubits**: Qubits lógicos vs. físicos necessários (N² variáveis binárias para TSP com N cidades)
4. **Profundidade do circuito**: Para gate-based (limita viabilidade em hardware NISQ)
5. **Número de cidades/nós**: Escala do problema testado
6. **Tipo de instância**: Aleatória, benchmark (TSPLIB), caso real de logística
7. **Taxa de sucesso (success rate)**: Fração de execuções que retornam solução factível
8. **Feasibility ratio**: Proporção de soluções que respeitam todas as restrições
9. **Optimality gap**: Diferença percentual entre solução encontrada e ótimo conhecido
10. **Sensibilidade a parâmetros**: Impacto de penalty λ, chain strength, profundidade p (QAOA)
11. **Robustez ao ruído**: Desempenho em hardware NISQ real vs. simulador ideal
12. **Tipo de abordagem**: Puro quântico vs. híbrido (horizontal hybrid quantum computing)
13. **Paradigma quântico**: QA (annealing) vs. GBC (gate-based) vs. Quantum-Inspired
14. **Embedding overhead**: Qubits físicos necessários para embedding no hardware (especialmente D-Wave)

### Métricas Específicas por Problema (Phillipson, 2025)

| Problema | Métricas Adicionais |
|----------|-------------------|
| VRP/CVRP | Número de veículos, capacidade, janelas de tempo, número de rotas |
| TSP/TSPTW | Custo total da rota, violação de time windows |
| Bin Packing | Número de bins utilizados, taxa de ocupação |
| Knapsack | Valor total, violação de capacidade |
| JSP/FJSP | Makespan, workload total, prioridade |
| Network Design | Custo de infraestrutura, cobertura de demanda |
| Fleet/TAP | Custo de manutenção, utilização de aeronaves |

## Tendências Observadas na Literatura

- **QAOA e Quantum Annealing** são os mais estudados para TSP e VRP
- **Abordagens híbridas** crescem em popularidade (2021–presente) e dominam a literatura — a maioria das soluções publicadas são híbridas (Phillipson, 2025)
- **QA domina**: a maioria das publicações usa Quantum Annealing como paradigma principal, devido ao maior número de qubits disponíveis e ao full-stack oferecido pela D-Wave
- **QAOA e VQE** são o segundo paradigma mais usado, porém ainda muito limitados em performance
- **Grover's Search** é muito citado mas pouco implementado para TSP (requer muitos qubits)
- **D-Wave** domina os trabalhos experimentais com annealing (2000Q e Advantage com 5640 qubits)
- **IBM Quantum** domina gate-based experimental (até 127 qubits)
- **Gap significativo** entre escala teórica e experimental (artigos testam 5–30 cidades vs. TSPs reais com centenas/milhares)
- **Fluxo principal de pesquisa** começa por volta de 2020 (Phillipson, 2025)
- **Routing e Scheduling** são os tópicos mais cobertos; **Prediction/QML** tem poucos trabalhos e é identificado como lacuna
- **Metaheurísticas quânticas** (QACO, Quantum Genetic) estão emergindo como nova tendência
- **Quantum Reinforcement Learning** para VRP é ainda prova de conceito, mas demonstra potencial
- **Poucos artigos** demonstram vantagem clara sobre métodos clássicos — a maioria indica "potencial" futuro
- **Sensibilidade a parâmetros** (penalty λ, chain strength, profundidade p) é um desafio transversal pouco explorado

## Referência Bibliográfica Principal

- Phillipson, F. (2025). "Quantum Computing in Logistics and Supply Chain Management - an Overview". Maastricht University / TNO. arXiv:2042.17520v2. — Overview de 80+ artigos cobrindo routing, network design, fleet maintenance, cargo loading, prediction e scheduling.
