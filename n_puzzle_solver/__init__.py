"""
N-Puzzle Solver - Solucionador Completo de N-Puzzles

Este projeto fornece uma implementação completa de um solucionador de N-Puzzles
com múltiplos algoritmos de busca, métricas de performance e interface interativa.

Módulos principais:
- puzzle: Classe principal do puzzle com validação e geração
- main: Interface principal do programa
- search: Algoritmos de busca (BFS, DFS, IDS, A*, Greedy)
- utils: Utilitários (métricas, visualização)

Autor: Desenvolvido com assistência de IA
Versão: 2.0
"""

from .puzzle import Puzzle, PuzzleGenerator, PuzzleValidator, InvalidPuzzleStateError
from .main import NPuzzleSolver

__version__ = "2.0"
__author__ = "Desenvolvido com assistência de IA"

__all__ = [
    'Puzzle',
    'PuzzleGenerator', 
    'PuzzleValidator',
    'InvalidPuzzleStateError',
    'NPuzzleSolver'
]
