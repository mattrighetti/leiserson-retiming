import networkx as nx
import numpy as np
from algorithms.binary_search import binary_search

__all__ = ['binary_search', 'bf_algorithm_test']


# def binary_search(graph: nx.DiGraph, D_sorted, W, D) -> tuple:
#     """
#     Binary search feasible clock using Bellman-Ford algorithm
#
#     source: http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20[相容模式].pdf
#
#     :param graph:
#     :param D_sorted:
#     :param W: W matrix
#     :param D: D matrix
#     :return: Tuple that contains the minimum feasible clock period and the retiming values to achieve that
#     """
#     low = 0
#     high = len(D_sorted) - 1
#
#     tuple_ = (np.inf, None)
#
#     while low <= high:
#         mid = (high + low) // 2
#
#         results = bf_algorithm_test(graph, D_sorted[mid], W, D)
#
#         if results['valid']:
#             tuple_ = (D_sorted[mid], results['r'])
#             high = mid - 1
#         else:
#             low = mid + 1
#
#     r_values = tuple_[1]
#     r_values.pop('N+1')
#
#     return tuple_[0], r_values


@binary_search
def bf_algorithm_test(graph: nx.DiGraph, clock_period, W: np.array, D: np.array) -> dict:
    """

    :param graph: A directed graph
    :param W: W matrix
    :param D: D matrix
    :param clock_period: Clock period to test
    :return: A dictionary containing whether or not a retiming for a certain clock is valid, the retiming value and
        its clock period
    """
    retiming_value = None
    constraint_graph = generate_constraint_graph(graph, W, D, clock_period)

    try:
        retiming_value, _ = nx.algorithms.single_source_bellman_ford(constraint_graph, 'N+1')
        valid = True
        retiming_value.pop('N+1')
    except nx.exception.NetworkXUnbounded:
        valid = False

    return {'valid': valid, 'r': retiming_value, 'clock_period': clock_period}


def generate_constraint_graph(graph: nx.DiGraph, W, D, clock_period) -> nx.DiGraph:
    """
    Generates a constraint graph to work with the Bellman-Ford algorithm

    source: https://www.oreilly.com/library/view/vlsi-digital-signal/9780471241867/sec-4.3.html

    :param graph: A directed graph
    :param D: D matrix
    :param W: W matrix
    :param clock_period: Clock_period to test
    :return: Constraint graph on which Bellman-Ford algorithm can operate on
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
    """
    Returns a graph containing the same edges and nodes as the one passed as input, plus a node called N+1
    needed for the Bellman-Ford algorithm. Node N+1 has to be connected with edges to every other node in the graph
    and those edges must have weight of zero.

    :param graph: A directed graph
    :return: A directed graph containing every node and edge as the original one, plus a node N+1 connected
        to every other node with edges of weight zero
    """

    copy_graph = graph.copy()
    copy_graph.add_weighted_edges_from(
        [('N+1', n, 0.0) for n in copy_graph.nodes]
    )

    return copy_graph


def add_missing_edges(graph: nx.DiGraph, D, W, clock_period) -> nx.DiGraph:
    """
    Returns a graph that for each node with D(u, v) > c will have an edge, and will add a weight value of
    w(e) = W[u, v] - 1 to that edge

    :param graph: A directed graph
    :param D: D matrix
    :param W: W matrix
    :param clock_period: Clock period to test
    :return: An edited directed graph that will have that for each node with D(u, v) > c will
        have an edge, and will add a weight value of
        w(e) = W[u, v] - 1 to that edge
    """
    n_vertices = len(D)

    for i in range(n_vertices):
        for j in range(n_vertices):
            if D[i, j] > clock_period:
                if (j, i) not in graph.edges:
                    graph.add_edge(j, i)
                graph.edges[j, i]['weight'] = W[i, j] - 1

    return graph