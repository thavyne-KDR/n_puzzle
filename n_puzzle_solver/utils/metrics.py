"""
Métricas de Performance

Este módulo fornece funcionalidades para coletar e analisar métricas
de performance dos algoritmos de busca.
"""

import time
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class SearchMetrics:
    """
    Classe para armazenar métricas de uma execução de busca.
    
    Attributes:
        algorithm: Nome do algoritmo utilizado
        execution_time: Tempo de execução em segundos
        nodes_explored: Número de nós explorados
        solution_length: Número de movimentos na solução
        max_depth: Profundidade máxima atingida
        memory_usage: Uso de memória (estimativo)
        success: Se a busca foi bem-sucedida
        optimal: Se a solução é ótima
        additional_info: Informações adicionais específicas do algoritmo
    """
    algorithm: str
    execution_time: float
    nodes_explored: int
    solution_length: int
    max_depth: int
    memory_usage: int
    success: bool
    optimal: bool
    additional_info: Dict[str, Any] = None


class MetricsCollector:
    """
    Coletor de métricas para análise de performance dos algoritmos.
    
    Attributes:
        metrics_history: Lista de métricas coletadas
        start_time: Timestamp do início da execução atual
    """
    
    def __init__(self):
        """Inicializa o coletor de métricas."""
        self.metrics_history: List[SearchMetrics] = []
        self.start_time = None
    
    def start_measurement(self):
        """Inicia a medição de tempo."""
        self.start_time = time.time()
    
    def stop_measurement_and_record(self, algorithm_instance, success: bool, 
                                   solution: List[str]) -> SearchMetrics:
        """
        Para a medição e registra as métricas.
        
        Args:
            algorithm_instance: Instância do algoritmo executado
            success: Se a busca foi bem-sucedida
            solution: Solução encontrada
        
        Returns:
            Objeto SearchMetrics com as métricas coletadas
        """
        if self.start_time is None:
            raise ValueError("Medição não foi iniciada")
        
        execution_time = time.time() - self.start_time
        
        # Obtém métricas específicas do algoritmo
        algo_metrics = algorithm_instance.get_metrics()
        
        # Estima uso de memória (simplificado)
        memory_usage = self._estimate_memory_usage(algorithm_instance)
        
        metrics = SearchMetrics(
            algorithm=algo_metrics.get('algorithm', 'Unknown'),
            execution_time=execution_time,
            nodes_explored=algo_metrics.get('nodes_explored', 0),
            solution_length=len(solution) if success else 0,
            max_depth=algo_metrics.get('max_depth', 0),
            memory_usage=memory_usage,
            success=success,
            optimal=algo_metrics.get('optimal', False),
            additional_info=algo_metrics
        )
        
        self.metrics_history.append(metrics)
        self.start_time = None
        
        return metrics
    
    def _estimate_memory_usage(self, algorithm_instance) -> int:
        """
        Estima o uso de memória do algoritmo.
        
        Args:
            algorithm_instance: Instância do algoritmo
        
        Returns:
            Estimativa de uso de memória em bytes
        """
        # Estimativa simplificada baseada no número de nós explorados
        nodes = algorithm_instance.nodes_explored
        
        # Estimativa: cada nó ocupa aproximadamente 100 bytes
        # (estado do puzzle + metadados)
        estimated_bytes = nodes * 100
        
        return estimated_bytes
    
    def get_comparison_report(self) -> Dict[str, Any]:
        """
        Gera relatório comparativo das métricas coletadas.
        
        Returns:
            Dicionário com análise comparativa
        """
        if not self.metrics_history:
            return {"error": "Nenhuma métrica coletada"}
        
        successful_runs = [m for m in self.metrics_history if m.success]
        
        if not successful_runs:
            return {"error": "Nenhuma execução bem-sucedida"}
        
        report = {
            "total_runs": len(self.metrics_history),
            "successful_runs": len(successful_runs),
            "algorithms_tested": list(set(m.algorithm for m in self.metrics_history)),
            "performance_summary": {}
        }
        
        # Análise por algoritmo
        algorithms = {}
        for metrics in successful_runs:
            algo = metrics.algorithm
            if algo not in algorithms:
                algorithms[algo] = []
            algorithms[algo].append(metrics)
        
        for algo, runs in algorithms.items():
            avg_time = sum(r.execution_time for r in runs) / len(runs)
            avg_nodes = sum(r.nodes_explored for r in runs) / len(runs)
            avg_solution = sum(r.solution_length for r in runs) / len(runs)
            avg_memory = sum(r.memory_usage for r in runs) / len(runs)
            
            report["performance_summary"][algo] = {
                "runs": len(runs),
                "avg_execution_time": round(avg_time, 4),
                "avg_nodes_explored": round(avg_nodes, 2),
                "avg_solution_length": round(avg_solution, 2),
                "avg_memory_usage": round(avg_memory, 2),
                "optimal_solutions": sum(1 for r in runs if r.optimal)
            }
        
        return report
    
    def export_to_csv(self, filename: str):
        """
        Exporta métricas para arquivo CSV.
        
        Args:
            filename: Nome do arquivo CSV de saída
        """
        import csv
        
        if not self.metrics_history:
            print("Nenhuma métrica para exportar")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'algorithm', 'execution_time', 'nodes_explored', 
                'solution_length', 'max_depth', 'memory_usage', 
                'success', 'optimal'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for metrics in self.metrics_history:
                writer.writerow({
                    'algorithm': metrics.algorithm,
                    'execution_time': metrics.execution_time,
                    'nodes_explored': metrics.nodes_explored,
                    'solution_length': metrics.solution_length,
                    'max_depth': metrics.max_depth,
                    'memory_usage': metrics.memory_usage,
                    'success': metrics.success,
                    'optimal': metrics.optimal
                })
        
        print(f"Métricas exportadas para {filename}")
    
    def clear_history(self):
        """Limpa o histórico de métricas."""
        self.metrics_history.clear()
    
    def print_metrics(self, metrics: SearchMetrics):
        """
        Imprime métricas formatadas.
        
        Args:
            metrics: Métricas a serem impressas
        """
        print("\n" + "="*50)
        print(f"MÉTRICAS - {metrics.algorithm}")
        print("="*50)
        print(f"Sucesso: {'Sim' if metrics.success else 'Não'}")
        
        if metrics.success:
            print(f"Tempo de execução: {metrics.execution_time:.4f}s")
            print(f"Nós explorados: {metrics.nodes_explored}")
            print(f"Comprimento da solução: {metrics.solution_length}")
            print(f"Profundidade máxima: {metrics.max_depth}")
            print(f"Uso de memória: {metrics.memory_usage / 1024:.2f} KB")
            print(f"Solução ótima: {'Sim' if metrics.optimal else 'Não'}")
            
            if metrics.additional_info:
                print("\nInformações adicionais:")
                for key, value in metrics.additional_info.items():
                    if key not in ['algorithm', 'nodes_explored', 'max_depth', 'solution_length', 'optimal']:
                        print(f"  {key}: {value}")
        
        print("="*50)
