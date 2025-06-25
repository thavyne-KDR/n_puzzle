"""
Módulo de algoritmos de busca para N-Puzzle Solver.

Este módulo contém implementações de diferentes algoritmos de busca:
- BFS (Busca em Largura)
- DFS (Busca em Profundidade)
- IDS (Busca com Aprofundamento Iterativo)
- A* (Busca A*)
- Greedy (Busca Gulosa)
- Heurísticas
"""

from .bfs import BFS
from .dfs import DFS
from .ids import IDS
from .astar import AStar
from .greedy import GreedySearch
from .heuristics import manhattan_distance, misplaced_tiles, linear_conflict

__all__ = [
    'BFS',
    'DFS', 
    'IDS',
    'AStar',
    'GreedySearch',
    'manhattan_distance',
    'misplaced_tiles',
    'linear_conflict'
]
