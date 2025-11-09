from abc import ABC, abstractmethod
import time
from typing import Dict
from graph import Graph, Node

class GraphColoringAlgorithm(ABC):
    """
    Interface for graph coloring algorithms.

    Defines the standard methods that any graph coloring algorithm
    should implement.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize the algorithm with a graph.

        Args:
            graph: A Graph object to be colored.
        """
        self.graph: Graph = graph
        self.coloring: Dict[Node, int] = {}
        self.execution_time: float = 0.0

    def color_graph(self) -> Dict[Node, int]:
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
    def _color_graph_impl(self) -> None:
        """
        Internal implementation of the coloring algorithm.
        Subclasses must implement this method.
        """
        pass

    def is_valid_coloring(self, coloring: Dict[Node, int] = None) -> bool:
        """
        Check if a given coloring is valid for the graph.

        Args:
            coloring: A dictionary mapping nodes to colors.

        Returns:
            True if the coloring is valid, False otherwise.
        """
        actual_coloring = coloring if coloring is not None else self.coloring

        for edge in self.graph.get_edges():
            if actual_coloring.get(edge[0]) == actual_coloring.get(edge[1]):
                return False
        return True

    def get_chromaticity(self) -> int:
        """
        Get the chromatic number (minimum number of colors needed).

        Returns:
            An integer representing the chromatic number.
        """
        if not self.coloring:
            return 0
        return len(set(self.coloring.values()))

    def get_execution_time(self) -> float:
        """
        Get the execution time of the coloring algorithm.

        Returns:
            A float representing the execution time in seconds.
        """
        return self.execution_time