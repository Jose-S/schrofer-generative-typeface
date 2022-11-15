import networkx as nx

# import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

# Graph Contants
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 1 A 2 B 3
# C   D   E
# 4 F 5 G 6
# H   I   J
# 7 K 8 L 9
edges = {
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
all_edges = np.array(list(edges.values()))

# return list of all subsets of length r from arr
def rSubset(arr, r):

    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))


# Return a list of edge tuples (ex: (1,2))
# given arr = list of edge keys (ex = A)
def getEdges(arr):
    # return a list of all edge values
    # arr is a tuple of keys in edges
    # uses list comprehension
    return [edges[k] for k in arr]


# Given a path length generate
# Generate all possible graphs (forest) with
# path_len edges in a graph with nodes (global)
def generateGraphs(path_len, forest=False):

    graphs = []
    # All path_len path graphs
    paths = rSubset(edges, path_len)
    print(len(paths))
    graphs_len = len(paths)
    for i in range(graphs_len):
        # get edge tuple list (A -> (1,2))
        # for each edge key in paths[i]
        lst_of_edges = getEdges(paths[i])
        # create graph
        G = nx.Graph()
        G.add_nodes_from(nodes)
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


# calculate number of forest
# with between min_edges and max_edges
def calcNumForest(min_edges, max_edges):
    count = 0
    for i in range(min_edges, max_edges + 1):
        all_g = generateGraphs(i, forest=True)
        count = count + len(all_g)
    return count
