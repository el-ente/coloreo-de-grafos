"""
Unit tests for Greedy Graph Coloring Algorithm.

Tests verify correctness of the first-fit greedy coloring
for various graph structures and configurations.
"""

import unittest
from graph import Node, Graph
from greedy_coloring import GreedyColoring


class TestGreedyColoring(unittest.TestCase):
    """Test suite for GreedyColoring class."""
    
    def test_single_node(self):
        """A single node should use 1 color."""
        graph = Graph()
        node = Node("A")
        graph.add_node(node)
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 1)
        self.assertEqual(coloring[node], 1)
        self.assertEqual(len(set(coloring.values())), 1)
        self.assertTrue(greedy.is_valid_coloring())
    
    def test_two_disconnected_nodes(self):
        """Two disconnected nodes should use 1 color."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        graph.add_node(node_a)
        graph.add_node(node_b)
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 2)
        # Ambos nodos pueden tener el mismo color (no hay arista)
        self.assertEqual(coloring[node_a], 1)
        self.assertEqual(coloring[node_b], 1)
        self.assertEqual(len(set(coloring.values())), 1)
        self.assertTrue(greedy.is_valid_coloring())
    
    def test_two_connected_nodes(self):
        """Two connected nodes should use 2 colors."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_edge(node_a, node_b)
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 2)
        # Los nodos deben tener colores diferentes
        self.assertNotEqual(coloring[node_a], coloring[node_b])
        self.assertEqual(len(set(coloring.values())), 2)
        self.assertTrue(greedy.is_valid_coloring())
    
    def test_triangle(self):
        """A triangle (K3) should use 3 colors."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(3)]  # A, B, C
        
        for node in nodes:
            graph.add_node(node)
        
        # Crear triángulo completo
        graph.add_edge(nodes[0], nodes[1])
        graph.add_edge(nodes[1], nodes[2])
        graph.add_edge(nodes[2], nodes[0])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 3)
        self.assertEqual(len(set(coloring.values())), 3)
        self.assertTrue(greedy.is_valid_coloring())
        
        # Todos los nodos deben tener colores diferentes
        colors = set(coloring.values())
        self.assertEqual(len(colors), 3)
    
    def test_bipartite_graph(self):
        """A bipartite graph K2,2 should use 2 colors."""
        graph = Graph()
        # Conjunto 1: A, B
        # Conjunto 2: C, D
        nodes = [Node(chr(65 + i)) for i in range(4)]
        
        for node in nodes:
            graph.add_node(node)
        
        # Conectar conjunto 1 con conjunto 2
        graph.add_edge(nodes[0], nodes[2])  # A-C
        graph.add_edge(nodes[0], nodes[3])  # A-D
        graph.add_edge(nodes[1], nodes[2])  # B-C
        graph.add_edge(nodes[1], nodes[3])  # B-D
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 4)
        self.assertEqual(len(set(coloring.values())), 2)
        self.assertTrue(greedy.is_valid_coloring())
        
        # A y B deben tener el mismo color
        # C y D deben tener el mismo color (diferente de A y B)
        self.assertEqual(coloring[nodes[0]], coloring[nodes[1]])
        self.assertEqual(coloring[nodes[2]], coloring[nodes[3]])
        self.assertNotEqual(coloring[nodes[0]], coloring[nodes[2]])
    
    def test_cycle_odd(self):
        """An odd cycle C5 should use 3 colors."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(5)]  # A, B, C, D, E
        
        for node in nodes:
            graph.add_node(node)
        
        # Crear ciclo: A-B-C-D-E-A
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        for i, j in edges:
            graph.add_edge(nodes[i], nodes[j])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 5)
        self.assertEqual(len(set(coloring.values())), 3)
        self.assertTrue(greedy.is_valid_coloring())
    
    def test_complete_graph(self):
        """A complete graph K4 should use 4 colors."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(4)]  # A, B, C, D
        
        for node in nodes:
            graph.add_node(node)
        
        # Conectar todos los nodos entre sí
        for i in range(4):
            for j in range(i + 1, 4):
                graph.add_edge(nodes[i], nodes[j])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 4)
        self.assertEqual(len(set(coloring.values())), 4)
        self.assertTrue(greedy.is_valid_coloring())
        
        # Todos los nodos deben tener colores diferentes
        colors = set(coloring.values())
        self.assertEqual(len(colors), 4)
    
    def test_star_graph(self):
        """A star graph should use 2 colors."""
        graph = Graph()
        center = Node("CENTER")
        graph.add_node(center)
        
        # Crear 5 nodos periféricos conectados solo al centro
        periphery = [Node(f"P{i}") for i in range(5)]
        for node in periphery:
            graph.add_node(node)
            graph.add_edge(center, node)
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        self.assertEqual(len(coloring), 6)
        self.assertEqual(len(set(coloring.values())), 2)
        self.assertTrue(greedy.is_valid_coloring())
        
        # Todos los nodos periféricos deben tener el mismo color
        # El centro debe tener un color diferente
        periphery_colors = [coloring[node] for node in periphery]
        self.assertEqual(len(set(periphery_colors)), 1)
        self.assertNotEqual(coloring[center], periphery_colors[0])
      
    def test_empty_graph_error(self):
        """Verify that empty graph raises ValueError."""
        graph = Graph()
        
        with self.assertRaises(ValueError) as context:
            GreedyColoring(graph)
        
        self.assertIn("Graph must contain at least one node", 
                      str(context.exception))
    
    def test_none_graph_error(self):
        """Verify that None graph raises ValueError."""
        with self.assertRaises(ValueError) as context:
            GreedyColoring(None)
        
        self.assertIn("Graph cannot be None", str(context.exception))
    
    def test_get_coloring_dict(self):
        """Test coloring dict with node IDs."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(3)]
        
        for node in nodes:
            graph.add_node(node)
        
        graph.add_edge(nodes[0], nodes[1])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        coloring_dict = {node.id: color for node, color in coloring.items()}
        
        # Verificar que las claves son IDs, no objetos Node
        self.assertIn('A', coloring_dict)
        self.assertIn('B', coloring_dict)
        self.assertIn('C', coloring_dict)
        self.assertEqual(len(coloring_dict), 3)
    
    def test_get_color_classes(self):
        """Test color classes group nodes by color."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(3)]
        
        for node in nodes:
            graph.add_node(node)
        
        # A-B conectados, C aislado
        graph.add_edge(nodes[0], nodes[1])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        from collections import defaultdict
        color_classes = defaultdict(list)
        for node, color in coloring.items():
            color_classes[color].append(node.id)
        color_classes = dict(color_classes)
        
        # Debe haber 2 colores
        self.assertEqual(len(color_classes), 2)
        
        # Verificar que A y C están en una clase, B en otra
        # (o alguna distribución válida)
        total_nodes = sum(len(nodes) for nodes in color_classes.values())
        self.assertEqual(total_nodes, 3)
    
    def test_multiple_colorings(self):
        """Test that calling color_graph multiple times overwrites previous coloring."""
        graph = Graph()
        nodes = [Node(chr(65 + i)) for i in range(3)]
        
        for node in nodes:
            graph.add_node(node)
        
        greedy = GreedyColoring(graph)
        
        # Primera coloración
        coloring1 = greedy.color_graph()
        self.assertEqual(len(coloring1), 3)
        
        # Segunda coloración (debe sobrescribir)
        coloring2 = greedy.color_graph()
        self.assertEqual(len(coloring2), 3)
        
        # Ambas deben ser iguales (mismo grafo, mismo orden)
        self.assertEqual(coloring1, coloring2)


if __name__ == '__main__':
    unittest.main()
