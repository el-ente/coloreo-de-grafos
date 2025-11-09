import time
from typing import Dict, List, Set, Optional
from graph import Node, Graph
from interfaces import GraphColoringAlgorithm


class GreedyColoring(GraphColoringAlgorithm):
    """
    Greedy first-fit algorithm for graph coloring.
    
    This algorithm processes vertices and assigns
    each vertex the smallest color that doesn't conflict with its
    already-colored neighbors.
    
    The resulting coloring is valid but may not use the minimum number
    of colors (not guaranteed to find the chromatic number).
    
    Attributes:
        graph: The Graph object to color
        coloring: Result of the coloring operation (node -> color mapping)

    """
    
    def __init__(self, graph: Graph) -> None:
        """
        Initialize the GreedyColoring algorithm.
        
        Args:
            graph: A Graph object to be colored
            
        Raises:
            ValueError: If graph is None, empty
        """
        super().__init__(graph)
        
        if graph is None:
            raise ValueError("Graph cannot be None")
        
        if not graph.nodes:
            raise ValueError("Graph must contain at least one node")
        
        self.coloring: Dict[Node, int] = {}
    
    def _color_graph_impl(self) -> None:
        """
        Color the graph using the greedy first-fit strategy.
        
        Processes vertices assigning each vertex the smallest color that doesn't conflict
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
        
        nodes = list(self.graph.get_nodes())
        
        self.coloring = {}
        
        for node in nodes:
            forbidden_colors: Set[int] = set()
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
