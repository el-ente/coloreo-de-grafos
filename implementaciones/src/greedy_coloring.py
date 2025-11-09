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
    
    def get_num_colors(self):
        """
        Get the number of colors used in the coloring.
        
        Returns:
            int: Number of unique colors used.
        """
        return len(set(self.coloring.values()))
    
    def get_coloring_dict(self):
        """
        Get the coloring as a dictionary with node IDs as keys.
        
        Returns:
            dict: Mapping from node IDs to color integers.
        """
        return {node.id: color for node, color in self.coloring.items()}
    
    def get_color_classes(self):
        """
        Get the color classes, grouping nodes by their assigned color.
        
        Returns:
            dict: Mapping from color to list of node IDs.
        """
        classes = {}
        for node, color in self.coloring.items():
            if color not in classes:
                classes[color] = []
            classes[color].append(node.id)
        return classes
    
    def is_valid_coloring(self, coloring=None):
        """
        Check if the coloring is valid for the graph.
        
        Args:
            coloring: Optional coloring dict. If None, uses self.coloring.
        
        Returns:
            bool: True if valid, False otherwise.
        """
        if coloring is None:
            coloring = self.coloring
        return super().is_valid_coloring(coloring)
