"""
Módulo de Análise Comparativa e Relatórios
Implementa todas as funcionalidades de análise solicitadas na especificação
"""

import time
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os
import sys

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False


@dataclass
class AlgorithmResult:
    """Resultado detalhado de execução de um algoritmo."""
    name: str
    success: bool
    execution_time: float
    nodes_explored: int
    solution_length: int
    max_depth: int
    memory_usage: int
    heuristic: Optional[str] = None
    optimal: bool = True
    solution_path: List[str] = None
    search_tree_info: Dict[str, Any] = None


@dataclass
class ProblemInstance:
    """Instância de problema para análise."""
    name: str
    size: int
    initial_state: List[List[int]]
    difficulty: str
    description: str


class ComparisonAnalyzer:
    """Analisador comparativo de algoritmos de busca."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.results: Dict[str, List[AlgorithmResult]] = {}
        self.problems: List[ProblemInstance] = []
        
    def add_result(self, problem_name: str, result: AlgorithmResult):
        """Adiciona resultado de execução."""
        if problem_name not in self.results:
            self.results[problem_name] = []
        self.results[problem_name].append(result)
    
    def add_problem(self, problem: ProblemInstance):
        """Adiciona instância de problema."""
        self.problems.append(problem)
    
    def generate_comparison_table(self) -> str:
        """Gera tabela comparativa dos resultados."""
        if not self.results:
            return "❌ Nenhum resultado para comparar."
        
        table = "📊 TABELA COMPARATIVA DE ALGORITMOS\n"
        table += "=" * 80 + "\n"
        
        # Cabeçalho
        table += f"{'Problema':<15} {'Algoritmo':<12} {'Sucesso':<8} {'Tempo(s)':<10} "
        table += f"{'Nós':<8} {'Passos':<8} {'Prof.':<8} {'Mem.(KB)':<10}\n"
        table += "-" * 80 + "\n"
        
        for problem_name, results in self.results.items():
            for i, result in enumerate(results):
                prob_name = problem_name if i == 0 else ""
                success_str = "✅" if result.success else "❌"
                
                table += f"{prob_name:<15} {result.name:<12} {success_str:<8} "
                table += f"{result.execution_time:<10.3f} {result.nodes_explored:<8} "
                table += f"{result.solution_length:<8} {result.max_depth:<8} "
                table += f"{result.memory_usage:<10}\n"
            
            if len(results) > 1:
                table += "-" * 80 + "\n"
        
        return table
    
    def generate_performance_summary(self) -> str:
        """Gera resumo de performance dos algoritmos."""
        if not self.results:
            return "❌ Nenhum resultado para analisar."
        
        summary = "\n📈 RESUMO DE PERFORMANCE\n"
        summary += "=" * 50 + "\n"
        
        # Coleta estatísticas por algoritmo
        algo_stats = {}
        for results in self.results.values():
            for result in results:
                if result.name not in algo_stats:
                    algo_stats[result.name] = {
                        'executions': 0,
                        'successes': 0,
                        'total_time': 0,
                        'total_nodes': 0,
                        'total_steps': 0,
                        'times': [],
                        'nodes': [],
                        'steps': []
                    }
                
                stats = algo_stats[result.name]
                stats['executions'] += 1
                if result.success:
                    stats['successes'] += 1
                    stats['total_time'] += result.execution_time
                    stats['total_nodes'] += result.nodes_explored
                    stats['total_steps'] += result.solution_length
                    stats['times'].append(result.execution_time)
                    stats['nodes'].append(result.nodes_explored)
                    stats['steps'].append(result.solution_length)
        
        # Gera estatísticas
        for algo_name, stats in algo_stats.items():
            summary += f"\n🔍 {algo_name}:\n"
            summary += f"  Execuções: {stats['executions']}\n"
            summary += f"  Taxa de Sucesso: {stats['successes']}/{stats['executions']}"
            summary += f" ({100*stats['successes']/stats['executions']:.1f}%)\n"
            
            if stats['successes'] > 0:
                avg_time = stats['total_time'] / stats['successes']
                avg_nodes = stats['total_nodes'] / stats['successes'] 
                avg_steps = stats['total_steps'] / stats['successes']
                
                summary += f"  Tempo Médio: {avg_time:.3f}s\n"
                summary += f"  Nós Médios: {avg_nodes:.1f}\n"
                summary += f"  Passos Médios: {avg_steps:.1f}\n"
                
                if len(stats['times']) > 1:
                    min_time = min(stats['times'])
                    max_time = max(stats['times'])
                    summary += f"  Tempo Min/Max: {min_time:.3f}s / {max_time:.3f}s\n"
        
        return summary
    
    def generate_algorithm_ranking(self) -> str:
        """Gera ranking dos algoritmos por diferentes critérios."""
        if not self.results:
            return "❌ Nenhum resultado para ranking."
        
        ranking = "\n🏆 RANKING DE ALGORITMOS\n"
        ranking += "=" * 40 + "\n"
        
        # Coleta dados para ranking
        algo_performance = {}
        for results in self.results.values():
            for result in results:
                if result.success:
                    if result.name not in algo_performance:
                        algo_performance[result.name] = {
                            'times': [],
                            'nodes': [],
                            'optimal_count': 0,
                            'total_count': 0
                        }
                    
                    perf = algo_performance[result.name]
                    perf['times'].append(result.execution_time)
                    perf['nodes'].append(result.nodes_explored)
                    if result.optimal:
                        perf['optimal_count'] += 1
                    perf['total_count'] += 1
        
        # Ranking por velocidade (tempo médio)
        if algo_performance:
            ranking += "\n⚡ Por Velocidade (Tempo Médio):\n"
            speed_ranking = sorted(algo_performance.items(), 
                                 key=lambda x: sum(x[1]['times'])/len(x[1]['times']))
            for i, (name, perf) in enumerate(speed_ranking, 1):
                avg_time = sum(perf['times']) / len(perf['times'])
                ranking += f"  {i}. {name}: {avg_time:.3f}s\n"
            
            # Ranking por eficiência (nós explorados)
            ranking += "\n🎯 Por Eficiência (Nós Médios):\n"
            efficiency_ranking = sorted(algo_performance.items(),
                                      key=lambda x: sum(x[1]['nodes'])/len(x[1]['nodes']))
            for i, (name, perf) in enumerate(efficiency_ranking, 1):
                avg_nodes = sum(perf['nodes']) / len(perf['nodes'])
                ranking += f"  {i}. {name}: {avg_nodes:.1f} nós\n"
            
            # Ranking por otimalidade
            ranking += "\n✨ Por Otimalidade:\n"
            optimal_ranking = sorted(algo_performance.items(),
                                   key=lambda x: x[1]['optimal_count']/x[1]['total_count'],
                                   reverse=True)
            for i, (name, perf) in enumerate(optimal_ranking, 1):
                optimal_rate = perf['optimal_count'] / perf['total_count']
                ranking += f"  {i}. {name}: {optimal_rate:.1%} soluções ótimas\n"
        
        return ranking
    
    def generate_detailed_report(self) -> str:
        """Gera relatório completo de análise."""
        report = "📋 RELATÓRIO COMPLETO DE ANÁLISE N-PUZZLE\n"
        report += "=" * 60 + "\n"
        report += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        report += f"Problemas Analisados: {len(self.problems)}\n"
        report += f"Execuções Realizadas: {sum(len(results) for results in self.results.values())}\n"
        report += "\n"
        
        # Seção 1: Formulação do Problema
        report += "🔍 1. FORMULAÇÃO DO PROBLEMA\n"
        report += "-" * 30 + "\n"
        report += "• Representação dos estados: Matriz NxN com números 1 a N²-1 e 0 (espaço vazio)\n"
        report += "• Estado inicial: Configuração fornecida pelo usuário\n"
        report += "• Estado objetivo: Números ordenados sequencialmente com 0 no final\n"
        report += "• Operadores: Mover espaço vazio para cima, baixo, esquerda, direita\n"
        report += "• Condição objetivo: Estado atual == estado objetivo\n"
        report += "• Custo de ação: Uniforme = 1 para todos os movimentos\n\n"
        
        # Seção 2: Problemas Testados
        report += "🧩 2. INSTÂNCIAS DE PROBLEMAS TESTADAS\n"
        report += "-" * 35 + "\n"
        for problem in self.problems:
            report += f"• {problem.name}: {problem.size}x{problem.size} - {problem.difficulty}\n"
            report += f"  Descrição: {problem.description}\n"
        report += "\n"
        
        # Seção 3: Tabela Comparativa
        report += "📊 3. RESULTADOS COMPARATIVOS\n"
        report += "-" * 30 + "\n"
        report += self.generate_comparison_table()
        report += "\n"
        
        # Seção 4: Análise de Performance
        report += "📈 4. ANÁLISE DE PERFORMANCE\n"
        report += "-" * 28 + "\n"
        report += self.generate_performance_summary()
        report += "\n"
        
        # Seção 5: Rankings
        report += "🏆 5. RANKINGS COMPARATIVOS\n"
        report += "-" * 27 + "\n"
        report += self.generate_algorithm_ranking()
        report += "\n"
        
        # Seção 6: Conclusões
        report += "💡 6. CONCLUSÕES E RECOMENDAÇÕES\n"
        report += "-" * 33 + "\n"
        report += self._generate_conclusions()
        
        return report
    
    def _generate_conclusions(self) -> str:
        """Gera conclusões baseadas nos resultados."""
        if not self.results:
            return "❌ Dados insuficientes para conclusões."
        
        conclusions = ""
        
        # Análise de algoritmos sem informação
        uninformed_algos = ['BFS', 'DFS', 'IDS']
        informed_algos = ['A*', 'Greedy']
        
        has_uninformed = any(any(r.name in uninformed_algos for r in results) 
                           for results in self.results.values())
        has_informed = any(any(r.name in informed_algos for r in results)
                         for results in self.results.values())
        
        if has_uninformed:
            conclusions += "🔍 BUSCAS SEM INFORMAÇÃO:\n"
            conclusions += "• BFS: Garante solução ótima, mas uso intensivo de memória\n"
            conclusions += "• DFS: Menor uso de memória, mas não garante otimalidade\n"
            conclusions += "• IDS: Combina vantagens de BFS e DFS\n\n"
        
        if has_informed:
            conclusions += "⭐ BUSCAS COM INFORMAÇÃO:\n"
            conclusions += "• A*: Melhor para soluções ótimas com heurísticas admissíveis\n"
            conclusions += "• Greedy: Mais rápida, mas não garante otimalidade\n"
            conclusions += "• Heurística Manhattan geralmente superior a Misplaced Tiles\n\n"
        
        conclusions += "📋 RECOMENDAÇÕES DE USO:\n"
        conclusions += "• Para puzzles 8: Todos os algoritmos funcionam bem\n"
        conclusions += "• Para puzzles 15: Prefira algoritmos informados (A*, Greedy)\n"
        conclusions += "• Para puzzles 24: Use apenas A* com heurísticas eficientes\n"
        conclusions += "• Para análise educacional: Compare BFS vs DFS vs A*\n"
        
        return conclusions
    
    def save_report(self, filename: str = None) -> str:
        """Salva relatório em arquivo."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_npuzzle_{timestamp}.txt"
        
        try:
            report = self.generate_detailed_report()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            return f"✅ Relatório salvo em: {filename}"
        except Exception as e:
            return f"❌ Erro ao salvar relatório: {e}"
    
    def export_data_json(self, filename: str = None) -> str:
        """Exporta dados em formato JSON."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dados_npuzzle_{timestamp}.json"
        
        try:
            data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_problems': len(self.problems),
                    'total_executions': sum(len(results) for results in self.results.values())
                },
                'problems': [asdict(p) for p in self.problems],
                'results': {
                    problem: [asdict(result) for result in results]
                    for problem, results in self.results.items()
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return f"✅ Dados exportados em: {filename}"
        except Exception as e:
            return f"❌ Erro ao exportar dados: {e}"
    
    def create_performance_plots(self, output_dir: str = "graficos") -> str:
        """Cria gráficos de performance (requer matplotlib)."""
        if not HAS_PLOTTING:
            return ("❌ Bibliotecas de gráficos não instaladas.\n"
                   "Execute: pip install matplotlib pandas seaborn")
        
        if not self.results:
            return "❌ Nenhum resultado para plotar."
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Prepara dados
            data = []
            for problem_name, results in self.results.items():
                for result in results:
                    if result.success:
                        data.append({
                            'Problema': problem_name,
                            'Algoritmo': result.name,
                            'Tempo (s)': result.execution_time,
                            'Nós Explorados': result.nodes_explored,
                            'Passos Solução': result.solution_length,
                            'Heurística': result.heuristic or 'N/A'
                        })
            
            if not data:
                return "❌ Nenhum resultado bem-sucedido para plotar."
            
            df = pd.DataFrame(data)
            
            # Configuração de estilo
            plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
            
            # Gráfico 1: Tempo de Execução
            plt.figure(figsize=(12, 8))
            if len(df['Problema'].unique()) > 1:
                sns.barplot(data=df, x='Algoritmo', y='Tempo (s)', hue='Problema')
                plt.title('Comparação de Tempo de Execução por Algoritmo e Problema')
            else:
                sns.barplot(data=df, x='Algoritmo', y='Tempo (s)')
                plt.title('Comparação de Tempo de Execução por Algoritmo')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/tempo_execucao.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Gráfico 2: Nós Explorados
            plt.figure(figsize=(12, 8))
            if len(df['Problema'].unique()) > 1:
                sns.barplot(data=df, x='Algoritmo', y='Nós Explorados', hue='Problema')
                plt.title('Comparação de Nós Explorados por Algoritmo e Problema')
            else:
                sns.barplot(data=df, x='Algoritmo', y='Nós Explorados')
                plt.title('Comparação de Nós Explorados por Algoritmo')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/nos_explorados.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Gráfico 3: Eficiência (Tempo vs Nós)
            plt.figure(figsize=(10, 8))
            for algo in df['Algoritmo'].unique():
                algo_data = df[df['Algoritmo'] == algo]
                plt.scatter(algo_data['Nós Explorados'], algo_data['Tempo (s)'], 
                           label=algo, alpha=0.7, s=60)
            
            plt.xlabel('Nós Explorados')
            plt.ylabel('Tempo de Execução (s)')
            plt.title('Eficiência dos Algoritmos (Tempo vs Nós Explorados)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/eficiencia.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Gráfico 4: Distribuição de Performance
            if len(df) > 10:  # Só faz sentido com muitos dados
                fig, axes = plt.subplots(1, 2, figsize=(15, 6))
                
                # Distribuição de tempos
                sns.boxplot(data=df, x='Algoritmo', y='Tempo (s)', ax=axes[0])
                axes[0].set_title('Distribuição dos Tempos de Execução')
                axes[0].tick_params(axis='x', rotation=45)
                
                # Distribuição de nós
                sns.boxplot(data=df, x='Algoritmo', y='Nós Explorados', ax=axes[1])
                axes[1].set_title('Distribuição dos Nós Explorados')
                axes[1].tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                plt.savefig(f"{output_dir}/distribuicao.png", dpi=300, bbox_inches='tight')
                plt.close()
            
            return f"✅ Gráficos salvos no diretório: {output_dir}/"
            
        except Exception as e:
            return f"❌ Erro ao criar gráficos: {e}"


class SearchTreeVisualizer:
    """Visualizador de árvores de busca."""
    
    def __init__(self):
        """Inicializa o visualizador."""
        self.tree_data = {}
    
    def generate_tree_representation(self, puzzle, solution_path: List[str]) -> str:
        """Gera representação textual da árvore de busca."""
        tree_str = "🌳 ÁRVORE DE BUSCA (Caminho da Solução)\n"
        tree_str += "=" * 50 + "\n"
        
        if not solution_path:
            tree_str += "📍 Estado Inicial (já é objetivo)\n"
            tree_str += puzzle.visualize()
            return tree_str
        
        tree_str += "📍 Estado Inicial:\n"
        tree_str += puzzle.visualize() + "\n"
        
        current_puzzle = puzzle.copy()
        for i, move in enumerate(solution_path):
            tree_str += f"    |\n    📁 Movimento {i+1}: {move}\n    |\n    v\n"
            
            # Aplica movimento
            if move == "UP":
                current_puzzle.move_up()
            elif move == "DOWN":
                current_puzzle.move_down()
            elif move == "LEFT":
                current_puzzle.move_left()
            elif move == "RIGHT":
                current_puzzle.move_right()
            
            # Mostra estado resultante
            tree_str += current_puzzle.visualize()
            
            if i < len(solution_path) - 1:
                tree_str += "\n"
        
        tree_str += "\n🎯 Estado Objetivo Alcançado!\n"
        
        return tree_str
    
    def generate_path_analysis(self, puzzle, solution_path: List[str]) -> str:
        """Gera análise detalhada do caminho da solução."""
        if not solution_path:
            return "🎯 Solução encontrada no estado inicial (0 movimentos)."
        
        analysis = "📊 ANÁLISE DO CAMINHO DA SOLUÇÃO\n"
        analysis += "=" * 40 + "\n"
        analysis += f"📏 Comprimento do caminho: {len(solution_path)} movimentos\n"
        analysis += f"🎯 Sequência de movimentos: {' → '.join(solution_path)}\n\n"
        
        # Análise de padrões de movimento
        move_counts = {}
        for move in solution_path:
            move_counts[move] = move_counts.get(move, 0) + 1
        
        analysis += "📈 Distribuição de movimentos:\n"
        for move, count in sorted(move_counts.items()):
            percentage = (count / len(solution_path)) * 100
            analysis += f"  {move}: {count} vezes ({percentage:.1f}%)\n"
        
        # Verifica eficiência
        total_moves = len(solution_path)
        if total_moves <= 10:
            efficiency = "Muito Eficiente"
        elif total_moves <= 20:
            efficiency = "Eficiente"
        elif total_moves <= 30:
            efficiency = "Moderado"
        else:
            efficiency = "Pode ser otimizado"
        
        analysis += f"\n💡 Avaliação de eficiência: {efficiency}\n"
        
        return analysis


# Funções utilitárias para integração com o sistema principal
def create_comparison_analyzer() -> ComparisonAnalyzer:
    """Cria e retorna uma instância do analisador comparativo."""
    return ComparisonAnalyzer()


def create_tree_visualizer() -> SearchTreeVisualizer:
    """Cria e retorna uma instância do visualizador de árvores."""
    return SearchTreeVisualizer()
