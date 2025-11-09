from abc import ABC, abstractmethod
import time

class GraphColoringAlgorithm(ABC):
    """
    Interface for graph coloring algorithms.

    Defines the standard methods that any graph coloring algorithm
    should implement.
    """

    def __init__(self, graph):
        """
        Initialize the algorithm with a graph.

        Args:
            graph: A Graph object to be colored.
        """
        self.graph = graph
        self.coloring = {}
        self.execution_time = 0.0

    def color_graph(self):
        """
        Perform the graph coloring and return the result.
        Measures execution time automatically.

        Returns:
            A dictionary mapping nodes to their assigned colors.
        """
        start_time = time.time()
        self._color_graph_impl()
        self.execution_time = time.time() - start_time
        return self.coloring

    @abstractmethod
    def _color_graph_impl(self):
        """
        Internal implementation of the coloring algorithm.
        Subclasses must implement this method.
        """
        pass

    def is_valid_coloring(self, coloring):
        """
        Check if a given coloring is valid for the graph.

        Args:
            coloring: A dictionary mapping nodes to colors.

        Returns:
            True if the coloring is valid, False otherwise.
        """
        for edge in self.graph.get_edges():
            if coloring.get(edge[0]) == coloring.get(edge[1]):
                return False
        return True

    def get_chromaticity(self):
        """
        Get the chromatic number (minimum number of colors needed).

        Returns:
            An integer representing the chromatic number.
        """
        if not self.coloring:
            return 0
        return len(set(self.coloring.values()))

    def get_execution_time(self):
        """
        Get the execution time of the coloring algorithm.

        Returns:
            A float representing the execution time in seconds.
        """
        return self.execution_time