"""
Brute Force Graph Coloring Algorithm.

This module implements an exhaustive search approach to graph coloring.
It explores all possible color assignments until finding a valid coloring.

Educational Purpose:
- Demonstrates the concept of exact algorithms
- Shows why brute force becomes impractical for large graphs
- Useful for understanding the graph coloring problem fundamentally
"""

from itertools import product
from graph import Node, Graph


class BruteForceColoring:
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
    
    def __init__(self, graph):
        """
        Initialize the BruteForceColoring algorithm.
        
        Args:
            graph: A Graph object to be colored
            
        Raises:
            ValueError: If graph is None or empty
        """
        if graph is None:
            raise ValueError("Graph cannot be None")
        
        if not graph.nodes:
            raise ValueError("Graph must contain at least one node")
        
        self.graph = graph
        self.coloring = {}
    
    def color_graph(self):
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
    
    def _find_valid_coloring_with_k_colors(self, nodes, k):
        """
        Search for valid k-coloring using backtracking.
        
        Args:
            nodes: List of nodes to color
            k: Number of colors to use
            
        Returns:
            Dictionary with valid coloring, or None if not possible
        """
        coloring = {}
        
        def backtrack(node_index):
            if node_index == len(nodes):
                return True
            
            node = nodes[node_index]
            
            # Try assigning each color
            for color in range(k):
                coloring[node] = color
                
                # Check if safe (only against already colored neighbors)
                if self._is_safe_partial_coloring(node, coloring):
                    if backtrack(node_index + 1):
                        return True
                
                del coloring[node]
            
            return False
        
        if backtrack(0):
            return coloring
        return None
    
    def _is_safe_partial_coloring(self, node, coloring):
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
    
    def _is_valid_coloring(self, coloring):
        """
        Verify if a complete coloring is valid for the entire graph.
        
        Args:
            coloring: Dictionary mapping nodes to colors
            
        Returns:
            True if the coloring is valid, False otherwise
        """
        # Check all nodes have a color assignment
        if set(coloring.keys()) != self.graph.get_nodes():
            return False
        
        # Verify no adjacent nodes share the same color
        for edge in self.graph.get_edges():
            node1, node2 = edge
            if coloring[node1] == coloring[node2]:
                return False
        
        return True
    
    def is_valid_coloring(self, coloring):
        """
        Public method to check if a given coloring is valid.
        
        Args:
            coloring: Dictionary mapping nodes to colors
            
        Returns:
            True if the coloring is valid, False otherwise
            
        Raises:
            ValueError: If coloring doesn't include all nodes
        """
        if set(coloring.keys()) != self.graph.get_nodes():
            raise ValueError("Coloring must include all nodes")
        
        return self._is_valid_coloring(coloring)
    
    def get_chromaticity(self):
        """
        Get the chromatic number (minimum colors needed).
        
        Returns:
            Integer representing the minimum number of colors needed
            
        Raises:
            RuntimeError: If color_graph() has not been called yet
            
        Note:
            You must call color_graph() before calling this method.
        """
        if not self.coloring:
            raise RuntimeError(
                "No coloring found. Call color_graph() first to compute the coloring."
            )
        
        # Chromatic number is max color used + 1 (colors are 0-indexed)
        return max(self.coloring.values()) + 1


# ============================================================================
# Análisis de Complejidad / Complexity Analysis
# ============================================================================
"""
TEMPORAL COMPLEXITY (Complejidad Temporal):
- For k colors and n nodes: O(k^n * E)
  where E = number of edges (validation cost)
- Worst case: O(n^n * E) when trying all possibilities
- Example: 5 nodes, 10 colors → ~100,000 combinations to test
- Example: 10 nodes, 10 colors → ~10 billion combinations to test

SPACE COMPLEXITY (Complejidad Espacial):
- O(n) for storing the coloring and node list
- O(k^n) in the worst case for generating all combinations

PRACTICAL LIMITATIONS (Limitaciones Prácticas):
- Impractical for graphs with more than ~15-20 nodes
- Becomes exponentially slower as nodes or colors increase
- Better approaches exist: greedy (fast but suboptimal),
  Welsh-Powell (faster heuristic), or sophisticated techniques
  like branch-and-bound, constraint propagation

USE CASES (Casos de Uso):
- Educational purposes: understanding the problem fundamentally
- Small graphs: < 10 nodes
- Finding exact chromatic number for research
- Verification: testing if a solution is optimal
"""


# ============================================================================
# Example of use / Ejemplo de uso
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BRUTE FORCE GRAPH COLORING - Example")
    print("=" * 70)
    
    # Crear un grafo de ejemplo
    print("\n1. Creating a graph with 4 nodes...")
    print("-" * 70)
    
    graph = Graph()
    
    # Crear nodos
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    
    # Añadir nodos al grafo
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)
    
    # Crear un grafo con la siguiente estructura:
    #     A --- B
    #     |  \  |
    #     C -- D
    # (A es adyacente a B, C, D; B es adyacente a A, D; etc.)
    
    print("Adding edges: A-B, A-C, A-D, B-D, C-D")
    graph.add_edge(node_a, node_b)  # A - B
    graph.add_edge(node_a, node_c)  # A - C
    graph.add_edge(node_a, node_d)  # A - D
    graph.add_edge(node_b, node_d)  # B - D
    graph.add_edge(node_c, node_d)  # C - D
    
    print(f"Graph: {graph}")
    print(f"Number of edges: {len(graph.get_edges())}")
    
    # Aplicar el algoritmo de fuerza bruta
    print("\n2. Applying Brute Force Coloring algorithm...")
    print("-" * 70)
    
    coloring_algorithm = BruteForceColoring(graph)
    result = coloring_algorithm.color_graph()
    
    print("Coloring found:")
    for node in sorted(graph.get_nodes(), key=lambda n: n.id):
        color = result[node]
        print(f"  Node {node.id}: Color {color}")
    
    # Mostrar número cromático
    print("\n3. Chromatic Number Analysis")
    print("-" * 70)
    chromatic_number = coloring_algorithm.get_chromaticity()
    print(f"Chromatic Number: {chromatic_number}")
    print(f"(This graph requires a minimum of {chromatic_number} colors)")
    
    # Validar la coloración
    print("\n4. Validation")
    print("-" * 70)
    is_valid = coloring_algorithm.is_valid_coloring(result)
    print(f"Is the coloring valid? {is_valid}")
    
    # Mostrar aristas para verificar
    print("\nVerifying that adjacent nodes have different colors:")
    for edge in graph.get_edges():
        node1, node2 = edge
        color1 = result[node1]
        color2 = result[node2]
        status = "✓" if color1 != color2 else "✗"
        print(f"  {status} {node1.id}(color {color1}) -- {node2.id}(color {color2})")
    
    print("\n" + "=" * 70)
    print("COMPLEXITY ANALYSIS")
    print("=" * 70)
    print("""
Time Complexity: O(k^n * E)
  - k: number of colors tried
  - n: number of nodes
  - E: number of edges (for validation)

For this example (4 nodes):
  - At k=1: 1 combination tested
  - At k=2: 2^4 = 16 combinations
  - At k=3: 3^4 = 81 combinations
  - Found valid at k=3 (81 combinations maximum)

This algorithm becomes impractical for graphs with more than 15-20 nodes.
    """)
    
    # Ejemplo adicional: grafo más simple (triángulo)
    print("\n" + "=" * 70)
    print("ADDITIONAL EXAMPLE: Triangle (K3)")
    print("=" * 70)
    
    graph2 = Graph()
    x = Node("X")
    y = Node("Y")
    z = Node("Z")
    
    graph2.add_node(x)
    graph2.add_node(y)
    graph2.add_node(z)
    
    graph2.add_edge(x, y)
    graph2.add_edge(y, z)
    graph2.add_edge(z, x)
    
    print("\nGraph: Triangle (all nodes connected to each other)")
    
    coloring_algo2 = BruteForceColoring(graph2)
    result2 = coloring_algo2.color_graph()
    
    print("Coloring:")
    for node in sorted(graph2.get_nodes(), key=lambda n: n.id):
        print(f"  {node.id}: Color {result2[node]}")
    
    chromatic_number2 = coloring_algo2.get_chromaticity()
    print(f"\nChromatic Number: {chromatic_number2} (triangle requires exactly 3 colors)")
