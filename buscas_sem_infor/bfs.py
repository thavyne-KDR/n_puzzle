from collections import deque
from typing import Set, List
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import ResultadoBusca

class BFS:
    def __init__(self, problema: ProblemaPuzzle):
        self.problema = problema
        self.nos_expandidos = 0
        self.nos_gerados = 0
        self.memoria_maxima = 0
        self.nos_arvore = []
    
    def buscar(self, limite_tempo: int = 300, limite_memoria: int = 100000) -> ResultadoBusca:
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, "BFS", 0)
        
        # Inicialização
        fronteira = deque([self.problema.estado_inicial])
        visitados: Set[str] = set()
        visitados.add(self.problema.estado_inicial.hash_estado)
        
        self.nos_gerados = 1
        self.nos_arvore.append(self.problema.estado_inicial)
        
        while fronteira:
            # Verificar limites
            tempo_atual = time.time()
            if tempo_atual - inicio_tempo > limite_tempo:
                print(f"Limite de tempo excedido ({limite_tempo}s)")
                break
            
            if len(fronteira) + len(visitados) > limite_memoria:
                print(f"Limite de memória excedido ({limite_memoria} nós)")
                break
            
            # Atualizar memória máxima
            memoria_atual = len(fronteira) + len(visitados)
            self.memoria_maxima = max(self.memoria_maxima, memoria_atual)
            
            # Expandir nó
            estado_atual = fronteira.popleft()
            self.nos_expandidos += 1
            
            if estado_atual.eh_objetivo(self.problema.estado_objetivo):
                tempo_execucao = time.time() - inicio_tempo
                caminho = self.problema.reconstruir_caminho(estado_atual)
                return ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, 
                                    tempo_execucao, len(caminho) - 1, True, "BFS", self.memoria_maxima)
            
            sucessores = self.problema.obter_sucessores(estado_atual)
            for sucessor in sucessores:
                if sucessor.hash_estado not in visitados:
                    visitados.add(sucessor.hash_estado)
                    fronteira.append(sucessor)
                    self.nos_gerados += 1
                    if len(self.nos_arvore) < 1000:
                        self.nos_arvore.append(sucessor)
        
        tempo_execucao = time.time() - inicio_tempo
        return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, 
                            tempo_execucao, 0, False, "BFS", self.memoria_maxima)
    
    def obter_nos_arvore(self) -> List[EstadoPuzzle]:
        return self.nos_arvore

def executar_bfs(problema: ProblemaPuzzle, mostrar_caminho: bool = True, 
                 mostrar_arvore: bool = False) -> ResultadoBusca:
    print("\n" + "="*50)
    print("EXECUTANDO BUSCA EM LARGURA (BFS)")
    print("="*50)
    
    bfs = BFS(problema)
    resultado = bfs.buscar()
    resultado.nos_arvore = bfs.obter_nos_arvore()
    
    print(resultado)
    
    if resultado.sucesso and mostrar_caminho:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_caminho_detalhado(resultado.caminho)
    
    if mostrar_arvore:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_arvore_busca(bfs.obter_nos_arvore())
    
    return resultado
