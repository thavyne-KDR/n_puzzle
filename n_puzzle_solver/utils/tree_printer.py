"""
Impressão da Árvore de Busca

Este módulo fornece funcionalidades para visualizar textualmente
a árvore de busca gerada pelos algoritmos.
"""

from typing import List, Dict, Any, Optional
from puzzle import Puzzle


class TreeNode:
    """
    Representa um nó na árvore de busca.
    
    Attributes:
        puzzle: Estado do puzzle neste nó
        parent: Nó pai
        children: Lista de nós filhos
        move: Movimento que levou a este nó
        depth: Profundidade do nó na árvore
        cost: Custo acumulado até este nó
        heuristic: Valor heurístico (se aplicável)
    """
    
    def __init__(self, puzzle: Puzzle, parent: Optional['TreeNode'] = None, 
                 move: Optional[str] = None, depth: int = 0):
        """
        Inicializa um nó da árvore.
        
        Args:
            puzzle: Estado do puzzle
            parent: Nó pai
            move: Movimento que levou a este nó
            depth: Profundidade na árvore
        """
        self.puzzle = puzzle
        self.parent = parent
        self.children: List['TreeNode'] = []
        self.move = move
        self.depth = depth
        self.cost = depth  # Para algoritmos simples, custo = profundidade
        self.heuristic = None
        
        if parent:
            parent.children.append(self)
    
    def add_child(self, puzzle: Puzzle, move: str) -> 'TreeNode':
        """
        Adiciona um nó filho.
        
        Args:
            puzzle: Estado do puzzle do filho
            move: Movimento que leva ao filho
        
        Returns:
            Novo nó filho criado
        """
        child = TreeNode(puzzle, self, move, self.depth + 1)
        return child
    
    def get_path_from_root(self) -> List[str]:
        """
        Obtém o caminho da raiz até este nó.
        
        Returns:
            Lista de movimentos da raiz até este nó
        """
        path = []
        node = self
        while node.parent is not None:
            path.append(node.move)
            node = node.parent
        return list(reversed(path))


class TreePrinter:
    """
    Classe para impressão textual da árvore de busca.
    
    Attributes:
        max_depth: Profundidade máxima para impressão
        max_children: Número máximo de filhos por nó a mostrar
        show_puzzles: Se deve mostrar os estados dos puzzles
    """
    
    def __init__(self, max_depth: int = 5, max_children: int = 4, 
                 show_puzzles: bool = False):
        """
        Inicializa o impressor de árvore.
        
        Args:
            max_depth: Profundidade máxima para impressão
            max_children: Número máximo de filhos por nó
            show_puzzles: Se deve mostrar estados dos puzzles
        """
        self.max_depth = max_depth
        self.max_children = max_children
        self.show_puzzles = show_puzzles
    
    def print_tree(self, root: TreeNode, title: str = "Árvore de Busca"):
        """
        Imprime a árvore de busca de forma textual.
        
        Args:
            root: Nó raiz da árvore
            title: Título da impressão
        """
        print(f"\n{title}")
        print("=" * len(title))
        print("Legenda: [profundidade] movimento -> estado")
        if self.show_puzzles:
            print("Estados do puzzle são mostrados abaixo de cada nó")
        print()
        
        self._print_node(root, "", True, set())
    
    def _print_node(self, node: TreeNode, prefix: str, is_last: bool, 
                   visited: set, is_root: bool = True):
        """
        Imprime um nó e seus filhos recursivamente.
        
        Args:
            node: Nó atual
            prefix: Prefixo para indentação
            is_last: Se é o último filho
            visited: Conjunto de nós já visitados (para evitar loops)
            is_root: Se é o nó raiz
        """
        # Evita loops infinitos
        if id(node) in visited:
            print(f"{prefix}{'└── ' if is_last else '├── '}[CICLO DETECTADO]")
            return
        
        visited.add(id(node))
        
        # Para de imprimir se atingiu profundidade máxima
        if node.depth > self.max_depth:
            print(f"{prefix}{'└── ' if is_last else '├── '}[...] (profundidade máxima atingida)")
            return
        
        # Formata informações do nó
        if is_root:
            node_info = f"[{node.depth}] RAIZ"
        else:
            node_info = f"[{node.depth}] {node.move}"
        
        # Adiciona informações extras se disponíveis
        extras = []
        if hasattr(node, 'heuristic') and node.heuristic is not None:
            extras.append(f"h={node.heuristic}")
        if hasattr(node, 'cost'):
            extras.append(f"g={node.cost}")
        
        if extras:
            node_info += f" ({', '.join(extras)})"
        
        # Verifica se é estado objetivo
        if node.puzzle.is_goal():
            node_info += " ★ OBJETIVO"
        
        # Imprime o nó
        connector = "└── " if is_last else "├── "
        if is_root:
            print(node_info)
        else:
            print(f"{prefix}{connector}{node_info}")
        
        # Imprime estado do puzzle se solicitado
        if self.show_puzzles and not is_root:
            puzzle_lines = str(node.puzzle).split('\n')
            for i, line in enumerate(puzzle_lines):
                if is_last:
                    print(f"{prefix}    {line}")
                else:
                    print(f"{prefix}│   {line}")
        
        # Imprime filhos (limitando quantidade)
        children_to_show = node.children[:self.max_children]
        if len(node.children) > self.max_children:
            # Adiciona nó indicando que há mais filhos
            children_to_show.append(None)  # Placeholder para "mais filhos"
        
        for i, child in enumerate(children_to_show):
            is_last_child = (i == len(children_to_show) - 1)
            
            if child is None:
                # Mostra indicação de mais filhos
                remaining = len(node.children) - self.max_children
                connector = "└── " if is_last_child else "├── "
                if is_root:
                    print(f"    {connector}[...] (+{remaining} filhos)")
                else:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    print(f"{new_prefix}{connector}[...] (+{remaining} filhos)")
            else:
                if is_root:
                    new_prefix = "    "
                else:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                
                self._print_node(child, new_prefix, is_last_child, visited, False)
        
        visited.remove(id(node))
    
    def generate_solution_path_tree(self, solution_path: List[str], 
                                   initial_puzzle: Puzzle) -> TreeNode:
        """
        Gera uma árvore representando apenas o caminho da solução.
        
        Args:
            solution_path: Lista de movimentos da solução
            initial_puzzle: Estado inicial do puzzle
        
        Returns:
            Nó raiz da árvore do caminho da solução
        """
        root = TreeNode(initial_puzzle)
        current_node = root
        current_puzzle = initial_puzzle
        
        for move in solution_path:
            new_puzzle = current_puzzle.move(move)
            if new_puzzle:
                current_node = current_node.add_child(new_puzzle, move)
                current_puzzle = new_puzzle
        
        return root
    
    def print_solution_path(self, solution_path: List[str], 
                           initial_puzzle: Puzzle):
        """
        Imprime o caminho da solução de forma linear.
        
        Args:
            solution_path: Lista de movimentos da solução
            initial_puzzle: Estado inicial do puzzle
        """
        print("\nCAMINHO DA SOLUÇÃO")
        print("=" * 18)
        
        current_puzzle = initial_puzzle
        print(f"Estado inicial (Passo 0):")
        print(current_puzzle)
        print()
        
        for step, move in enumerate(solution_path, 1):
            current_puzzle = current_puzzle.move(move)
            if current_puzzle:
                print(f"Passo {step}: {move}")
                print(current_puzzle)
                if current_puzzle.is_goal():
                    print("★ OBJETIVO ALCANÇADO!")
                print()
    
    def export_tree_to_text(self, root: TreeNode, filename: str):
        """
        Exporta a árvore para um arquivo de texto.
        
        Args:
            root: Nó raiz da árvore
            filename: Nome do arquivo de saída
        """
        import sys
        from io import StringIO
        
        # Captura a saída da impressão
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            self.print_tree(root, "Árvore de Busca Exportada")
        finally:
            sys.stdout = old_stdout
        
        # Salva no arquivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(captured_output.getvalue())
        
        print(f"Árvore exportada para {filename}")
