#!/usr/bin/env python3
"""
N-Puzzle Solver - Interface Principal Completa v3.0 

Sistema completo para resolução de N-Puzzle com implementação de todos os requisitos:

PARTE 1 - BUSCAS SEM INFORMAÇÃO:
- Puzzles 8 e 15 números
- Algoritmos: BFS, DFS, IDS
- Formulação completa do problema
- Geração e exibição da árvore de busca
- Análise comparativa detalhada

PARTE 2 - BUSCAS COM INFORMAÇÃO:
- Puzzles 8, 15 e 24 números
- Algoritmos: A*, Greedy Search
- Heurísticas: Manhattan, Peças Fora do Lugar, Conflito Linear
- Visualização de árvores de busca
- Métricas e análises de performance

CARACTERÍSTICAS TÉCNICAS:
- Entrada: configuração inicial do tabuleiro (lista/matriz nxn)  
- Saída: sequência de movimentos, número de passos, tempo de execução, árvore de busca
- Operadores: mover para cima, baixo, esquerda, direita (custo uniforme = 1)
- Visualização em tempo real e análise comparativa
- Geração de gráficos e tabelas de performance

Uso: python main.py
"""

import json
import time
import os
import sys
import subprocess
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

def auto_install_dependencies():
    """Instala automaticamente as dependências necessárias (modo silencioso)."""
    required_packages = [
        'pandas>=1.5.0',
        'matplotlib>=3.6.0', 
        'seaborn>=0.12.0',
        'numpy>=1.24.0'
    ]
    
    for package in required_packages:
        package_name = package.split('>=')[0]
        try:
            __import__(package_name)
        except ImportError:
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package, '--quiet'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                return False
    
    return True

# Executa instalação automática das dependências (modo silencioso)
if auto_install_dependencies():
    # Agora importa as bibliotecas com segurança
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        VISUALIZATION_AVAILABLE = True
    except ImportError:
        VISUALIZATION_AVAILABLE = False
        
        # Define mocks para compatibilidade
        class MockVisualization:
            def __getattr__(self, name):
                def mock_method(*args, **kwargs):
                    return None
                return mock_method
        
        pd = MockVisualization()
        plt = MockVisualization()
        sns = MockVisualization()
        np = MockVisualization()
else:
    VISUALIZATION_AVAILABLE = False
    
    # Define mocks para compatibilidade
    class MockVisualization:
        def __getattr__(self, name):
            def mock_method(*args, **kwargs):
                return None
            return mock_method
    
    pd = MockVisualization()
    plt = MockVisualization()
    sns = MockVisualization()
    np = MockVisualization()

# Importações principais do projeto
try:
    from puzzle import Puzzle, PuzzleGenerator, PuzzleValidator, InvalidPuzzleStateError
    from search.bfs import BFS
    from search.dfs import DFS
    from search.ids import IDS
    from search.astar import AStar
    from search.greedy import GreedySearch
    from utils.metrics import MetricsCollector, SearchMetrics
    from utils.tree_printer import TreePrinter
    from utils.analysis import (ComparisonAnalyzer, SearchTreeVisualizer, 
                              AlgorithmResult, ProblemInstance)
except ImportError as e:
    print(f"❌ Erro de importação do módulo principal: {e}")
    print("Certifique-se de que todos os módulos estão no diretório correto.")
    print("Estrutura esperada:")
    print("  n_puzzle_solver/")
    print("  ├── main.py")
    print("  ├── puzzle.py")
    print("  ├── search/")
    print("  │   ├── bfs.py")
    print("  │   ├── dfs.py")
    print("  │   └── ...")
    print("  └── utils/")
    sys.exit(1)


class NPuzzleSolver:
    """Classe principal do solucionador N-Puzzle com interface avançada."""
    
    def __init__(self):
        """Inicializa o solucionador."""
        self.examples = self.load_examples()
        self.metrics_collector = MetricsCollector()
        self.tree_printer = TreePrinter()
        self.comparison_analyzer = ComparisonAnalyzer()
        self.tree_visualizer = SearchTreeVisualizer()
        self.current_puzzle = None
        self.last_solution = None
        self.algorithms = {
            '1': ('BFS', BFS),
            '2': ('DFS', DFS),
            '3': ('IDS', IDS),
            '4': ('A*', AStar),
            '5': ('Greedy', GreedySearch)
        }
        
        # Configura disponibilidade de funcionalidades
        self.visualization_enabled = VISUALIZATION_AVAILABLE
    
    def load_examples(self) -> Dict[str, Any]:
        """Carrega exemplos pré-definidos do arquivo JSON."""
        try:
            examples_path = Path('examples/examples.json')
            if examples_path.exists():
                with open(examples_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.create_default_examples()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            return self.create_default_examples()
    
    def create_default_examples(self) -> Dict[str, Any]:
        """Cria exemplos padrão caso o arquivo não exista."""
        return {
            "8_puzzle": {
                "easy": {
                    "initial_state": [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
                    "description": "Muito fácil - apenas um movimento"
                },
                "medium": {
                    "initial_state": [[1, 2, 3], [4, 0, 6], [7, 5, 8]],
                    "description": "Médio - alguns movimentos necessários"
                },                "hard": {
                    "initial_state": [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
                    "description": "Difícil - muitos movimentos necessários"
                }
            }
        }
    
    def print_main_menu(self):
        """Exibe o menu principal aprimorado."""
        print("\n" + "🧩" + "="*48 + "🧩")
        print("         N-PUZZLE SOLVER v3.0")
        print("=" * 50)
        
        # Status das funcionalidades
        status_icon = "✅" if self.visualization_enabled else "⚠️"
        status_text = "COMPLETO" if self.visualization_enabled else "BÁSICO"
        print(f"{status_icon} Modo: {status_text}")
        
        if not self.visualization_enabled:
            print("� Algumas funcionalidades limitadas (dependências automáticas)")
        
        print("\n�🔍 ALGORITMOS DE BUSCA:")
        print("  1. 🔄 Busca em Largura (BFS)")
        print("  2. ⬇️  Busca em Profundidade (DFS)")
        print("  3. 🔁 Busca com Aprofundamento Iterativo (IDS)")
        print("  4. ⭐ Busca A* (com heurísticas)")
        print("  5. 🎯 Busca Gulosa")
        
        print("\n⚙️ FUNCIONALIDADES:")
        print("  6. 📊 Comparar Algoritmos")
        print("  7. 📂 Carregar Exemplo")
        print("  8. 🎲 Gerar Puzzle Aleatório")
        print("  9. 🎨 Criar Puzzle Personalizado")
        print("  10. 📈 Ver Estatísticas")
        print("  11. 💾 Salvar/Carregar Estado")
        print("  12. 📋 Gerar Relatório")
        
        # Funcionalidades avançadas com indicadores
        viz_icon = "📊" if self.visualization_enabled else "📋"
        print(f"  13. {viz_icon} Análise Avançada")
        print("  14. 🌳 Visualizar Árvore")
        print(f"  15. {viz_icon} Exportar Dados")
        print("  16. ❓ Ajuda")
        
        print("\n  0. 🚪 Sair")
        print("=" * 50)
        
        if self.current_puzzle:
            print(f"📋 Puzzle atual: {self.current_puzzle.size}x{self.current_puzzle.size}")
            print(f"🎯 É objetivo: {'Sim' if self.current_puzzle.is_goal() else 'Não'}")
            print(f"✅ Solucionável: {'Sim' if self.current_puzzle.is_solvable() else 'Não'}")
    
    def get_puzzle_input(self) -> Optional[Puzzle]:
        """Obtém entrada do puzzle do usuário com validação."""
        try:
            print("\n🔧 CONFIGURANDO O PUZZLE:")
            print("Tamanhos suportados: 3 (8-puzzle), 4 (15-puzzle), 5 (24-puzzle)")
            
            while True:
                try:
                    size = int(input("📏 Digite o tamanho do puzzle (3-5): "))
                    if 3 <= size <= 5:
                        break
                    else:
                        print("❌ Tamanho deve estar entre 3 e 5.")
                except ValueError:
                    print("❌ Digite um número válido.")
            
            print(f"\n📝 Digite o estado inicial do {size*size-1}-puzzle:")
            print("💡 Dica: Use 0 para representar o espaço vazio")
            print("📋 Formato: números separados por espaços")
            
            initial_state = []
            for i in range(size):
                while True:
                    try:
                        row_input = input(f"Linha {i+1}: ").strip()
                        row = list(map(int, row_input.split()))
                        
                        if len(row) != size:
                            print(f"❌ Digite exatamente {size} números.")
                            continue
                        
                        initial_state.append(row)
                        break
                    except ValueError:
                        print("❌ Digite apenas números separados por espaços.")
            
            puzzle = Puzzle(initial_state)
            
            print(f"\n✅ Puzzle criado com sucesso!")
            print(f"📊 Estado atual:\n{puzzle.visualize()}")
            
            if not puzzle.is_solvable():
                print("⚠️ ATENÇÃO: Este puzzle não é solucionável!")
                choice = input("Deseja continuar mesmo assim? (s/n): ").lower()
                if choice != 's':
                    return None
            
            return puzzle
            
        except InvalidPuzzleStateError as e:
            print(f"❌ Estado do puzzle inválido: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None

    def run_single_algorithm(self, algorithm_choice: str, puzzle: Puzzle) -> bool:
        """
        Executa um único algoritmo no puzzle.
        
        Args:
            algorithm_choice: Escolha do algoritmo ('1'-'5')
            puzzle: Puzzle para resolver
            
        Returns:
            True se executou com sucesso, False caso contrário
        """
        if algorithm_choice not in self.algorithms:
            print("❌ Algoritmo inválido!")
            return False
        
        algo_name, algo_class = self.algorithms[algorithm_choice]
        
        try:
            print(f"\n🚀 EXECUTANDO {algo_name}")
            print("=" * 30)
              # Configurações especiais para alguns algoritmos
            if algorithm_choice == '4':  # A*
                heuristic = self.choose_heuristic()
                algorithm = algo_class(heuristic)
            elif algorithm_choice == '5':  # Greedy
                heuristic = self.choose_heuristic()
                algorithm = algo_class(heuristic)
            elif algorithm_choice == '2':  # DFS
                depth_limit = self.get_depth_limit()
                algorithm = algo_class(depth_limit)
            elif algorithm_choice == '3':  # IDS
                max_depth = self.get_max_depth()
                algorithm = algo_class(max_depth)
            else:
                algorithm = algo_class()
            
            # Ativa visualização em tempo real automaticamente
            print("\n🎬 VISUALIZAÇÃO EM TEMPO REAL ATIVADA!")
            print("💡 Dica: Pressione Ctrl+C para interromper se necessário")
            
            # Configuração automática de velocidade baseada no algoritmo
            auto_delay = self.get_auto_delay_for_algorithm(algorithm_choice)
            
            # Função wrapper para compatibilidade com os algoritmos
            def visualization_callback(puzzle, nodes_explored=0, depth=0, message=""):
                return self.display_current_state(puzzle, nodes_explored, depth, message)
            
            algorithm.set_real_time_visualization(True, auto_delay, visualization_callback)
            
            # Pequena pausa para mostrar a mensagem
            import time
            time.sleep(2)
            
            # Executa o algoritmo
            self.metrics_collector.start_measurement()
            success, solution = algorithm.search(puzzle)
            metrics = self.metrics_collector.stop_measurement_and_record(algorithm, success, solution)
            
            # Exibe resultados
            self.display_results(success, solution, metrics, puzzle)
            
            # Registra resultado para análise comparativa
            heuristic_name = None
            if algorithm_choice in ['4', '5']:  # A* e Greedy
                heuristic_name = getattr(algorithm, 'heuristic_name', 'manhattan')
            
            self.record_algorithm_result(algo_name, puzzle, success, solution, metrics, heuristic_name)
            
            if success:
                self.last_solution = solution
                
                # Pergunta se quer ver a árvore de busca
                if input("\n🌳 Deseja ver a árvore de busca? (s/n): ").lower() == 's':
                    self.show_search_tree(puzzle, solution)
                
                # Pergunta se quer ver o caminho da solução
                if input("🛤️ Deseja ver o caminho da solução passo a passo? (s/n): ").lower() == 's':
                    self.show_solution_path(puzzle, solution)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
    
    def record_algorithm_result(self, algo_name: str, puzzle: Puzzle, success: bool, 
                               solution: List[str], metrics: SearchMetrics, heuristic_name: Optional[str] = None):
        """
        Registra resultado de algoritmo para análise comparativa.
        
        Args:
            algo_name: Nome do algoritmo
            puzzle: Puzzle resolvido
            success: Se foi bem-sucedido
            solution: Solução encontrada
            metrics: Métricas coletadas
            heuristic_name: Nome da heurística (se aplicável)
        """
        # Cria instância do problema se não existir
        problem_name = f"puzzle_{puzzle.size}x{puzzle.size}"
        
        # Verifica se o problema já foi adicionado
        if not any(p.name == problem_name for p in self.comparison_analyzer.problems):
            problem_instance = ProblemInstance(
                name=problem_name,
                size=puzzle.size,
                initial_state=puzzle.state,
                difficulty="custom",
                description=f"Puzzle {puzzle.size}x{puzzle.size} personalizado"
            )
            self.comparison_analyzer.add_problem(problem_instance)
        
        # Cria resultado do algoritmo
        algorithm_result = AlgorithmResult(
            name=algo_name,
            success=success,
            execution_time=metrics.execution_time,
            nodes_explored=metrics.nodes_explored,
            solution_length=metrics.solution_length,
            max_depth=metrics.max_depth,
            memory_usage=metrics.memory_usage,
            heuristic=heuristic_name,
            optimal=metrics.optimal,
            solution_path=solution if success else None
        )
        
        # Adiciona resultado à análise comparativa
        self.comparison_analyzer.add_result(problem_name, algorithm_result)

    def get_auto_delay_for_algorithm(self, algorithm_choice: str) -> float:
        """Configura automaticamente o delay baseado no algoritmo escolhido."""
        # Velocidades otimizadas para cada algoritmo
        auto_delays = {
            '1': 0.8,   # BFS - moderado para ver a exploração sistemática
            '2': 1.0,   # DFS - um pouco mais lento para ver a profundidade
            '3': 0.6,   # IDS - mais rápido pois explora muito
            '4': 0.5,   # A* - rápido para mostrar eficiência
            '5': 0.4    # Greedy - muito rápido para mostrar velocidade
        }
        
        delay = auto_delays.get(algorithm_choice, 0.5)
          # Informa ao usuário a velocidade escolhida
        speed_names = {
            '1': 'Moderada (BFS explora sistematicamente)',
            '2': 'Lenta (DFS vai fundo)',  
            '3': 'Rápida (IDS explora muito)',
            '4': 'Eficiente (A* é inteligente)',
            '5': 'Muito Rápida (Greedy é veloz)'
        }
        
        algo_name = self.algorithms[algorithm_choice][0]
        speed_desc = speed_names.get(algorithm_choice, 'Padrão')
        print(f"⚡ Velocidade automática para {algo_name}: {speed_desc}")
        
        return delay
    
    def get_visualization_delay(self) -> float:
        """Obtém o delay para visualização em tempo real."""
        print("\n⏱️ CONFIGURAÇÃO DE VELOCIDADE:")
        print("1. 🐌 Muito Lenta (2s por estado)")
        print("2. 🐢 Lenta (1s por estado)")
        print("3. 🚶 Normal (0.5s por estado)")
        print("4. 🏃 Rápida (0.2s por estado)")
        print("5. 🚀 Muito Rápida (0.1s por estado)")
        
        while True:
            choice = input("Escolha a velocidade (1-5): ").strip()
            delays = {'1': 2.0, '2': 1.0, '3': 0.5, '4': 0.2, '5': 0.1}
            if choice in delays:
                return delays[choice]
            else:
                print("❌ Escolha inválida. Digite 1, 2, 3, 4 ou 5.")
    
    def display_current_state(self, puzzle, nodes_explored, depth, message=""):
        """Exibe o estado atual durante a busca em tempo real."""
        
        # Exibe apenas o estado do puzzle de forma simples e limpa
        puzzle_lines = puzzle.visualize(show_info=False).strip().split('\n')
        for line in puzzle_lines:
            print(line)
        print()  # Linha em branco para separar estados

    def choose_heuristic(self) -> str:
        """Permite ao usuário escolher a heurística."""
        print("\n🎯 ESCOLHA DA HEURÍSTICA:")
        print("1. Manhattan Distance (recomendada)")
        print("2. Misplaced Tiles")
        print("3. Linear Conflict")
        
        while True:
            choice = input("Escolha (1-3): ").strip()
            if choice == '1':
                return 'manhattan'
            elif choice == '2':
                return 'misplaced'
            elif choice == '3':
                return 'linear_conflict'
            else:
                print("❌ Escolha inválida. Digite 1, 2 ou 3.")
    
    def get_depth_limit(self) -> int:
        """Obtém limite de profundidade para DFS."""
        while True:
            try:
                limit = int(input("📏 Digite o limite de profundidade para DFS (padrão: 50): ") or "50")
                if limit > 0:
                    return limit
                else:
                    print("❌ Limite deve ser positivo.")
            except ValueError:
                print("❌ Digite um número válido.")
    
    def get_max_depth(self) -> int:
        """Obtém profundidade máxima para IDS."""
        while True:
            try:
                max_depth = int(input("📏 Digite a profundidade máxima para IDS (padrão: 50): ") or "50")
                if max_depth > 0:
                    return max_depth
                else:
                    print("❌ Profundidade deve ser positiva.")
            except ValueError:
                print("❌ Digite um número válido.")
    
    def display_results(self, success: bool, solution: List[str], metrics: SearchMetrics, puzzle: Puzzle):
        """Exibe os resultados da busca de forma organizada."""
        print("\n" + "🎯" + "="*28 + "🎯")
        print("         RESULTADOS")
        print("=" * 30)
        
        if success:
            print("✅ SOLUÇÃO ENCONTRADA!")
            print(f"🎮 Movimentos: {' → '.join(solution) if solution else 'Nenhum'}")
            print(f"📏 Comprimento da solução: {len(solution)}")
        else:
            print("❌ SOLUÇÃO NÃO ENCONTRADA!")
        
        print(f"\n📊 MÉTRICAS DE PERFORMANCE:")
        print(f"⏱️  Tempo de execução: {metrics.execution_time:.4f}s")
        print(f"🔍 Nós explorados: {metrics.nodes_explored:,}")
        print(f"📊 Profundidade máxima: {metrics.max_depth}")
        print(f"💾 Uso de memória: {metrics.memory_usage / 1024:.2f} KB")
        print(f"🎯 Solução ótima: {'Sim' if metrics.optimal else 'Não'}")
        
        if metrics.additional_info:
            print(f"\nℹ️ INFORMAÇÕES ADICIONAIS:")
            for key, value in metrics.additional_info.items():
                if key not in ['algorithm', 'nodes_explored', 'max_depth', 'solution_length', 'optimal']:
                    print(f"   {key}: {value}")
    
    def show_search_tree(self, initial_puzzle: Puzzle, solution: List[str]):
        """Mostra a árvore de busca (versão simplificada)."""
        print("\n🌳 ÁRVORE DE BUSCA (Caminho da Solução):")
        print("=" * 40)
        
        tree_root = self.tree_printer.generate_solution_path_tree(solution, initial_puzzle)
        self.tree_printer.print_tree(tree_root, "Caminho da Solução")
    
    def show_solution_path(self, initial_puzzle: Puzzle, solution: List[str]):
        """Mostra o caminho da solução passo a passo."""
        print("\n🛤️ CAMINHO DA SOLUÇÃO:")
        print("=" * 25)
        
        self.tree_printer.print_solution_path(solution, initial_puzzle)
    
    def compare_algorithms(self, puzzle: Puzzle):
        """Compara todos os algoritmos no mesmo puzzle com análise completa."""
        if not puzzle:
            print("❌ Nenhum puzzle carregado para comparação.")
            return
        
        print("\n📊 COMPARAÇÃO ABRANGENTE DE ALGORITMOS")
        print("=" * 45)
        print(f"🧩 Puzzle: {puzzle.size}x{puzzle.size}")
        print(f"🎯 Solucionável: {'Sim' if puzzle.is_solvable() else 'Não'}")
        print("🔄 Executando todos os algoritmos...")
        
        # Configuração de algoritmos para comparação
        algorithms_config = [
            ('1', 'BFS', BFS, {}),
            ('2', 'DFS', DFS, {'depth_limit': 30}),
            ('3', 'IDS', IDS, {'max_depth': 30}),
            ('4', 'A*-Manhattan', AStar, {'heuristic': 'manhattan'}),
            ('4', 'A*-Misplaced', AStar, {'heuristic': 'misplaced'}),
            ('4', 'A*-Linear', AStar, {'heuristic': 'linear_conflict'}),
            ('5', 'Greedy-Manhattan', GreedySearch, {'heuristic': 'manhattan'}),
            ('5', 'Greedy-Misplaced', GreedySearch, {'heuristic': 'misplaced'})
        ]
        
        results = {}
        
        for choice, name, algo_class, config in algorithms_config:
            try:
                print(f"\n⏳ Testando {name}...")
                
                # Instancia algoritmo com configuração
                if 'heuristic' in config:
                    algorithm = algo_class(config['heuristic'])
                elif 'depth_limit' in config:
                    algorithm = algo_class(config['depth_limit'])
                elif 'max_depth' in config:
                    algorithm = algo_class(config['max_depth'])
                else:
                    algorithm = algo_class()
                
                # Executa algoritmo
                self.metrics_collector.start_measurement()
                success, solution = algorithm.search(puzzle)
                metrics = self.metrics_collector.stop_measurement_and_record(algorithm, success, solution)
                
                # Registra resultado para análise
                heuristic_name = config.get('heuristic', None)
                self.record_algorithm_result(name, puzzle, success, solution, metrics, heuristic_name)
                
                results[name] = {
                    'success': success,
                    'solution_length': len(solution) if success else 0,
                    'time': metrics.execution_time,
                    'nodes': metrics.nodes_explored,
                    'depth': metrics.max_depth,
                    'memory': metrics.memory_usage,
                    'optimal': metrics.optimal,
                    'heuristic': heuristic_name
                }
                
                status = "✅" if success else "❌"
                if success:
                    print(f"{status} {name}: {len(solution)} movimentos, {metrics.execution_time:.4f}s, {metrics.nodes_explored} nós")
                else:
                    print(f"{status} {name}: Falhou após {metrics.execution_time:.4f}s")
                
            except Exception as e:
                print(f"❌ {name}: Erro - {e}")
                results[name] = {'success': False, 'error': str(e)}
        
        # Exibe análise completa
        self.display_comprehensive_comparison(results)
    
    def display_comprehensive_comparison(self, results: Dict[str, Dict]):
        """Exibe análise completa dos resultados de comparação."""
        print("\n🏆 ANÁLISE COMPLETA DOS RESULTADOS")
        print("=" * 40)
        
        successful = {name: data for name, data in results.items() if data.get('success', False)}
        failed = {name: data for name, data in results.items() if not data.get('success', False)}
        
        if not successful:
            print("❌ Nenhum algoritmo encontrou solução.")
            return
        
        # Estatísticas gerais
        print(f"✅ Algoritmos bem-sucedidos: {len(successful)}/{len(results)}")
        print(f"❌ Algoritmos que falharam: {len(failed)}")
        
        # Tabela de resultados
        print("\n📊 TABELA DE RESULTADOS:")
        print("-" * 85)
        print(f"{'Algoritmo':<18} {'Sucesso':<8} {'Movimentos':<10} {'Tempo(s)':<10} {'Nós':<8} {'Ótimo':<8}")
        print("-" * 85)
        
        for name, data in results.items():
            if data.get('success', False):
                optimal_str = "Sim" if data['optimal'] else "Não"
                print(f"{name:<18} {'✅':<8} {data['solution_length']:<10} {data['time']:<10.4f} {data['nodes']:<8} {optimal_str:<8}")
            else:
                print(f"{name:<18} {'❌':<8} {'N/A':<10} {'N/A':<10} {'N/A':<8} {'N/A':<8}")
        
        # Rankings
        print("\n🏆 RANKINGS:")
        
        # Por velocidade
        time_ranking = sorted(successful.items(), key=lambda x: x[1]['time'])
        print("\n⚡ Por Velocidade (Tempo):")
        for i, (name, data) in enumerate(time_ranking[:5], 1):
            print(f"  {i}. {name}: {data['time']:.4f}s")
        
        # Por eficiência
        nodes_ranking = sorted(successful.items(), key=lambda x: x[1]['nodes'])
        print("\n🎯 Por Eficiência (Nós Explorados):")
        for i, (name, data) in enumerate(nodes_ranking[:5], 1):
            print(f"  {i}. {name}: {data['nodes']} nós")
        
        # Por otimalidade
        optimal_solutions = [data['solution_length'] for data in successful.values() if data['optimal']]
        if optimal_solutions:
            optimal_length = min(optimal_solutions)
            optimal_algos = [name for name, data in successful.items() 
                           if data['solution_length'] == optimal_length]
            print(f"\n✨ Solução Ótima ({optimal_length} movimentos):")
            for algo in optimal_algos:
                print(f"  • {algo}")
        
        # Análise por categoria
        print("\n📋 ANÁLISE POR CATEGORIA:")
        
        uninformed = {name: data for name, data in successful.items() if name in ['BFS', 'DFS', 'IDS']}
        informed = {name: data for name, data in successful.items() if 'A*' in name or 'Greedy' in name}
        
        if uninformed:
            avg_time_uninformed = sum(data['time'] for data in uninformed.values()) / len(uninformed)
            avg_nodes_uninformed = sum(data['nodes'] for data in uninformed.values()) / len(uninformed)
            print(f"🔍 Buscas Sem Informação: {avg_time_uninformed:.4f}s médio, {avg_nodes_uninformed:.0f} nós médio")
        
        if informed:
            avg_time_informed = sum(data['time'] for data in informed.values()) / len(informed)
            avg_nodes_informed = sum(data['nodes'] for data in informed.values()) / len(informed)
            print(f"⭐ Buscas Com Informação: {avg_time_informed:.4f}s médio, {avg_nodes_informed:.0f} nós médio")
        
        # Recomendações
        print("\n💡 RECOMENDAÇÕES:")
        if len(successful) > 0:
            fastest = min(successful.items(), key=lambda x: x[1]['time'])
            most_efficient = min(successful.items(), key=lambda x: x[1]['nodes'])
            
            print(f"⚡ Mais rápido: {fastest[0]} ({fastest[1]['time']:.4f}s)")
            print(f"🎯 Mais eficiente: {most_efficient[0]} ({most_efficient[1]['nodes']} nós)")
            
            # Recomendação por tamanho do puzzle (usando puzzle atual)
            if self.current_puzzle:
                if self.current_puzzle.size == 3:
                    print("📋 Para puzzles 3x3: Todos os algoritmos são viáveis")
                elif self.current_puzzle.size == 4:
                    print("📋 Para puzzles 4x4: Prefira algoritmos informados (A*, Greedy)")
                elif self.current_puzzle.size >= 5:
                    print("📋 Para puzzles 5x5+: Use apenas A* com heurística Manhattan")
        
        print("\n" + "="*40)
    
    def display_comparison_results(self, results: Dict[str, Dict]):
        """Exibe resultados da comparação de algoritmos."""
        print("\n🏆 RESULTADOS DA COMPARAÇÃO:")
        print("=" * 35)
        
        successful = {name: data for name, data in results.items() if data.get('success', False)}
        
        if not successful:
            print("❌ Nenhum algoritmo encontrou solução.")
            return
        
        # Ranking por tempo
        print("\n⚡ RANKING POR VELOCIDADE:")
        time_ranking = sorted(successful.items(), key=lambda x: x[1]['time'])
        for i, (name, data) in enumerate(time_ranking, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"{medal} {i}º {name}: {data['time']:.4f}s")
        
        # Ranking por eficiência (menos nós)
        print("\n🧠 RANKING POR EFICIÊNCIA (MENOS NÓS):")
        nodes_ranking = sorted(successful.items(), key=lambda x: x[1]['nodes'])
        for i, (name, data) in enumerate(nodes_ranking, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"{medal} {i}º {name}: {data['nodes']:,} nós")
        
        # Algoritmos ótimos
        optimal_algos = [name for name, data in successful.items() if data.get('optimal', False)]
        if optimal_algos:
            print(f"\n🎯 ALGORITMOS COM SOLUÇÃO ÓTIMA: {', '.join(optimal_algos)}")
    
    def load_example_puzzle(self):
        """Carrega um puzzle de exemplo."""
        if not self.examples:
            print("❌ Nenhum exemplo disponível.")
            return None
        
        print("\n📂 EXEMPLOS DISPONÍVEIS:")
        print("=" * 25)
        
        categories = list(self.examples.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.replace('_', '-').title()}")
        
        try:
            cat_choice = int(input("\nEscolha a categoria: ")) - 1
            if 0 <= cat_choice < len(categories):
                category = categories[cat_choice]
                
                difficulties = list(self.examples[category].keys())
                if 'description' in difficulties:
                    difficulties.remove('description')
                
                print(f"\n📊 DIFICULDADES DISPONÍVEIS ({category}):")
                for i, diff in enumerate(difficulties, 1):
                    desc = self.examples[category][diff].get('description', 'Sem descrição')
                    print(f"{i}. {diff.title()}: {desc}")
                
                diff_choice = int(input("\nEscolha a dificuldade: ")) - 1
                if 0 <= diff_choice < len(difficulties):
                    difficulty = difficulties[diff_choice]
                    state = self.examples[category][difficulty]['initial_state']
                    
                    puzzle = Puzzle(state)
                    print(f"\n✅ Exemplo carregado: {category} - {difficulty}")
                    print(f"📊 Estado:\n{puzzle.visualize()}")
                    
                    return puzzle
        
        except (ValueError, IndexError, KeyError) as e:
            print(f"❌ Erro ao carregar exemplo: {e}")
        
        return None
    
    def generate_random_puzzle(self):
        """Gera um puzzle aleatório."""
        print("\n🎲 GERADOR DE PUZZLE ALEATÓRIO")
        print("=" * 32)
        
        try:
            while True:
                size = int(input("📏 Tamanho do puzzle (3-5): "))
                if 3 <= size <= 5:
                    break
                print("❌ Tamanho deve estar entre 3 e 5.")
            
            print("🔄 Gerando puzzle aleatório...")
            puzzle = Puzzle.create_random(size)
            
            print(f"✅ Puzzle {size}x{size} gerado com sucesso!")
            print(f"📊 Estado:\n{puzzle.visualize()}")
            
            return puzzle
            
        except Exception as e:
            print(f"❌ Erro ao gerar puzzle: {e}")
            return None
    
    def save_state(self, puzzle: Puzzle):
        """Salva o estado atual em arquivo."""
        try:
            filename = input("💾 Nome do arquivo (sem extensão): ").strip()
            if not filename:
                filename = f"puzzle_state_{int(time.time())}"
            
            filepath = f"{filename}.json"
            data = puzzle.to_dict()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Estado salvo em: {filepath}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    
    def load_state(self):
        """Carrega estado de arquivo."""
        try:
            filename = input("📂 Nome do arquivo (com ou sem extensão): ").strip()
            if not filename.endswith('.json'):
                filename += '.json'
            
            if not os.path.exists(filename):
                print(f"❌ Arquivo não encontrado: {filename}")
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            puzzle = Puzzle.from_dict(data)
            print(f"✅ Estado carregado de: {filename}")
            print(f"📊 Estado:\n{puzzle.visualize()}")
            
            return puzzle
            
        except Exception as e:
            print(f"❌ Erro ao carregar: {e}")
            return None
    
    def show_statistics(self):
        """Mostra estatísticas dos algoritmos executados."""
        if not self.metrics_collector.metrics_history:
            print("❌ Nenhuma estatística disponível. Execute alguns algoritmos primeiro.")
            return
        
        print("\n📈 ESTATÍSTICAS GERAIS")
        print("=" * 25)
        
        report = self.metrics_collector.get_comparison_report()
        
        if 'error' in report:
            print(f"❌ {report['error']}")
            return
        
        print(f"📊 Total de execuções: {report['total_runs']}")
        print(f"✅ Execuções bem-sucedidas: {report['successful_runs']}")
        print(f"🔧 Algoritmos testados: {', '.join(report['algorithms_tested'])}")
        
        print(f"\n🏆 PERFORMANCE POR ALGORITMO:")
        for algo, stats in report['performance_summary'].items():
            print(f"\n📋 {algo}:")
            print(f"   Execuções: {stats['runs']}")
            print(f"   Tempo médio: {stats['avg_execution_time']:.4f}s")
            print(f"   Nós médios: {stats['avg_nodes_explored']:.0f}")
            print(f"   Solução média: {stats['avg_solution_length']:.1f} movimentos")
            print(f"   Soluções ótimas: {stats['optimal_solutions']}")
          # Opção de exportar
        if input("\n💾 Deseja exportar estatísticas para CSV? (s/n): ").lower() == 's':
            filename = f"statistics_{int(time.time())}.csv"
            self.metrics_collector.export_to_csv(filename)
    
    def run(self):
        """Executa o loop principal do programa."""        
        while True:
            try:
                self.print_main_menu()
                choice = input("\n🎯 Escolha uma opção: ").strip()
                
                if choice == '0':
                    self.exit_program()
                    break
                elif choice in ['1', '2', '3', '4', '5']:
                    self.handle_algorithm_choice(choice)
                elif choice == '6':
                    self.handle_comparison()
                elif choice == '7':
                    self.handle_load_example()
                elif choice == '8':
                    self.handle_random_puzzle()
                elif choice == '9':
                    self.handle_custom_puzzle()
                elif choice == '10':
                    self.show_statistics()
                elif choice == '11':
                    self.handle_save_load()
                elif choice == '12':
                    self.handle_generate_report()
                elif choice == '13':
                    self.handle_advanced_analysis()
                elif choice == '14':
                    self.handle_tree_visualization()
                elif choice == '15':
                    self.handle_export_data()
                elif choice == '16':
                    self.show_help()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                if choice != '0':
                    input("\n⏎ Pressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Interrompido pelo usuário.")
                self.exit_program()
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("⏎ Pressione Enter para continuar...")
    
    def handle_algorithm_choice(self, choice: str):
        """Lida com a escolha de algoritmo."""
        if not self.current_puzzle:
            print("❌ Nenhum puzzle carregado!")
            print("💡 Carregue um exemplo (opção 7) ou crie um puzzle (opção 9).")
            return
        
        self.run_single_algorithm(choice, self.current_puzzle)
    
    def handle_comparison(self):
        """Lida com a comparação de algoritmos."""
        if not self.current_puzzle:
            print("❌ Nenhum puzzle carregado para comparação!")
            print("💡 Carregue um exemplo (opção 7) ou crie um puzzle (opção 9).")
            return
        
        print("⚠️ A comparação pode demorar para puzzles complexos.")
        if input("Continuar? (s/n): ").lower() == 's':
            self.compare_algorithms(self.current_puzzle)
    
    def handle_load_example(self):
        """Lida com o carregamento de exemplo."""
        puzzle = self.load_example_puzzle()
        if puzzle:
            self.current_puzzle = puzzle
    
    def handle_random_puzzle(self):
        """Lida com a geração de puzzle aleatório."""
        puzzle = self.generate_random_puzzle()
        if puzzle:
            self.current_puzzle = puzzle
    
    def handle_custom_puzzle(self):
        """Lida com a criação de puzzle personalizado."""
        puzzle = self.get_puzzle_input()
        if puzzle:
            self.current_puzzle = puzzle
    
    def handle_save_load(self):
        """Lida com salvar/carregar estado."""
        print("\n💾 SALVAR/CARREGAR ESTADO:")
        print("1. 💾 Salvar estado atual")
        print("2. 📂 Carregar estado")
        
        choice = input("Escolha (1-2): ").strip()
        
        if choice == '1':
            if self.current_puzzle:
                self.save_state(self.current_puzzle)
            else:
                print("❌ Nenhum puzzle carregado para salvar.")
        elif choice == '2':
            puzzle = self.load_state()
            if puzzle:
                self.current_puzzle = puzzle
        else:
            print("❌ Opção inválida.")
    
    def handle_advanced_analysis(self):
        """Gerencia análise comparativa avançada."""
        if not self.comparison_analyzer.results:
            print("❌ Nenhum resultado de comparação disponível!")
            print("💡 Execute comparações de algoritmos primeiro (opção 6).")
            return
        
        print("\n🔍 ANÁLISE COMPARATIVA AVANÇADA")
        print("=" * 40)
        print("1. 📊 Tabela Comparativa Detalhada")
        print("2. 📈 Resumo de Performance")
        print("3. 🏆 Rankings de Algoritmos")  
        print("4. 💡 Conclusões e Recomendações")
        print("5. 📋 Relatório Completo")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == '1':
            print(self.comparison_analyzer.generate_comparison_table())
        elif choice == '2':
            print(self.comparison_analyzer.generate_performance_summary())
        elif choice == '3':
            print(self.comparison_analyzer.generate_algorithm_ranking())
        elif choice == '4':
            print(self.comparison_analyzer._generate_conclusions())
        elif choice == '5':
            print(self.comparison_analyzer.generate_detailed_report())
        else:
            print("❌ Opção inválida!")
    
    def handle_generate_report(self):
        """Gera relatório completo de análise."""
        if not self.comparison_analyzer.results:
            print("❌ Nenhum resultado para relatório!")
            print("💡 Execute alguns algoritmos primeiro.")
            return
        
        print("\n📋 GERAÇÃO DE RELATÓRIO")
        print("=" * 30)
        
        # Exibe relatório na tela
        report = self.comparison_analyzer.generate_detailed_report()
        print(report)
        
        # Pergunta se quer salvar
        save_choice = input("\n💾 Deseja salvar o relatório em arquivo? (s/n): ").lower()
        if save_choice == 's':
            result = self.comparison_analyzer.save_report()
            print(result)
    
    def handle_tree_visualization(self):
        """Gerencia visualização de árvores de busca."""
        if not self.last_solution:
            print("❌ Nenhuma solução disponível para visualizar!")
            print("💡 Execute um algoritmo primeiro.")
            return
        
        if not self.current_puzzle:
            print("❌ Puzzle atual não disponível!")
            return
        
        print("\n🌳 VISUALIZAÇÃO DA ÁRVORE DE BUSCA")
        print("=" * 40)
        
        # Gera visualização da árvore
        tree_repr = self.tree_visualizer.generate_tree_representation(
            self.current_puzzle, self.last_solution
        )
        print(tree_repr)
        
        # Análise do caminho
        print("\n" + "="*50)
        path_analysis = self.tree_visualizer.generate_path_analysis(
            self.current_puzzle, self.last_solution
        )
        print(path_analysis)
    
    def export_basic_json(self):
        """Exporta dados básicos em JSON quando pandas não está disponível."""
        try:
            timestamp = int(time.time())
            filename = f"n_puzzle_results_{timestamp}.json"
            
            # Coleta dados básicos
            basic_data = {
                "timestamp": datetime.now().isoformat(),
                "total_results": len(getattr(self.comparison_analyzer, 'results', {})),
                "algorithms_tested": list(getattr(self.comparison_analyzer, 'results', {}).keys()),
                "export_type": "basic_json_export",
                "note": "Para exportação completa, todas as dependências foram instaladas automaticamente"
            }
            
            # Adiciona dados se disponíveis
            if hasattr(self.comparison_analyzer, 'results'):
                basic_data["results"] = self.comparison_analyzer.results
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(basic_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Dados básicos exportados para: {filename}")
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
    
    def handle_export_data(self):
        """Gerencia exportação de dados com tratamento automático de dependências."""
        if not hasattr(self, 'comparison_analyzer') or not self.comparison_analyzer.results:
            print("❌ Nenhum dado para exportar!")
            print("💡 Execute comparações de algoritmos primeiro.")
            return
        
        print("\n📊 EXPORTAÇÃO DE DADOS")
        print("=" * 30)
        
        if not self.visualization_enabled:
            print("⚠️ Modo de exportação limitado")
            print("📄 Exportação disponível: JSON básico")
            
            choice = input("Deseja exportar dados básicos em JSON? (s/n): ").lower()
            if choice == 's':
                self.export_basic_json()
            return
        
        # Menu completo para quando as bibliotecas estão disponíveis
        print("1. 📄 Exportar dados em JSON")
        print("2. 📊 Gerar gráficos de performance")
        print("3. 📦 Exportar tudo (dados + gráficos)")
        
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == '1':
            result = self.comparison_analyzer.export_data_json()
            print(result)
        elif choice == '2':
            result = self.comparison_analyzer.create_performance_plots()
            print(result)
        elif choice == '3':
            json_result = self.comparison_analyzer.export_data_json()
            plots_result = self.comparison_analyzer.create_performance_plots()
            print(json_result)
            print(plots_result)
        else:
            print("❌ Opção inválida!")
    
    def show_help(self):
        """Mostra ajuda com informações sobre dependências."""
        print("\n❓ AJUDA - N-PUZZLE SOLVER")
        print("=" * 30)
        
        print("🧩 SOBRE O SISTEMA:")
        print("  • Resolve puzzles deslizantes (8, 15, 24 peças)")
        print("  • 5 algoritmos de busca implementados")
        print("  • Análise comparativa de performance")
        print("  • Instalação automática de dependências")
        
        print("\n🔧 FUNCIONALIDADES:")
        print("  ✅ Sempre disponíveis:")
        print("     • Resolução de puzzles")
        print("     • Comparação básica de algoritmos")
        print("     • Visualização textual de árvores")
        print("     • Exportação básica em JSON")
        
        if self.visualization_enabled:
            print("  ✅ Funcionalidades avançadas ativas:")
            print("     • Gráficos de performance")
            print("     • Análise estatística detalhada")
            print("     • Exportação completa de dados")
            print("     • Visualizações interativas")
        else:
            print("  ⚠️ Funcionalidades limitadas:")
            print("     • Gráficos não disponíveis")
            print("     • Análise estatística básica")
            print("     • Exportação limitada")
            
            print("\n📦 INSTALAÇÃO AUTOMÁTICA:")
            print("   O sistema tentou instalar automaticamente:")
            print("   pandas, matplotlib, seaborn, numpy")
            print("   Se ainda há problemas, tente manualmente:")
            print("   pip install pandas matplotlib seaborn numpy")
        
        print("\n🎯 ALGORITMOS:")
        print("  • BFS: Ótimo, usa mais memória")
        print("  • DFS: Rápido, pode ser subótimo")
        print("  • IDS: Combina BFS e DFS")
        print("  • A*: Muito eficiente com heurísticas")
        print("  • Greedy: Rápido, segue heurística")
        
        print("\n💡 DICAS:")
        print("  1. Comece com exemplos simples")
        print("  2. Use A* para puzzles grandes")
        print("  3. Compare algoritmos para aprender")
        print("  4. Verifique se o puzzle é solucionável")
    
    def exit_program(self):
        """Encerra o programa com mensagem de despedida."""
        print("\n🎉 OBRIGADO POR USAR O N-PUZZLE SOLVER!")
        print("=" * 40)
        
        if hasattr(self, 'metrics_collector') and self.metrics_collector.metrics_history:
            total_runs = len(self.metrics_collector.metrics_history)
            print(f"📊 Total de execuções: {total_runs}")
            
            successful_runs = sum(1 for m in self.metrics_collector.metrics_history if m.success)
            print(f"✅ Execuções bem-sucedidas: {successful_runs}")
            
            if successful_runs > 0:
                avg_time = sum(m.execution_time for m in self.metrics_collector.metrics_history if m.success) / successful_runs
                print(f"⏱️ Tempo médio: {avg_time:.4f}s")
        
        print("\n💡 Dicas para próxima vez:")
        print("  • Experimente diferentes algoritmos")
        print("  • Compare performance entre eles")
        print("  • Tente puzzles de diferentes tamanhos")
        
        if not self.visualization_enabled:
            print("  • Dependências foram instaladas automaticamente")
        
        print("\n👋 Até a próxima!")

if __name__ == "__main__":
    try:
        solver = NPuzzleSolver()
        solver.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
