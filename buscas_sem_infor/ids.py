from typing import List, Optional, Set
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import ResultadoBusca

class IDS:
    def __init__(self, problema: ProblemaPuzzle):
        self.problema = problema
        self.nos_expandidos = 0
        self.nos_gerados = 0
        self.memoria_maxima = 0
        self.nos_arvore = []
        self.profundidade_atual = 0
    
    def buscar(self, limite_profundidade_max: int = 50, limite_tempo: int = 300) -> ResultadoBusca:
        inicio_tempo = time.time()
        
        if not self.problema.eh_solucionavel():
            return ResultadoBusca([], 0, 0, 0, 0, False, "IDS", 0)
        
        for profundidade_limite in range(limite_profundidade_max + 1):
            self.profundidade_atual = profundidade_limite
            
            if time.time() - inicio_tempo > limite_tempo:
                break
            
            print(f"Explorando profundidade {profundidade_limite}...")
            
            resultado = self._dfs_limitado(self.problema.estado_inicial, profundidade_limite, set(), inicio_tempo, limite_tempo)
            
            if resultado == "ENCONTRADO":
                tempo_execucao = time.time() - inicio_tempo
                return self.resultado_encontrado
            elif resultado == "LIMITE_TEMPO":
                break
        
        tempo_execucao = time.time() - inicio_tempo
        return ResultadoBusca([], self.nos_expandidos, self.nos_gerados, tempo_execucao, 0, False, "IDS", self.memoria_maxima)
    
    def _dfs_limitado(self, estado: EstadoPuzzle, limite_prof: int, visitados: Set[str], inicio_tempo: float, limite_tempo: int) -> str:
        if time.time() - inicio_tempo > limite_tempo:
            return "LIMITE_TEMPO"
        
        self.nos_expandidos += 1
        
        if len(self.nos_arvore) < 1000:
            self.nos_arvore.append(estado)
        
        self.memoria_maxima = max(self.memoria_maxima, len(visitados))
        
        if estado.eh_objetivo(self.problema.estado_objetivo):
            caminho = self.problema.reconstruir_caminho(estado)
            tempo_execucao = time.time() - inicio_tempo
            
            self.resultado_encontrado = ResultadoBusca(caminho, self.nos_expandidos, self.nos_gerados, tempo_execucao, len(caminho) - 1, True, "IDS", self.memoria_maxima)
            return "ENCONTRADO"
        
        if limite_prof <= 0:
            return "CUTOFF"
        
        visitados.add(estado.hash_estado)
        cutoff_ocorreu = False
        
        for sucessor in self.problema.obter_sucessores(estado):
            if sucessor.hash_estado not in visitados:
                self.nos_gerados += 1
                visitados_ramo = visitados.copy()
                
                resultado = self._dfs_limitado(sucessor, limite_prof - 1, visitados_ramo, inicio_tempo, limite_tempo)
                
                if resultado == "ENCONTRADO":
                    return "ENCONTRADO"
                elif resultado == "LIMITE_TEMPO":
                    return "LIMITE_TEMPO"
                elif resultado == "CUTOFF":
                    cutoff_ocorreu = True
        
        visitados.remove(estado.hash_estado)
        return "CUTOFF" if cutoff_ocorreu else "FALHA"
    
    def obter_nos_arvore(self) -> List[EstadoPuzzle]:
        return self.nos_arvore
def executar_ids(problema: ProblemaPuzzle, melhorado: bool = False, limite_profundidade: int = 50, mostrar_caminho: bool = True, mostrar_arvore: bool = False) -> ResultadoBusca:
    print(f"\n{'='*50}\nEXECUTANDO BUSCA COM APROFUNDAMENTO ITERATIVO (IDS)\nLimite de profundidade: {limite_profundidade}\n{'='*50}")
    
    ids = IDS(problema)
    resultado = ids.buscar(limite_profundidade_max=limite_profundidade)
    
    print(resultado)
    
    if resultado.sucesso and mostrar_caminho:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_caminho_detalhado(resultado.caminho)
    
    if mostrar_arvore:
        from utils.caminho import GeradorCaminhoVisual
        GeradorCaminhoVisual.imprimir_arvore_busca(ids.obter_nos_arvore())
    
    print(f"\nEstatísticas IDS: Profundidade final: {ids.profundidade_atual}, Nós expandidos: {ids.nos_expandidos}, Nós gerados: {ids.nos_gerados}, Memória máxima: {ids.memoria_maxima} nós, Fator ramificação: {ids.nos_gerados / max(1, ids.nos_expandidos):.2f}")
    
    return resultado
