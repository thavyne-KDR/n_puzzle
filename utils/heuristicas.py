from typing import List

def heuristica_pecas_fora_lugar(estado_atual: List[List[int]], estado_objetivo: List[List[int]]) -> int:
    pecas_fora = 0
    tamanho = len(estado_atual)
    
    for i in range(tamanho):
        for j in range(tamanho):
            if estado_atual[i][j] != 0 and estado_atual[i][j] != estado_objetivo[i][j]:
                pecas_fora += 1
    
    return pecas_fora

def heuristica_manhattan(estado_atual: List[List[int]], estado_objetivo: List[List[int]]) -> int:
    distancia_total = 0
    tamanho = len(estado_atual)
    
    posicoes_objetivo = {}
    for i in range(tamanho):
        for j in range(tamanho):
            if estado_objetivo[i][j] != 0:
                posicoes_objetivo[estado_objetivo[i][j]] = (i, j)
    
    for i in range(tamanho):
        for j in range(tamanho):
            numero = estado_atual[i][j]
            if numero != 0:
                pos_objetivo = posicoes_objetivo[numero]
                distancia = abs(i - pos_objetivo[0]) + abs(j - pos_objetivo[1])
                distancia_total += distancia
    
    return distancia_total

def heuristica_manhattan_melhorada(estado_atual: List[List[int]], estado_objetivo: List[List[int]]) -> int:
    manhattan = heuristica_manhattan(estado_atual, estado_objetivo)
    conflitos = 0
    tamanho = len(estado_atual)
    
    posicoes_objetivo = {}
    for i in range(tamanho):
        for j in range(tamanho):
            if estado_objetivo[i][j] != 0:
                posicoes_objetivo[estado_objetivo[i][j]] = (i, j)
    
    for i in range(tamanho):
        for j in range(tamanho - 1):
            num1 = estado_atual[i][j]
            num2 = estado_atual[i][j + 1]
            
            if num1 != 0 and num2 != 0:
                pos1_obj = posicoes_objetivo[num1]
                pos2_obj = posicoes_objetivo[num2]
                
                if pos1_obj[0] == pos2_obj[0] == i and pos1_obj[1] > pos2_obj[1]:
                    conflitos += 2
    
    for j in range(tamanho):
        for i in range(tamanho - 1):
            num1 = estado_atual[i][j]
            num2 = estado_atual[i + 1][j]
            
            if num1 != 0 and num2 != 0:
                pos1_obj = posicoes_objetivo[num1]
                pos2_obj = posicoes_objetivo[num2]
                
                if pos1_obj[1] == pos2_obj[1] == j and pos1_obj[0] > pos2_obj[0]:
                    conflitos += 2
    
    return manhattan + conflitos

def comparar_heuristicas(estado_atual: List[List[int]], estado_objetivo: List[List[int]]) -> dict:
    return {
        'pecas_fora_lugar': heuristica_pecas_fora_lugar(estado_atual, estado_objetivo),
        'manhattan': heuristica_manhattan(estado_atual, estado_objetivo),
        'manhattan_melhorada': heuristica_manhattan_melhorada(estado_atual, estado_objetivo)
    }
