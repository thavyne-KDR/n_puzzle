import time
import random
from typing import List, Dict
from problema import ProblemaPuzzle, EstadoPuzzle
from utils.caminho import AnalisadorResultados, GeradorCaminhoVisual, ResultadoBusca
from utils.heuristicas import comparar_heuristicas
from buscas_sem_infor.bfs import executar_bfs
from buscas_sem_infor.dfs import executar_dfs
from buscas_sem_infor.ids import executar_ids
from buscas_com_info.a_estrela import executar_a_estrela
from buscas_com_info.gulosa import executar_busca_gulosa

class SistemaNPuzzle:
    def __init__(self):
        self.analisador = AnalisadorResultados()
        self.problema_atual = None
    
    def criar_problema(self, estado_inicial: List[List[int]], tipo_puzzle: int) -> bool:
        try:
            self.problema_atual = ProblemaPuzzle(estado_inicial, tipo_puzzle)
            print(f"\n🧩 PUZZLE {tipo_puzzle} CRIADO")
            print("📋 Estado inicial:")
            self._imprimir_tabuleiro_formatado(self.problema_atual.estado_inicial.tabuleiro)
            
            if not self.problema_atual.eh_solucionavel():
                print("❌ Puzzle não solucionável")
                return False
            
            print("✅ Solucionável")
            heuristicas = comparar_heuristicas(
                self.problema_atual.estado_inicial.tabuleiro,
                self.problema_atual.estado_objetivo
            )
            
            print("🧠 Heurísticas:", ", ".join(f"{k}:{v}" for k,v in heuristicas.items()))
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def _executar_algoritmo(self, nome: str, func_exec, **kwargs):
        """Função genérica para executar algoritmos"""
        print(f"\n{nome}")
        resultado = func_exec(self.problema_atual, mostrar_caminho=False, **kwargs)
        self.analisador.adicionar_resultado(resultado)
        
        if resultado.sucesso:
            print(f"✅ Sucesso! Nós: {resultado.nos_expandidos}, "
                  f"Tempo: {resultado.tempo_execucao:.4f}s, Prof: {resultado.profundidade}")
            self._mostrar_solucao_interativa(resultado)
        else:
            print("❌ Solução não encontrada!")
            print(f"💡 Motivos: Puzzle muito difícil ou limites insuficientes")
            
        return resultado

    def menu_interativo(self):
        while True:
            print(f"\n{'='*40}")
            print("      🧩 SISTEMA N-PUZZLE 🧩")
            print(f"{'='*40}")
            print("🔍 ALGORITMOS:")
            print("  1.🔄 BFS  2.⬇️ DFS  3.🔁 IDS  4.⭐ A*  5.🎯 Gulosa")
            print("⚙️ FUNÇÕES:")
            print("  6.📊 Comparar (9 algoritmos)  7.📚 Exemplo  8.🎲 Aleatório")
            print("  0.🚪 Sair")
            print(f"{'='*40}")
            
            try:
                escolha = input("🎯 Opção: ").strip()
                
                if escolha == "0":
                    print("👋 Saindo...")
                    break
                elif escolha == "1":
                    self._executar_bfs()
                elif escolha == "2":
                    self._executar_dfs()
                elif escolha == "3":
                    self._executar_ids()
                elif escolha == "4":
                    self._executar_a_estrela()
                elif escolha == "5":
                    self._executar_busca_gulosa()
                elif escolha == "6":
                    self._comparar_algoritmos()
                elif escolha == "7":
                    self._carregar_exemplo()
                elif escolha == "8":
                    self._gerar_puzzle_aleatorio()
                else:
                    print(f"❌ Opção '{escolha}' inválida!")
                    
            except KeyboardInterrupt:
                print("\n⚠️ Cancelado (Ctrl+C)")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

    def _carregar_exemplo(self):
        opcoes = {"1": 8, "2": 15, "3": 24}
        print("\n📚 Exemplos MÉDIOS para demonstração:")
        print("  1. Puzzle-8 (20 passos)")
        print("  2. Puzzle-15 (13 passos)")  
        print("  3. Puzzle-24 (11 passos)")
        print("  0. Voltar")
        
        escolha = input("🎯 Escolha: ").strip()
        if escolha == "0":
            return
        elif escolha in opcoes:
            tipo = opcoes[escolha]
            estado_inicial = ProblemaPuzzle.criar_puzzle_exemplo(tipo)
            if self.criar_problema(estado_inicial, tipo):
                print(f"✅ Puzzle {tipo} (MÉDIO) carregado!")
        else:
            print("❌ Opção inválida!")
        input("\n⏎ Enter para continuar...")

    def _executar_a_estrela(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
            
        print("\n🧠 A*: 1.Manhattan 2.Peças fora lugar 3.Manhattan melhorada")
        escolha = input("🎯 Escolha (1-3): ").strip()
        
        if escolha == "3":
            heuristica = "manhattan_melhorada"
        elif escolha == "2":
            heuristica = "pecas_fora_lugar"
        else:
            heuristica = "manhattan"
        
        resultado = self._executar_algoritmo(f"⭐ A* ({heuristica})", executar_a_estrela, 
                                           heuristica=heuristica)
        input("\n⏎ Enter para continuar...")

    def _executar_bfs(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
        
        resultado = self._executar_algoritmo("🔄 BUSCA EM LARGURA (BFS)", executar_bfs)
        input("\n⏎ Enter para continuar...")
    
    def _executar_dfs(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
        
        limite = input("📏 Limite DFS (Enter=25): ").strip()
        limite_prof = 25 if not limite else int(limite) if limite.isdigit() else 25
        
        resultado = self._executar_algoritmo(f"⬇️ DFS (limite: {limite_prof})", executar_dfs, 
                                           limite_profundidade=limite_prof)
        input("\n⏎ Enter para continuar...")
    
    def _executar_ids(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
        
        limite = input("📏 Limite IDS (Enter=50): ").strip()
        limite_prof = 50 if not limite else int(limite) if limite.isdigit() else 50
        
        resultado = self._executar_algoritmo(f"🔁 IDS (limite: {limite_prof})", executar_ids, 
                                           limite_profundidade=limite_prof)
        input("\n⏎ Enter para continuar...")
    
    def _executar_busca_gulosa(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
            
        print("\n🧠 Busca Gulosa: 1.Manhattan 2.Peças fora lugar 3.Manhattan melhorada")
        escolha = input("🎯 Escolha (1-3): ").strip()
        
        if escolha == "3":
            heuristica = "manhattan_melhorada"
        elif escolha == "2":
            heuristica = "pecas_fora_lugar"
        else:
            heuristica = "manhattan"
        
        resultado = self._executar_algoritmo(f"🎯 Gulosa ({heuristica})", executar_busca_gulosa, 
                                           heuristica=heuristica)
        input("\n⏎ Enter para continuar...")
    
    def _comparar_algoritmos(self):
        if not self.problema_atual:
            print("❌ Carregue um puzzle primeiro (opção 7)")
            input("\n⏎ Enter para continuar...")
            return
            
        print("\n📊 Comparando todos os algoritmos...")
        confirmar = input("🤔 Executar comparação completa? (S/n): ").strip().lower()
        if confirmar in ['n', 'no', 'nao', 'não']:
            return
        
        print("\n🔄 Executando algoritmos...")
        self.analisador.limpar_resultados()
        
        # BFS
        print("1/9 - BFS...")
        resultado_bfs = executar_bfs(self.problema_atual, mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_bfs)
        
        # DFS
        print("2/9 - DFS...")
        resultado_dfs = executar_dfs(self.problema_atual, limite_profundidade=25, mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_dfs)
        
        # IDS  
        print("3/9 - IDS...")
        resultado_ids = executar_ids(self.problema_atual, limite_profundidade=50, mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_ids)
        
        # A* Manhattan
        print("4/9 - A* (Manhattan)...")
        resultado_a_man = executar_a_estrela(self.problema_atual, heuristica="manhattan", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_a_man)
        
        # A* Peças fora
        print("5/9 - A* (Peças fora)...")
        resultado_a_peca = executar_a_estrela(self.problema_atual, heuristica="pecas_fora_lugar", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_a_peca)
        
        # A* Manhattan Melhorada
        print("6/9 - A* (Manhattan Melhorada)...")
        resultado_a_mel = executar_a_estrela(self.problema_atual, heuristica="manhattan_melhorada", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_a_mel)
        
        # Gulosa Manhattan
        print("7/9 - Gulosa (Manhattan)...")
        resultado_g_man = executar_busca_gulosa(self.problema_atual, heuristica="manhattan", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_g_man)
        
        # Gulosa Peças fora
        print("8/9 - Gulosa (Peças fora)...")
        resultado_g_peca = executar_busca_gulosa(self.problema_atual, heuristica="pecas_fora_lugar", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_g_peca)
        
        # Gulosa Manhattan Melhorada
        print("9/9 - Gulosa (Manhattan Melhorada)...")
        resultado_g_mel = executar_busca_gulosa(self.problema_atual, heuristica="manhattan_melhorada", mostrar_caminho=False)
        self.analisador.adicionar_resultado(resultado_g_mel)
        
        print("\n📈 RESULTADOS DA COMPARAÇÃO:")
        print(self.analisador.gerar_tabela_comparativa())
        
        # Análise detalhada dos melhores algoritmos
        sucessos = [r for r in self.analisador.resultados if r.sucesso]
        if sucessos:
            print(f"\n🏆 ANÁLISE DOS MELHORES ALGORITMOS:")
            
            # Melhor por profundidade (solução ótima)
            melhor_prof = self.analisador.obter_melhor_resultado("profundidade")
            print(f"🎯 SOLUÇÃO ÓTIMA (menor profundidade): {melhor_prof.algoritmo}")
            print(f"   Profundidade: {melhor_prof.profundidade} | Nós: {melhor_prof.nos_expandidos} | Tempo: {melhor_prof.tempo_execucao:.4f}s")
            
            # Melhor por eficiência (menos nós expandidos)
            melhor_efic = min(sucessos, key=lambda x: x.nos_expandidos)
            print(f"🚀 MAIS EFICIENTE (menos nós): {melhor_efic.algoritmo}")
            print(f"   Profundidade: {melhor_efic.profundidade} | Nós: {melhor_efic.nos_expandidos} | Tempo: {melhor_efic.tempo_execucao:.4f}s")
            
            # Melhor por tempo
            melhor_tempo = self.analisador.obter_melhor_resultado("tempo")
            print(f"⚡ MAIS RÁPIDO: {melhor_tempo.algoritmo}")
            print(f"   Profundidade: {melhor_tempo.profundidade} | Nós: {melhor_tempo.nos_expandidos} | Tempo: {melhor_tempo.tempo_execucao:.4f}s")
            
            # Recomendação geral
            melhor_geral = self.analisador.obter_melhor_resultado_score()
            print(f"\n🌟 MELHOR ALGORITMO GERAL (score balanceado): {melhor_geral.algoritmo}")
            print(f"   Profundidade: {melhor_geral.profundidade} | Nós: {melhor_geral.nos_expandidos} | Tempo: {melhor_geral.tempo_execucao:.4f}s")
            
            print(f"\n💡 RECOMENDAÇÃO:")
            if melhor_efic.algoritmo.startswith("A*"):
                print(f"   Use {melhor_efic.algoritmo} - Melhor custo-benefício!")
            elif melhor_prof.nos_expandidos < 1000:
                print(f"   Use {melhor_prof.algoritmo} - Garante solução ótima com boa eficiência!")
            else:
                print(f"   Use {melhor_tempo.algoritmo} - Melhor para problemas grandes!")
        
        input("\n⏎ Enter para continuar...")
    
    def _gerar_puzzle_aleatorio(self):
        opcoes = {"1": 8, "2": 15, "3": 24}
        print("\n🎲 Gerar puzzle aleatório:")
        print("  1. Puzzle-8 (3x3)")
        print("  2. Puzzle-15 (4x4)")  
        print("  3. Puzzle-24 (5x5)")
        print("  0. Voltar")
        
        escolha = input("🎯 Escolha: ").strip()
        if escolha == "0":
            return
        elif escolha in opcoes:
            tipo = opcoes[escolha]
            
            # Gerar puzzle aleatório
            tamanho = int((tipo + 1) ** 0.5)
            objetivo = list(range(tipo + 1))
            tabuleiro = [objetivo[i * tamanho:(i + 1) * tamanho] for i in range(tamanho)]
            estado = EstadoPuzzle(tabuleiro, tamanho)
            
            # Embaralhar
            embaralhamentos = 100 if tipo == 8 else 200 if tipo == 15 else 300
            for _ in range(embaralhamentos):
                acoes = estado.obter_acoes_possiveis()
                if acoes:
                    acao = random.choice(acoes)
                    estado = estado.aplicar_acao(acao)
            
            estado_inicial = estado.tabuleiro
            if self.criar_problema(estado_inicial, tipo):
                print(f"✅ Puzzle {tipo} aleatório gerado!")
        else:
            print("❌ Opção inválida!")
        input("\n⏎ Enter para continuar...")

    def _mostrar_solucao_interativa(self, resultado: ResultadoBusca):
        """Mostra a solução de forma interativa com opções"""
        ver_movimentos = input("\n🎯 Deseja ver os movimentos passo a passo? (S/n): ")
        if ver_movimentos.lower() not in ['n', 'no', 'nao', 'não']:
            print(f"\n{'='*50}")
            print(f"SEQUÊNCIA DE MOVIMENTOS ({len(resultado.caminho)-1} passos)")
            print(f"{'='*50}")
            
            for i, estado in enumerate(resultado.caminho):
                if i == 0:
                    print("🏁 ESTADO INICIAL:")
                else:
                    print(f"\nPASSO {i} - Ação: {estado.acao}")
                
                # Mostrar o tabuleiro com formatação de chaves
                self._imprimir_tabuleiro_formatado(estado.tabuleiro)
                
                if i < len(resultado.caminho) - 1:
                    # Pausa automática de 2 segundos entre os passos
                    time.sleep(2)
                else:
                    print("\n🏆 OBJETIVO ALCANÇADO!")
    
    def _imprimir_tabuleiro_formatado(self, tabuleiro: List[List[int]]):
        """Imprime o tabuleiro com chaves no formato { }"""
        print()
        for linha in tabuleiro:
            linha_str = "{"
            for j, num in enumerate(linha):
                if num == 0:
                    linha_str += "   "
                else:
                    linha_str += f"{num:2d} "
                if j < len(linha) - 1:
                    linha_str += " "
            linha_str += "}"
            print(linha_str)
        print()

def main():
    sistema = SistemaNPuzzle()
    sistema.menu_interativo()

if __name__ == "__main__":
    main()