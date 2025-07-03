"""
Representação do Tabuleiro N-Puzzle e Operadores

Este módulo define a classe Puzzle que representa o estado do tabuleiro
e implementa os operadores de movimento (cima, baixo, esquerda, direita).
Inclui validações, otimizações e funcionalidades avançadas.
"""

import copy
import random
import itertools
from typing import List, Tuple, Optional, Set, Dict, Any
from dataclasses import dataclass


@dataclass
class PuzzleMove:
    """Representa um movimento no puzzle com informações detalhadas."""
    direction: str
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    tile_moved: int
    
    def __str__(self) -> str:
        return f"Move {self.tile_moved} {self.direction} ({self.from_pos} -> {self.to_pos})"


class PuzzleError(Exception):
    """Exceção base para erros relacionados ao puzzle."""
    pass


class InvalidPuzzleStateError(PuzzleError):
    """Lançada quando o estado do puzzle é inválido."""
    pass


class InvalidMoveError(PuzzleError):
    """Lançada quando um movimento inválido é tentado."""
    pass


class PuzzleValidator:
    """Classe utilitária para validação de puzzles."""
    
    @staticmethod
    def is_valid_puzzle(state: List[List[int]]) -> bool:
        """
        Verifica se o estado do puzzle é válido.
        
        Args:
            state: Matriz 2D representando o estado do puzzle
            
        Returns:
            True se o puzzle for válido, False caso contrário
        """
        if not state or not all(isinstance(row, list) for row in state):
            return False
        
        size = len(state)
        if size == 0 or not all(len(row) == size for row in state):
            return False
        
        # Verifica se todos os números de 0 a n²-1 estão presentes
        flat_state = [cell for row in state for cell in row]
        expected_numbers = set(range(size * size))
        actual_numbers = set(flat_state)
        
        return expected_numbers == actual_numbers
    
    @staticmethod
    def is_solvable(state: List[List[int]]) -> bool:
        """
        Verifica se o puzzle é solucionável usando a contagem de inversões.
        
        Args:
            state: Matriz 2D representando o estado do puzzle
            
        Returns:
            True se o puzzle for solucionável, False caso contrário
        """
        if not PuzzleValidator.is_valid_puzzle(state):
            return False
        
        size = len(state)
        flat_state = [cell for row in state for cell in row if cell != 0]
        
        # Conta inversões
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        
        # Para puzzles de tamanho ímpar, é solucionável se inversões for par
        if size % 2 == 1:
            return inversions % 2 == 0
        
        # Para puzzles de tamanho par, consideramos a posição do espaço vazio
        empty_row = next(i for i, row in enumerate(state) if 0 in row)
        
        # Se o espaço vazio está em uma linha ímpar de baixo para cima,
        # e o número de inversões é par, então é solucionável
        if (size - empty_row) % 2 == 1:
            return inversions % 2 == 0
        else:
            return inversions % 2 == 1


class PuzzleGenerator:
    """Gerador de puzzles aleatórios e configurações específicas."""
    
    @staticmethod
    def generate_goal_state(size: int) -> List[List[int]]:
        """
        Gera o estado objetivo para um puzzle de tamanho dado.
        
        Args:
            size: Tamanho do puzzle (n x n)
            
        Returns:
            Matriz 2D representando o estado objetivo
        """
        state = []
        num = 1
        for i in range(size):
            row = []
            for j in range(size):
                if i == size - 1 and j == size - 1:
                    row.append(0)  # Espaço vazio na última posição
                else:
                    row.append(num)
                    num += 1
            state.append(row)
        return state
    
    @staticmethod
    def generate_random_puzzle(size: int, max_attempts: int = 1000) -> List[List[int]]:
        """
        Gera um puzzle aleatório solucionável.
        
        Args:
            size: Tamanho do puzzle (n x n)
            max_attempts: Número máximo de tentativas para gerar puzzle solucionável
            
        Returns:
            Matriz 2D representando um puzzle aleatório solucionável
            
        Raises:
            PuzzleError: Se não conseguir gerar um puzzle solucionável
        """
        for _ in range(max_attempts):
            numbers = list(range(size * size))
            random.shuffle(numbers)
            
            state = []
            for i in range(size):
                row = []
                for j in range(size):
                    row.append(numbers[i * size + j])
                state.append(row)
            
            if PuzzleValidator.is_solvable(state):
                return state
        
        raise PuzzleError(f"Não foi possível gerar puzzle solucionável após {max_attempts} tentativas")
    
    @staticmethod
    def generate_puzzle_from_moves(size: int, num_moves: int) -> List[List[int]]:
        """
        Gera um puzzle aplicando movimentos aleatórios ao estado objetivo.
        
        Args:
            size: Tamanho do puzzle (n x n)
            num_moves: Número de movimentos aleatórios a aplicar
            
        Returns:
            Matriz 2D representando o puzzle gerado
        """
        goal_state = PuzzleGenerator.generate_goal_state(size)
        puzzle = Puzzle(goal_state)
        
        for _ in range(num_moves):
            possible_moves = puzzle.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                new_puzzle = puzzle.move(move)
                if new_puzzle:
                    puzzle = new_puzzle
        
        return puzzle.state


class Puzzle:
    """
    Representa um estado do N-Puzzle com funcionalidades avançadas.
    
    Attributes:
        state: Matriz 2D representando o estado atual do puzzle
        size: Tamanho do tabuleiro (n x n)
        empty_pos: Posição (linha, coluna) do espaço vazio (0)
        move_history: Histórico de movimentos realizados
        parent: Estado pai (para reconstrução do caminho)
        depth: Profundidade do estado na árvore de busca
        cost: Custo acumulado até este estado
    """
    
    def __init__(self, state: List[List[int]], parent: Optional['Puzzle'] = None, 
                 move_made: Optional[str] = None, depth: int = 0):
        """
        Inicializa um novo estado do puzzle.
        
        Args:
            state: Matriz 2D representando o estado inicial
            parent: Estado pai (opcional)
            move_made: Movimento que levou a este estado (opcional)
            depth: Profundidade na árvore de busca
            
        Raises:
            InvalidPuzzleStateError: Se o estado do puzzle for inválido
        """
        if not PuzzleValidator.is_valid_puzzle(state):
            raise InvalidPuzzleStateError("Estado do puzzle inválido")
        
        self.state = [row[:] for row in state]  # Deep copy mais eficiente
        self.size = len(state)
        self.empty_pos = self._find_empty_position()
        self.parent = parent
        self.move_made = move_made
        self.depth = depth
        self.cost = depth  # Para algoritmos simples, custo = profundidade
        self.move_history: List[str] = []
        
        # Constrói histórico de movimentos
        if parent and move_made:
            self.move_history = parent.move_history + [move_made]
    
    def _find_empty_position(self) -> Tuple[int, int]:
        """
        Encontra a posição do espaço vazio (0) no tabuleiro.
        
        Returns:
            Tupla (linha, coluna) da posição do espaço vazio
            
        Raises:
            InvalidPuzzleStateError: Se o espaço vazio não for encontrado
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0:
                    return (i, j)
        raise InvalidPuzzleStateError("Espaço vazio não encontrado no tabuleiro")    
    def is_goal(self) -> bool:
        """
        Verifica se o estado atual é o estado objetivo.
        
        Returns:
            True se for o estado objetivo, False caso contrário
        """
        return self._is_goal_optimized()
    
    def _is_goal_optimized(self) -> bool:
        """Versão otimizada da verificação de estado objetivo."""
        expected = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # Última posição deve ser 0 (espaço vazio)
                    return self.state[i][j] == 0
                if self.state[i][j] != expected:
                    return False
                expected += 1
        return True
    
    def distance_to_goal(self) -> int:
        """
        Calcula a distância de Manhattan até o estado objetivo.
        
        Returns:
            Distância de Manhattan total
        """
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                value = self.state[i][j]
                if value != 0:  # Ignora o espaço vazio
                    target_row = (value - 1) // self.size
                    target_col = (value - 1) % self.size
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance
    
    def misplaced_tiles_count(self) -> int:
        """
        Conta o número de peças fora de lugar.
        
        Returns:
            Número de peças fora de lugar
        """
        count = 0
        expected = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    if self.state[i][j] != 0:
                        count += 1
                else:
                    if self.state[i][j] != expected:
                        count += 1
                    expected += 1
        return count
    
    def get_possible_moves(self) -> List[str]:
        """
        Retorna lista de movimentos possíveis a partir do estado atual.
        
        Returns:
            Lista de strings representando os movimentos possíveis
            ['up', 'down', 'left', 'right']
        """
        moves = []
        row, col = self.empty_pos
        
        if row > 0:
            moves.append('up')
        if row < self.size - 1:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < self.size - 1:
            moves.append('right')
        
        return moves
    
    def move(self, direction: str) -> Optional['Puzzle']:
        """
        Executa um movimento e retorna o novo estado.
        
        Args:
            direction: Direção do movimento ('up', 'down', 'left', 'right')
        
        Returns:
            Novo objeto Puzzle com o estado após o movimento
            
        Raises:
            InvalidMoveError: Se o movimento for inválido
        """
        if direction not in self.get_possible_moves():
            raise InvalidMoveError(f"Movimento '{direction}' não é válido nesta posição")
        
        new_state = [row[:] for row in self.state]  # Deep copy eficiente
        row, col = self.empty_pos
        
        # Determina a nova posição do espaço vazio
        move_map = {
            'up': (row - 1, col),
            'down': (row + 1, col),
            'left': (row, col - 1),
            'right': (row, col + 1)
        }
        
        new_row, new_col = move_map[direction]
        
        # Troca os valores
        new_state[row][col] = new_state[new_row][new_col]
        new_state[new_row][new_col] = 0
        
        return Puzzle(new_state, parent=self, move_made=direction, depth=self.depth + 1)
    
    def move_safe(self, direction: str) -> Optional['Puzzle']:
        """
        Versão segura do movimento que retorna None em vez de lançar exceção.
        
        Args:
            direction: Direção do movimento
            
        Returns:
            Novo estado ou None se movimento inválido
        """
        try:
            return self.move(direction)
        except InvalidMoveError:
            return None
    
    def get_move_details(self, direction: str) -> Optional[PuzzleMove]:
        """
        Obtém detalhes sobre um movimento específico.
        
        Args:
            direction: Direção do movimento
            
        Returns:
            Objeto PuzzleMove com detalhes do movimento ou None se inválido
        """
        if direction not in self.get_possible_moves():
            return None
        
        row, col = self.empty_pos
        move_map = {
            'up': (row - 1, col),
            'down': (row + 1, col),
            'left': (row, col - 1),
            'right': (row, col + 1)
        }
        
        new_row, new_col = move_map[direction]
        tile_moved = self.state[new_row][new_col]
        
        return PuzzleMove(
            direction=direction,
            from_pos=(new_row, new_col),
            to_pos=(row, col),
            tile_moved=tile_moved
        )
    
    def get_successors(self) -> List[Tuple['Puzzle', str]]:
        """
        Retorna todos os estados sucessores possíveis.
        
        Returns:
            Lista de tuplas (novo_estado, movimento_executado)
        """
        successors = []
        for move in self.get_possible_moves():
            new_puzzle = self.move(move)
            if new_puzzle:
                successors.append((new_puzzle, move))
        return successors
    
    def get_successors_with_details(self) -> List[Tuple['Puzzle', PuzzleMove]]:
        """
        Retorna todos os estados sucessores com detalhes dos movimentos.
        
        Returns:
            Lista de tuplas (novo_estado, detalhes_movimento)
        """
        successors = []
        for move in self.get_possible_moves():
            new_puzzle = self.move_safe(move)
            move_details = self.get_move_details(move)
            if new_puzzle and move_details:
                successors.append((new_puzzle, move_details))
        return successors
    
    @classmethod
    def from_list(cls, flat_list: List[int]) -> 'Puzzle':
        """
        Cria um puzzle a partir de uma lista linear.
        
        Args:
            flat_list: Lista linear com os valores do puzzle
            
        Returns:
            Novo objeto Puzzle
            
        Raises:
            InvalidPuzzleStateError: Se a lista não formar um quadrado perfeito
        """
        size = int(len(flat_list) ** 0.5)
        if size * size != len(flat_list):
            raise InvalidPuzzleStateError("Lista não forma um quadrado perfeito")
        
        state = []
        for i in range(size):
            row = flat_list[i * size:(i + 1) * size]
            state.append(row)
        
        return cls(state)
    
    @classmethod
    def create_goal(cls, size: int) -> 'Puzzle':
        """
        Cria o estado objetivo para um tamanho dado.
        
        Args:
            size: Tamanho do puzzle (n x n)
            
        Returns:
            Objeto Puzzle representando o estado objetivo
        """
        state = PuzzleGenerator.generate_goal_state(size)
        return cls(state)
    
    @classmethod
    def create_random(cls, size: int, max_attempts: int = 1000) -> 'Puzzle':
        """
        Cria um puzzle aleatório solucionável.
        
        Args:
            size: Tamanho do puzzle (n x n)
            max_attempts: Número máximo de tentativas
            
        Returns:
            Objeto Puzzle aleatório solucionável
        """
        state = PuzzleGenerator.generate_random_puzzle(size, max_attempts)
        return cls(state)
    
    def clone(self) -> 'Puzzle':
        """
        Cria uma cópia independente do puzzle.
        
        Returns:
            Nova instância de Puzzle com o mesmo estado
        """
        return Puzzle(self.state, self.parent, self.move_made, self.depth)
    
    def get_flat_state(self) -> List[int]:
        """
        Retorna o estado como uma lista linear.
        
        Returns:
            Lista linear com os valores do puzzle
        """
        return [cell for row in self.state for cell in row]
    
    def get_state_string(self) -> str:
        """
        Retorna uma representação string compacta do estado.
        
        Returns:
            String representando o estado (útil para hashing)
        """
        return ''.join(map(str, self.get_flat_state()))
    
    def is_solvable(self) -> bool:
        """
        Verifica se o puzzle atual é solucionável.
        
        Returns:
            True se for solucionável, False caso contrário
        """
        return PuzzleValidator.is_solvable(self.state)
    
    def get_path_from_root(self) -> List[str]:
        """
        Obtém o caminho da raiz até este estado.
        
        Returns:
            Lista de movimentos da raiz até este estado
        """
        return self.move_history.copy()
    
    def get_path_length(self) -> int:
        """
        Retorna o comprimento do caminho da raiz até este estado.
        
        Returns:
            Número de movimentos da raiz
        """
        return len(self.move_history)
    
    def apply_moves(self, moves: List[str]) -> Optional['Puzzle']:
        """
        Aplica uma sequência de movimentos.
        
        Args:
            moves: Lista de movimentos para aplicar
            
        Returns:
            Estado final após aplicar todos os movimentos ou None se algum for inválido
        """
        current = self
        for move in moves:
            current = current.move_safe(move)
            if current is None:
                return None
        return current
    
    def undo_move(self) -> Optional['Puzzle']:
        """
        Desfaz o último movimento (retorna ao estado pai).
        
        Returns:
            Estado pai ou None se for a raiz
        """
        return self.parent
    
    def get_inversion_count(self) -> int:
        """
        Calcula o número de inversões no puzzle.
        
        Returns:
            Número de inversões
        """
        flat_state = [cell for cell in self.get_flat_state() if cell != 0]
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions
    
    def get_complexity_estimate(self) -> Dict[str, int]:
        """
        Retorna estimativas de complexidade do puzzle.
        
        Returns:
            Dicionário com métricas de complexidade
        """
        return {
            'manhattan_distance': self.distance_to_goal(),
            'misplaced_tiles': self.misplaced_tiles_count(),
            'inversion_count': self.get_inversion_count(),
            'depth': self.depth
        }
    
    def visualize(self, show_coordinates: bool = False, show_info: bool = True) -> str:
        """
        Cria uma visualização aprimorada do puzzle.
        
        Args:
            show_coordinates: Se deve mostrar coordenadas
            show_info: Se deve mostrar informações extras (distância, movimentos, etc.)
            
        Returns:
            String com visualização do puzzle
        """
        if show_coordinates:
            result = ["   " + " ".join(f"{j:2d}" for j in range(self.size))]
            result.append("  " + "---" * self.size)
        else:
            result = []
        
        for i, row in enumerate(self.state):
            row_str = []
            if show_coordinates:
                row_str.append(f"{i}|")
            
            # Cria a linha com chaves envolvendo toda a linha
            line_content = ""
            for j, cell in enumerate(row):
                if cell == 0:
                    line_content += "    "  # 4 espaços para o espaço vazio
                else:
                    line_content += f"{cell:2d}  "  # número com 2 espaços após
            
            # NÃO remove espaços do final para manter formatação consistente
            if show_coordinates:
                row_str.append(f"{{{line_content}}}")
            else:
                row_str.append(f"{{{line_content}}}")
            
            result.append(" ".join(row_str) if show_coordinates else row_str[0])
        
        # Adiciona informações extras apenas se solicitado
        if show_info:
            info = []
            if self.move_history:
                info.append(f"Movimentos: {' -> '.join(self.move_history)}")
            info.append(f"Distância Manhattan: {self.distance_to_goal()}")
            info.append(f"Peças fora de lugar: {self.misplaced_tiles_count()}")
            info.append(f"Solucionável: {'Sim' if self.is_solvable() else 'Não'}")
            
            if info:
                result.append("")
                result.extend(info)
        
        return "\n".join(result)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o puzzle para um dicionário.
        
        Returns:
            Dicionário representando o puzzle
        """
        return {
            'state': self.state,
            'size': self.size,
            'empty_pos': self.empty_pos,
            'move_history': self.move_history,
            'depth': self.depth,
            'manhattan_distance': self.distance_to_goal(),
            'misplaced_tiles': self.misplaced_tiles_count(),
            'is_goal': self.is_goal(),
            'is_solvable': self.is_solvable()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Puzzle':
        """
        Cria um puzzle a partir de um dicionário.
        
        Args:
            data: Dicionário com dados do puzzle
            
        Returns:
            Novo objeto Puzzle
        """
        puzzle = cls(data['state'])
        puzzle.depth = data.get('depth', 0)
        # move_history será reconstruído se necessário
        return puzzle
    
    def __eq__(self, other) -> bool:
        """Compara dois estados do puzzle para igualdade."""
        if not isinstance(other, Puzzle):
            return False
        return self.state == other.state
    
    def __lt__(self, other) -> bool:
        """Comparação para uso em heaps (baseada no custo)."""
        if not isinstance(other, Puzzle):
            return NotImplemented
        return self.cost < other.cost
    
    def __le__(self, other) -> bool:
        """Comparação menor ou igual."""
        if not isinstance(other, Puzzle):
            return NotImplemented
        return self.cost <= other.cost
    
    def __gt__(self, other) -> bool:
        """Comparação maior que."""
        if not isinstance(other, Puzzle):
            return NotImplemented
        return self.cost > other.cost
    
    def __ge__(self, other) -> bool:
        """Comparação maior ou igual."""
        if not isinstance(other, Puzzle):
            return NotImplemented
        return self.cost >= other.cost
    
    def __hash__(self) -> int:
        """
        Permite usar Puzzle como chave em dicionários e sets.
        Baseado no estado do tabuleiro para garantir consistência.
        """
        return hash(tuple(tuple(row) for row in self.state))
    
    def __str__(self) -> str:
        """Representação string limpa do estado do puzzle."""
        return self.visualize()
    
    def __repr__(self) -> str:
        """Representação para debug com informações completas."""
        return (f"Puzzle(size={self.size}, depth={self.depth}, "
                f"manhattan={self.distance_to_goal()}, "
                f"goal={self.is_goal()})")


# Funções utilitárias do módulo
def create_puzzle_from_string(puzzle_string: str) -> Puzzle:
    """
    Cria um puzzle a partir de uma string formatada.
    
    Args:
        puzzle_string: String com números separados por espaços/quebras de linha
        
    Returns:
        Novo objeto Puzzle
        
    Example:
        >>> puzzle_str = "1 2 3\\n4 5 6\\n7 8 0"
        >>> puzzle = create_puzzle_from_string(puzzle_str)
    """
    lines = puzzle_string.strip().split('\n')
    state = []
    for line in lines:
        row = [int(x) for x in line.split()]
        state.append(row)
    return Puzzle(state)


def puzzles_are_equivalent(puzzle1: Puzzle, puzzle2: Puzzle) -> bool:
    """
    Verifica se dois puzzles são equivalentes (mesmo estado).
    
    Args:
        puzzle1: Primeiro puzzle
        puzzle2: Segundo puzzle
        
    Returns:
        True se forem equivalentes, False caso contrário
    """
    return puzzle1 == puzzle2


def calculate_puzzle_statistics(puzzles: List[Puzzle]) -> Dict[str, Any]:
    """
    Calcula estatísticas de uma lista de puzzles.
    
    Args:
        puzzles: Lista de objetos Puzzle
        
    Returns:
        Dicionário com estatísticas
    """
    if not puzzles:
        return {}
    
    stats = {
        'total_puzzles': len(puzzles),
        'avg_manhattan_distance': sum(p.distance_to_goal() for p in puzzles) / len(puzzles),
        'avg_misplaced_tiles': sum(p.misplaced_tiles_count() for p in puzzles) / len(puzzles),
        'solvable_count': sum(1 for p in puzzles if p.is_solvable()),
        'goal_states': sum(1 for p in puzzles if p.is_goal()),
        'unique_states': len(set(puzzles)),
        'size_distribution': {}
    }
    
    # Distribuição por tamanho
    for puzzle in puzzles:
        size = puzzle.size
        if size not in stats['size_distribution']:
            stats['size_distribution'][size] = 0
        stats['size_distribution'][size] += 1
    
    return stats


# Constantes úteis
DIRECTION_OPPOSITES = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

DIRECTION_VECTORS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# Exemplo de uso e testes
if __name__ == "__main__":
    # Demonstração básica do uso da classe Puzzle
    print("🧩 DEMONSTRAÇÃO DO N-PUZZLE SOLVER")
    print("=" * 40)
    
    # Cria um puzzle 3x3 simples
    print("\n1️⃣ Criando puzzle 3x3:")
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    puzzle = Puzzle(initial_state)
    print(f"Estado inicial:\n{puzzle.visualize()}")
    
    # Testa validação
    print(f"\n✅ Puzzle válido: {PuzzleValidator.is_valid_puzzle(puzzle.state)}")
    print(f"✅ Puzzle solucionável: {puzzle.is_solvable()}")
    print(f"✅ É estado objetivo: {puzzle.is_goal()}")
    
    # Mostra métricas
    print(f"\n📊 Métricas:")
    print(f"   Distância Manhattan: {puzzle.distance_to_goal()}")
    print(f"   Peças fora de lugar: {puzzle.misplaced_tiles_count()}")
    print(f"   Número de inversões: {puzzle.get_inversion_count()}")
    
    # Testa movimentos
    print(f"\n🎮 Movimentos possíveis: {puzzle.get_possible_moves()}")
    
    # Aplica alguns movimentos
    print("\n2️⃣ Aplicando movimentos:")
    moves_to_try = ['up', 'right', 'down']
    current = puzzle
    
    for move in moves_to_try:
        try:
            new_puzzle = current.move(move)
            print(f"\nApós movimento '{move}':")
            print(new_puzzle.visualize())
            current = new_puzzle
            
            if current.is_goal():
                print("🎉 OBJETIVO ALCANÇADO!")
                break
        except InvalidMoveError as e:
            print(f"❌ Movimento inválido: {e}")
    
    # Demonstra geração de puzzle aleatório
    print("\n3️⃣ Gerando puzzle aleatório:")
    try:
        random_puzzle = Puzzle.create_random(3)
        print(f"Puzzle aleatório gerado:\n{random_puzzle.visualize()}")
    except PuzzleError as e:
        print(f"❌ Erro ao gerar puzzle: {e}")
    
    # Demonstra estado objetivo
    print("\n4️⃣ Estado objetivo:")
    goal = Puzzle.create_goal(3)
    print(f"Estado objetivo 3x3:\n{goal.visualize()}")
    
    print("\n✨ Demonstração concluída!")
