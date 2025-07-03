"""
Busca em Largura (Breadth-First Search - BFS)

Implementa o algoritmo de busca em largura para resolução do N-Puzzle.
Garante encontrar a solução ótima (menor número de movimentos).
"""

import time
from collections import deque
from typing import List, Optional, Tuple, Callable
from puzzle import Puzzle


class BFS:
    """
    Implementação do algoritmo de Busca em Largura.
    
    Attributes:
        nodes_explored: Contador de nós explorados
        max_depth: Profundidade máxima atingida
        solution_path: Caminho da solução encontrada
        real_time_viz: Se deve mostrar visualização em tempo real
        viz_delay: Delay entre visualizações
        viz_callback: Função para exibir estado atual
    """
    
    def __init__(self):
        """Inicializa o algoritmo BFS."""
        self.nodes_explored = 0
        self.max_depth = 0
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
        Executa a busca em largura.
        
        Args:
            initial_puzzle: Estado inicial do puzzle
        
        Returns:
            Tupla (sucesso, caminho_solução)
            - sucesso: True se encontrou solução, False caso contrário
            - caminho_solução: Lista de movimentos para resolver o puzzle
        """
        if initial_puzzle.is_goal():
            return True, []
          # Fila para BFS: (puzzle, caminho, profundidade)
        queue = deque([(initial_puzzle, [], 0)])
        visited = {initial_puzzle}
        
        self.nodes_explored = 0
        self.max_depth = 0
        
        while queue:
            current_puzzle, path, depth = queue.popleft()
            self.nodes_explored += 1
            self.max_depth = max(self.max_depth, depth)
            
            # Visualização em tempo real
            if self.real_time_viz and self.viz_callback and self.nodes_explored % 5 == 0:
                self.viz_callback(current_puzzle, self.nodes_explored, depth, f"BFS - Explorando nível {depth}")
                time.sleep(self.viz_delay)
            
            # Explora todos os sucessores
            for successor, move in current_puzzle.get_successors():
                if successor not in visited:
                    visited.add(successor)
                    new_path = path + [move]
                    
                    if successor.is_goal():
                        # Visualiza estado final
                        if self.real_time_viz and self.viz_callback:
                            self.viz_callback(successor, self.nodes_explored + 1, depth + 1, "🎉 SOLUÇÃO ENCONTRADA!")
                            time.sleep(self.viz_delay * 2)  # Pausa maior no final
                        
                        self.solution_path = new_path
                        return True, new_path
                    
                    queue.append((successor, new_path, depth + 1))
        
        # Solução não encontrada
        return False, []
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas da busca executada.
        
        Returns:
            Dicionário com métricas de performance
        """
        return {
            'algorithm': 'BFS',
            'nodes_explored': self.nodes_explored,
            'max_depth': self.max_depth,
            'solution_length': len(self.solution_path),
            'optimal': True  # BFS sempre encontra solução ótima
        }
