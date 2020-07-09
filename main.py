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


def read_from_file(from_file):
    raise Exception("Not implemented")


class DAGraph(object):
    def __init__(self, num_nodes, register_weight, from_file=None):
        self.num_nodes = num_nodes
        self.register_weight = register_weight

        if from_file is None:
            self.dag = generate_random_directed_weighted_graph(num_nodes)
        else:
            self.dag = read_from_file(from_file)

        self.w = self._gen_matrix_w()
        self.d = self._gen_matrix_d()

    def _gen_matrix_w(self):
        """
        Generates a W matrix.
        The quantity W(u,v) is the minimum number of registers on any path from vertex u to vertex v.
        :return: W matrix
        """
        n = max(max(self.dag.edges()))
        W = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

        for (u, v) in self.dag.edges():
            try:
                shortest_path = nx.dijkstra_path_length(self.dag, u, v)
                W[u - 1][v - 1] = shortest_path
            except nx.NetworkXNoPath:
                W[u - 1][v - 1] = -2

        return W

    def _gen_matrix_d(self):
        D = [[i * self.register_weight for i in self.w[j]] for j in range(len(self.w))]
        return D


if __name__ == '__main__':
    g = DAGraph(num_nodes=10, register_weight=2)
    print(g.w)
    print(g.d)
