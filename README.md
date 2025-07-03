<<<<<<< HEAD
# Sistema N-Puzzle - Documentação Completa

## Descrição do Projeto

Este projeto implementa uma solução completa para o problema do N-Puzzle, incluindo todos os algoritmos de busca solicitados, heurísticas admissíveis e análise comparativa detalhada.

## Especificações Implementadas

### Problema N-Puzzle

- **Tipos suportados**: 8-puzzle (3x3), 15-puzzle (4x4) e 24-puzzle (5x5)
- **Representação de estados**: Matriz bidimensional com 0 representando espaço vazio
- **Operadores**: Movimento para cima, baixo, esquerda, direita (custo uniforme = 1)
- **Verificação de solvabilidade**: Implementada baseada na teoria de inversões

### Algoritmos de Busca Sem Informação

#### 1. Busca em Largura (BFS)

- **Arquivo**: `buscas_sem_infor/bfs.py`
- **Características**:
  - Completo e ótimo
  - Garante solução com menor número de passos
  - Alto uso de memória
- **Otimizações**: Limite de tempo e memória configurável

#### 2. Busca em Profundidade (DFS)

- **Arquivo**: `buscas_sem_infor/dfs.py`
- **Características**:
  - Versões recursiva e iterativa
  - Limite de profundidade obrigatório
  - Baixo uso de memória
- **Otimizações**: Prevenção de ciclos, limite de profundidade adaptável

#### 3. Busca com Aprofundamento Iterativo (IDS)

- **Arquivo**: `buscas_sem_infor/ids.py`
- **Características**:
  - Combina vantagens de BFS e DFS
  - Completo e ótimo
  - Uso eficiente de memória
- **Otimizações**: Versão melhorada com incrementos configuráveis

### Algoritmos de Busca Com Informação

#### 1. A\* (A Estrela)

- **Arquivo**: `buscas_com_info/a_estrela.py`
- **Características**:
  - Completo e ótimo (com heurística admissível)
  - Função de avaliação: f(n) = g(n) + h(n)
  - Múltiplas heurísticas suportadas
- **Otimizações**: Versão bidirecional implementada

#### 2. Busca Gulosa (Greedy Best-First)

- **Arquivo**: `buscas_com_info/gulosa.py`
- **Características**:
  - Usa apenas h(n) para ordenação
  - Rápida, mas não garante otimalidade
  - Múltiplas heurísticas suportadas
- **Otimizações**: Versão melhorada com prevenção de ciclos avançada

### Heurísticas Implementadas

#### 1. Peças Fora do Lugar

- **Função**: `utils/heuristicas.py` - `heuristica_pecas_fora_lugar()`
- **Descrição**: Conta número de peças em posições incorretas
- **Propriedades**: Admissível, simples de calcular

#### 2. Distância de Manhattan

- **Função**: `utils/heuristicas.py` - `heuristica_manhattan()`
- **Descrição**: Soma das distâncias Manhattan de cada peça
- **Propriedades**: Admissível, mais informativa que peças fora do lugar

#### 3. Manhattan Melhorada

- **Função**: `utils/heuristicas.py` - `heuristica_manhattan_melhorada()`
- **Descrição**: Manhattan + penalidades por conflitos lineares
- **Propriedades**: Mais informativa, ainda admissível

## Estrutura do Projeto

```
Projeto_N_Puzzle/
├── main.py                 # Sistema principal com menu interativo
├── problema.py             # Formulação do problema e representação de estados
├── utils/                  # Utilitários
│   ├── __init__.py
│   ├── caminho.py         # Análise de resultados e visualização
│   └── heuristicas.py     # Implementação das heurísticas
├── buscas_sem_infor/      # Algoritmos sem informação
│   ├── __init__.py
│   ├── bfs.py             # Busca em Largura
│   ├── dfs.py             # Busca em Profundidade
│   └── ids.py             # Aprofundamento Iterativo
└── buscas_com_info/       # Algoritmos com informação
    ├── __init__.py
    ├── a_estrela.py       # Algoritmo A*
    └── gulosa.py          # Busca Gulosa
```

## Como Usar

### Execução Básica

```bash
python main.py
```

### Modos de Execução

```bash
# Demonstração automática com puzzle 8
python main.py --demo

# Análise automática com puzzle 15
python main.py --puzzle15
```

### Menu Interativo

O sistema oferece um menu completo com as seguintes opções:

1. **Análise completa automática**: Executa todos os algoritmos e gera relatório
2. **Puzzle personalizado**: Permite criar configurações customizadas
3. **Teste de algoritmo específico**: Executa apenas um algoritmo escolhido
4. **Comparação de heurísticas**: Compara todas as heurísticas disponíveis
5. **Visualização de resultados**: Mostra caminhos e árvores de busca
6. **Exportação de dados**: Salva resultados em CSV para análise externa

## Resultados e Análises

### Saídas do Sistema

Para cada execução, o sistema fornece:

1. **Sequência de movimentos**: Passos da solução encontrada
2. **Número total de passos**: Profundidade da solução
3. **Tempo de execução**: Em segundos com 4 casas decimais
4. **Estatísticas de busca**:
   - Nós expandidos
   - Nós gerados
   - Memória máxima utilizada
   - Fator de ramificação efetivo

### Análise Comparativa

- **Tabela comparativa**: Todos os algoritmos lado a lado
- **Identificação do melhor algoritmo** por diferentes critérios:
  - Menor tempo de execução
  - Menor número de nós expandidos
  - Menor profundidade (solução ótima)
  - Menor uso de memória

### Visualização

- **Caminho da solução**: Sequência visual de estados
- **Árvore de busca**: Representação textual dos primeiros níveis
- **Exportação CSV**: Para criação de gráficos externos

## Exemplos de Configurações

### Puzzle 8 (Exemplo fácil)

```
1 2 3
4 0 6
7 5 8
```

### Puzzle 8 (Exemplo médio)

```
2 8 3
1 6 4
7 0 5
```

### Puzzle 15 (Exemplo)

```
1  2  3  4
5  6  7  8
9  10 11 12
13 14 0  15
```

## Características Técnicas

### Otimizações Implementadas

1. **Detecção de solvabilidade**: Evita buscas desnecessárias
2. **Prevenção de ciclos**: Em todos os algoritmos
3. **Limites de tempo e memória**: Evita execuções infinitas
4. **Hash de estados**: Comparação eficiente de configurações
5. **Estruturas de dados otimizadas**: Heap para prioridades, sets para visitados

### Limitações e Considerações

1. **Puzzle 24**: Muito complexo, requer limites baixos de profundidade
2. **DFS**: Limitado por profundidade para evitar caminhos muito longos
3. **Memória**: Limitada a 100.000 nós por padrão
4. **Tempo**: Limitado a 5 minutos por execução por padrão

### Complexidade dos Algoritmos

| Algoritmo | Tempo  | Espaço | Completo | Ótimo   |
| --------- | ------ | ------ | -------- | ------- |
| BFS       | O(b^d) | O(b^d) | Sim      | Sim     |
| DFS       | O(b^m) | O(bm)  | Não\*    | Não     |
| IDS       | O(b^d) | O(bd)  | Sim      | Sim     |
| A\*       | O(b^d) | O(b^d) | Sim\*\*  | Sim\*\* |
| Gulosa    | O(b^m) | O(b^m) | Não      | Não     |

\*Com limite de profundidade  
\*\*Com heurística admissível

## Validação e Testes

### Casos de Teste Incluídos

1. **Puzzles solucionáveis**: Configurações com solução garantida
2. **Puzzles insolucionáveis**: Detectados automaticamente
3. **Casos extremos**: Estado inicial = estado objetivo
4. **Diferentes tamanhos**: 8, 15 e 24 puzzles

### Verificação de Corretude

- Todas as soluções são validadas
- Verificação de admissibilidade das heurísticas
- Testes de consistência entre algoritmos

## Expansões Possíveis

1. **Interface gráfica**: Visualização interativa dos estados
2. **Mais heurísticas**: Padrão databases, conflitos direcionais
3. **Algoritmos avançados**: IDA*, RBFS, SMA*
4. **Paralelização**: Execução simultânea de múltiplos algoritmos
5. **Otimizações de memória**: Compressão de estados, garbage collection

Este sistema fornece uma implementação completa e educacional do problema N-Puzzle, adequada tanto para aprendizado quanto para análise de desempenho de algoritmos de busca.
