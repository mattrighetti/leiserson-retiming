import networkx as nx
import numpy as np
from utils import Weight


def get_matrices_shapes(graph, np_matrix):
    num_nodes = graph.number_of_nodes()
    return np_matrix.shape(num_nodes, num_nodes)


def cp_min_clock(graph) -> float:
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


def calculate_WD(self) -> (np.array, np.array):
    graph = nx.DiGraph()
    W = np.zeros(get_matrices_shapes(self.graph, np), dtype=np.int)
    D = np.zeros(get_matrices_shapes(self.graph, np))

    graph.add_weighted_edges_from(
        [(u, v, Weight(self.graph.edges[u, v]["weight"], -self.delay[v])) for (u, v) in self.graph.edges]
    )

    path_max_len = dict(nx.floyd_warshall(graph))

    for u in graph.nodes:
        for v in graph.nodes:
            cw = path_max_len[u][v]
            W[int(u), int(v)] = cw.x
            D[int(u), int(v)] = self.delay[v] - cw.y

    return W, D
