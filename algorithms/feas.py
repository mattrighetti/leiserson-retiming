import networkx as nx
from algorithms.common import apply_retiming
from algorithms.clock_period import delta_cp, cp
from algorithms.binary_search import binary_search

__all__ = ['binary_search', 'feas']


@binary_search
def feas(graph: nx.DiGraph, clock_period) -> dict:
    """
    Applies FEAS algorithm to input graph with a specified clock and returns a retiming dictionary to achieve it

    :param graph:
    :param clock_period:
    :return:
    """
    copy_graph = graph.copy()
    r_vertices = dict([(v, 0.0) for v in copy_graph.nodes])

    num_vertices = copy_graph.number_of_nodes()

    # 2. Repeat the following |V| - 1 times
    for _ in range(num_vertices - 1):
        copy_graph = apply_retiming(graph, r_vertices)
        deltas = delta_cp(copy_graph)
        for (key, value) in deltas.items():
            if value > clock_period:
                r_vertices[key] = r_vertices[key] + 1

    if cp(copy_graph) > clock_period:
        valid = False
    else:
        valid = True

    return {'valid': valid, 'r': r_vertices, 'clock_period': clock_period}