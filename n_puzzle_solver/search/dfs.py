"""
Busca em Profundidade (Depth-First Search - DFS)

Implementa o algoritmo de busca em profundidade com limite de profundidade
para evitar busca infinita no N-Puzzle.
"""

import time
from typing import List, Tuple, Set, Callable
from puzzle import Puzzle


class DFS:
    """
    Implementação do algoritmo de Busca em Profundidade.
    
    Attributes:
        depth_limit: Limite máximo de profundidade
        nodes_explored: Contador de nós explorados
        max_depth_reached: Profundidade máxima atingida
        solution_path: Caminho da solução encontrada
        real_time_viz: Se deve mostrar visualização em tempo real
        viz_delay: Delay entre visualizações
        viz_callback: Função para exibir estado atual
    """
    
    def __init__(self, depth_limit: int = 50):
        """
        Inicializa o algoritmo DFS.
        
        Args:
            depth_limit: Profundidade máxima para busca
        """
        self.depth_limit = depth_limit
        self.nodes_explored = 0
        self.max_depth_reached = 0
        self.solution_path = []
        self.real_time_viz = False
        self.viz_delay = 0.5
        self.viz_callback = None
    
    def set_real_time_visualization(self, enabled: bool, delay: float = 0.5, callback: Callable = None):
        """Configura visualização em tempo real."""
        self.real_time_viz = enabled
        self.viz_delay = delay
        self.viz_callback = callback

    def search(self, initial_puzzle: Puzzle) -> Tuple[bool, List[str]]:
        """
        Executa a busca em profundidade.
        
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
        
        visited = set()
        
        def dfs_recursive(puzzle: Puzzle, path: List[str], depth: int) -> bool:
            """
            Função recursiva para DFS.
            
            Args:
                puzzle: Estado atual do puzzle
                path: Caminho percorrido até agora
                depth: Profundidade atual
              Returns:
                True se encontrou solução, False caso contrário
            """
            if depth > self.depth_limit:
                return False
            
            self.nodes_explored += 1
            self.max_depth_reached = max(self.max_depth_reached, depth)
            
            # Visualização em tempo real
            if self.real_time_viz and self.viz_callback and self.nodes_explored % 10 == 0:
                message = f"DFS - Profundidade {depth}/{self.depth_limit}"
                self.viz_callback(puzzle, self.nodes_explored, depth, message)
                time.sleep(self.viz_delay)
            
            if puzzle.is_goal():
                # Visualiza estado final
                if self.real_time_viz and self.viz_callback:
                    self.viz_callback(puzzle, self.nodes_explored, depth, "🎉 SOLUÇÃO ENCONTRADA!")
                    time.sleep(self.viz_delay * 2)
                
                self.solution_path = path.copy()
                return True
            
            visited.add(puzzle)
            
            # Explora sucessores em profundidade
            for successor, move in puzzle.get_successors():
                if successor not in visited:
                    path.append(move)
                    if dfs_recursive(successor, path, depth + 1):
                        return True
                    path.pop()
            
            visited.remove(puzzle)
            return False
        
        success = dfs_recursive(initial_puzzle, [], 0)
        return success, self.solution_path.copy()
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas da busca executada.
        
        Returns:
            Dicionário com métricas de performance
        """
        return {
            'algorithm': 'DFS',
            'nodes_explored': self.nodes_explored,
            'max_depth': self.max_depth_reached,
            'solution_length': len(self.solution_path),
            'optimal': False,  # DFS não garante solução ótima
            'depth_limit': self.depth_limit
        }
