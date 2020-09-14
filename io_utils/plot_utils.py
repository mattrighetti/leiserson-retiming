from os import path
import networkx as nx

__all__ = ['save_graph_to_file',
           'read_graph_from_file']


def save_graph_to_file(graph: nx.DiGraph, file_path: str) -> None:
    """
    Saves graph to a file named `file_path`

    :param graph: Graph to be saved
    :param file_path: File path where you would like to save the graph
    :return: None
    """
    with open(file_path, 'w') as file:
        nx.nx_pydot.write_dot(graph, file)


def read_graph_from_file(file_path: str) -> nx.DiGraph:
    """
    Reads a graph from file that has
    - delay attributes as float
    - weight attributes as int
    - node labels as int

    :param file_path: File path of the graph file
    :return: Graph read from file
    """
    if not path.exists(file_path):
        raise FileNotFoundError

    with open(file_path, 'r') as file:
        graph = nx.nx_agraph.read_dot(file)

    graph = nx.convert_node_labels_to_integers(graph)
    float_delay_dict = dict([(k, float(v)) for k, v in nx.get_node_attributes(graph, 'delay').items()])
    int_weight_dict = dict([(k, float(v.replace('"', ''))) for k, v in nx.get_edge_attributes(graph, 'weight').items()])
    nx.set_node_attributes(graph, float_delay_dict, 'delay')
    nx.set_edge_attributes(graph, int_weight_dict, 'weight')

    return graph