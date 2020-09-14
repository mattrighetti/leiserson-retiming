import numpy as np
import networkx as nx
from algorithms.common import apply_retiming
from algorithms.clock_period import delta_cp, cp
from algorithms.binary_search.binary_search import binary_search

__all__ = ['feas', 'bellman_ford']


@binary_search
def feas(graph: nx.DiGraph, clock_period) -> dict:
    """
    Applies FEAS algorithm to input graph with a specified clock and returns a retiming dictionary to achieve it

    :param graph:
    :param clock_period:
    :return:
    """
    copy_graph = None
    r_vertices = dict([(v, 0.0) for v in graph.nodes])

    num_vertices = graph.number_of_nodes()

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


@binary_search
def bellman_ford(graph: nx.DiGraph, clock_period, W: np.array, D: np.array) -> dict:
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
    :return: An edited directed graph that for each node with D(u, v) > c will
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
