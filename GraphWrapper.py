import numpy as np
import networkx as nx

from utils import Weight
from utils.functions import cp_delta, get_matrices_shapes


class GraphWrapper:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.delay = nx.get_node_attributes(graph, "delay")
        self.W_matrix, self.D_matrix = None, None

    def fill_WD(self):
        self.W_matrix, self.D_matrix = self._calculate_WD()



    def calc_feas(self, var):
        r_list = []
        graph_r = self.graph.copy()

        for i in range(len(self.graph.nodes) - 1):
            r = {}
            delta = cp_delta(graph_r)

            for vertex in delta.keys():
                if delta[vertex] > var:
                    r[vertex] = r.get(vertex, 0) + 1

            graph_r = get_retimed_graph(graph_r, r)
            r_list.append(r)

        r_final = merge_r_list(r_list)
        delta, cp = cp_