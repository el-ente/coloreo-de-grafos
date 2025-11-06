"""
Unit tests for Welsh-Powell Graph Coloring Algorithm.

Tests verify correctness of the Welsh-Powell heuristic for
various graph structures and edge cases.
"""

import unittest
from graph import Node, Graph
from welsh_powell_coloring import (
    welsh_powell_coloring,
    get_sorted_nodes_by_degree,
    get_first_available_color,
    validate_coloring
)
from greedy_coloring import GreedyColoring


class TestHelperFunctions(unittest.TestCase):
    """Test suite for helper functions."""
    
    def test_get_first_available_color_empty_set(self):
        """First available color from empty set should be 1."""
        color = get_first_available_color(set())
        self.assertEqual(color, 1)
    
    def test_get_first_available_color_with_gaps(self):
        """Should find the smallest gap in the color set."""
        color = get_first_available_color({1, 2, 4})
        self.assertEqual(color, 3)
    
    def test_get_first_available_color_no_one(self):
        """If 1 is not used, should return 1."""
        color = get_first_available_color({2, 3, 4})
        self.assertEqual(color, 1)
    
    def test_get_first_available_color_sequential(self):
        """With sequential colors, should return next number."""
        color = get_first_available_color({1, 2, 3})
        self.assertEqual(color, 4)
    
    def test_get_sorted_nodes_by_degree(self):
        """Nodes should be sorted by degree descending."""
        graph = Graph()
        
        # Crear grafo estrella: centro conectado a 3 hojas
        center = Node("center")
        leaf1 = Node("leaf1")
        leaf2 = Node("leaf2")
        leaf3 = Node("leaf3")
        
        graph.add_node(center)
        graph.add_node(leaf1)
        graph.add_node(leaf2)
        graph.add_node(leaf3)
        
        graph.add_edge(center, leaf1)
        graph.add_edge(center, leaf2)
        graph.add_edge(center, leaf3)
        
        sorted_nodes = get_sorted_nodes_by_degree(graph)
        
        # El centro debe estar primero (grado 3)
        self.assertEqual(sorted_nodes[0], center)
        # Las hojas después (grado 1 cada una)
        self.assertEqual(len(sorted_nodes), 4)
        self.assertEqual(graph.get_degree(sorted_nodes[0]), 3)
        self.assertEqual(graph.get_degree(sorted_nodes[1]), 1)
    
    def test_get_sorted_nodes_ties_broken_by_id(self):
        """When degrees are equal, should sort by ID lexicographically."""
        graph = Graph()
        
        # Tres nodos aislados (mismo grado 0)
        node_c = Node("c")
        node_a = Node("a")
        node_b = Node("b")
        
        graph.add_node(node_c)
        graph.add_node(node_a)
        graph.add_node(node_b)
        
        sorted_nodes = get_sorted_nodes_by_degree(graph)
        
        # Deben estar ordenados alfabéticamente
        self.assertEqual(sorted_nodes[0].id, "a")
        self.assertEqual(sorted_nodes[1].id, "b")
        self.assertEqual(sorted_nodes[2].id, "c")
    
    def test_validate_coloring_valid(self):
        """Valid coloring should return True with no errors."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_edge(node_a, node_b)
        
        # Coloreo válido: vecinos tienen colores diferentes
        coloring = {node_a: 1, node_b: 2}
        
        is_valid, errors = validate_coloring(graph, coloring)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_coloring_invalid(self):
        """Invalid coloring should return False with error messages."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_edge(node_a, node_b)
        
        # Coloreo inválido: vecinos tienen el mismo color
        coloring = {node_a: 1, node_b: 1}
        
        is_valid, errors = validate_coloring(graph, coloring)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("both have color", errors[0].lower())
    
    def test_validate_coloring_missing_node(self):
        """Should detect when a node has no color assigned."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        
        # Coloreo incompleto
        coloring = {node_a: 1}
        
        is_valid, errors = validate_coloring(graph, coloring)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("no color", errors[0].lower())


class TestWelshPowellColoring(unittest.TestCase):
    """Test suite for welsh_powell_coloring function."""
    
    def test_none_graph(self):
        """Should raise ValueError for None graph."""
        with self.assertRaises(ValueError) as context:
            welsh_powell_coloring(None)
        
        self.assertIn("cannot be None", str(context.exception))
    
    def test_empty_graph(self):
        """Should raise ValueError for empty graph."""
        graph = Graph()
        
        with self.assertRaises(ValueError) as context:
            welsh_powell_coloring(graph)
        
        self.assertIn("cannot be empty", str(context.exception))
    
    def test_single_node(self):
        """Single node should use color 1."""
        graph = Graph()
        node = Node("A")
        graph.add_node(node)
        
        coloring = welsh_powell_coloring(graph)
        
        self.assertEqual(len(coloring), 1)
        self.assertEqual(coloring[node], 1)
    
    def test_two_isolated_nodes(self):
        """Two isolated nodes should both use color 1."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        
        coloring = welsh_powell_coloring(graph)
        
        self.assertEqual(len(coloring), 2)
        self.assertEqual(coloring[node_a], 1)
        self.assertEqual(coloring[node_b], 1)
    
    def test_multiple_isolated_nodes(self):
        """Multiple isolated nodes should all use color 1."""
        graph = Graph()
        nodes = [Node(f"v{i}") for i in range(5)]
        
        for node in nodes:
            graph.add_node(node)
        
        coloring = welsh_powell_coloring(graph)
        
        self.assertEqual(len(coloring), 5)
        # Todos deben tener el mismo color
        colors = set(coloring.values())
        self.assertEqual(len(colors), 1)
        self.assertEqual(1 in colors, True)
    
    def test_triangle_graph(self):
        """Complete graph K3 (triangle) should use exactly 3 colors."""
        graph = Graph()
        node_a = Node("A")
        node_b = Node("B")
        node_c = Node("C")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_node(node_c)
        
        # Crear triángulo
        graph.add_edge(node_a, node_b)
        graph.add_edge(node_b, node_c)
        graph.add_edge(node_c, node_a)
        
        coloring = welsh_powell_coloring(graph)
        
        # Verificar que usa 3 colores
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 3)
        
        # Verificar que el coloreo es válido
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_complete_graph_k4(self):
        """Complete graph K4 should use exactly 4 colors."""
        graph = Graph()
        nodes = [Node(f"v{i}") for i in range(1, 5)]
        
        for node in nodes:
            graph.add_node(node)
        
        # Conectar todos con todos
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                graph.add_edge(nodes[i], nodes[j])
        
        coloring = welsh_powell_coloring(graph)
        
        # K4 necesita 4 colores
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 4)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_bipartite_graph(self):
        """Bipartite graph should use exactly 2 colors."""
        graph = Graph()
        
        # Conjunto A
        a1 = Node("a1")
        a2 = Node("a2")
        a3 = Node("a3")
        
        # Conjunto B
        b1 = Node("b1")
        b2 = Node("b2")
        
        for node in [a1, a2, a3, b1, b2]:
            graph.add_node(node)
        
        # Conectar cada nodo de A con cada nodo de B
        graph.add_edge(a1, b1)
        graph.add_edge(a1, b2)
        graph.add_edge(a2, b1)
        graph.add_edge(a2, b2)
        graph.add_edge(a3, b1)
        graph.add_edge(a3, b2)
        
        coloring = welsh_powell_coloring(graph)
        
        # Debe usar exactamente 2 colores
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 2)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_star_graph(self):
        """Star graph should use 2 colors."""
        graph = Graph()
        
        center = Node("center")
        leaves = [Node(f"leaf{i}") for i in range(5)]
        
        graph.add_node(center)
        for leaf in leaves:
            graph.add_node(leaf)
            graph.add_edge(center, leaf)
        
        coloring = welsh_powell_coloring(graph)
        
        # Debe usar 2 colores (centro y hojas)
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 2)
        
        # El centro debe tener un color diferente a todas las hojas
        center_color = coloring[center]
        for leaf in leaves:
            self.assertNotEqual(coloring[leaf], center_color)
        
        # Todas las hojas pueden tener el mismo color
        leaf_colors = [coloring[leaf] for leaf in leaves]
        self.assertEqual(len(set(leaf_colors)), 1)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_linear_graph(self):
        """Linear graph (path) should use at most 2 colors."""
        graph = Graph()
        
        nodes = [Node(f"v{i}") for i in range(6)]
        for node in nodes:
            graph.add_node(node)
        
        # Crear camino: v0-v1-v2-v3-v4-v5
        for i in range(len(nodes) - 1):
            graph.add_edge(nodes[i], nodes[i + 1])
        
        coloring = welsh_powell_coloring(graph)
        
        # Debe usar máximo 2 colores
        num_colors = len(set(coloring.values()))
        self.assertLessEqual(num_colors, 2)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_cycle_odd(self):
        """Odd cycle (C5) should use exactly 3 colors."""
        graph = Graph()
        
        nodes = [Node(f"v{i}") for i in range(5)]
        for node in nodes:
            graph.add_node(node)
        
        # Crear ciclo: v0-v1-v2-v3-v4-v0
        for i in range(len(nodes)):
            graph.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])
        
        coloring = welsh_powell_coloring(graph)
        
        # Ciclo impar necesita 3 colores
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 3)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_cycle_even(self):
        """Even cycle (C6) should use exactly 2 colors."""
        graph = Graph()
        
        nodes = [Node(f"v{i}") for i in range(6)]
        for node in nodes:
            graph.add_node(node)
        
        # Crear ciclo: v0-v1-v2-v3-v4-v5-v0
        for i in range(len(nodes)):
            graph.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])
        
        coloring = welsh_powell_coloring(graph)
        
        # Ciclo par necesita 2 colores
        num_colors = len(set(coloring.values()))
        self.assertEqual(num_colors, 2)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_disconnected_components(self):
        """Graph with multiple components should color each independently."""
        graph = Graph()
        
        # Componente 1: triángulo
        t1 = Node("t1")
        t2 = Node("t2")
        t3 = Node("t3")
        
        graph.add_node(t1)
        graph.add_node(t2)
        graph.add_node(t3)
        
        graph.add_edge(t1, t2)
        graph.add_edge(t2, t3)
        graph.add_edge(t3, t1)
        
        # Componente 2: arista simple
        e1 = Node("e1")
        e2 = Node("e2")
        
        graph.add_node(e1)
        graph.add_node(e2)
        graph.add_edge(e1, e2)
        
        # Componente 3: nodo aislado
        isolated = Node("isolated")
        graph.add_node(isolated)
        
        coloring = welsh_powell_coloring(graph)
        
        # Debe colorear todos los nodos
        self.assertEqual(len(coloring), 6)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_all_nodes_same_degree(self):
        """Graph where all nodes have same degree."""
        graph = Graph()
        
        # Ciclo C4: todos los nodos tienen grado 2
        nodes = [Node(f"v{i}") for i in range(4)]
        for node in nodes:
            graph.add_node(node)
        
        for i in range(len(nodes)):
            graph.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])
        
        coloring = welsh_powell_coloring(graph)
        
        # Verificar que el algoritmo maneja este caso
        # (el orden secundario por ID debe resolver empates)
        self.assertEqual(len(coloring), 4)
        
        # Verificar validez
        is_valid, _ = validate_coloring(graph, coloring)
        self.assertTrue(is_valid)
    
    def test_comparison_with_greedy(self):
        """Welsh-Powell should use <= colors than basic greedy."""
        # Crear un grafo donde el orden importa
        graph = Graph()
        
        # Crear grafo "comb" donde Welsh-Powell debería hacer mejor
        # Estructura: una línea de nodos de alto grado con hojas
        backbone = [Node(f"b{i}") for i in range(4)]
        for node in backbone:
            graph.add_node(node)
        
        # Conectar backbone linealmente
        for i in range(len(backbone) - 1):
            graph.add_edge(backbone[i], backbone[i + 1])
        
        # Añadir hojas a cada nodo del backbone
        for i, bb_node in enumerate(backbone):
            for j in range(3):
                leaf = Node(f"leaf{i}_{j}")
                graph.add_node(leaf)
                graph.add_edge(bb_node, leaf)
        
        # Aplicar Welsh-Powell
        wp_coloring = welsh_powell_coloring(graph)
        wp_colors = len(set(wp_coloring.values()))
        
        # Aplicar greedy básico (sin ordenamiento previo)
        greedy = GreedyColoring(graph)
        greedy_coloring = greedy.color_graph()
        greedy_colors = greedy.get_num_colors()
        
        # Welsh-Powell debe usar <= colores que greedy básico
        self.assertLessEqual(wp_colors, greedy_colors)
        
        # Ambos deben ser válidos
        is_valid_wp, _ = validate_coloring(graph, wp_coloring)
        is_valid_greedy, _ = validate_coloring(graph, greedy_coloring)
        
        self.assertTrue(is_valid_wp)
        self.assertTrue(is_valid_greedy)


if __name__ == "__main__":
    unittest.main()
