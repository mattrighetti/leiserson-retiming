import networkx as nx

__all__ = ['apply_retiming',
           'get_subgraph_with_weight']


def apply_retiming(graph: nx.DiGraph, r) -> nx.DiGraph:
    retimed_graph = nx.DiGraph()

    retimed_graph.add_weighted_edges_from(
        [(u, v, graph.edges[u, v]['weight'] + r.get(v, 0) - r.get(u, 0)) for (u, v) in graph.edges]
    )

    return retimed_graph


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