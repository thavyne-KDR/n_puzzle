import heapq
from typing import List, Optional, Set
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import ResultadoBusca
from utils.heuristicas import heuristica_manhattan, heuristica_pecas_fora_lugar, heuristica_manhattan_melhorada

class NoGuloso:
    def __init__(self, estado: EstadoPuzzle, custo_h: int, profundidade: int = 0):
        self.estado = estado
        self.custo_h = custo_h
        self.profundidade = profundidade
    
    def __lt__(self, other):
        if self.custo_h == other.custo_h:
            return self.profundidade < other.profundidade
        return self.custo_h < other.custo_h
    
    def __eq__(self, other):
        return self.estado.hash_estado == other.estado.hash_estado

class BuscaGulosa:
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
    
    def buscar(self, limite_tempo: int = 300, limite_memoria: int = 100000, evitar_ciclos: bool = True) -> ResultadoBusca:
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, f"Busca Gulosa ({self.nome_heuristica})", 0)
        
        estado_inicial = self.problema.estado_inicial
        h_inicial = self.funcao_heuristica(estado_inicial.tabuleiro, self.problema.estado_objetivo)
        no_inicial = NoGuloso(estado_inicial, h_inicial, 0)
        
        fronteira = [no_inicial]
        heapq.heapify(fronteira)
        visitados: Set[str] = set() if evitar_ciclos else None
        
        self.nos_gerados = 1
        self.nos_arvore.append(estado_inicial)
        
        while fronteira:
            tempo_atual = time.time()
            if tempo_atual - inicio_tempo > limite_tempo or len(fronteira) > limite_memoria:
                break
            
            self.memoria_maxima = max(self.memoria_maxima, len(fronteira) + (len(visitados) if visitados else 0))
            
            no_atual = heapq.heappop(fronteira)
            estado_atual = no_atual.estado
            
            if evitar_ciclos:
                if estado_atual.hash_estado in visitados:
                    continue
                visitados.add(estado_atual.hash_estado)
            
            self.nos_expandidos += 1
            
            if estado_atual.eh_objetivo(self.problema.estado_objetivo):
                tempo_execucao = time.time() - inicio_tempo
                caminho = self.problema.reconstruir_caminho(estado_atual)
                return ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, tempo_execucao, len(caminho) - 1, True, f"Busca Gulosa ({self.nome_heuristica})", self.memoria_maxima)
            
            for sucessor in self.problema.obter_sucessores(estado_atual):
                if not evitar_ciclos or sucessor.hash_estado not in visitados:
                    custo_h = self.funcao_heuristica(sucessor.tabuleiro, self.problema.estado_objetivo)
                    novo_no = NoGuloso(sucessor, custo_h, no_atual.profundidade + 1)
                    heapq.heappush(fronteira, novo_no)
                    
                    self.nos_gerados += 1
                    
                    if len(self.nos_arvore) < 1000:
                        self.nos_arvore.append(sucessor)
        
        tempo_execucao = time.time() - inicio_tempo
        return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, tempo_execucao, 0, False, f"Busca Gulosa ({self.nome_heuristica})", self.memoria_maxima)
    
    def obter_nos_arvore(self) -> List[EstadoPuzzle]:
        return self.nos_arvore

def executar_busca_gulosa(problema: ProblemaPuzzle, heuristica: str = "manhattan", evitar_ciclos: bool = True, mostrar_caminho: bool = True, mostrar_arvore: bool = False) -> ResultadoBusca:
    print(f"\n{'='*50}\nEXECUTANDO BUSCA GULOSA\nHeurística: {heuristica}\nEvitar ciclos: {evitar_ciclos}\n{'='*50}")
    
    busca_gulosa = BuscaGulosa(problema, heuristica)
    resultado = busca_gulosa.buscar(evitar_ciclos=evitar_ciclos)
    
    print(resultado)
    
    if resultado.sucesso and mostrar_caminho:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_caminho_detalhado(resultado.caminho)
    
    if mostrar_arvore:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_arvore_busca(busca_gulosa.obter_nos_arvore())
    
    print(f"\nEstatísticas Busca Gulosa ({busca_gulosa.nome_heuristica}): Nós expandidos: {busca_gulosa.nos_expandidos}, Nós gerados: {busca_gulosa.nos_gerados}, Memória máxima: {busca_gulosa.memoria_maxima} nós, Fator ramificação: {busca_gulosa.nos_gerados / max(1, busca_gulosa.nos_expandidos):.2f}")
    
    return resultado
