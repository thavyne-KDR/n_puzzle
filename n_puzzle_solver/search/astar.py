"""
Algoritmo A* (A-Star)

Implementa o algoritmo A* que usa uma função de avaliação f(n) = g(n) + h(n)
onde g(n) é o custo do caminho e h(n) é a heurística.
"""

import time
import heapq
from typing import List, Tuple, Dict, Set, Callable
from puzzle import Puzzle
from search.heuristics import manhattan_distance, misplaced_tiles


class AStar:
    """
    Implementação do algoritmo A*.
    
    Attributes:
        nodes_explored: Contador de nós explorados
        max_depth: Profundidade máxima atingida
        solution_path: Caminho da solução encontrada
        heuristic_func: Função heurística utilizada
        real_time_viz: Se deve mostrar visualização em tempo real
        viz_delay: Delay entre visualizações
        viz_callback: Função para exibir estado atual
    """
    
    def __init__(self, heuristic: str = 'manhattan'):
        """
        Inicializa o algoritmo A*.
        
        Args:
            heuristic: Tipo de heurística ('manhattan' ou 'misplaced')
        """
        self.nodes_explored = 0
        self.max_depth = 0
        self.solution_path = []
        self.real_time_viz = False
        self.viz_delay = 0.5
        self.viz_callback = None
        
        if heuristic == 'manhattan':
            self.heuristic_func = manhattan_distance
        elif heuristic == 'misplaced':
            self.heuristic_func = misplaced_tiles
        else:
            raise ValueError(f"Heurística desconhecida: {heuristic}")
        
        self.heuristic_name = heuristic
    
    def set_real_time_visualization(self, enabled: bool, delay: float = 0.5, callback: Callable = None):
        """Configura visualização em tempo real."""
        self.real_time_viz = enabled
        self.viz_delay = delay
        self.viz_callback = callback
    
    def search(self, initial_puzzle: Puzzle) -> Tuple[bool, List[str]]:
        """
        Executa a busca A*.
        
        Args:
            initial_puzzle: Estado inicial do puzzle
        
        Returns:
            Tupla (sucesso, caminho_solução)
        """
        if initial_puzzle.is_goal():
            return True, []
        
        # Priority queue: (f_score, g_score, puzzle, path)
        open_set = []
        heapq.heappush(open_set, (
            self.heuristic_func(initial_puzzle),  # f_score inicial = h_score
            0,  # g_score
            initial_puzzle,
            []  # path
        ))
          # Conjuntos para controle de visitados
        closed_set: Set[Puzzle] = set()
        open_dict: Dict[Puzzle, int] = {initial_puzzle: 0}  # puzzle -> g_score
        
        self.nodes_explored = 0
        self.max_depth = 0
        
        while open_set:
            f_score, g_score, current_puzzle, path = heapq.heappop(open_set)
            
            # Verifica se já foi processado com custo menor
            if current_puzzle in closed_set:
                continue
            
            closed_set.add(current_puzzle)
            self.nodes_explored += 1
            self.max_depth = max(self.max_depth, len(path))
            
            # Visualização em tempo real
            if self.real_time_viz and self.viz_callback and self.nodes_explored % 3 == 0:
                h_value = self.heuristic_func(current_puzzle)
                message = f"A* ({self.heuristic_name}) - f={f_score:.1f}, g={g_score}, h={h_value}"
                self.viz_callback(current_puzzle, self.nodes_explored, len(path), message)
                time.sleep(self.viz_delay)
            
            # Verifica se é o objetivo
            if current_puzzle.is_goal():
                # Visualiza estado final
                if self.real_time_viz and self.viz_callback:
                    self.viz_callback(current_puzzle, self.nodes_explored, len(path), "🎉 SOLUÇÃO ÓTIMA ENCONTRADA!")
                    time.sleep(self.viz_delay * 2)
                
                self.solution_path = path
                return True, path
            
            # Explora sucessores
            for successor, move in current_puzzle.get_successors():
                if successor in closed_set:
                    continue
                
                tentative_g_score = g_score + 1
                new_path = path + [move]
                
                # Se não está no open_set ou encontrou caminho melhor
                if (successor not in open_dict or 
                    tentative_g_score < open_dict[successor]):
                    
                    open_dict[successor] = tentative_g_score
                    h_score = self.heuristic_func(successor)
                    f_score = tentative_g_score + h_score
                    
                    heapq.heappush(open_set, (
                        f_score,
                        tentative_g_score,
                        successor,
                        new_path
                    ))
            
            # Visualização em tempo real
            if self.real_time_viz and self.viz_callback:
                self.viz_callback(current_puzzle)
                time.sleep(self.viz_delay)
        
        # Solução não encontrada
        return False, []
    
    def get_metrics(self) -> dict:
        """
        Retorna métricas da busca executada.
        
        Returns:
            Dicionário com métricas de performance
        """
        return {
            'algorithm': 'A*',
            'heuristic': self.heuristic_name,
            'nodes_explored': self.nodes_explored,
            'max_depth': self.max_depth,
            'solution_length': len(self.solution_path),
            'optimal': True  # A* com heurística admissível é ótimo
        }
