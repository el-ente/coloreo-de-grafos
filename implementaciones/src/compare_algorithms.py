"""
Comparison of Graph Coloring Algorithms.

This script compares the performance and results of three different
graph coloring algorithms:
1. Brute Force (exact, slow)
2. Greedy First-Fit (fast, suboptimal)
3. Welsh-Powell (fast, better heuristic)

Educational Purpose:
- Demonstrate trade-offs between optimality and speed
- Show how algorithm choice affects both result quality and runtime
- Visualize performance differences across different graph types
"""

import time
from graph import Node, Graph
from brute_force_coloring import BruteForceColoring
from greedy_coloring import GreedyColoring
from welsh_powell_coloring import WelshPowellColoring
from utils import create_bipartite_graph, create_cycle_graph, create_complete_graph, create_star_graph


def compare_algorithms(graph, graph_name, chromatic_number=None):
    """
    Compare all three algorithms on the same graph.
    
    Args:
        graph: Graph object to color
        graph_name: Descriptive name for the graph
        chromatic_number: Known chromatic number (optional)
    """
    print("\n" + "=" * 70)
    print(f"GRAPH: {graph_name}")
    print("=" * 70)
    print(f"Nodes: {len(graph.get_nodes())}, Edges: {len(graph.get_edges())}")
    if chromatic_number:
        print(f"Chromatic Number (optimal): {chromatic_number}")
    print()

    results = {}

    # 1. Brute Force (skip for large graphs)
    num_nodes = len(graph.get_nodes())
    if num_nodes <= 12:  # Only run brute force for small graphs
        print("🔍 Brute Force (exact algorithm):")
        bf = BruteForceColoring(graph)
        bf.color_graph()
        results['brute_force'] = {
            'colors': bf.get_chromaticity(),
            'time': bf.get_execution_time(),
            'valid': bf.is_valid_coloring(bf.coloring)
        }
        print(f"   Colors used: {results['brute_force']['colors']}")
        print(f"   Execution time: {results['brute_force']['time']:.6f} seconds")
        print(f"   Valid: {results['brute_force']['valid']}")
    else:
        print("🔍 Brute Force: SKIPPED (graph too large)")
        results['brute_force'] = None

    # 2. Greedy (natural order)
    print("\n🟢 Greedy First-Fit (natural order):")
    greedy = GreedyColoring(graph, order_strategy='natural')
    greedy.color_graph()
    results['greedy'] = {
        'colors': greedy.get_chromaticity(),
        'time': greedy.get_execution_time(),
        'valid': greedy.is_valid_coloring(greedy.coloring)
    }
    print(f"   Colors used: {results['greedy']['colors']}")
    print(f"   Execution time: {results['greedy']['time']:.6f} seconds")
    print(f"   Valid: {results['greedy']['valid']}")

    # 3. Welsh-Powell
    print("\n🎯 Welsh-Powell (degree-ordered heuristic):")
    wp = WelshPowellColoring(graph)
    wp.color_graph()
    results['welsh_powell'] = {
        'colors': wp.get_chromaticity(),
        'time': wp.get_execution_time(),
        'valid': wp.is_valid_coloring(wp.coloring)
    }
    print(f"   Colors used: {results['welsh_powell']['colors']}")
    print(f"   Execution time: {results['welsh_powell']['time']:.6f} seconds")
    print(f"   Valid: {results['welsh_powell']['valid']}")

    # Analysis
    print("\n" + "-" * 70)
    print("ANALYSIS:")
    print("-" * 70)

    if results['brute_force']:
        bf_colors = results['brute_force']['colors']
        print(f"✓ Brute Force found optimal solution: {bf_colors} colors")

        if results['greedy']['colors'] == bf_colors:
            print(f"✓ Greedy is OPTIMAL")
        else:
            overhead = results['greedy']['colors'] - bf_colors
            print(f"⚠ Greedy uses {overhead} extra color(s) ({results['greedy']['colors']} vs {bf_colors})")

        if results['welsh_powell']['colors'] == bf_colors:
            print(f"✓ Welsh-Powell is OPTIMAL")
        else:
            overhead = results['welsh_powell']['colors'] - bf_colors
            print(f"⚠ Welsh-Powell uses {overhead} extra color(s) ({results['welsh_powell']['colors']} vs {bf_colors})")

    if chromatic_number:
        if results['welsh_powell']['colors'] == chromatic_number:
            print(f"✓ Welsh-Powell achieved chromatic number: {chromatic_number}")
        if results['greedy']['colors'] == chromatic_number:
            print(f"✓ Greedy achieved chromatic number: {chromatic_number}")

    # Speed comparison
    print("\nSpeed Comparison:")
    if results['brute_force']:
        bf_time = results['brute_force']['time']
        greedy_speedup = bf_time / results['greedy']['time'] if results['greedy']['time'] > 0 else float('inf')
        wp_speedup = bf_time / results['welsh_powell']['time'] if results['welsh_powell']['time'] > 0 else float('inf')

        print(f"  Greedy is {greedy_speedup:.1f}x faster than Brute Force")
        print(f"  Welsh-Powell is {wp_speedup:.1f}x faster than Brute Force")

    if results['greedy']['time'] > 0 and results['welsh_powell']['time'] > 0:
        ratio = results['greedy']['time'] / results['welsh_powell']['time']
        if ratio > 1:
            print(f"  Greedy is {ratio:.1f}x faster than Welsh-Powell")
        else:
            print(f"  Welsh-Powell is {1/ratio:.1f}x faster than Greedy")

    return results


if __name__ == "__main__":
    print("=" * 70)
    print("GRAPH COLORING ALGORITHMS - PERFORMANCE COMPARISON")
    print("=" * 70)
    print("\nThis script compares three algorithms:")
    print("  1. Brute Force: Guarantees optimal, but VERY slow (O(k^n))")
    print("  2. Greedy First-Fit: Fast but may be suboptimal (O(n²))")
    print("  3. Welsh-Powell: Fast heuristic with better results (O(n² + m))")
    print("\nNote: Brute Force is only tested on small graphs (≤10 nodes)")
    
    # Test 1: Small cycle (odd)
    graph1, _ = create_cycle_graph(5)
    compare_algorithms(graph1, "Cycle C5 (odd cycle)", chromatic_number=3)
    
    # Test 2: Small cycle (even)
    graph2, _ = create_cycle_graph(6)
    compare_algorithms(graph2, "Cycle C6 (even cycle)", chromatic_number=2)
    
    # Test 3: Complete graph (clique)
    graph3, _ = create_complete_graph(5)
    compare_algorithms(graph3, "Complete Graph K5 (clique)", chromatic_number=5)
    
    # Test 4: Star graph
    graph4, _ = create_star_graph(7)
    compare_algorithms(graph4, "Star Graph (1 center + 6 leaves)", chromatic_number=2)
    
    # Test 5: Bipartite graph
    graph5, _ = create_bipartite_graph(4, 4)
    compare_algorithms(graph5, "Complete Bipartite K(4,4)", chromatic_number=2)
    
    # Test 6: Larger cycle (Brute Force will be skipped)
    graph6, _ = create_cycle_graph(15)
    compare_algorithms(graph6, "Cycle C15 (large odd cycle)", chromatic_number=3)
    
    # Test 7: Larger complete graph
    graph7, _ = create_complete_graph(12)
    compare_algorithms(graph7, "Complete Graph K12 (large clique)", chromatic_number=12)
    