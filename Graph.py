# --------------- IMPORTS --------------

# import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from itertools import combinations

# --------------- DEFINITIONS --------------

# Graph Theory Definitons
# Nodes (aka vertex): A single entity
# Edge: Connection between two nodes
# Graph: Data structure formed by nodes and edges
# Path: A sequence of non-repeated edges (1st and last node have a degree of 1)
# Cycle: A path that starts at a given node and ends at the same node


# --------------- CONSTATNS --------------

NODES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 1 A 2 B 3
# C   D   E
# 4 F 5 G 6
# H   I   J
# 7 K 8 L 9
EDGES: dict[str, tuple] = {
    "A": (1, 2),
    "B": (2, 3),
    "C": (1, 4),
    "D": (2, 5),
    "E": (3, 6),
    "F": (4, 5),
    "G": (5, 6),
    "H": (4, 7),
    "I": (5, 8),
    "J": (6, 9),
    "K": (7, 8),
    "L": (8, 9),
}

## Edges List format flat (for debugging)
ALL_EDGES_FLAT = np.array(list(EDGES.values()))

# --------------- FUNCTIONS --------------


def generate_path_combinations(edges: list, r: int) -> list:
    """
    Generates a list of all path combinations of r-length

    Parameters
    ----------
    edges : list
        A list of edges used to generate path combinations
    r : int
        The lenght of each combination generated

    Returns
    -------
    list
        A list of all paths of r-length
    """
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(edges, r))


def convert_to_edge_tuples(edge_keys: list) -> list[tuple[int, int]]:
    """
    Converts Edge Key List to Edge Tuple List

    Parameters
    ----------
    edge_keys : list
        A list of Edge Keys (ex: ["A", "C", "D"])

    Returns
    -------
    list[tuple[int,int]]
         A list of Edge tuples(ex: [(1,2) ,(2,4) ,(4,1)])
    """
    # uses list comprehension to convert Dict of Tuples to Lis tof Tuples
    return [EDGES[k] for k in edge_keys]


# Given a path length generate
# Generate all possible graphs (forest) with
# path_len edges in a graph with nodes (global)
def generate_graphs(path_len: int, forest: bool = False) -> list[nx.Graph]:
    """
    Generate a list of Graphs with path_len edges

    Parameters
    ----------
    path_len : int
        Length of Path (Numbe rof edges in Graph)
    forest : bool, optional
        Only generate forest graphs(no cycles), by default False

    Returns
    -------
    list[nx.Graph]
        List of Graphs (NX Objects)
    """

    graphs: list[nx.Graph] = []
    paths = generate_path_combinations(EDGES, path_len)
    paths_len = len(paths)

    for i in range(paths_len):
        # get edge tuple list (A -> (1,2))
        # for each edge key in paths[i]
        lst_of_edges = convert_to_edge_tuples(paths[i])
        # create graph
        G = nx.Graph()
        G.add_nodes_from(NODES)
        G.add_edges_from(lst_of_edges)
        # diferentiate between forest and trees
        if forest and nx.is_forest(G):
            graphs.append(G)
        elif not forest:
            graphs.append(G)

    return graphs


# # Draw preatty graph using matplotlib
# # Currently broken without positions array dictionary
# def drawGraph(g):
#     nx.draw(
#         G,
#         pos=positions,
#         with_labels=False,
#         node_color="#000000",
#         node_size=5200,
#         width=75,
#         font_weight="bold",
#     )


# # Draw graph using matplotlib
# def drawBareGraph(g):
#     nx.draw(G, pos=positions, with_labels=True, width=2, font_weight="bold")

# ----------- UTILITY FUNCTIONS -----------


def calc_num_forest(min_edges: int, max_edges: int) -> int:
    """
    Utility Function used to calculate number of Forest Graphs with min_edges to max_edges

    Parameters
    ----------
    min_edges : int
        Minimum edge count of forest
    max_edges : int
        Maximun edge count of forest

    Returns
    -------
    int
        Number of Forest with min_edges to max_edges
    """
    counter = 0
    for i in range(min_edges, max_edges + 1):
        G_List = generate_graphs(i, forest=True)
        counter = counter + len(G_List)
    return counter
