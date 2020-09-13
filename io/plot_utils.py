from os import path
import networkx as nx

__all__ = ['save_graph_to_file',
           'read_graph_from_file']


def save_graph_to_file(graph: nx.DiGraph, file_path: str) -> None:
    with open(file_path, 'w+') as file:
        string_representation = nx.nx_pydot.to_pydot(graph)
        file.write(string_representation)


def read_graph_from_file(file_path: str) -> nx.DiGraph:
    if not path.exists(file_path):
        raise FileNotFoundError

    with open(file_path, 'r') as file:
        graph = nx.nx_pydot.from_pydot(file.read())

    return graph