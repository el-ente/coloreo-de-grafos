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
    
    def test_greedy_order_dependency(self):
        """Test that node order affects greedy coloring result quality.
        
        Greedy is order-sensitive. This test demonstrates that different
        iteration orders can produce different (but valid) colorings with
        potentially different numbers of colors.
        """
        graph = Graph()
        
        # Crear un "wheel graph": centro conectado a un ciclo exterior
        # Estructura: center conectado a v0, v1, v2, v3, v4
        # y v0-v1-v2-v3-v4-v0 forman un ciclo
        center = Node("center")
        outer = [Node(f"v{i}") for i in range(5)]
        
        graph.add_node(center)
        for node in outer:
            graph.add_node(node)
            graph.add_edge(center, node)
        
        # Conectar el ciclo exterior
        for i in range(5):
            graph.add_edge(outer[i], outer[(i + 1) % 5])
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        # El coloreo debe ser válido independientemente del orden
        self.assertTrue(greedy.is_valid_coloring())
        
        # Un wheel graph con ciclo impar necesita 4 colores (centro + 3 del ciclo)
        # o potencialmente más dependiendo del orden
        num_colors = len(set(coloring.values()))
        self.assertGreaterEqual(num_colors, 4)
        self.assertLessEqual(num_colors, 6)  # No debería necesitar más de n nodos
    
    def test_worst_case_greedy(self):
        """Test greedy on a graph where it may not be optimal.
        
        On a complete bipartite graph, greedy might use 3 colors if it
        colors nodes in an unfortunate order, even though 2 is optimal.
        """
        graph = Graph()
        
        # K_{3,3}: Grafo bipartito completo
        set_a = [Node(f"a{i}") for i in range(3)]
        set_b = [Node(f"b{i}") for i in range(3)]
        
        for node in set_a + set_b:
            graph.add_node(node)
        
        # Conectar cada nodo de set_a con cada nodo de set_b
        for a_node in set_a:
            for b_node in set_b:
                graph.add_edge(a_node, b_node)
        
        greedy = GreedyColoring(graph)
        coloring = greedy.color_graph()
        
        num_colors = len(set(coloring.values()))
        
        # El coloreo debe ser válido
        self.assertTrue(greedy.is_valid_coloring())
        
        # Un bipartito K_{3,3} necesita exactamente 2 colores óptimamente
        # Greedy debería encontrarlo si procesa nodos en orden adecuado
        # pero podría usar más colores en el peor caso
        self.assertGreaterEqual(num_colors, 2)
        self.assertLessEqual(num_colors, 6)
    
    def test_chromatic_number_vs_used_colors(self):
        """Compare colors used vs known chromatic numbers.
        
        For certain graph families, we know the exact chromatic number.
        This test verifies greedy finds valid colorings, even if not optimal.
        """
        # Test 1: Complete graph K_n needs exactly n colors
        k5 = Graph()
        k5_nodes = [Node(f"k{i}") for i in range(5)]
        
        for node in k5_nodes:
            k5.add_node(node)
        
        # Conectar todos con todos
        for i in range(5):
            for j in range(i + 1, 5):
                k5.add_edge(k5_nodes[i], k5_nodes[j])
        
        greedy_k5 = GreedyColoring(k5)
        coloring_k5 = greedy_k5.color_graph()
        
        # K_5 necesita exactamente 5 colores (número cromático = 5)
        self.assertEqual(len(set(coloring_k5.values())), 5)
        self.assertTrue(greedy_k5.is_valid_coloring())
        
        # Test 2: Even cycle needs 2 colors
        c6 = Graph()
        c6_nodes = [Node(f"c{i}") for i in range(6)]
        
        for node in c6_nodes:
            c6.add_node(node)
        
        for i in range(6):
            c6.add_edge(c6_nodes[i], c6_nodes[(i + 1) % 6])
        
        greedy_c6 = GreedyColoring(c6)
        coloring_c6 = greedy_c6.color_graph()
        
        # C_6 (ciclo par) necesita exactamente 2 colores
        self.assertEqual(len(set(coloring_c6.values())), 2)
        self.assertTrue(greedy_c6.is_valid_coloring())
        
        # Test 3: Tree (bipartite) - greedy should find a valid coloring
        # Trees are bipartite and need at most 2 colors optimally,
        # but greedy may use 3 depending on node order
        tree = Graph()
        tree_nodes = [Node(f"t{i}") for i in range(7)]
        
        for node in tree_nodes:
            tree.add_node(node)
        
        # Crear un árbol binario
        #       t0
        #      /  \
        #    t1    t2
        #   / \   / \
        #  t3 t4 t5 t6
        tree.add_edge(tree_nodes[0], tree_nodes[1])
        tree.add_edge(tree_nodes[0], tree_nodes[2])
        tree.add_edge(tree_nodes[1], tree_nodes[3])
        tree.add_edge(tree_nodes[1], tree_nodes[4])
        tree.add_edge(tree_nodes[2], tree_nodes[5])
        tree.add_edge(tree_nodes[2], tree_nodes[6])
        
        greedy_tree = GreedyColoring(tree)
        coloring_tree = greedy_tree.color_graph()
        
        # Trees are bipartite (optimal = 2), but greedy may use more
        # depending on node iteration order. Just verify it's valid and reasonable.
        num_colors_tree = len(set(coloring_tree.values()))
        self.assertGreaterEqual(num_colors_tree, 2)  # At least 2 (has edges)
        self.assertLessEqual(num_colors_tree, 4)  # Should not be too bad
        self.assertTrue(greedy_tree.is_valid_coloring())


if __name__ == '__main__':
    unittest.main()
