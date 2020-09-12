import networkx as nx
import numpy as np

__all__ = ['binary_search']


def binary_search(graph: nx.DiGraph, D_sorted, W, D):
    """
    Binary search feasible clock using Bellman-Ford algorithm

    source: http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20[相容模式].pdf

    :param graph:
    :param D_sorted:
    :param W: W matrix
    :param D: D matrix
    :return:
    """
    low = 0
    high = len(D_sorted) - 1

    tuple_ = (np.inf, None)

    while low <= high:
        mid = (high + low) // 2

        results = bf_algorithm_test(graph, W, D, D_sorted[mid])

        if results['valid']:
            tuple_ = (D_sorted[mid], results['r'])
            high = mid - 1
        else:
            low = mid + 1

    r_values = tuple_[1]
    r_values.pop('N+1')

    return tuple_[0], r_values


def bf_algorithm_test(graph: nx.DiGraph, W: np.array, D: np.array, clock_period):
    retiming_value = None
    constraint_graph = generate_constraint_graph(graph, W, D, clock_period)

    try:
        retiming_value, not_care = nx.algorithms.single_source_bellman_ford(constraint_graph, 'N+1')
        valid = True
    except nx.exception.NetworkXUnbounded:
        valid = False

    return {'valid': valid, 'r': retiming_value, 'clock_period': clock_period}


def generate_constraint_graph(graph: nx.DiGraph, W, D, clock_period) -> nx.DiGraph:
    """
    Generates a constraint graph to work with the Bellman-Ford algorithm

    source: https://www.oreilly.com/library/view/vlsi-digital-signal/9780471241867/sec-4.3.html

    :param graph: original graph
    :param D: D matrix
    :param W: W matrix
    :param clock_period: clock_period to test
    :return: constraint graph
    """
    # 1. For each node make an edge with opposite direction
    constraint_graph = graph.reverse(copy=True)
    # 2a. For each node with D(u, v) > c create an edge if it does not exist
    # 2b. Set w(e) = W(u, v) - 1
    constraint_graph = add_missing_edges(constraint_graph, D, W, clock_period)
    # 3. Connect each node to a N+1 node with w(e) = 0 and d(n+1) = 0
    constraint_graph = connect_zero_weight_node(constraint_graph)
    return constraint_graph


def connect_zero_weight_node(graph: nx.DiGraph) -> nx.DiGraph:
    original_nodes = np.array(graph.nodes)

    for n in original_nodes:
        graph.add_edge('N+1', n, weight=0)

    return graph


def add_missing_edges(graph: nx.DiGraph, D, W, clock_period) -> nx.DiGraph:
    n_vertices = len(D)

    for i in range(n_vertices):
        for j in range(n_vertices):
            if D[i, j] > clock_period:
                if (j, i) not in graph.edges:
                    graph.add_edge(j, i)
                graph.edges[j, i]['weight'] = W[i, j] - 1

    return graph