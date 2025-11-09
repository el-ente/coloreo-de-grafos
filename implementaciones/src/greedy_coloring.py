"""
Greedy Graph Coloring Algorithm (First-Fit).

This module implements a greedy approach to graph coloring using
the first-fit strategy. It processes vertices sequentially and
assigns the smallest available color that doesn't conflict with
neighbors.

Educational Purpose:
- Demonstrates greedy algorithmic paradigm
- Shows trade-off between speed and optimality
- Practical for large graphs where exact solutions are infeasible
"""

import time
from graph import Node, Graph
from interfaces import GraphColoringAlgorithm


class GreedyColoring(GraphColoringAlgorithm):
    """
    Greedy first-fit algorithm for graph coloring.
    
    This algorithm processes vertices in a specified order and assigns
    each vertex the smallest color that doesn't conflict with its
    already-colored neighbors.
    
    The resulting coloring is valid but may not use the minimum number
    of colors (not guaranteed to find the chromatic number).
    
    Attributes:
        graph: The Graph object to color
        coloring: Result of the coloring operation (node -> color mapping)
        order_strategy: Strategy for ordering vertices ('natural' or 'degree')
    """
    
    def __init__(self, graph, order_strategy='natural'):
        """
        Initialize the GreedyColoring algorithm.
        
        Args:
            graph: A Graph object to be colored
            order_strategy: Strategy for ordering vertices
                           'natural' - order by node ID
                           'degree' - order by degree (descending)
            
        Raises:
            ValueError: If graph is None, empty, or order_strategy is invalid
        """
        super().__init__(graph)
        
        if graph is None:
            raise ValueError("Graph cannot be None")
        
        if not graph.nodes:
            raise ValueError("Graph must contain at least one node")
        
        if order_strategy not in ['natural', 'degree']:
            raise ValueError("order_strategy must be 'natural' or 'degree'")
        
        self.coloring = {}
        self.order_strategy = order_strategy
    
    def _color_graph_impl(self):
        """
        Color the graph using the greedy first-fit strategy.
        
        Processes vertices in the order specified by order_strategy,
        assigning each vertex the smallest color that doesn't conflict
        with its already-colored neighbors.
        
        Returns:
            dict: Mapping from Node objects to color integers (1-indexed)
            
        Time Complexity: O(n²) where n is the number of vertices
        Space Complexity: O(n) for storing the coloring
        
        Example:
            >>> greedy = GreedyColoring(graph)
            >>> coloring = greedy.color_graph()
            >>> print(coloring[node_a])
            1
        """
        
        # Obtener lista ordenada de nodos según la estrategia
        nodes = list(self.graph.get_nodes())
        
        if self.order_strategy == 'natural':
            # Ordenar por node.id (alfabéticamente o numéricamente)
            nodes.sort(key=lambda n: str(n.id))
        else:  # 'degree'
            # Ordenar por grado descendente, desempatar por node.id
            nodes.sort(key=lambda n: (-self.graph.get_degree(n), str(n.id)))
        
        # Inicializar coloración vacía
        self.coloring = {}
        
        # Procesar cada nodo en orden
    
    def color_graph(self):
        """
        Color the graph using the greedy first-fit strategy.
        
        Processes vertices in the order specified by order_strategy,
        assigning each vertex the smallest color that doesn't conflict
        with its already-colored neighbors.
        
        Returns:
            dict: Mapping from Node objects to color integers (1-indexed)
            
        Time Complexity: O(n²) where n is the number of vertices
        Space Complexity: O(n) for storing the coloring
        
        Example:
            >>> greedy = GreedyColoring(graph)
            >>> coloring = greedy.color_graph()
            >>> print(coloring[node_a])
            1
        """
        start_time = time.time()
        
        # Obtener lista ordenada de nodos según la estrategia
        nodes = list(self.graph.get_nodes())
        
        if self.order_strategy == 'natural':
            # Ordenar por node.id (alfabéticamente o numéricamente)
            nodes.sort(key=lambda n: str(n.id))
        else:  # 'degree'
            # Ordenar por grado descendente, desempatar por node.id
            nodes.sort(key=lambda n: (-self.graph.get_degree(n), str(n.id)))
        
        # Inicializar coloración vacía
        self.coloring = {}
        
        # Procesar cada nodo en orden
        for node in nodes:
            # Recolectar colores de vecinos ya coloreados
            forbidden_colors = set()
            neighbors = self.graph.get_neighbors(node)
            
            for neighbor in neighbors:
                if neighbor in self.coloring:
                    forbidden_colors.add(self.coloring[neighbor])
            
            # Encontrar el menor color disponible (first-fit)
            color = 1
            while color in forbidden_colors:
                color += 1
            
            # Asignar el color al nodo
            self.coloring[node] = color
        
        return self.coloring


if __name__ == "__main__":
    # 1. Crear un grafo de ejemplo (ciclo de 5 nodos)
    print("=" * 60)
    print("ALGORITMO CODICIOSO: FIRST-FIT")
    print("=" * 60)
    
    graph = Graph()
    nodes = [Node(chr(65 + i)) for i in range(5)]  # A, B, C, D, E
    
    for node in nodes:
        graph.add_node(node)
    
    # Crear ciclo: A-B-C-D-E-A
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    for i, j in edges:
        graph.add_edge(nodes[i], nodes[j])
    
    print(f"\nGrafo creado: {graph}")
    print(f"Número cromático esperado: 3 (ciclo impar)")
    
    # 2. Colorear con estrategia natural
    print("\n" + "-" * 60)
    print("ESTRATEGIA: Orden Natural")
    print("-" * 60)
    
    greedy_natural = GreedyColoring(graph, order_strategy='natural')
    coloring_natural = greedy_natural.color_graph()
    
    print(f"⏱️  Execution time: {greedy_natural.get_execution_time():.6f} seconds")
    print(f"\nColoración obtenida:")
    for node, color in sorted(coloring_natural.items(), key=lambda x: x[0].id):
        print(f"  {node.id}: Color {color}")
    
    print(f"\nNúmero de colores usados: {greedy_natural.get_chromaticity()}")
    print(f"¿Coloración válida? {greedy_natural.is_valid_coloring(coloring_natural)}")
    
    # Verificar que ningún par de vecinos tiene el mismo color
    print("\nVerificación de vecinos:")
    for node in nodes:
        neighbors = graph.get_neighbors(node)
        neighbor_colors = [coloring_natural[n] for n in neighbors]
        print(f"  {node.id} (Color {coloring_natural[node]}) - Vecinos: {neighbor_colors}")
    
    # 3. Colorear con estrategia por grado
    print("\n" + "-" * 60)
    print("ESTRATEGIA: Orden por Grado (descendente)")
    print("-" * 60)
    
    greedy_degree = GreedyColoring(graph, order_strategy='degree')
    coloring_degree = greedy_degree.color_graph()
    
    print(f"⏱️  Execution time: {greedy_degree.get_execution_time():.6f} seconds")
    print(f"\nColoración obtenida:")
    for node, color in sorted(coloring_degree.items(), key=lambda x: x[0].id):
        print(f"  {node.id}: Color {color}")
    
    print(f"\nNúmero de colores usados: {greedy_degree.get_chromaticity()}")
    print(f"¿Coloración válida? {greedy_degree.is_valid_coloring(coloring_degree)}")
    
    # 4. Comparación
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPARATIVO")
    print("=" * 60)
    print(f"Número cromático teórico: 3")
    print(f"Colores usados (natural): {greedy_natural.get_chromaticity()}")
    print(f"Colores usados (por grado): {greedy_degree.get_chromaticity()}")
    print(f"\nNota: El algoritmo codicioso no garantiza encontrar el mínimo,")
    print(f"pero es mucho más rápido que la fuerza bruta para grafos grandes.")
