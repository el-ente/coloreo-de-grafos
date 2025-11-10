import time
from functools import wraps
from typing import Callable, Tuple, TypeVar
from graph import Graph, Node

T = TypeVar('T')


def time_measured(func: Callable[..., T]) -> Callable[..., Tuple[T, float]]:
    """
    Decorator that measures the execution time of a function.
    
    Args:
        func: Function to be decorated
        
    Returns:
        A function that returns a tuple (result, time_ns) where:
        - result: The value returned by the original function
        - time_ns: Execution time in nanoseconds
        
    Example:
        @time_measured
        def my_function(x, y):
            return x + y
            
        result, elapsed_ns = my_function(5, 3)
        print(f"Result: {result}, Time: {elapsed_ns} ns")
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[T, float]:
        start_time = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        elapsed_ns = end_time - start_time
        return result, elapsed_ns
    
    return wrapper

def create_cycle_graph(n):
    """Create a cycle graph with n nodes."""
    graph = Graph()
    nodes = [Node(f"v{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    for i in range(n):
        graph.add_edge(nodes[i], nodes[(i + 1) % n])
    
    return graph, nodes


def create_complete_graph(n):
    """Create a complete graph (clique) with n nodes."""
    graph = Graph()
    nodes = [Node(f"k{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(nodes[i], nodes[j])
    
    return graph, nodes


def create_star_graph(n):
    """Create a star graph with 1 center and n-1 leaves."""
    graph = Graph()
    center = Node("center")
    graph.add_node(center)
    
    leaves = [Node(f"leaf{i}") for i in range(n - 1)]
    for leaf in leaves:
        graph.add_node(leaf)
        graph.add_edge(center, leaf)
    
    return graph, [center] + leaves


def create_bipartite_graph(n1, n2):
    """Create a complete bipartite graph K(n1, n2)."""
    graph = Graph()
    
    set_a = [Node(f"a{i}") for i in range(n1)]
    set_b = [Node(f"b{i}") for i in range(n2)]
    
    for node in set_a + set_b:
        graph.add_node(node)
    
    for a in set_a:
        for b in set_b:
            graph.add_edge(a, b)
    
    return graph, set_a + set_b

def create_path_graph(n):
    """Create a path graph with n nodes (linear chain)."""
    graph = Graph()
    nodes = [Node(f"p{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    for i in range(n - 1):
        graph.add_edge(nodes[i], nodes[i + 1])
    
    return graph, nodes


def create_wheel_graph(n):
    """Create a wheel graph with n+1 nodes (1 center + n cycle nodes)."""
    graph = Graph()
    center = Node("hub")
    graph.add_node(center)
    
    rim_nodes = [Node(f"rim{i}") for i in range(n)]
    for node in rim_nodes:
        graph.add_node(node)
        graph.add_edge(center, node)
    
    # Connect rim nodes in a cycle
    for i in range(n):
        graph.add_edge(rim_nodes[i], rim_nodes[(i + 1) % n])
    
    return graph, [center] + rim_nodes


def create_petersen_graph():
    """Create the Petersen graph (famous graph with chromatic number 3)."""
    graph = Graph()
    
    # Outer pentagon
    outer = [Node(f"o{i}") for i in range(5)]
    # Inner pentagram
    inner = [Node(f"i{i}") for i in range(5)]
    
    for node in outer + inner:
        graph.add_node(node)
    
    # Outer pentagon edges
    for i in range(5):
        graph.add_edge(outer[i], outer[(i + 1) % 5])
    
    # Inner pentagram edges (connect every 2nd vertex)
    for i in range(5):
        graph.add_edge(inner[i], inner[(i + 2) % 5])
    
    # Connect outer to inner
    for i in range(5):
        graph.add_edge(outer[i], inner[i])
    
    return graph, outer + inner


def create_grid_graph(rows, cols):
    """Create a grid graph with rows x cols nodes."""
    graph = Graph()
    nodes = [[Node(f"g{i}_{j}") for j in range(cols)] for i in range(rows)]
    
    for row in nodes:
        for node in row:
            graph.add_node(node)
    
    # Horizontal edges
    for i in range(rows):
        for j in range(cols - 1):
            graph.add_edge(nodes[i][j], nodes[i][j + 1])
    
    # Vertical edges
    for i in range(rows - 1):
        for j in range(cols):
            graph.add_edge(nodes[i][j], nodes[i + 1][j])
    
    return graph, [node for row in nodes for node in row]


def create_planar_graph(n):
    """Create a simple planar graph (triangulation)."""
    graph = Graph()
    nodes = [Node(f"pl{i}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    # Create a simple planar structure (outer cycle + some internal edges)
    for i in range(n):
        graph.add_edge(nodes[i], nodes[(i + 1) % n])
    
    # Add some internal edges without violating planarity
    if n >= 4:
        for i in range(n - 2):
            graph.add_edge(nodes[0], nodes[i + 2])
    
    return graph, nodes

def create_tree_graph(height):
    """Create a complete binary tree with given height."""
    graph = Graph()
    nodes = []
    
    # Create nodes level by level
    num_nodes = 2 ** (height + 1) - 1
    for i in range(num_nodes):
        node = Node(f"t{i}")
        graph.add_node(node)
        nodes.append(node)
    
    # Connect parent to children
    for i in range(num_nodes // 2):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        if left_child < num_nodes:
            graph.add_edge(nodes[i], nodes[left_child])
        if right_child < num_nodes:
            graph.add_edge(nodes[i], nodes[right_child])
    
    return graph, nodes


def create_hypercube_graph(dimension):
    """Create a hypercube graph of given dimension (2^dimension nodes)."""
    graph = Graph()
    n = 2 ** dimension
    nodes = [Node(f"h{format(i, f'0{dimension}b')}") for i in range(n)]
    
    for node in nodes:
        graph.add_node(node)
    
    # Connect nodes that differ in exactly one bit
    for i in range(n):
        for j in range(i + 1, n):
            # Count differing bits
            xor = i ^ j
            if bin(xor).count('1') == 1:  # Differ in exactly one bit
                graph.add_edge(nodes[i], nodes[j])
    
    return graph, nodes


def create_prism_graph(n):
    """Create a prism graph (two n-cycles connected)."""
    graph = Graph()
    
    # First cycle
    cycle1 = [Node(f"c1_{i}") for i in range(n)]
    # Second cycle
    cycle2 = [Node(f"c2_{i}") for i in range(n)]
    
    for node in cycle1 + cycle2:
        graph.add_node(node)
    
    # First cycle edges
    for i in range(n):
        graph.add_edge(cycle1[i], cycle1[(i + 1) % n])
    
    # Second cycle edges
    for i in range(n):
        graph.add_edge(cycle2[i], cycle2[(i + 1) % n])
    
    # Connect corresponding nodes between cycles
    for i in range(n):
        graph.add_edge(cycle1[i], cycle2[i])
    
    return graph, cycle1 + cycle2


def create_kneser_graph(n, k):
    """Create Kneser graph KG(n,k) - nodes are k-subsets of {0,...,n-1}."""
    from itertools import combinations
    
    graph = Graph()
    
    # Generate all k-subsets
    subsets = list(combinations(range(n), k))
    nodes = [Node(f"ks{','.join(map(str, s))}") for s in subsets]
    
    for node in nodes:
        graph.add_node(node)
    
    # Connect disjoint subsets
    for i in range(len(subsets)):
        for j in range(i + 1, len(subsets)):
            if not set(subsets[i]) & set(subsets[j]):  # Disjoint sets
                graph.add_edge(nodes[i], nodes[j])
    
    return graph, nodes


def create_ladder_graph(n):
    """Create a ladder graph (two parallel paths connected by rungs)."""
    graph = Graph()
    
    # Two parallel paths
    path1 = [Node(f"l1_{i}") for i in range(n)]
    path2 = [Node(f"l2_{i}") for i in range(n)]
    
    for node in path1 + path2:
        graph.add_node(node)
    
    # Path edges
    for i in range(n - 1):
        graph.add_edge(path1[i], path1[i + 1])
        graph.add_edge(path2[i], path2[i + 1])
    
    # Rungs connecting paths
    for i in range(n):
        graph.add_edge(path1[i], path2[i])
    
    return graph, path1 + path2


def create_circular_ladder_graph(n):
    """Create a circular ladder (Prism graph, cycles instead of paths)."""
    # This is actually the same as prism_graph, but included for clarity
    return create_prism_graph(n)


def create_friendship_graph(n):
    """Create a friendship graph (n triangles sharing a common vertex)."""
    graph = Graph()
    
    # Central node
    center = Node("center")
    graph.add_node(center)
    
    # Create n triangles
    nodes = [center]
    for i in range(n):
        # Two nodes per triangle
        node1 = Node(f"f{i}_1")
        node2 = Node(f"f{i}_2")
        graph.add_node(node1)
        graph.add_node(node2)
        
        # Connect triangle
        graph.add_edge(center, node1)
        graph.add_edge(center, node2)
        graph.add_edge(node1, node2)
        
        nodes.extend([node1, node2])
    
    return graph, nodes


def create_crown_graph(n):
    """Create a crown graph (complete bipartite minus perfect matching)."""
    graph = Graph()
    
    set_a = [Node(f"crown_a{i}") for i in range(n)]
    set_b = [Node(f"crown_b{i}") for i in range(n)]
    
    for node in set_a + set_b:
        graph.add_node(node)
    
    # Complete bipartite
    for i in range(n):
        for j in range(n):
            if i != j:  # Minus perfect matching
                graph.add_edge(set_a[i], set_b[j])
    
    return graph, set_a + set_b


