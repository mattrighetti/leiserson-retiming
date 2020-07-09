import networkx as nx
import random


def generate_random_directed_weighted_graph(num_nodes=10):
    """
    Generates a random directional weighted acyclic graph.
    Weight in this case is associated to the numbers of registers on a single edge.
    :param num_nodes: Number of nodes in the graph
    :return: directional acyclic weighted graph
    """
    G = nx.gnp_random_graph(num_nodes, 0.5, directed=True)
    DAG = nx.DiGraph([(u, v, {'num_registers': random.randint(0, 5)}) for (u, v) in G.edges() if u < v])
    return DAG


def _gen_matrix_w(graph):
    """
    Generates a W matrix.
    The quantity W(u,v) is the minimum number of registers on any path from vertex u to vertex v.
    :param graph: directional acyclic graph
    :return: W matrix
    """
    n = max(max(graph.edges()))
    W = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for (u, v) in graph.edges():
        try:
            shortest_path = nx.dijkstra_path_length(graph, u, v)
            W[u - 1][v - 1] = shortest_path
        except nx.NetworkXNoPath:
            W[u - 1][v - 1] = -2

    return W


def _gen_matrix_d(W_matrix, register_weight):
    D = [[i * register_weight for i in W_matrix[j]] for j in range(len(W_matrix))]
    return D


def gen_wd_matrices(graph, register_weight):
    W_matrix = _gen_matrix_w(graph)
    D_matrix = _gen_matrix_d(W_matrix, register_weight)
    return W_matrix, D_matrix


class DAGraph(object):
    def __init__(self, num_nodes, register_weight):
        self.num_nodes = num_nodes
        self.register_weight = register_weight

        self.dag = generate_random_directed_weighted_graph(num_nodes)
        self.w, self.d = gen_wd_matrices(self.dag, self.register_weight)


if __name__ == '__main__':
    g = DAGraph(num_nodes=10, register_weight=2)
    print(g.w)
    print(g.d)
