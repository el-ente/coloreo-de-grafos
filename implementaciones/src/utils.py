import time
from functools import wraps
from typing import Callable, Tuple, Any, TypeVar
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
