import numpy as np
import networkx as nx


class GraphWrapper:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.delay = nx.get_node_attributes(graph, "delay")
        self.W_matrix, self.D_matrix = None, None

    def fill_WD(self):
        self.W_matrix, self.D_matrix = self._calculate_WD()

    def _calculate_WD(self) -> (np.array, np.array):
        graph = nx.DiGraph()
        W = np.zeros(self._get_matrices_shapes(), dtype=np.int)
        D = np.zeros(self._get_matrices_shapes())

        path_max_len = dict(nx.floyd_warshall(graph))

        for u in graph.nodes:
            for v in graph.nodes:
                cw = path_max_len[u][v]
                W[int(u), int(v)] = cw.x
                D[int(u), int(v)] = self.delay[v] - cw.y

        return W, D

    def _get_matrices_shapes(self):
        num_nodes = self.graph.number_of_nodes()
        return np.shape(num_nodes, num_nodes)