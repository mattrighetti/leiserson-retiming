import networkx as nx

__all__ = ['apply_retiming',
           'get_subgraph_with_weight',
           'check_if_legal',
           'remove_cycles']


def apply_retiming(graph: nx.DiGraph, r) -> nx.DiGraph:
    retimed_graph = nx.DiGraph()

    retimed_graph.add_weighted_edges_from(
        [(u, v, graph.edges[u, v]['weight'] + r[v] - r[u]) for (u, v) in graph.edges]
    )

    retimed_graph.add_nodes_from(
        [(node, {'delay': graph.nodes[node]['delay']}) for node in graph.nodes]
    )

    return retimed_graph


def check_if_legal(graph: nx.DiGraph) -> bool:
    for edge in graph.edges:
        if graph.edges[edge]['weight'] < 0:
            return False

    return True


def remove_cycles(graph):
    max_node = max(graph.nodes)
    min_node = min(graph.nodes)

    try:
        graph.remove_edge(min_node, max_node)
    except nx.exception.NetworkXError:
        print("")

    graph.remove_edges_from([(u, v) for (u, v) in graph.edges if u > v and (u, v) != (max_node, min_node)])

    return graph


def get_subgraph_with_weight(graph: nx.DiGraph, weight, copy=True) -> nx.DiGraph:
    weight_mask = graph.edges['weight'] == weight

    if copy:
        copy_graph = nx.DiGraph()
        copy_graph.add_weighted_edges_from(
            [(u, v, 0.0) for (u, v) in graph.edges[weight_mask]]
        )
        return copy_graph
    else:
        raise NotImplemented