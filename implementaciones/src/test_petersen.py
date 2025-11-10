"""
Script para probar los tres algoritmos de coloreo con el grafo de Petersen.

El grafo de Petersen es un grafo clásico con 10 nodos y 15 aristas,
conocido por tener número cromático 3.
"""

from greedy_coloring import GreedyColoring
from welsh_powell_coloring import WelshPowellColoring
from brute_force_coloring import BruteForceColoring
from utils import create_petersen_graph, time_measured


def print_coloring(coloring, algorithm_name):
    """Imprime el coloreo de forma ordenada."""
    print(f"\n{algorithm_name}:")
    print(f"  Número de colores usados: {len(set(coloring.values()))}")
    print(f"  Coloreo:")
    for node, color in sorted(coloring.items(), key=lambda x: str(x[0].id)):
        print(f"    {node.id}: color {color}")


def main():
    # Crear el grafo de Petersen
    print("="*60)
    print("GRAFO DE PETERSEN - Prueba de Algoritmos de Coloreo")
    print("="*60)
    
    graph, nodes = create_petersen_graph()
    
    print(f"\nCaracterísticas del grafo:")
    print(f"  Nodos: {len(nodes)}")
    print(f"  Aristas: {len(graph.get_edges())}")
    print(f"  Número cromático conocido: 3")
    
    # Lista de algoritmos a probar
    algorithms = [
        (GreedyColoring, "Greedy Coloring"),
        (WelshPowellColoring, "Welsh-Powell Coloring"),
        (BruteForceColoring, "Brute Force Coloring")
    ]
    
    print("\n" + "="*60)
    print("RESULTADOS")
    print("="*60)
    
    # Ejecutar cada algoritmo
    for algo_class, algo_name in algorithms:
        algorithm = algo_class(graph)
        
        @time_measured
        def run():
            return algorithm.color_graph()
        
        coloring, time_ns = run()
        
        print(f"\n{algo_name}:")
        print(f"  Tiempo de ejecución: {time_ns:,} ns ({time_ns / 1_000_000:.4f} ms)")
        print(f"  Número de colores usados: {len(set(coloring.values()))}")
        print(f"  Coloreo:")
        for node, color in sorted(coloring.items(), key=lambda x: str(x[0].id)):
            print(f"    {node.id}: color {color}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
