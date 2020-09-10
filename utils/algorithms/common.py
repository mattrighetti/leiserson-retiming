import networkx as nx

__all__ = ['get_subgraph_with_weight']


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