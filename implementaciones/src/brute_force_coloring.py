"""
Brute Force Graph Coloring Algorithm.

This module implements an exhaustive search approach to graph coloring.
It explores all possible color assignments until finding a valid coloring.

Educational Purpose:
- Demonstrates the concept of exact algorithms
- Shows why brute force becomes impractical for large graphs
- Useful for understanding the graph coloring problem fundamentally
"""

import time
from itertools import product
from typing import Dict, List, Optional
from graph import Node, Graph
from interfaces import GraphColoringAlgorithm


class BruteForceColoring(GraphColoringAlgorithm):
    """
    Exhaustive search algorithm for graph coloring.
    
    This algorithm explores all possible k-colorations of a graph,
    starting with k=1 and incrementing until a valid coloring is found.
    
    The resulting coloring uses the minimum number of colors possible
    (the chromatic number), but computation time grows exponentially
    with the number of nodes and colors.
    
    Attributes:
        graph: The Graph object to color
        coloring: Result of the coloring operation (node -> color mapping)
    """
    
    def __init__(self, graph: Graph, with_logging = False, step_delay = 0) -> None:
        super().__init__(graph)
        self.coloring: Dict[Node, int] = {}
        self.with_logging = with_logging
        self.step_delay = step_delay
    
    def _color_graph_impl(self) -> None:
        """
        Find a valid coloring of the graph using brute force.
        
        Returns:
            Dictionary mapping each node to its assigned color (integer >= 0)
            
        Algorithm:
        1. Start with k=1 color
        2. Generate all possible k-colorations using backtracking
        3. Test each coloration for validity
        4. If valid, return it; otherwise increment k and repeat
        
        The upper bound uses Brooks' theorem: χ(G) ≤ Δ + 1
        where Δ is the maximum degree of the graph.
        """
        
        nodes = list(self.graph.get_nodes())
        num_nodes = len(nodes)
        
        # Upper bound optimization: Brooks' theorem states χ(G) ≤ Δ + 1
        # Exception: complete graphs and odd cycles need Δ + 1 colors
        max_degree = self.graph.get_max_degree()
        upper_bound = min(max_degree + 1, num_nodes)
        
        # Try with k colors, starting from 1
        for k in range(1, upper_bound + 1):
            # Search for valid k-coloring using backtracking
            valid_coloring = self._find_valid_coloring_with_k_colors(nodes, k)
            
            if valid_coloring is not None:
                self.coloring = valid_coloring
                return self.coloring
        
        # This should never happen for a valid graph
        return {}
    
    def _find_valid_coloring_with_k_colors(self, nodes: List[Node], k: int) -> Optional[Dict[Node, int]]:
        """
        Search for valid k-coloring using backtracking.
        
        Args:
            nodes: List of nodes to color
            k: Number of colors to use
            
        Returns:
            Dictionary with valid coloring, or None if not possible
        """
        coloring: Dict[Node, int] = {}
        
        def backtrack(node_index: int) -> bool:
            if node_index == len(nodes):
                return True
            
            node = nodes[node_index]
            
            # Try assigning each color
            for color in range(k):
                if (self.step_delay > 0):
                    time.sleep(self.step_delay)

                coloring[node] = color
                if (self.with_logging):
                    print([val for val in coloring.values()])
                
                # Check if safe (only against already colored neighbors)
                if self._is_safe_partial_coloring(node, coloring):
                    if backtrack(node_index + 1):
                        return True
                
                del coloring[node]
            
            return False
        
        if backtrack(0):
            return coloring
        return None
    
    def _is_safe_partial_coloring(self, node: Node, coloring: Dict[Node, int]) -> bool:
        """
        Check if current node's color conflicts with already colored neighbors.
        
        Args:
            node: The node to check
            coloring: Dictionary mapping nodes to colors (partial or complete)
            
        Returns:
            True if no conflicts with colored neighbors, False otherwise
        """
        for neighbor in self.graph.get_neighbors(node):
            if neighbor in coloring and coloring[neighbor] == coloring[node]:
                return False
        return True
    