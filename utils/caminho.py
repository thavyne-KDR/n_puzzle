from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ResultadoBusca:
    caminho: List[Any]
    nos_expandidos: int
    nos_gerados: int
    tempo_execucao: float
    profundidade: int
    sucesso: bool
    algoritmo: str
    memoria_maxima: int = 0
    
    def __str__(self) -> str:
        return f"""
Algoritmo: {self.algoritmo}
Sucesso: {'Sim' if self.sucesso else 'Não'}
Profundidade da solução: {self.profundidade}
Nós expandidos: {self.nos_expandidos}
Nós gerados: {self.nos_gerados}
Tempo de execução: {self.tempo_execucao:.4f}s
Memória máxima (nós): {self.memoria_maxima}
"""

class AnalisadorResultados:
    def __init__(self):
        self.resultados: List[ResultadoBusca] = []
    
    def adicionar_resultado(self, resultado: ResultadoBusca):
        self.resultados.append(resultado)
    
    def limpar_resultados(self):
        self.resultados.clear()
    
    def gerar_tabela_comparativa(self) -> str:
        if not self.resultados:
            return "Nenhum resultado para comparar."
        
        tabela = f"\n{'='*100}\nCOMPARAÇÃO DE ALGORITMOS\n{'='*100}\n"
        tabela += f"{'Algoritmo':<25} {'Sucesso':<8} {'Profund.':<8} {'Expandidos':<12} {'Gerados':<10} {'Tempo(s)':<10} {'Memória':<8}\n"
        tabela += "-" * 100 + "\n"
        
        for resultado in self.resultados:
            sucesso = "Sim" if resultado.sucesso else "Não"
            tabela += f"{resultado.algoritmo:<25} {sucesso:<8} {resultado.profundidade:<8} {resultado.nos_expandidos:<12} {resultado.nos_gerados:<10} {resultado.tempo_execucao:<10.4f} {resultado.memoria_maxima:<8}\n"
        
        return tabela
    
    def obter_melhor_resultado(self, criterio: str = "profundidade") -> ResultadoBusca:
        if not self.resultados:
            return None
        
        sucessos = [r for r in self.resultados if r.sucesso]
        if not sucessos:
            return None
        
        if criterio == "profundidade":
            return min(sucessos, key=lambda x: x.profundidade)
        elif criterio == "tempo":
            return min(sucessos, key=lambda x: x.tempo_execucao)
        elif criterio == "memoria":
            return min(sucessos, key=lambda x: x.memoria_maxima)
        else:
            return sucessos[0]
    
    def obter_melhor_resultado_score(self) -> ResultadoBusca:
        """
        Calcula o melhor algoritmo baseado em um score que considera:
        - Profundidade da solução (30% - ótimo é importante)
        - Eficiência (nós expandidos) (40% - muito importante)
        - Tempo de execução (30% - importante)
        """
        sucessos = [r for r in self.resultados if r.sucesso]
        if not sucessos:
            return None
        
        if len(sucessos) == 1:
            return sucessos[0]
        
        # Normalizar métricas (0 a 1, onde 0 é melhor)
        min_prof = min(r.profundidade for r in sucessos)
        max_prof = max(r.profundidade for r in sucessos)
        
        min_nos = min(r.nos_expandidos for r in sucessos)
        max_nos = max(r.nos_expandidos for r in sucessos)
        
        min_tempo = min(r.tempo_execucao for r in sucessos)
        max_tempo = max(r.tempo_execucao for r in sucessos)
        
        melhor_score = float('inf')
        melhor_resultado = None
        
        for resultado in sucessos:
            # Normalizar profundidade (0-1)
            norm_prof = 0 if max_prof == min_prof else (resultado.profundidade - min_prof) / (max_prof - min_prof)
            
            # Normalizar nós expandidos (0-1)
            norm_nos = 0 if max_nos == min_nos else (resultado.nos_expandidos - min_nos) / (max_nos - min_nos)
            
            # Normalizar tempo (0-1)
            norm_tempo = 0 if max_tempo == min_tempo else (resultado.tempo_execucao - min_tempo) / (max_tempo - min_tempo)
            
            # Score final (pesos: profundidade 30%, nós 40%, tempo 30%)
            score = (norm_prof * 0.3) + (norm_nos * 0.4) + (norm_tempo * 0.3)
            
            if score < melhor_score:
                melhor_score = score
                melhor_resultado = resultado
        
        return melhor_resultado

class GeradorCaminhoVisual:
    @staticmethod
    def imprimir_caminho_simples(caminho: List[Any]):
        print(f"\nCaminho da solução ({len(caminho)} estados):")
        for i, estado in enumerate(caminho):
            if i == 0:
                print(f"Estado inicial:")
            else:
                print(f"Passo {i} - Ação: {estado.acao}")
            print(estado)
            if i < len(caminho) - 1:
                print("↓")
    
    @staticmethod
    def imprimir_caminho_detalhado(caminho: List[Any]):
        print(f"\n{'='*50}\nCAMINHO DA SOLUÇÃO ({len(caminho)} estados)\n{'='*50}")
        for i, estado in enumerate(caminho):
            if i == 0:
                print("Estado inicial:")
            else:
                print(f"Passo {i} - Ação: {estado.acao}")
            print(estado)
            if i < len(caminho) - 1:
                print("-" * 20)
    
    @staticmethod
    def imprimir_arvore_busca(nos_arvore: List[Any], limite: int = 10):
        print(f"\nÁrvore de busca (primeiros {min(limite, len(nos_arvore))} nós):")
        for i, no in enumerate(nos_arvore[:limite]):
            print(f"Nó {i+1}:")
            print(no)
            print("-" * 15)
    
    @staticmethod
    def salvar_caminho_arquivo(caminho: List[Any], nome_arquivo: str):
        try:
            with open(nome_arquivo, 'w') as f:
                f.write(f"Caminho da solução ({len(caminho)} estados):\n\n")
                for i, estado in enumerate(caminho):
                    if i == 0:
                        f.write("Estado inicial:\n")
                    else:
                        f.write(f"Passo {i} - Ação: {estado.acao}\n")
                    f.write(str(estado) + "\n")
                    if i < len(caminho) - 1:
                        f.write("-" * 20 + "\n")
            print(f"Caminho salvo em {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

class EstatisticasAvancadas:
    @staticmethod
    def calcular_fator_ramificacao(resultado: ResultadoBusca) -> float:
        if resultado.nos_expandidos == 0:
            return 0.0
        return resultado.nos_gerados / resultado.nos_expandidos
    
    @staticmethod
    def comparar_eficiencia(resultados: List[ResultadoBusca]) -> Dict[str, Any]:
        if not resultados:
            return {}
        
        sucessos = [r for r in resultados if r.sucesso]
        if not sucessos:
            return {"erro": "Nenhum algoritmo teve sucesso"}
        
        melhor_tempo = min(sucessos, key=lambda x: x.tempo_execucao)
        melhor_memoria = min(sucessos, key=lambda x: x.memoria_maxima)
        melhor_profundidade = min(sucessos, key=lambda x: x.profundidade)
        
        return {
            "melhor_tempo": melhor_tempo.algoritmo,
            "melhor_memoria": melhor_memoria.algoritmo,
            "melhor_profundidade": melhor_profundidade.algoritmo,
            "total_algoritmos": len(resultados),
            "algoritmos_sucesso": len(sucessos)
        }
