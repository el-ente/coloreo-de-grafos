"""
Script para medir el tiempo de ejecución de algoritmos de coloreo de grafos.

Mide el rendimiento de tres algoritmos (Greedy, Welsh-Powell, Brute Force)
sobre diferentes tipos de grafos con tamaños de n=1 hasta n=10.
"""

import csv
from datetime import datetime
from greedy_coloring import GreedyColoring
from welsh_powell_coloring import WelshPowellColoring
from brute_force_coloring import BruteForceColoring
from utils import (
    time_measured,
    create_cycle_graph,
    create_complete_graph,
    create_star_graph,
    create_bipartite_graph,
    create_path_graph,
    create_wheel_graph,
    create_petersen_graph,
    create_grid_graph,
    create_planar_graph,
    create_tree_graph,
    create_hypercube_graph,
    create_prism_graph,
    create_kneser_graph,
    create_ladder_graph,
    create_friendship_graph,
    create_crown_graph
)


def measure_algorithm(algorithm_class, graph, algorithm_name):
    """
    Mide el tiempo de ejecución de un algoritmo en un grafo dado.
    
    Args:
        algorithm_class: Clase del algoritmo (GreedyColoring, etc.)
        graph: Grafo a colorear
        algorithm_name: Nombre del algoritmo para mensajes
        
    Returns:
        Tuple (tiempo_ns, num_colores) o (None, None) si falla
    """
    try:
        algorithm = algorithm_class(graph)
        
        @time_measured
        def run():
            return algorithm.color_graph()
        
        coloring, time_ns = run()
        num_colors = len(set(coloring.values())) if coloring else 0
        return time_ns, num_colors
    except Exception as e:
        return None, None


def measure_graph_type(graph_creator, graph_name, n_values, algorithms):
    """
    Mide todos los algoritmos para un tipo de grafo específico.
    
    Args:
        graph_creator: Función que crea el grafo
        graph_name: Nombre descriptivo del tipo de grafo
        n_values: Lista de valores de n a probar
        algorithms: Lista de tuplas (clase, nombre)
        
    Returns:
        Diccionario con los resultados
    """
    results = {
        'graph_type': graph_name,
        'measurements': []
    }
    
    for n in n_values:
        try:
            graph, nodes = graph_creator(n)
            measurement = {
                'n': n,
                'num_nodes': len(nodes),
                'num_edges': len(graph.get_edges()),
                'algorithms': {}
            }
            
            for algo_class, algo_name in algorithms:
                time_ns, num_colors = measure_algorithm(algo_class, graph, algo_name)
                measurement['algorithms'][algo_name] = {
                    'time_ns': time_ns,
                    'time_ms': time_ns / 1_000_000 if time_ns else None,
                    'num_colors': num_colors
                }
            
            results['measurements'].append(measurement)
        except Exception as e:
            print(f"Error con {graph_name} n={n}: {e}")
    
    return results


def format_time(time_ns):
    """Formatea el tiempo en nanosegundos a una unidad legible."""
    if time_ns is None:
        return "N/A"
    
    if time_ns < 1_000:
        return f"{time_ns:.0f} ns"
    elif time_ns < 1_000_000:
        return f"{time_ns / 1_000:.2f} μs"
    elif time_ns < 1_000_000_000:
        return f"{time_ns / 1_000_000:.2f} ms"
    else:
        return f"{time_ns / 1_000_000_000:.2f} s"


def print_results(results):
    """Imprime los resultados en formato tabla."""
    print(f"\n{'='*80}")
    print(f"TIPO DE GRAFO: {results['graph_type']}")
    print(f"{'='*80}")
    
    print(f"\n{'n':<4} {'Nodos':<7} {'Aristas':<8} {'Algoritmo':<20} {'Tiempo':<15} {'Colores':<8}")
    print(f"{'-'*80}")
    
    for m in results['measurements']:
        n = m['n']
        num_nodes = m['num_nodes']
        num_edges = m['num_edges']
        
        first_row = True
        for algo_name, data in m['algorithms'].items():
            if first_row:
                print(f"{n:<4} {num_nodes:<7} {num_edges:<8} ", end="")
                first_row = False
            else:
                print(f"{'':<4} {'':<7} {'':<8} ", end="")
            
            time_str = format_time(data['time_ns'])
            colors_str = str(data['num_colors']) if data['num_colors'] is not None else "N/A"
            print(f"{algo_name:<20} {time_str:<15} {colors_str:<8}")


def save_results_to_csv(all_results, filename=None):
    """
    Guarda los resultados en un archivo CSV.
    
    Args:
        all_results: Lista de diccionarios con los resultados
        filename: Nombre del archivo CSV (opcional, se genera automáticamente si no se proporciona)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"measurements_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'graph_type', 'n', 'num_nodes', 'num_edges',
            'algorithm', 'time_ns', 'num_colors'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for results in all_results:
            graph_type = results['graph_type']
            for m in results['measurements']:
                n = m['n']
                num_nodes = m['num_nodes']
                num_edges = m['num_edges']
                
                for algo_name, data in m['algorithms'].items():
                    writer.writerow({
                        'graph_type': graph_type,
                        'n': n,
                        'num_nodes': num_nodes,
                        'num_edges': num_edges,
                        'algorithm': algo_name,
                        'time_ns': data['time_ns'] if data['time_ns'] is not None else '',
                        'num_colors': data['num_colors'] if data['num_colors'] is not None else ''
                    })
    
    return filename


def main():
    """Función principal que ejecuta todas las mediciones."""
    
    # Definir algoritmos a probar
    algorithms = [
        (GreedyColoring, "Greedy"),
        (WelshPowellColoring, "Welsh-Powell"),
        (BruteForceColoring, "Brute Force")
    ]
    
    # Definir tipos de grafos a probar
    graph_types = [
        (create_cycle_graph, "Grafo Cíclico", range(3, 11)),  # n >= 3 para ciclos
        (create_complete_graph, "Grafo Completo", range(1, 11)),
        (create_star_graph, "Grafo Estrella", range(2, 11)),  # n >= 2 para estrella
        (create_path_graph, "Grafo Camino", range(1, 11)),
        (create_tree_graph, "Árbol Binario (altura)", range(1, 5)),  # Menos valores por crecimiento exponencial
        (lambda n: create_bipartite_graph(n, n), "Grafo Bipartito K(n,n)", range(1, 11)),
        (create_wheel_graph, "Grafo Rueda", range(3, 11)),  # n >= 3
        (lambda n: create_grid_graph(n, n), "Grafo Cuadrícula n×n", range(2, 6)),  # Menos valores
        (create_ladder_graph, "Grafo Escalera", range(2, 11)),
        (create_prism_graph, "Grafo Prisma", range(3, 11)),  # n >= 3
    ]
    
    print("\n" + "="*80)
    print("MEDICIONES DE ALGORITMOS DE COLOREO DE GRAFOS")
    print("="*80)
    print("\nAlgoritmos evaluados:")
    for _, name in algorithms:
        print(f"  - {name}")
    print(f"\nRango de valores de n: varía según el tipo de grafo")
    
    # Ejecutar mediciones para cada tipo de grafo
    all_results = []
    for graph_creator, graph_name, n_values in graph_types:
        results = measure_graph_type(graph_creator, graph_name, n_values, algorithms)
        all_results.append(results)
        print_results(results)
    
    # Guardar resultados en CSV
    csv_filename = save_results_to_csv(all_results)
    
    print(f"\n{'='*80}")
    print("MEDICIONES COMPLETADAS")
    print(f"{'='*80}")
    print(f"\nResultados guardados en: {csv_filename}\n")


if __name__ == "__main__":
    main()
