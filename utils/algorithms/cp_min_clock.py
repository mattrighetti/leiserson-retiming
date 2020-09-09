import networkx as nx

__all__ = ['cp_min_clock']


def cp_min_clock(graph: nx.DiGraph) -> float:
    zero_edges_subgraph = nx.DiGraph()

    zero_edges = []
    non_zero_edges = []
    for edge in graph.edges:
        if edge["weight"] == 0:
            zero_edges.append(edge)
        else:
            non_zero_edges.append(edge)

    zero_edges_subgraph.add_edges_from(zero_edges)
    zero_edges_subgraph_ordered = nx.topological_sort(zero_edges_subgraph)

    delta_vertices = {}
    # Iterate over ordered v
    for v in zero_edges_subgraph_ordered:
        # Find max delta(u)
        max_incoming_u_delta = 0

        for (u, v_inner) in zero_edges_subgraph.in_edges(v):
            if delta_vertices[u] > max_incoming_u_delta:
                max_incoming_u_delta = delta_vertices[u]

        delta_vertices[v] = max_incoming_u_delta + v["delay"]

    return max(delta_vertices.values())