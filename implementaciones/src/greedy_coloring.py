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
            order_strategy: Strategy for ordering vertices
                           'natural' - order by node ID
                           'degree' - order by degree (descending)
            
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
    
    def get_num_colors(self) -> int:
        """
        Get the number of colors used in the coloring.
        
        Returns:
            int: Number of unique colors used.
        """
        return self.get_chromaticity()
    
    def get_coloring_dict(self) -> Dict[str, int]:
        """
        Get the coloring as a dictionary with node IDs as keys.
        
        Returns:
            dict: Mapping from node IDs to color integers.
        """
        return {node.id: color for node, color in self.coloring.items()}
    
    def get_color_classes(self) -> Dict[int, List[str]]:
        """
        Get the color classes, grouping nodes by their assigned color.
        
        Returns:
            dict: Mapping from color to list of node IDs.
        """
        classes: Dict[int, List[str]] = {}
        for node, color in self.coloring.items():
            if color not in classes:
                classes[color] = []
            classes[color].append(node.id)
        return classes
    
    def is_valid_coloring(self, coloring: Optional[Dict[Node, int]] = None) -> bool:
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
