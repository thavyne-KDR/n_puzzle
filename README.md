# 🧩 N-Puzzle IA

![N-Puzzle](https://upload.wikimedia.org/wikipedia/commons/8/88/15-puzzle.png)

![Python](https://img.shields.io/badge/python-3.7%2B-blue) ![Status](https://img.shields.io/badge/status-educacional-success) ![License](https://img.shields.io/badge/license-MIT-green)

---

## 📑 Sumário

- [📋 Descrição](#-descrição)
- [🚀 Funcionalidades](#-funcionalidades)
- [🔍 Algoritmos Implementados](#-algoritmos-implementados)
- [💡 Exemplo de Execução](#-exemplo-de-execução)
- [📊 Métricas de Performance](#-métricas-de-performance)
- [🗂️ Fluxo do Sistema](#-fluxo-do-sistema)
- [📝 Licença](#-licença)

---

## 📋 Descrição

Este repositório apresenta uma implementação acadêmica do problema N-Puzzle utilizando algoritmos clássicos de busca informada e não informada.

O objetivo é fornecer uma base para estudos em Inteligência Artificial, permitindo a análise de desempenho, comparação de heurísticas e compreensão dos métodos de resolução de problemas.

---

## 🚀 Funcionalidades

- Suporte a diferentes tamanhos de puzzle: 8, 15 e 24 peças
- Interface interativa via terminal
- Visualização do caminho da solução
- Métricas detalhadas: tempo de execução, número de passos, nós expandidos
- Implementação de duas heurísticas: Peças Fora do Lugar e Distância Manhattan

---

## 🔍 Algoritmos Implementados

| Algoritmo | Tipo          | Heurística | Descrição                                            |
| --------- | ------------- | ---------- | ---------------------------------------------------- |
| BFS       | Não informada | ❌         | Solução ótima, alto consumo de memória               |
| DFS       | Não informada | ❌         | Baixo consumo de memória, pode gerar caminhos longos |
| IDS       | Não informada | ❌         | Combina BFS e DFS                                    |
| Gulosa    | Informada     | ✔️         | Rápida, não garante solução ótima                    |
| A\*       | Informada     | ✔️         | Ótima com heurística admissível                      |

---

## 💡 Exemplo de Execução

```text
🧩 N-PUZZLE
----------------------
Escolha o tamanho do puzzle:
   [1] 8 peças
   [2] 15 peças
   [3] 24 peças

Digite o estado inicial (ou use o padrão):
   Exemplo: 1 2 3 4 5 6 7 8 0

Selecione o algoritmo de busca:
   [1] BFS
   [2] DFS
   [3] IDS
   [4] Gulosa
   [5] A*

Escolha a heurística (se aplicável):
   [1] Peças Fora do Lugar
   [2] Distância Manhattan

----------------------
✔️ Solução encontrada!
Passos: 25
Tempo: 0.32s
Nós expandidos: 1200
Profundidade máxima: 18
Solução: [1, 2, 3, 4, 5, 6, 7, 8, 0]
```

---

## 📊 Métricas de Performance

- Número de passos da solução
- Tempo de execução
- Nós expandidos
- Profundidade máxima atingida

---

## 🗂️ Fluxo do Sistema

```text
main.py
   │
   ▼
problema.py
   │
   ▼
buscas_com_info/   buscas_sem_infor/
   │
   ▼
utils/
```

---

## 📝 Licença

Este projeto tem finalidade educacional e está aberto para uso e modificação.
