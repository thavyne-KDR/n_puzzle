"""
Módulo de algoritmos de busca com informação para o N-Puzzle.
Implementa A* e Busca Gulosa com diferentes heurísticas.
"""

from .a_estrela import executar_a_estrela
from .gulosa import executar_busca_gulosa

__all__ = ['executar_a_estrela', 'executar_busca_gulosa']
