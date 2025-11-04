"""
Graph data structures for graph coloring algorithms.

This module provides the fundamental classes for representing
graphs used in educational examples of graph coloring.
"""


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
    
    def __init__(self, node_id, data=None):
        """
        Initialize a Node.
        
        Args:
            node_id: Unique identifier for this node
            data: Optional data to store in the node (default: None)
        """
        self.id = node_id
        self.data = data
    
    def __repr__(self):
        """Return a readable representation of the node."""
        if self.data is not None:
            return f"Node({self.id}, data={self.data})"
        return f"Node({self.id})"
    
    def __eq__(self, other):
        """Check equality based on node id."""
        if isinstance(other, Node):
            return self.id == other.id
        return False
    
    def __hash__(self):
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
    
    def __init__(self):
        """Initialize an empty graph."""
        # Diccionario de adyacencia: cada nodo mapea a su lista de vecinos
        self.adjacency_list = {}
        # Conjunto de nodos para acceso rápido
        self.nodes = set()
    
    def add_node(self, node):
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
    
    def add_edge(self, node1, node2):
        """
        Connect two nodes with an undirected edge.
        
        Args:
            node1: First node
            node2: Second node
            
        Raises:
            ValueError: If either node doesn't exist or trying to create self-loop
        """
        if node1 not in self.nodes:
            raise ValueError(f"Node {node1} not in graph")
        
        if node2 not in self.nodes:
            raise ValueError(f"Node {node2} not in graph")
        
        if node1 == node2:
            raise ValueError("Self-loops are not allowed")
        
        # Evitar aristas duplicadas
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)
    
    def get_neighbors(self, node):
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
    
    def get_nodes(self):
        """
        Get all nodes in the graph.
        
        Returns:
            Set of all nodes
        """
        return self.nodes.copy()
    
    def get_edges(self):
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
    
    def get_degree(self, node):
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
    
    def has_edge(self, node1, node2):
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
    
    def __repr__(self):
        """Return a readable representation of the graph."""
        num_nodes = len(self.nodes)
        num_edges = len(self.get_edges())
        return f"Graph(nodes={num_nodes}, edges={num_edges})"


# ============================================================================
# Ejemplo de uso / Usage example
# ============================================================================

if __name__ == "__main__":
    # Crear un grafo simple
    graph = Graph()
    
    # Crear nodos
    print("=" * 50)
    print("Creando nodos...")
    print("=" * 50)
    
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    
    print(f"{node_a}")
    print(f"{node_b}")
    print(f"{node_c}")
    print(f"{node_d}")
    
    # Añadir nodos al grafo
    print("\n" + "=" * 50)
    print("Añadiendo nodos al grafo...")
    print("=" * 50)
    
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)
    
    print(f"{graph}")
    
    # Añadir aristas
    print("\n" + "=" * 50)
    print("Conectando nodos con aristas...")
    print("=" * 50)
    
    graph.add_edge(node_a, node_b)
    graph.add_edge(node_a, node_c)
    graph.add_edge(node_b, node_c)
    graph.add_edge(node_c, node_d)
    
    print(f"Grafo actualizado: {graph}")
    
    # Consultar propiedades del grafo
    print("\n" + "=" * 50)
    print("Consultando propiedades del grafo...")
    print("=" * 50)
    
    print(f"\nGrado de cada nodo:")
    for node in graph.get_nodes():
        degree = graph.get_degree(node)
        print(f"  Grado de {node.id}: {degree}")
    
    print(f"\nVecinos de {node_a.id}: {[n.id for n in graph.get_neighbors(node_a)]}")
    print(f"Vecinos de {node_c.id}: {[n.id for n in graph.get_neighbors(node_c)]}")
    
    print(f"\nAristas del grafo:")
    for edge in graph.get_edges():
        print(f"  {edge[0].id} -- {edge[1].id}")
    
    print(f"\n¿Existe arista entre {node_a.id} y {node_b.id}? {graph.has_edge(node_a, node_b)}")
    print(f"¿Existe arista entre {node_a.id} y {node_d.id}? {graph.has_edge(node_a, node_d)}")
