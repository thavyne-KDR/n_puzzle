"""
Módulo de algoritmos de busca sem informação para o N-Puzzle.
Implementa BFS, DFS e IDS.
"""

from .bfs import executar_bfs
from .dfs import executar_dfs
from .ids import executar_ids

__all__ = ['executar_bfs', 'executar_dfs', 'executar_ids']
