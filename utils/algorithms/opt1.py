import networkx as nx
import numpy as np
from utils.algorithms.wd import wd

__all__ = ['opt1']


def opt1(graph: nx.DiGraph) -> int:
    # 1. Calculate WD
    W, D = wd(graph)

    # 2. Sort the elements in the range of D
    sorted_D = np.unique(D)

    # 3. Binary search minimum clock period in D(u, v) values using Bellman-Ford algorithm
    #     to check if Theorem 7 can be satisfied
    binary_search_minimum_clock_period(sorted_D)

    # 4. For the minimum found before, use values of r(u) found by Bellman-Ford as the optimal retiming

    return 0


def binary_search_minimum_clock_period(sorted_D):
    raise NotImplemented("binary_search_minimum_clock_period has not yet been implemented")