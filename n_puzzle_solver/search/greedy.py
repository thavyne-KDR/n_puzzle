"""
Busca Gulosa (Greedy Search)

Implementa o algoritmo de busca gulosa que usa apenas a função heurística
para guiar a busca, sem considerar o custo do caminho.
"""

import heapq
from typing import List, Tuple, Set
from puzzle import Puzzle
from search.heuristics import manhattan_distance, misplaced_tiles


class GreedySearch:
    """
    Implementação do algoritmo de Busca Gulosa.
    
    Attributes:
        nodes_explored: Contador de nós explorados
        max_depth: Profundidade máxima atingida
        solution_path: Caminho da solução encontrada
        heuristic_func: Função heurística utilizada
    """
    
    def __init__(self, heuristic: str = 'manhattan'):
        """
        Inicializa o algoritmo de busca gulosa.
        
        Args:
            heuristic: Tipo de heurística ('manhattan' ou 'misplaced')
        """
        self.nodes_explored = 0
        self.max_depth = 0
        self.solution_path = []
        
        if heuristic == 'manhattan':
            self.heuristic_func = manhattan_distance
        elif heuristic == 'misplaced':
            self.heuristic_func = misplaced_tiles
        else:
            raise ValueError(f"Heurística desconhecida: {heuristic}")
        
        self.heuristic_name = heuristic
        self.real_time_viz = False
        self.viz_delay = 0.5
        self.viz_callback = None
    
    def search(self, initial_puzzle: Puzzle) -> Tuple[bool, List[str]]:
        """
        Executa a busca gulosa.
        
        Args:
            initial_puzzle: Estado inicial do puzzle
        
        Returns:
            Tupla (sucesso, caminho_solução)
        """
        if initial_puzzle.is_goal():
            return True, []
        
        # Priority queue: (h_score, depth, puzzle, path)
        open_set = []
        heapq.heappush(open_set, (
            self.heuristic_func(initial_puzzle),
            0,  # depth
            initial_puzzle,
            []  # path
        ))
        
        visited: Set[Puzzle] = set()
        self.nodes_explored = 0
        self.max_depth = 0
        
        while open_set:
            h_score, depth, current_puzzle, path = heapq.heappop(open_set)
            
            # Verifica se já foi visitado
            if current_puzzle in visited:
                continue
            
            visited.add(current_puzzle)
            self.nodes_explored += 1
            self.max_depth = max(self.max_depth, depth)
            
            # Verifica se é o objetivo
            if current_puzzle.is_goal():
                self.solution_path = path
                return True, path
            
            # Explora sucessores
            for successor, move in current_puzzle.get_successors():
                if successor not in visited:
                    h_score = self.heuristic_func(successor)
                    new_path = path + [move]
                    
                    heapq.heappush(open_set, (
                        h_score,
                        depth + 1,
                        successor,
                        new_path
                    ))
        
        # Solução não encontrada
        return False, []
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas da busca executada.
        
        Returns:
            Dicionário com métricas de performance
        """
        return {
            'algorithm': 'Greedy',
            'heuristic': self.heuristic_name,
            'nodes_explored': self.nodes_explored,
            'max_depth': self.max_depth,
            'solution_length': len(self.solution_path),
            'optimal': False  # Busca gulosa não garante solução ótima
        }
    
    def set_real_time_visualization(self, enabled: bool, delay: float = 0.5, callback = None):
        """Configura visualização em tempo real."""
        self.real_time_viz = enabled
        self.viz_delay = delay
        self.viz_callback = callback
