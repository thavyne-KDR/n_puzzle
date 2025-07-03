"""
Módulo de utilitários para o N-Puzzle.
Contém funções para análise de caminhos, heurísticas e visualização.
"""

from .caminho import ResultadoBusca, AnalisadorResultados, GeradorCaminhoVisual
from .heuristicas import (
    heuristica_manhattan, 
    heuristica_pecas_fora_lugar, 
    heuristica_manhattan_melhorada,
    comparar_heuristicas
)

__all__ = [
    'ResultadoBusca',
    'AnalisadorResultados', 
    'GeradorCaminhoVisual',
    'heuristica_manhattan',
    'heuristica_pecas_fora_lugar',
    'heuristica_manhattan_melhorada',
    'comparar_heuristicas'
]
