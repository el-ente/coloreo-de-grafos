"""
Graph data structures for graph coloring algorithms.

This module provides the fundamental classes for representing
graphs used in educational examples of graph coloring.
"""

from typing import Dict, List, Set, Optional, Any


class Node:
    """
    Represents a vertex in a graph.
    
    Attributes:
        id: Unique identifier for the node
        data: Optional data associated with the node
    
    A node encapsulates vertex information but does not store
    information about its neighbors - that responsibility belongs
    to the Graph class.
    """
    
    def __init__(self, node_id: str, data: Optional[Any] = None) -> None:
        """
        Initialize a Node.
        
        Args:
            node_id: Unique identifier for this node
            data: Optional data to store in the node (default: None)
        """
        self.id = node_id
        self.data = data
    
    def __repr__(self) -> str:
        """Return a readable representation of the node."""
        if self.data is not None:
            return f"Node({self.id}, data={self.data})"
        return f"Node({self.id})"
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on node id."""
        if isinstance(other, Node):
            return self.id == other.id
        return False
    
    def __hash__(self) -> int:
        """Make nodes hashable so they can be used in sets and dicts."""
        return hash(self.id)


class Graph:
    """
    Represents an undirected graph using an adjacency list.
    
    The graph manages nodes and edges, providing methods to:
    - Add nodes and edges
    - Query graph structure (neighbors, degrees, edges)
    - Verify connectivity between nodes
    
    Attributes:
        adjacency_list: Dictionary mapping nodes to their neighbors
        nodes: Set of all nodes in the graph
    """
    
    def __init__(self) -> None:
        """Initialize an empty graph."""
        # Diccionario de adyacencia: cada nodo mapea a su lista de vecinos
        self.adjacency_list: Dict[Node, List[Node]] = {}
        # Conjunto de nodos para acceso rápido
        self.nodes: Set[Node] = set()
    
    def add_node(self, node: Node) -> None:
        """
        Add a node to the graph.
        
        Args:
            node: Node object to add
            
        Raises:
            ValueError: If node is None or already exists
        """
        if node is None:
            raise ValueError("Cannot add None as a node")
        
        if node in self.nodes:
            raise ValueError(f"Node {node} already exists in the graph")
        
        # Inicializamos la lista de adyacencia para este nodo
        self.adjacency_list[node] = []
        self.nodes.add(node)
    
    def add_edge(self, node1: Node, node2: Node) -> None:
        """Connect two nodes with an undirected edge."""
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} not in graph")
        
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} not in graph")
        
        if node1 == node2:
            raise ValueError("Self-loops are not allowed")
        
        # Directamente agregar si no existe
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
            self.adjacency_list[node2].append(node1)
    
    def get_neighbors(self, node: Node) -> List[Node]:
        """
        Get all neighbors of a given node.
        
        Args:
            node: The node to query
            
        Returns:
            List of neighbor nodes
            
        Raises:
            ValueError: If node doesn't exist in the graph
        """
        if node not in self.nodes:
            raise ValueError(f"Node {node} not in graph")
        
        return self.adjacency_list[node].copy()
    
    def get_nodes(self) -> Set[Node]:
        """
        Get all nodes in the graph.
        
        Returns:
            Set of all nodes
        """
        return self.nodes.copy()
    
    def get_edges(self) -> List[tuple[Node, Node]]:
        """
        Get all edges in the graph.
        
        Returns:
            List of tuples representing edges (node1, node2)
            Each edge appears only once (no duplicates for undirected graphs)
        """
        edges = []
        # Para evitar duplicados en grafos no dirigidos, solo contamos
        # las aristas donde el primer nodo tiene ID menor
        for node in sorted(self.nodes, key=lambda n: str(n.id)):
            for neighbor in self.adjacency_list[node]:
                if str(node.id) < str(neighbor.id):
                    edges.append((node, neighbor))
        
        return edges
    
    def get_degree(self, node: Node) -> int:
        """
        Get the degree (number of neighbors) of a node.
        
        Args:
            node: The node to query
            
        Returns:
            Number of neighbors connected to the node
            
        Raises:
            ValueError: If node doesn't exist in the graph
        """
        if node not in self.nodes:
            raise ValueError(f"Node {node} not in graph")
        
        return len(self.adjacency_list[node])
    
    def has_edge(self, node1: Node, node2: Node) -> bool:
        """
        Check if there is an edge between two nodes.
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            True if edge exists, False otherwise
            
        Raises:
            ValueError: If either node doesn't exist
        """
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} not in graph")
        
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} not in graph")
        
        return node2 in self.adjacency_list[node1]
    
    def get_max_degree(self) -> int:
        """Get the maximum degree in the graph."""
        if not self.nodes:
            return 0
        return max(self.get_degree(node) for node in self.nodes)
    
    def __repr__(self) -> str:
        """Return a readable representation of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.get_edges())
        return f"Graph(nodes={num_nodes}, edges={num_edges})"
