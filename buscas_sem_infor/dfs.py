from typing import List, Optional, Set
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import ResultadoBusca

class DFS:
    def __init__(self, problema: ProblemaPuzzle):
        self.problema = problema
        self.nos_expandidos = 0
        self.nos_gerados = 0
        self.memoria_maxima = 0
        self.nos_arvore = []
    
    def buscar(self, limite_profundidade: int = 50, limite_tempo: int = 300) -> ResultadoBusca:
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, "DFS", 0)
        
        resultado_dfs = self._dfs_recursivo(self.problema.estado_inicial, set(), limite_profundidade, inicio_tempo, limite_tempo)
        tempo_execucao = time.time() - inicio_tempo
        
        if resultado_dfs:
            caminho = self.problema.reconstruir_caminho(resultado_dfs)
            return ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, tempo_execucao, len(caminho) - 1, True, "DFS", self.memoria_maxima)
        else:
            return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, tempo_execucao, 0, False, "DFS", self.memoria_maxima)
    
    def _dfs_recursivo(self, estado: EstadoPuzzle, visitados: Set[str], limite_prof: int, inicio_tempo: float, limite_tempo: int) -> Optional[EstadoPuzzle]:
        if time.time() - inicio_tempo > limite_tempo or limite_prof <= 0:
            return None
        
        if len(self.nos_arvore) < 1000:
            self.nos_arvore.append(estado)
        
        self.nos_expandidos += 1
        visitados.add(estado.hash_estado)
        self.memoria_maxima = max(self.memoria_maxima, len(visitados))
        
        if estado.eh_objetivo(self.problema.estado_objetivo):
            return estado
        
        for sucessor in self.problema.obter_sucessores(estado):
            if sucessor.hash_estado not in visitados:
                self.nos_gerados += 1
                resultado = self._dfs_recursivo(sucessor, visitados.copy(), limite_prof - 1, inicio_tempo, limite_tempo)
                if resultado is not None:
                    return resultado
        return None
    
    def obter_nos_arvore(self) -> List[EstadoPuzzle]:
        return self.nos_arvore
class DFSIterativo:
    def __init__(self, problema: ProblemaPuzzle):
        self.problema = problema
        self.nos_expandidos = 0
        self.nos_gerados = 0
        self.memoria_maxima = 0
        self.nos_arvore = []
    
    def buscar(self, limite_profundidade: int = 50, limite_tempo: int = 300) -> ResultadoBusca:
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, "DFS-Iterativo", 0)
        
        pilha = [(self.problema.estado_inicial, 0, set())]
        self.nos_gerados = 1
        
        while pilha:
            if time.time() - inicio_tempo > limite_tempo:
                break
            
            estado_atual, profundidade, visitados_caminho = pilha.pop()
            
            if profundidade > limite_profundidade or estado_atual.hash_estado in visitados_caminho:
                continue
            
            self.nos_expandidos += 1
            novo_visitados = visitados_caminho.copy()
            novo_visitados.add(estado_atual.hash_estado)
            
            if len(self.nos_arvore) < 1000:
                self.nos_arvore.append(estado_atual)
            
            self.memoria_maxima = max(self.memoria_maxima, len(pilha) + len(novo_visitados))
            
            if estado_atual.eh_objetivo(self.problema.estado_objetivo):
                tempo_execucao = time.time() - inicio_tempo
                caminho = self.problema.reconstruir_caminho(estado_atual)
                return ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, tempo_execucao, len(caminho) - 1, True, "DFS-Iterativo", self.memoria_maxima)
            
            sucessores = self.problema.obter_sucessores(estado_atual)
            sucessores.reverse()
            
            for sucessor in sucessores:
                if sucessor.hash_estado not in novo_visitados:
                    pilha.append((sucessor, profundidade + 1, novo_visitados))
                    self.nos_gerados += 1
        
        tempo_execucao = time.time() - inicio_tempo
        return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, tempo_execucao, 0, False, "DFS-Iterativo", self.memoria_maxima)

def executar_dfs(problema: ProblemaPuzzle, iterativo: bool = False, limite_profundidade: int = 50, mostrar_caminho: bool = True, mostrar_arvore: bool = False) -> ResultadoBusca:
    tipo_dfs = "ITERATIVO" if iterativo else "RECURSIVO"
    print(f"\n{'='*50}\nEXECUTANDO BUSCA EM PROFUNDIDADE (DFS {tipo_dfs})\nLimite de profundidade: {limite_profundidade}\n{'='*50}")
    
    dfs = DFSIterativo(problema) if iterativo else DFS(problema)
    resultado = dfs.buscar(limite_profundidade=limite_profundidade)
    
    print(resultado)
    
    if resultado.sucesso and mostrar_caminho:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_caminho_detalhado(resultado.caminho)
    
    if mostrar_arvore:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_arvore_busca(dfs.obter_nos_arvore())
    
    print(f"\nEstatísticas DFS: Nós expandidos: {dfs.nos_expandidos}, Nós gerados: {dfs.nos_gerados}, Memória máxima: {dfs.memoria_maxima} nós, Fator ramificação: {dfs.nos_gerados / max(1, dfs.nos_expandidos):.2f}")
    
    return resultado
