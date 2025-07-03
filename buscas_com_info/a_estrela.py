import heapq
from typing import List, Optional, Set
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import ResultadoBusca
from utils.heuristicas import heuristica_manhattan, heuristica_pecas_fora_lugar, heuristica_manhattan_melhorada

class NoAEstrela:
    def __init__(self, estado: EstadoPuzzle, custo_g: int, custo_h: int):
        self.estado = estado
        self.custo_g = custo_g
        self.custo_h = custo_h
        self.custo_f = custo_g + custo_h
    
    def __lt__(self, other):
        if self.custo_f == other.custo_f:
            return self.custo_h < other.custo_h
        return self.custo_f < other.custo_f
    
    def __eq__(self, other):
        return self.estado.hash_estado == other.estado.hash_estado

class AEstrela:
    def __init__(self, problema: ProblemaPuzzle, heuristica: str = "manhattan"):
        self.problema = problema
        self.nos_expandidos = 0
        self.nos_gerados = 0
        self.memoria_maxima = 0
        self.nos_arvore = []
        
        if heuristica == "manhattan":
            self.funcao_heuristica = heuristica_manhattan
        elif heuristica == "pecas_fora_lugar":
            self.funcao_heuristica = heuristica_pecas_fora_lugar
        elif heuristica == "manhattan_melhorada":
            self.funcao_heuristica = heuristica_manhattan_melhorada
        else:
            raise ValueError(f"Heurística '{heuristica}' não reconhecida")
        
        self.nome_heuristica = heuristica
    
    def buscar(self, limite_tempo: int = 300, limite_memoria: int = 500000) -> ResultadoBusca:  # Aumentado para 500k
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, f"A* ({self.nome_heuristica})", 0)
        
        estado_inicial = self.problema.estado_inicial
        h_inicial = self.funcao_heuristica(estado_inicial.tabuleiro, self.problema.estado_objetivo)
        no_inicial = NoAEstrela(estado_inicial, 0, h_inicial)
        
        fronteira = [no_inicial]
        heapq.heapify(fronteira)
        custos_conhecidos = {estado_inicial.hash_estado: 0}
        fechados: Set[str] = set()
        
        self.nos_gerados = 1
        self.nos_arvore.append(estado_inicial)
        
        while fronteira:
            tempo_atual = time.time()
            if tempo_atual - inicio_tempo > limite_tempo or len(fronteira) + len(fechados) > limite_memoria:
                break
            
            memoria_atual = len(fronteira) + len(fechados)
            self.memoria_maxima = max(self.memoria_maxima, memoria_atual)
            
            no_atual = heapq.heappop(fronteira)
            estado_atual = no_atual.estado
            
            if estado_atual.hash_estado in fechados:
                continue
            
            fechados.add(estado_atual.hash_estado)
            self.nos_expandidos += 1
            
            if estado_atual.eh_objetivo(self.problema.estado_objetivo):
                tempo_execucao = time.time() - inicio_tempo
                caminho = self.problema.reconstruir_caminho(estado_atual)
                return ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, tempo_execucao, len(caminho) - 1, True, f"A* ({self.nome_heuristica})", self.memoria_maxima)
            
            for sucessor in self.problema.obter_sucessores(estado_atual):
                novo_custo_g = no_atual.custo_g + 1
                
                if (sucessor.hash_estado not in custos_conhecidos or novo_custo_g < custos_conhecidos[sucessor.hash_estado]):
                    custos_conhecidos[sucessor.hash_estado] = novo_custo_g
                    custo_h = self.funcao_heuristica(sucessor.tabuleiro, self.problema.estado_objetivo)
                    novo_no = NoAEstrela(sucessor, novo_custo_g, custo_h)
                    heapq.heappush(fronteira, novo_no)
                    
                    self.nos_gerados += 1
                    
                    if len(self.nos_arvore) < 1000:
                        self.nos_arvore.append(sucessor)
        
        tempo_execucao = time.time() - inicio_tempo
        return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, tempo_execucao, 0, False, f"A* ({self.nome_heuristica})", self.memoria_maxima)
    
    def obter_nos_arvore(self) -> List[EstadoPuzzle]:
        return self.nos_arvore
    
def executar_a_estrela(problema: ProblemaPuzzle, heuristica: str = "manhattan", bidirecional: bool = False, mostrar_caminho: bool = True, mostrar_arvore: bool = False) -> ResultadoBusca:
    print(f"\n{'='*50}\nEXECUTANDO ALGORITMO A*\nHeurística: {heuristica}\n{'='*50}")
    
    a_estrela = AEstrela(problema, heuristica)
    resultado = a_estrela.buscar()
    
    print(resultado)
    
    if resultado.sucesso and mostrar_caminho:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_caminho_detalhado(resultado.caminho)
    
    if mostrar_arvore:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_arvore_busca(a_estrela.obter_nos_arvore())
    
    print(f"\nEstatísticas A* ({a_estrela.nome_heuristica}): Nós expandidos: {a_estrela.nos_expandidos}, Nós gerados: {a_estrela.nos_gerados}, Memória máxima: {a_estrela.memoria_maxima} nós, Fator ramificação: {a_estrela.nos_gerados / max(1, a_estrela.nos_expandidos):.2f}")
    
    return resultado
