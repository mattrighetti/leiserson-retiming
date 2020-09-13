import networkx as nx
import numpy as np
from algorithms.wd import wd
from algorithms.bellman_ford import binary_search

__all__ = ['opt1']


def opt1(graph: nx.DiGraph) -> (float, dict):
    """
    Applies OPT1 algorithm to input graph and returns a minimum feasible clock and the retiming values to achieve it

    :param graph: A directed graph
    :return: Minimum feasible clock and the retiming values to achieve it
    """

    # 1. Calculate WD
    W, D = wd(graph)

    # 2. Sort the elements in the range of D
    sorted_D = np.unique(D)

    # 3. Binary search minimum clock period in D(u, v) values using Bellman-Ford algorithm
    #     to check if Theorem 7 can be satisfied
    min_clock_period, retiming = binary_search(graph, sorted_D, W, D)

    # 4. For the minimum found before, use values of r(u) found by Bellman-Ford as the optimal retiming
    return min_clock_period, retiming