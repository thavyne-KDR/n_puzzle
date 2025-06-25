"""
Heurísticas para Algoritmos de Busca Informada

Este módulo implementa diferentes funções heurísticas para serem usadas
nos algoritmos A* e Busca Gulosa.
"""

from typing import Tuple
from puzzle import Puzzle


def manhattan_distance(puzzle: Puzzle) -> int:
    """
    Calcula a distância de Manhattan para o estado objetivo.
    
    A distância de Manhattan é a soma das distâncias horizontais e verticais
    de cada peça até sua posição correta no estado objetivo.
    
    Args:
        puzzle: Estado atual do puzzle
    
    Returns:
        Valor da heurística (distância de Manhattan total)
    """
    distance = 0
    size = puzzle.size
    
    for i in range(size):
        for j in range(size):
            value = puzzle.state[i][j]
            if value != 0:  # Ignora o espaço vazio
                # Calcula posição objetivo
                target_row = (value - 1) // size
                target_col = (value - 1) % size
                
                # Soma distância Manhattan
                distance += abs(i - target_row) + abs(j - target_col)
    
    return distance


def misplaced_tiles(puzzle: Puzzle) -> int:
    """
    Conta o número de peças fora de lugar.
    
    Esta heurística conta quantas peças não estão em suas posições corretas
    no estado objetivo (excluindo o espaço vazio).
    
    Args:
        puzzle: Estado atual do puzzle
    
    Returns:
        Número de peças fora de lugar
    """
    misplaced = 0
    size = puzzle.size
    expected = 1
    
    for i in range(size):
        for j in range(size):
            if i == size - 1 and j == size - 1:
                # Última posição deve ser 0 (espaço vazio)
                if puzzle.state[i][j] != 0:
                    misplaced += 1
            else:
                if puzzle.state[i][j] != expected:
                    misplaced += 1
                expected += 1
    
    return misplaced


def linear_conflict(puzzle: Puzzle) -> int:
    """
    Heurística de conflito linear combinada com distância de Manhattan.
    
    Dois blocos estão em conflito linear se:
    1. Estão na mesma linha ou coluna
    2. Suas posições objetivo estão na mesma linha ou coluna
    3. A ordem relativa está invertida
    
    Args:
        puzzle: Estado atual do puzzle
    
    Returns:
        Distância de Manhattan + 2 * número de conflitos lineares
    """
    distance = manhattan_distance(puzzle)
    conflicts = 0
    size = puzzle.size
    
    # Verifica conflitos nas linhas
    for i in range(size):
        conflicts += _count_conflicts_in_line(puzzle.state[i], i, size, True)
    
    # Verifica conflitos nas colunas
    for j in range(size):
        column = [puzzle.state[i][j] for i in range(size)]
        conflicts += _count_conflicts_in_line(column, j, size, False)
    
    return distance + 2 * conflicts


def _count_conflicts_in_line(line: list, line_index: int, size: int, is_row: bool) -> int:
    """
    Conta conflitos lineares em uma linha ou coluna.
    
    Args:
        line: Lista representando linha ou coluna
        line_index: Índice da linha/coluna
        size: Tamanho do puzzle
        is_row: True se for linha, False se for coluna
    
    Returns:
        Número de conflitos lineares na linha/coluna
    """
    conflicts = 0
    
    # Filtra valores que pertencem a esta linha/coluna no estado objetivo
    relevant_tiles = []
    for pos, value in enumerate(line):
        if value != 0:
            if is_row:
                target_row = (value - 1) // size
                if target_row == line_index:
                    relevant_tiles.append((pos, value))
            else:
                target_col = (value - 1) % size
                if target_col == line_index:
                    relevant_tiles.append((pos, value))
    
    # Conta conflitos entre pares de blocos relevantes
    for i in range(len(relevant_tiles)):
        for j in range(i + 1, len(relevant_tiles)):
            pos1, val1 = relevant_tiles[i]
            pos2, val2 = relevant_tiles[j]
            
            if is_row:
                target_pos1 = (val1 - 1) % size
                target_pos2 = (val2 - 1) % size
            else:
                target_pos1 = (val1 - 1) // size
                target_pos2 = (val2 - 1) // size
            
            # Verifica se estão em conflito
            if ((pos1 < pos2 and target_pos1 > target_pos2) or
                (pos1 > pos2 and target_pos1 < target_pos2)):
                conflicts += 1
    
    return conflicts


def get_heuristic_function(name: str):
    """
    Retorna a função heurística pelo nome.
    
    Args:
        name: Nome da heurística ('manhattan', 'misplaced', 'linear_conflict')
    
    Returns:
        Função heurística correspondente
    """
    heuristics = {
        'manhattan': manhattan_distance,
        'misplaced': misplaced_tiles,
        'linear_conflict': linear_conflict
    }
    
    if name not in heuristics:
        raise ValueError(f"Heurística desconhecida: {name}")
    
    return heuristics[name]
