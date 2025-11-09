"""
Welsh-Powell Graph Coloring Algorithm.

This module implements the Welsh-Powell heuristic, an improved greedy
algorithm that colors high-degree nodes first to achieve better results
than naive first-fit approaches.
"""

import time
from typing import Dict, List, Set, Tuple, Optional
from graph import Node, Graph
from interfaces import GraphColoringAlgorithm


def get_sorted_nodes_by_degree(graph: Graph) -> List[Node]:
    """
    Sort graph nodes in descending order by degree.
    
    Helper function that encapsulates the sorting logic,
    making the main algorithm more readable. In case of ties
    in degree, nodes are sorted lexicographically by ID to
    ensure deterministic results.
    
    Args:
        graph: Graph object
        
    Returns:
        list: Nodes sorted by degree (highest first), with ties
              broken by node ID
              
    Example:
        >>> graph = Graph()
        >>> # ... add nodes ...
        >>> sorted_nodes = get_sorted_nodes_by_degree(graph)
        >>> sorted_nodes[0]  # Node with highest degree
    """
    nodes = list(graph.get_nodes())
    # Ordenar por: 1) grado descendente, 2) ID ascendente (lexicográfico)
    return sorted(nodes, key=lambda n: (-graph.get_degree(n), str(n.id)))


def get_first_available_color(neighbor_colors: Set[int]) -> int:
    """
    Find the smallest positive integer not in the set.
    
    This implements the "first-fit" strategy: given a set of
    colors already used by neighbors, find the smallest color
    number (starting from 1) that is not in the set.
    
    Args:
        neighbor_colors: Set of integers representing used colors
        
    Returns:
        int: First available color (starting from 1)
        
    Example:
        >>> get_first_available_color({1, 2, 4})
        3
        >>> get_first_available_color({2, 3})
        1
        >>> get_first_available_color(set())
        1
    """
    color = 1
    while color in neighbor_colors:
        color += 1
    return color


def validate_coloring(graph: Graph, coloring: Dict[Node, int]) -> Tuple[bool, List[str]]:
    """
    Verify that a coloring is valid (no adjacent nodes share colors).
    
    This is an educational tool to understand and verify the constraint
    being satisfied by the coloring algorithm. Useful for testing and
    debugging.
    
    Args:
        graph: Graph object
        coloring: Dictionary mapping nodes to colors
        
    Returns:
        tuple: (is_valid: bool, errors: list of str)
               is_valid is True if coloring is valid
               errors contains descriptions of any violations found
               
    Example:
        >>> is_valid, errors = validate_coloring(graph, coloring)
        >>> if not is_valid:
        ...     for error in errors:
        ...         print(error)
    """
    errors: List[str] = []
    
    # Verificar que todos los nodos tienen un color asignado
    for node in graph.get_nodes():
        if node not in coloring:
            errors.append(f"Node {node.id} has no color assigned")
    
    # Verificar que no hay vecinos con el mismo color
    for node in graph.get_nodes():
        if node not in coloring:
            continue
            
        node_color = coloring[node]
        for neighbor in graph.get_neighbors(node):
            if neighbor in coloring and coloring[neighbor] == node_color:
                # Evitar duplicados reportando solo una vez por arista
                if str(node.id) < str(neighbor.id):
                    errors.append(
                        f"Adjacent nodes {node.id} and {neighbor.id} "
                        f"both have color {node_color}"
                    )
    
    is_valid = len(errors) == 0
    return (is_valid, errors)


class WelshPowellColoring(GraphColoringAlgorithm):
    """
    Welsh-Powell heuristic for graph coloring.
    """
    
    def __init__(self, graph: Graph) -> None:
        super().__init__(graph)
        self.coloring: Dict[Node, int] = {}

    def _color_graph_impl(self) -> None:
        """
        Color a graph using the Welsh-Powell heuristic.
        
        This algorithm improves upon greedy first-fit by coloring
        high-degree nodes first, which are more constrained and
        harder to color later in the process. The intuition is that
        nodes with many neighbors have fewer color options available,
        so they should be colored early.
        
        Algorithm steps:
        1. Calculate the degree of each node
        2. Sort nodes in descending order by degree
        3. Apply first-fit greedy coloring in this order
        4. Return the resulting coloring
        
        Time Complexity: O(n² + m) where n = nodes, m = edges
        Space Complexity: O(n) for storing coloring and sorted list
        
        Args:
            graph: A Graph object with nodes and edges
            
        Returns:
            tuple: (coloring, execution_time) where:
                   - coloring: dict mapping each node to its assigned color (int)
                   - execution_time: float representing seconds elapsed
                  Colors start from 1 (not 0)
                  
        Raises:
            ValueError: If graph is None or empty
            
        Example:
            >>> graph = Graph()
            >>> # ... add nodes and edges ...
            >>> wp = WelshPowellColoring(graph)
            >>> coloring = wp.color_graph()
            >>> exec_time = wp.get_execution_time()
            >>> print(f"Color: {coloring[node_a]}, Time: {exec_time:.6f}s")
        """
        
        # Validación inicial
        if self.graph is None:
            raise ValueError("Graph cannot be None")
        
        if not self.graph.get_nodes():
            raise ValueError("Graph cannot be empty")
        
        # Paso 1 y 2: Obtener nodos ordenados por grado descendente
        sorted_nodes = get_sorted_nodes_by_degree(self.graph)
        
        # Paso 3: Coloreo greedy en el orden establecido
        for node in sorted_nodes:
            # Obtener colores de vecinos ya coloreados
            neighbor_colors: Set[int] = set()
            for neighbor in self.graph.get_neighbors(node):
                if neighbor in self.coloring:
                    neighbor_colors.add(self.coloring[neighbor])
            
            # Asignar el primer color disponible
            color = get_first_available_color(neighbor_colors)
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


def welsh_powell_coloring(graph: Graph) -> Tuple[Dict[Node, int], float]:
    """
    Convenience function for Welsh-Powell coloring.
    
    This function provides a simple interface for coloring a graph
    using the Welsh-Powell heuristic. It creates a WelshPowellColoring
    instance, performs the coloring, and returns the result.
    
    Args:
        graph: A Graph object to color
        
    Returns:
        tuple: (coloring_dict, execution_time) where:
               - coloring_dict: dict mapping nodes to colors
               - execution_time: float in seconds
               
    Raises:
        ValueError: If graph is None or empty
    """
    algorithm = WelshPowellColoring(graph)
    coloring = algorithm.color_graph()
    execution_time = algorithm.get_execution_time()
    return coloring, execution_time
