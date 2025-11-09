"""
Unit tests for the Brute Force Graph Coloring Algorithm.

This module contains tests to verify the correctness of the
BruteForceColoring implementation using unittest framework.
"""

import unittest
from graph import Node, Graph
from brute_force_coloring import BruteForceColoring


class TestBruteForceColoring(unittest.TestCase):
    """Test suite for BruteForceColoring class."""
    
    def test_single_node(self):
        """Test coloring a graph with a single node."""
        graph = Graph()
        node_a = Node("A")
        graph.add_node(node_a)
        
        coloring_algo = BruteForceColoring(graph)
        result = coloring_algo.color_graph()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[node_a], 0)
        self.assertEqual(coloring_algo.get_chromaticity(), 1)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_disconnected_nodes(self):
        """Test coloring disconnected nodes (independent set)."""
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
        self.assertEqual(chromatic, 1)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_bipartite_graph(self):
        """Test coloring a bipartite graph (K_{2,2})."""
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
        
        self.assertEqual(chromatic, 2)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_triangle(self):
        """Test coloring a triangle (K_3 - complete graph)."""
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
        
        self.assertEqual(chromatic, 3)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
        
        # All three nodes should have different colors
        colors = set(result.values())
        self.assertEqual(len(colors), 3)
    
    def test_complete_graph_k4(self):
        """Test coloring a complete graph with 4 nodes (K_4)."""
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
        
        self.assertEqual(chromatic, 4)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_cycle_graph_c5(self):
        """Test coloring a cycle graph with 5 nodes (C_5)."""
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
        
        self.assertEqual(chromatic, 3)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_invalid_coloring_detection(self):
        """Test that is_valid_coloring correctly identifies invalid colorings."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        node_c = Node("C")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_node(node_c)
        
        # Create a path: A-B-C
        graph.add_edge(node_a, node_b)
        graph.add_edge(node_b, node_c)
        
        coloring_algo = BruteForceColoring(graph)
        
        # Valid coloring: alternating colors
        valid_coloring = {node_a: 0, node_b: 1, node_c: 0}
        self.assertTrue(coloring_algo.is_valid_coloring(valid_coloring))
        
        # Invalid coloring: adjacent nodes with same color
        invalid_coloring = {node_a: 0, node_b: 0, node_c: 1}
        self.assertFalse(coloring_algo.is_valid_coloring(invalid_coloring))
        
        # Another invalid: B and C have same color
        invalid_coloring2 = {node_a: 0, node_b: 1, node_c: 1}
        self.assertFalse(coloring_algo.is_valid_coloring(invalid_coloring2))
    
    def test_chromatic_number_correctness(self):
        """Verify chromatic number matches theoretical values for known graphs.
        
        Tests various graph families where the chromatic number is known:
        - Complete graphs K_n: χ(G) = n
        - Even cycles C_2k: χ(G) = 2
        - Odd cycles C_2k+1: χ(G) = 3
        - Bipartite graphs: χ(G) = 2
        """
        # Test 1: K_3 (triangle) - chromatic number = 3
        k3 = Graph()
        k3_nodes = [Node(f"k3_{i}") for i in range(3)]
        for node in k3_nodes:
            k3.add_node(node)
        for i in range(3):
            for j in range(i + 1, 3):
                k3.add_edge(k3_nodes[i], k3_nodes[j])
        
        k3_algo = BruteForceColoring(k3)
        k3_algo.color_graph()
        self.assertEqual(k3_algo.get_chromaticity(), 3)
        
        # Test 2: C_4 (even cycle) - chromatic number = 2
        c4 = Graph()
        c4_nodes = [Node(f"c4_{i}") for i in range(4)]
        for node in c4_nodes:
            c4.add_node(node)
        for i in range(4):
            c4.add_edge(c4_nodes[i], c4_nodes[(i + 1) % 4])
        
        c4_algo = BruteForceColoring(c4)
        c4_algo.color_graph()
        self.assertEqual(c4_algo.get_chromaticity(), 2)
        
        # Test 3: C_7 (odd cycle) - chromatic number = 3
        c7 = Graph()
        c7_nodes = [Node(f"c7_{i}") for i in range(7)]
        for node in c7_nodes:
            c7.add_node(node)
        for i in range(7):
            c7.add_edge(c7_nodes[i], c7_nodes[(i + 1) % 7])
        
        c7_algo = BruteForceColoring(c7)
        c7_algo.color_graph()
        self.assertEqual(c7_algo.get_chromaticity(), 3)
        
        # Test 4: Star graph (bipartite) - chromatic number = 2
        star = Graph()
        center = Node("center")
        star.add_node(center)
        leaves = [Node(f"leaf{i}") for i in range(4)]
        for leaf in leaves:
            star.add_node(leaf)
            star.add_edge(center, leaf)
        
        star_algo = BruteForceColoring(star)
        star_algo.color_graph()
        self.assertEqual(star_algo.get_chromaticity(), 2)
    
    def test_performance_limits(self):
        """Test behavior with graphs that approach computational limits.
        
        Brute force has exponential complexity O(n^n), so it becomes
        impractical for n > 10. This test verifies it works for small graphs
        and establishes performance baseline.
        """
        import time
        
        # Test with K_5 - should complete quickly
        k5 = Graph()
        k5_nodes = [Node(f"v{i}") for i in range(5)]
        for node in k5_nodes:
            k5.add_node(node)
        for i in range(5):
            for j in range(i + 1, 5):
                k5.add_edge(k5_nodes[i], k5_nodes[j])
        
        start = time.time()
        k5_algo = BruteForceColoring(k5)
        k5_algo.color_graph()
        elapsed = time.time() - start
        
        # Should complete in under 1 second for 5 nodes
        self.assertLess(elapsed, 1.0)
        self.assertEqual(k5_algo.get_chromaticity(), 5)
        
        # Test with slightly larger graph (6 nodes) - still manageable
        path6 = Graph()
        path_nodes = [Node(f"p{i}") for i in range(6)]
        for node in path_nodes:
            path6.add_node(node)
        for i in range(5):
            path6.add_edge(path_nodes[i], path_nodes[i + 1])
        
        start = time.time()
        path_algo = BruteForceColoring(path6)
        path_algo.color_graph()
        elapsed = time.time() - start
        
        # Should still complete reasonably fast
        self.assertLess(elapsed, 2.0)
        # Path graph needs only 2 colors
        self.assertEqual(path_algo.get_chromaticity(), 2)
    
    def test_empty_graph_handling(self):
        """Test behavior with empty graph.
        
        An empty graph (no nodes) should return an empty coloring
        with chromatic number 0.
        """
        graph = Graph()
        
        coloring_algo = BruteForceColoring(graph)
        result = coloring_algo.color_graph()
        
        # Empty graph should return empty coloring
        self.assertEqual(len(result), 0)
        self.assertEqual(coloring_algo.get_chromaticity(), 0)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
    
    def test_disconnected_components(self):
        """Test graph with multiple disconnected components."""
        graph = Graph()
        
        # Component 1: Triangle
        t1 = Node("t1")
        t2 = Node("t2")
        t3 = Node("t3")
        graph.add_node(t1)
        graph.add_node(t2)
        graph.add_node(t3)
        graph.add_edge(t1, t2)
        graph.add_edge(t2, t3)
        graph.add_edge(t3, t1)
        
        # Component 2: Single edge
        e1 = Node("e1")
        e2 = Node("e2")
        graph.add_node(e1)
        graph.add_node(e2)
        graph.add_edge(e1, e2)
        
        coloring_algo = BruteForceColoring(graph)
        result = coloring_algo.color_graph()
        
        # Chromatic number is max of components: max(3, 2) = 3
        self.assertEqual(coloring_algo.get_chromaticity(), 3)
        self.assertTrue(coloring_algo.is_valid_coloring(result))
        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()

