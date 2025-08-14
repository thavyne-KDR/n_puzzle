<div align="center">
   <h1>🧩 N-Puzzle IA</h1>
   <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/15-puzzle.png" alt="N-Puzzle" width="160"/>
</div>

---

## 📋 Sobre o Projeto

Sistema para explorar e comparar algoritmos de busca aplicados ao N-Puzzle, um clássico desafio de lógica. Foco educacional e prático, com código simples, visualização do processo e métricas de desempenho.

---

## 🚀 Funcionalidades

✅ Suporte a diferentes tamanhos de puzzle (8, 15, 24)
✅ Interface interativa no terminal
✅ Visualização do caminho da solução
✅ Métricas detalhadas: tempo, passos, nós expandidos
✅ Duas heurísticas: Peças Fora do Lugar e Distância Manhattan

---

## 🔍 Algoritmos

| Algoritmo | Tipo       | Heurística | Descrição                                            |
| --------- | ---------- | ---------- | ---------------------------------------------------- |
| BFS       | Cega       | ❌         | Solução ótima, alto consumo de memória               |
| DFS       | Cega       | ❌         | Baixo consumo de memória, pode gerar caminhos longos |
| IDS       | Cega       | ❌         | Mistura BFS e DFS                                    |
| Gulosa    | Heurística | ✔️         | Rápida, não garante solução ótima                    |
| A\*       | Heurística | ✔️         | Ótima com heurística admissível                      |

---

### 🎯 Heurísticas

1. **Peças Fora do Lugar:** Conta quantas peças estão fora da posição correta.
2. **Distância Manhattan:** Soma das distâncias de cada peça até sua posição objetivo.

---

## 🏗️ Estrutura do Projeto

```text
n_puzzle-main/
├── main.py
├── problema.py
├── buscas_com_info/
├── buscas_sem_infor/
├── utils/
└── README.md
```

---

## 🛠️ Como Usar

1. Tenha Python 3 instalado
2. Baixe o projeto
3. Execute no terminal:
   ```bash
   python main.py
   ```
4. Siga as instruções para escolher tamanho, estado inicial e algoritmo

---

## 💡 Exemplo de Uso

```
===== N-PUZZLE =====
Escolha o tamanho: 8, 15 ou 24
Escolha o algoritmo: BFS, DFS, IDS, Gulosa, A*
Veja o resultado: passos, tempo, nós expandidos
```

---

## 📊 Métricas de Performance

- Passos da solução
- Tempo de execução
- Nós expandidos
- Profundidade máxima

---

## 📚 Referências

- Artificial Intelligence: A Modern Approach (Russell & Norvig)
- [15 Puzzle - Wikipedia](https://en.wikipedia.org/wiki/15_puzzle)

---

## 🗂️ Fluxo do Sistema

```ascii
┌─────────────┐
│  main.py    │
└─────┬───────┘
   │
   ▼
┌─────────────┐
│ problema.py │
└─────┬───────┘
   │
   ▼
┌─────────────────────────────┐
│ Algoritmos de Busca        │
│ (buscas_com_info/, buscas_sem_infor/) │
└─────┬──────────────────────┘
   │
   ▼
┌─────────────┐
│  utils/     │
└─────────────┘
```

---

## 📝 Licença

Projeto educacional. Sinta-se livre para usar e modificar.
