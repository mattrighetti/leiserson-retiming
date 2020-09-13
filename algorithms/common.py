import networkx as nx

__all__ = ['apply_retiming',
           'get_subgraph_with_weight',
           'check_if_legal',
           'remove_backward_cycles']


def apply_retiming(graph: nx.DiGraph, r) -> nx.DiGraph:
    """
    Applies retiming passed as argument to input graph.

    :param graph: A directed graph
    :param r: A retiming dictionary
    :return: Retimed graph
    """

    retimed_graph = nx.DiGraph()

    retimed_graph.add_weighted_edges_from(
        [(u, v, graph.edges[u, v]['weight'] + r[v] - r[u]) for (u, v) in graph.edges]
    )

    retimed_graph.add_nodes_from(
        [(node, {'delay': graph.nodes[node]['delay']}) for node in graph.nodes]
    )

    return retimed_graph


def check_if_legal(graph: nx.DiGraph) -> bool:
    """
    Checks whether or not the graph is legal or not.

    :param graph: A directed graph
    :return: Boolean that tells if the graph is legal
    """

    for edge in graph.edges:
        if graph.edges[edge]['weight'] < 0:
            return False

    return True


def remove_backward_cycles(graph):
    """
    Removes every backward loop in directed graph.

    i.e. In a graph [(0, 1), (1, 2), (2, 3), (3, 0), (2, 1)] the algorithm will remove (2, 1) and (3, 0)

    :param graph: A directed graph
    :return: A directed graph without backward loops
    """

    max_node = max(graph.nodes)
    min_node = min(graph.nodes)

    try:
        graph.remove_edge(min_node, max_node)
    except nx.exception.NetworkXError:
        pass

    graph.remove_edges_from(
        [(u, v) for (u, v) in graph.edges if u > v and (u, v) != (max_node, min_node)]
    )

    return graph


def get_subgraph_with_weight(graph: nx.DiGraph, weight: float) -> nx.DiGraph:
    """
    Returns a graph that have as edges edges of the graph passed as input with a specified weight passed as input

    :param graph: A directed graph
    :param weight: Weight that edges have to have to be included in the returned graph
    :return: A directed graph created with edges taken from input graph and have the specified weight
    """

    copy_graph = nx.DiGraph()
    copy_graph.add_weighted_edges_from(
        [(edge, w) for edge, w in nx.get_edge_attributes(graph, 'weight').items() if w == weight]
    )

    return copy_graph