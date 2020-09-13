import networkx as nx

__all__ = ['cp',
           'delta_cp',
           'all_delta_cp']


def cp(graph: nx.DiGraph) -> float:
    """
    Returns the minimum clock period of a directed graph.

    :param graph: A directed graph
    :return: Minimum clock period of graph
    """

    delta_vertices = all_delta_cp(graph)
    return max(delta_vertices.values())


def delta_cp(graph: nx.DiGraph) -> dict:
    """
    Returns a dictionary that contains delta values needed for the CP algorithm.
    The dictionary will only contain delta values for nodes that are on edges that have
    s weight of 0.

    :param graph: A directed graph
    :return: Dictionary of delta values of nodes that have edges of weight 0
    """
    zero_edges_subgraph = nx.DiGraph()

    zero_edges = [edge for edge in graph.edges if graph.edges[edge]['weight'] == 0]
    zero_edges_subgraph.add_edges_from(zero_edges)
    zero_edges_subgraph_ordered = nx.topological_sort(zero_edges_subgraph)

    delta_vertices = {}

    for v in zero_edges_subgraph_ordered:
        max_incoming_u_delta = [delta_vertices.get(u, 0) for (u, _) in zero_edges_subgraph.in_edges(v)]
        delta_vertices[v] = max(max_incoming_u_delta, default=0) + graph.nodes[v]['delay']

    return delta_vertices


def all_delta_cp(graph: nx.DiGraph) -> dict:
    """
    Returns a dictionary that contains delta values needed for the CP algorithm.
    The dictionary will contain delta values for every node in graph passed as argument.

    :param graph: A directed graph
    :return: Dictionary of delta values of every node in graph
    """
    zero_edges_subgraph = nx.DiGraph()

    zero_edges = [edge for edge in graph.edges if graph.edges[edge]['weight'] == 0]
    zero_edges_subgraph.add_edges_from(zero_edges)
    zero_edges_subgraph_ordered = nx.topological_sort(zero_edges_subgraph)

    delta_vertices = {}

    for v in zero_edges_subgraph_ordered:
        max_incoming_u_delta = [delta_vertices.get(u, 0) for (u, _) in zero_edges_subgraph.in_edges(v)]
        delta_vertices[v] = max(max_incoming_u_delta, default=0) + graph.nodes[v]['delay']

    for non_zero_node in graph.nodes:
        if non_zero_node not in zero_edges_subgraph.nodes:
            delta_vertices[non_zero_node] = graph.nodes[non_zero_node]['delay']

    return delta_vertices