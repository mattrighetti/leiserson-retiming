import numpy as np
import networkx as nx
from algorithms.wd import wd
from algorithms.feas import binary_search

__all__ = ['opt2']


def opt2(graph: nx.DiGraph):
    # 1. Calculate WD
    W, D = wd(graph)

    # 2. Sort the elements in the range of D
    sorted_D = np.unique(D)

    # 3. Binary search minimum clock period in D(u, v) values using FEAS algorithm
    #     to check if Theorem 7 can be satisfied
    min_clock_period, retiming = binary_search(graph, sorted_D)

    # 4. For the minimum found before, use values of r(u) found by FEAS as the optimal retiming
    return min_clock_period, retiming