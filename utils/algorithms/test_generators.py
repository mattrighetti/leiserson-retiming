import networkx as nx
from random import randint
from utils.algorithms.common import remove_cycles

__all__ = ['generate_single_register_graph']


def generate_single_register_graph(num_nodes=10, p=0.25):
    circle_graph = nx.path_graph(num_nodes, create_using=nx.DiGraph)

    random_graph = nx.binomial_graph(n=num_nodes, p=p, seed=27, directed=True)

    graph = nx.compose(circle_graph, random_graph)

    for edge in graph.edges:
        graph.edges[edge]["weight"] = 0.0

    for node in graph.nodes:
        graph.nodes[node]["delay"] = randint(1, 10)

    graph.add_edge(num_nodes - 1, 0, weight=1.0)
    graph = remove_cycles(graph)
    return graph