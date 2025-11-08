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
from implementaciones.src.brute_force_coloring import BruteForceColoring
from greedy_coloring import GreedyColoring
from welsh_powell_coloring import welsh_powell_coloring


def create_cycle_graph(n):
    """Create a cycle graph with n nodes."""
    graph = Graph()
    nodes = [Node(f"v{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    for i in range(n):
        graph.add_edge(nodes[i], nodes[(i + 1) % n])
    
    return graph, nodes


def create_complete_graph(n):
    """Create a complete graph (clique) with n nodes."""
    graph = Graph()
    nodes = [Node(f"k{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(nodes[i], nodes[j])
    
    return graph, nodes


def create_star_graph(n):
    """Create a star graph with 1 center and n-1 leaves."""
    graph = Graph()
    center = Node("center")
    graph.add_node(center)
    
    leaves = [Node(f"leaf{i}") for i in range(n - 1)]
    for leaf in leaves:
        graph.add_node(leaf)
        graph.add_edge(center, leaf)
    
    return graph, [center] + leaves


def create_bipartite_graph(n1, n2):
    """Create a complete bipartite graph K(n1, n2)."""
    graph = Graph()
    
    set_a = [Node(f"a{i}") for i in range(n1)]
    set_b = [Node(f"b{i}") for i in range(n2)]
    
    for node in set_a + set_b:
        graph.add_node(node)
    
    for a in set_a:
        for b in set_b:
            graph.add_edge(a, b)
    
    return graph, set_a + set_b


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
    if num_nodes <= 12:  # Only run brute force for small graphs (⚠️ puede ser lento para >10)
        print("🔍 Brute Force (exact algorithm):")
        bf = BruteForceColoring(graph)
        bf_coloring = bf.color_graph()
        bf_colors = bf.get_chromaticity()
        bf_time = bf.get_execution_time()
        results['brute_force'] = {
            'colors': bf_colors,
            'time': bf_time,
            'valid': bf.is_valid_coloring(bf_coloring)
        }
        print(f"   Colors used: {bf_colors}")
        print(f"   Execution time: {bf_time:.6f} seconds")
        print(f"   Valid: {results['brute_force']['valid']}")
    else:
        print("🔍 Brute Force: SKIPPED (graph too large)")
        results['brute_force'] = None
    
    # 2. Greedy (natural order)
    print("\n🟢 Greedy First-Fit (natural order):")
    greedy = GreedyColoring(graph, order_strategy='natural')
    greedy_coloring = greedy.color_graph()
    greedy_colors = greedy.get_num_colors()
    greedy_time = greedy.get_execution_time()
    results['greedy'] = {
        'colors': greedy_colors,
        'time': greedy_time,
        'valid': greedy.is_valid_coloring()
    }
    print(f"   Colors used: {greedy_colors}")
    print(f"   Execution time: {greedy_time:.6f} seconds")
    print(f"   Valid: {results['greedy']['valid']}")
    
    # 3. Welsh-Powell
    print("\n🎯 Welsh-Powell (degree-ordered heuristic):")
    wp_coloring, wp_time = welsh_powell_coloring(graph)
    wp_colors = len(set(wp_coloring.values()))
    
    # Validate Welsh-Powell
    wp_valid = True
    for node in graph.get_nodes():
        if node not in wp_coloring:
            wp_valid = False
            break
    if wp_valid:
        for edge in graph.get_edges():
            if wp_coloring[edge[0]] == wp_coloring[edge[1]]:
                wp_valid = False
                break
    
    results['welsh_powell'] = {
        'colors': wp_colors,
        'time': wp_time,
        'valid': wp_valid
    }
    print(f"   Colors used: {wp_colors}")
    print(f"   Execution time: {wp_time:.6f} seconds")
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
    
    # Final summary
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. BRUTE FORCE: 
   - Always finds the optimal solution (minimum colors)
   - Becomes impractical for graphs with >10 nodes
   - Execution time grows exponentially

2. GREEDY FIRST-FIT:
   - Very fast, works on large graphs
   - Quality depends heavily on node ordering
   - May use more colors than necessary

3. WELSH-POWELL:
   - Fast like Greedy (O(n² + m))
   - Better results by processing high-degree nodes first
   - Often matches or beats Greedy
   - Good balance of speed and quality

RECOMMENDATION:
- Use Brute Force only for: small graphs, research, verification
- Use Greedy for: very large graphs, when speed is critical
- Use Welsh-Powell for: most practical applications
    """)
