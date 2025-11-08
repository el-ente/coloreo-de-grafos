"""
Unit tests for the Brute Force Graph Coloring Algorithm.

This module contains tests to verify the correctness of the
BruteForceColoring implementation.
"""

from graph import Node, Graph
from implementaciones.src.brute_force_coloring import BruteForceColoring


def test_single_node():
    """Test coloring a graph with a single node."""
    print("\n" + "="*60)
    print("TEST 1: Single Node")
    print("="*60)
    
    graph = Graph()
    node_a = Node("A")
    graph.add_node(node_a)
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    
    assert len(result) == 1, "Should have colored 1 node"
    assert result[node_a] == 0, "Single node should get color 0"
    assert coloring_algo.get_chromaticity() == 1, "Single node requires 1 color"
    
    print(f"✓ Single node colored with 1 color: {result}")
    print(f"✓ Chromatic number: {coloring_algo.get_chromaticity()}")


def test_disconnected_nodes():
    """Test coloring disconnected nodes (independent set)."""
    print("\n" + "="*60)
    print("TEST 2: Disconnected Nodes")
    print("="*60)
    
    graph = Graph()
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    # No edges added - all disconnected
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    
    chromatic = coloring_algo.get_chromaticity()
    assert chromatic == 1, "Disconnected nodes require only 1 color"
    assert coloring_algo.is_valid_coloring(result), "Coloring should be valid"
    
    print(f"✓ Three disconnected nodes colored with {chromatic} color")
    print(f"✓ Result: {[(n.id, result[n]) for n in [node_a, node_b, node_c]]}")


def test_bipartite_graph():
    """Test coloring a bipartite graph (K_{2,2})."""
    print("\n" + "="*60)
    print("TEST 3: Bipartite Graph (K_{2,2})")
    print("="*60)
    
    graph = Graph()
    # Create nodes for bipartite graph:
    # Set 1: A, B
    # Set 2: C, D
    # All nodes in Set 1 connected to all in Set 2
    
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)
    
    # Edges: A-C, A-D, B-C, B-D (complete bipartite)
    graph.add_edge(node_a, node_c)
    graph.add_edge(node_a, node_d)
    graph.add_edge(node_b, node_c)
    graph.add_edge(node_b, node_d)
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    chromatic = coloring_algo.get_chromaticity()
    
    assert chromatic == 2, "Bipartite graph requires exactly 2 colors"
    assert coloring_algo.is_valid_coloring(result), "Coloring should be valid"
    
    print(f"✓ Bipartite graph colored with {chromatic} colors")
    print(f"✓ Coloring: {[(n.id, result[n]) for n in sorted([node_a, node_b, node_c, node_d], key=lambda x: x.id)]}")


def test_triangle():
    """Test coloring a triangle (K_3 - complete graph)."""
    print("\n" + "="*60)
    print("TEST 4: Triangle (K_3)")
    print("="*60)
    
    graph = Graph()
    node_x = Node("X")
    node_y = Node("Y")
    node_z = Node("Z")
    
    graph.add_node(node_x)
    graph.add_node(node_y)
    graph.add_node(node_z)
    
    # Complete graph: all nodes connected to each other
    graph.add_edge(node_x, node_y)
    graph.add_edge(node_y, node_z)
    graph.add_edge(node_z, node_x)
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    chromatic = coloring_algo.get_chromaticity()
    
    assert chromatic == 3, "Triangle requires exactly 3 colors"
    assert coloring_algo.is_valid_coloring(result), "Coloring should be valid"
    
    # All three nodes should have different colors
    colors = set(result.values())
    assert len(colors) == 3, "All three nodes should have different colors"
    
    print(f"✓ Triangle colored with {chromatic} colors")
    print(f"✓ Coloring: {[(n.id, result[n]) for n in sorted([node_x, node_y, node_z], key=lambda x: x.id)]}")


def test_complete_graph_k4():
    """Test coloring a complete graph with 4 nodes (K_4)."""
    print("\n" + "="*60)
    print("TEST 5: Complete Graph (K_4)")
    print("="*60)
    
    graph = Graph()
    nodes = [Node(f"V{i}") for i in range(4)]
    
    for node in nodes:
        graph.add_node(node)
    
    # Connect all pairs (complete graph)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            graph.add_edge(nodes[i], nodes[j])
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    chromatic = coloring_algo.get_chromaticity()
    
    assert chromatic == 4, "K_4 requires exactly 4 colors"
    assert coloring_algo.is_valid_coloring(result), "Coloring should be valid"
    
    print(f"✓ Complete graph K_4 colored with {chromatic} colors")
    print(f"✓ Each node has a different color: {[result[n] for n in nodes]}")


def test_cycle_graph_c5():
    """Test coloring a cycle graph with 5 nodes (C_5)."""
    print("\n" + "="*60)
    print("TEST 6: Cycle Graph (C_5)")
    print("="*60)
    
    graph = Graph()
    nodes = [Node(f"N{i}") for i in range(5)]
    
    for node in nodes:
        graph.add_node(node)
    
    # Create a cycle: N0-N1-N2-N3-N4-N0
    for i in range(5):
        graph.add_edge(nodes[i], nodes[(i + 1) % 5])
    
    coloring_algo = BruteForceColoring(graph)
    result = coloring_algo.color_graph()
    chromatic = coloring_algo.get_chromaticity()
    
    assert chromatic == 3, "Odd cycle requires exactly 3 colors"
    assert coloring_algo.is_valid_coloring(result), "Coloring should be valid"
    
    print(f"✓ Cycle C_5 colored with {chromatic} colors")
    print(f"✓ Coloring: {[result[n] for n in nodes]}")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("BRUTE FORCE GRAPH COLORING - UNIT TESTS")
    print("="*60)
    
    try:
        test_single_node()
        test_disconnected_nodes()
        test_bipartite_graph()
        test_triangle()
        test_complete_graph_k4()
        test_cycle_graph_c5()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
