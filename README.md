# N-Puzzle Solver v3.0 🧩

Sistema completo e avançado para resolução de puzzles deslizantes (8-puzzle, 15-puzzle, 24-puzzle) com implementação de múltiplos algoritmos de busca e análise comparativa de performance.

## ✨ Características Principais

### � Algoritmos de Busca Implementados
- **BFS (Breadth-First Search)** - Busca em largura, garante solução ótima
- **DFS (Depth-First Search)** - Busca em profundidade com limite configurável  
- **IDS (Iterative Deepening Search)** - Combina vantagens de BFS e DFS
- **A*** - Busca heurística com múltiplas heurísticas disponíveis
- **Greedy Search** - Busca gulosa baseada em heurísticas

### 🎯 Heurísticas Avançadas
- **Manhattan Distance** - Soma das distâncias de Manhattan de cada peça
- **Misplaced Tiles** - Contagem de peças fora de lugar
- **Linear Conflict** - Detecção de conflitos lineares para maior precisão

### 🎨 Visualização Otimizada
- **Estados limpos**: Visualização compacta durante a busca
- **Formato consistente**: `{1  2  3}` para cada linha do puzzle
- **Tempo real**: Acompanhe a execução dos algoritmos passo a passo
- **Árvores de busca**: Visualização da estrutura de exploração

### 📊 Análise e Métricas
- **Comparação de algoritmos**: Execute todos simultaneamente
- **Métricas detalhadas**: Tempo, nós explorados, uso de memória
- **Rankings**: Por velocidade, eficiência e otimalidade
- **Exportação**: Dados em JSON e gráficos de performance
- **Condição de objetivo:** Estado atual = estado objetivo
- **Custo de ação:** Uniforme = 1 para todos os movimentos

### � **Algoritmos Implementados**

- **BFS (Busca em Largura)** - Garante solução ótima, uso intensivo de memória
- **DFS (Busca em Profundidade)** - Menor uso de memória, limite configurável
- **IDS (Busca com Aprofundamento Iterativo)** - Combina vantagens de BFS e DFS

### 🌳 **Geração da Árvore de Busca**

- Exibição do caminho do estado inicial até o objetivo
- Apresentação da árvore gerada com visualização textual
- Evidenciação do caminho correto encontrado

### 📈 **Análise Comparativa**

- Comparação do número de nós expandidos
- Comparação do tempo de execução
- Quantidade de estados expandidos
- Profundidade da solução
- Dados apresentados em tabelas e gráficos

## ⭐ PARTE 2 - BUSCAS COM INFORMAÇÃO

### 🎯 **Heurísticas Admissíveis Implementadas**

- **Manhattan Distance** - Soma das distâncias de Manhattan das peças
- **Misplaced Tiles** - Número de peças fora do lugar
- **Linear Conflict** - Conflito linear combinado com Manhattan

### 🔧 **Algoritmos Implementados**

- **A\* (A-Star)** - Algoritmo heurístico ótimo com f(n) = g(n) + h(n)
- **Greedy Search** - Busca gulosa usando apenas h(n)

### � **Geração da Árvore de Busca**

- Exibição do caminho do estado inicial até o objetivo
- Apresentação da árvore gerada evidenciando o caminho correto
- Análise detalhada do caminho da solução

## ✨ Funcionalidades Avançadas

### �🎬 **Visualização em Tempo Real**

- Visualização automática para todos os algoritmos
- Velocidade otimizada por algoritmo
- Progresso da busca em tempo real
- Estados do puzzle visualizados passo a passo

### 📊 **Análise Comparativa Completa**

- Comparação de todos os algoritmos no mesmo puzzle
- Tabelas de resultados detalhadas
- Rankings por velocidade, eficiência e otimalidade
- Análise por categoria (informada vs não-informada)
- Recomendações personalizadas por tamanho do puzzle

### 📋 **Geração de Relatórios**

- Relatórios completos em formato texto
- Exportação de dados em JSON
- Geração de gráficos de performance (matplotlib)
- Análise estatística detalhada
- Conclusões e recomendações

### 🔧 **Funcionalidades Auxiliares**

- Exemplos pré-definidos (8, 15, 24 puzzles)
- Gerador de puzzles aleatórios
- Validação automática de solucionabilidade
- Salvar/carregar estados
- Criação de puzzles personalizados

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas opcionais para gráficos (matplotlib, pandas, seaborn)

### Instalação Básica

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/n-puzzle-solver.git
cd n-puzzle-solver/n_puzzle_solver

# Execute o programa
python main.py
```

### Instalação Completa (com gráficos)

```bash
# Instale dependências opcionais
pip install matplotlib pandas seaborn numpy

# Execute o programa com funcionalidades completas
python main.py

# Instale as dependências
pip install -r n_puzzle_solver/requirements.txt

# Execute o programa
cd n_puzzle_solver
python main.py
```

## 🚀 Como Usar

### Instalação
```bash
git clone https://github.com/thavyne-KDR/n_puzzle.git
cd n_puzzle
pip install -r requirements.txt
```

### Execução
```bash
cd n_puzzle_solver
python main.py
```

### Menu Principal
```
🧩================================================🧩
         N-PUZZLE SOLVER v3.0
==================================================

🔍 ALGORITMOS DE BUSCA:
  1. 🔄 Busca em Largura (BFS)
  2. ⬇️  Busca em Profundidade (DFS)
  3. 🔁 Busca com Aprofundamento Iterativo (IDS)
  4. ⭐ Busca A* (com heurísticas)
  5. 🎯 Busca Gulosa

⚙️ FUNCIONALIDADES:
  6. 📊 Comparar Algoritmos
  7. 📂 Carregar Exemplo
  8. 🎲 Gerar Puzzle Aleatório
  9. 🎨 Criar Puzzle Personalizado
  10. 📈 Ver Estatísticas
```

## 📋 Exemplos de Uso

### Criando um Puzzle Personalizado
```python
from n_puzzle_solver.puzzle import Puzzle

# Criar puzzle 3x3
initial_state = [
    [1, 2, 3],
    [4, 0, 6],  # 0 representa o espaço vazio
    [7, 5, 8]
]

puzzle = Puzzle(initial_state)
print(puzzle.visualize())
```

### Executando Algoritmo A*
```python
from n_puzzle_solver.search.astar import AStar

# Criar solver A* com heurística Manhattan
solver = AStar('manhattan')
success, solution = solver.search(puzzle)

if success:
    print(f"Solução encontrada: {' → '.join(solution)}")
```

## 🏗️ Estrutura do Projeto

```
n_puzzle_solver/
├── main.py              # Interface principal
├── puzzle.py            # Classe Puzzle e utilitários
├── requirements.txt     # Dependências
├── examples/
│   └── examples.json    # Puzzles de exemplo
├── search/             # Algoritmos de busca
│   ├── __init__.py
│   ├── astar.py        # Algoritmo A*
│   ├── bfs.py          # Busca em largura
│   ├── dfs.py          # Busca em profundidade
│   ├── greedy.py       # Busca gulosa
│   ├── ids.py          # Busca com aprofundamento iterativo
│   └── heuristics.py   # Funções heurísticas
└── utils/              # Utilitários
    ├── __init__.py
    ├── analysis.py     # Análise comparativa
    ├── metrics.py      # Coleta de métricas
    └── tree_printer.py # Visualização de árvores
```

## 🎯 Funcionalidades Técnicas

### Validação Automática
- ✅ Verificação de puzzles válidos
- ✅ Detecção de puzzles solucionáveis
- ✅ Validação de movimentos
- ✅ Prevenção de estados inválidos

### Otimizações de Performance
- 🚀 Estruturas de dados eficientes
- 🚀 Hashing otimizado para estados
- 🚀 Prevenção de cycles
- 🚀 Memória gerenciada automaticamente

### Visualização Durante Busca
Durante a execução dos algoritmos, você verá apenas os estados limpos:
```
{ 1   2   3  }
{ 4       6  }
{ 7   5   8  }

{ 1   2   3  }
{ 4   5   6  }
{ 7       8  }
```

## 📊 Exemplo de Análise Comparativa

```
🏆 ANÁLISE COMPLETA DOS RESULTADOS
========================================
✅ Algoritmos bem-sucedidos: 6/8
❌ Algoritmos que falharam: 2

📊 TABELA DE RESULTADOS:
---------------------------------------------------------------------
Algoritmo          Sucesso  Movimentos Tempo(s)   Nós      Ótimo   
---------------------------------------------------------------------
BFS               ✅       4          0.0023     15       Sim     
A*-Manhattan      ✅       4          0.0018     8        Sim     
A*-Misplaced      ✅       4          0.0021     12       Sim     
Greedy-Manhattan  ✅       4          0.0012     6        Sim     

🏆 RANKINGS:
⚡ Por Velocidade (Tempo):
  1. Greedy-Manhattan: 0.0012s
  2. A*-Manhattan: 0.0018s
  3. A*-Misplaced: 0.0021s

🎯 Por Eficiência (Nós Explorados):
  1. Greedy-Manhattan: 6 nós
  2. A*-Manhattan: 8 nós
  3. A*-Misplaced: 12 nós
```

## 🔧 Dependências

### Obrigatórias
- Python 3.7+
- Nenhuma dependência externa obrigatória

### Opcionais (para funcionalidades avançadas)
- `pandas` - Análise de dados
- `matplotlib` - Gráficos de performance  
- `seaborn` - Visualizações estatísticas
- `numpy` - Operações numéricas otimizadas

```bash
pip install pandas matplotlib seaborn numpy
```

## 🎓 Conceitos Implementados

### Algoritmos de Busca
- **Busca Sem Informação**: BFS, DFS, IDS
- **Busca Com Informação**: A*, Greedy Search
- **Heurísticas**: Manhattan, Misplaced Tiles, Linear Conflict

### Estruturas de Dados
- **Estados**: Representação matricial eficiente
- **Árvore de Busca**: Navegação pai-filho
- **Fila de Prioridade**: Para algoritmos informados
- **Hash Tables**: Detecção rápida de estados visitados

### Análise de Complexidade
- **Temporal**: Medição precisa de tempo de execução
- **Espacial**: Contagem de nós explorados e memória
- **Otimalidade**: Verificação de soluções ótimas

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎯 Roadmap

- [ ] Interface gráfica (GUI) com Tkinter/PyQt
- [ ] Algoritmos adicionais (IDA*, SMA*)
- [ ] Puzzles de formatos diferentes (não-quadrados)
- [ ] Modo multithreading para comparações
- [ ] API REST para uso em web
- [ ] Plugins para heurísticas customizadas

## 📞 Contato

- **GitHub**: [@thavyne-KDR](https://github.com/thavyne-KDR)
- **Repositório**: [n_puzzle](https://github.com/thavyne-KDR/n_puzzle)

---

⭐ **Gostou do projeto? Deixe uma estrela no repositório!** ⭐
