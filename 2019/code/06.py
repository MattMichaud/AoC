import sys
sys.path.append('.')
from utils import data_import
import networkx as nx

def create_graph(orbits):
    DG = nx.Graph()
    for planet in orbits:
        edge = planet.split(')')
        DG.add_edge(*edge)
    return(DG)

def part1(filename):
    G = create_graph(data_import(filename, str))
    print('Part 1 Answer:', sum(nx.single_source_shortest_path_length(G, 'COM').values()))

def part2(filename):
    G = create_graph(data_import(filename, str))
    print('Part 2 Answer:',nx.shortest_path_length(G, 'YOU', 'SAN') - 2)

filename = '2019/inputs/06.txt'
part1(filename)
part2(filename)
