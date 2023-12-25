import networkx as nx
from itertools import combinations
from networkx.algorithms.flow import shortest_augmenting_path


def parse_input(filename):
    data = open(filename, "r").read().splitlines()
    inp_graph = nx.Graph()
    for line in data:
        start, ends = line.split(": ")
        ends = [e for e in ends.split()]
        for end in ends:
            inp_graph.add_edge(start, end)
    return inp_graph


def find_cut_value(graph, value):
    temp_graph = graph.copy()
    for node_a, node_b in combinations(temp_graph.nodes(), 2):
        edge_cuts = nx.minimum_edge_cut(temp_graph, node_a, node_b)
        if len(edge_cuts) == value:
            for edge in edge_cuts:
                temp_graph.remove_edge(*edge)
            size_of_a = len(nx.descendants(temp_graph, node_a)) + 1
            size_of_b = len(nx.descendants(temp_graph, node_b)) + 1
            return size_of_a * size_of_b


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/25.txt"
filename = puzzle

print("Part 1:", find_cut_value(parse_input(filename), 3))
print("Part 2: Merry Christmas")
