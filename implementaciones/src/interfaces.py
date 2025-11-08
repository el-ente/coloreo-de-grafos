from abc import ABC, abstractmethod

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

    @abstractmethod
    def color_graph(self):
        """
        Perform the graph coloring and return the result.

        Returns:
            A dictionary mapping nodes to their assigned colors.
        """
        pass

    @abstractmethod
    def is_valid_coloring(self, coloring):
        """
        Check if a given coloring is valid for the graph.

        Args:
            coloring: A dictionary mapping nodes to colors.

        Returns:
            True if the coloring is valid, False otherwise.
        """
        pass

    @abstractmethod
    def get_chromaticity(self):
        """
        Get the chromatic number (minimum number of colors needed).

        Returns:
            An integer representing the chromatic number.
        """
        pass

    @abstractmethod
    def get_execution_time(self):
        """
        Get the execution time of the coloring algorithm.

        Returns:
            A float representing the execution time in seconds.
        """
        pass