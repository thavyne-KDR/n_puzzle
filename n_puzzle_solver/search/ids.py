"""
Busca com Aprofundamento Iterativo (Iterative Deepening Search - IDS)

Implementa o algoritmo IDS que combina as vantagens do DFS (eficiência em memória)
com as do BFS (garantia de solução ótima).
"""

from typing import List, Tuple, Set
from puzzle import Puzzle


class IDS:
    """
    Implementação do algoritmo de Busca com Aprofundamento Iterativo.
    
    Attributes:
        nodes_explored: Contador de nós explorados
        max_depth_reached: Profundidade máxima atingida
        solution_path: Caminho da solução encontrada
        iterations: Número de iterações executadas
    """
    
    def __init__(self, max_depth: int = 50):
        """
        Inicializa o algoritmo IDS.
        
        Args:
            max_depth: Profundidade máxima para busca
        """
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.solution_path = []
        self.max_depth = max_depth
        self.iterations = 0
        self.real_time_viz = False
        self.viz_delay = 0.5
        self.viz_callback = None
    
    def search(self, initial_puzzle: Puzzle) -> Tuple[bool, List[str]]:
        """
        Executa a busca com aprofundamento iterativo.
        
        Args:
            initial_puzzle: Estado inicial do puzzle
        
        Returns:
            Tupla (sucesso, caminho_solução)
            - sucesso: True se encontrou solução, False caso contrário
            - caminho_solução: Lista de movimentos para resolver o puzzle
        """
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.solution_path = []
        self.iterations = 0
        
        # Busca iterativa aumentando a profundidade
        for depth_limit in range(self.max_depth + 1):
            self.iterations += 1
            found, path = self._depth_limited_search(initial_puzzle, depth_limit)
            
            if found:
                self.solution_path = path
                return True, path
        
        return False, []
    
    def _depth_limited_search(self, initial_puzzle: Puzzle, depth_limit: int) -> Tuple[bool, List[str]]:
        """
        Executa busca limitada por profundidade.
        
        Args:
            initial_puzzle: Estado inicial do puzzle
            depth_limit: Limite de profundidade para esta iteração
        
        Returns:
            Tupla (sucesso, caminho_solução)
        """
        visited = set()
        
        def dls_recursive(puzzle: Puzzle, path: List[str], depth: int) -> Tuple[bool, List[str]]:
            """
            Função recursiva para busca limitada por profundidade.
            
            Args:
                puzzle: Estado atual do puzzle
                path: Caminho percorrido até agora
                depth: Profundidade atual
            
            Returns:
                Tupla (sucesso, caminho)
            """
            self.nodes_explored += 1
            self.max_depth_reached = max(self.max_depth_reached, depth)
            
            if puzzle.is_goal():
                return True, path.copy()
            
            if depth >= depth_limit:
                return False, []
            
            visited.add(puzzle)
            
            # Explora sucessores
            for successor, move in puzzle.get_successors():
                if successor not in visited:
                    new_path = path + [move]
                    found, result_path = dls_recursive(successor, new_path, depth + 1)
                    if found:
                        return True, result_path
            
            visited.remove(puzzle)
            return False, []
        
        return dls_recursive(initial_puzzle, [], 0)
    
    def set_real_time_visualization(self, enabled: bool, delay: float = 0.5, callback = None):
        """Configura visualização em tempo real."""
        self.real_time_viz = enabled
        self.viz_delay = delay
        self.viz_callback = callback
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas da busca executada.
        
        Returns:
            Dicionário com métricas de performance
        """
        return {
            'algorithm': 'IDS',
            'nodes_explored': self.nodes_explored,
            'max_depth': self.max_depth_reached,
            'solution_length': len(self.solution_path),
            'optimal': True,  # IDS garante solução ótima
            'iterations': self.iterations,
            'max_depth_limit': self.max_depth
        }
