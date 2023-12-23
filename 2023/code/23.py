import networkx as nx
import sys
from collections import deque

sys.path.append(".")
from utils import tuple_add as addt

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
hills = [".><", ".<>", ".v^", ".^v"]  # used for bitwise or to determine "forward"


def parse_input(filename):
    lines = open(filename, "r").read().strip().split("\n")
    map = {}
    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            map[(r, c)] = lines[r][c]
    start_pos = (0, next(i for i, c in enumerate(lines[0]) if c == "."))
    end_pos = (len(lines) - 1, next(i for i, c in enumerate(lines[-1]) if c == "."))
    return map, start_pos, end_pos


def build_graphs(map, start, end):
    visited = {start}
    q = deque()
    for i, dir in enumerate(directions):
        if addt(start, dir) in map and map[addt(start, dir)] in ".<>^v":
            q.append((start, i))
    di_graph = nx.DiGraph()
    graph = nx.Graph()  # for part 2 where direction isn't important
    while q:
        begin, dir = q.popleft()  # start of a pathway
        previous = begin
        current = addt(begin, directions[dir])
        length = 1
        visited.add(current)
        way = hills[dir].index(map[current])
        next_directions = [
            (i, npos in visited)
            for i, di in enumerate(directions)
            for npos in [addt(current, di)]
            if npos in map and map[npos] != "#"
        ]
        while len(next_directions) == 2:  # on a pathway still
            dir = next(
                di
                for di, _ in next_directions
                if previous != addt(current, directions[di])
            )
            previous = current
            current = addt(current, directions[dir])
            length += 1
            way |= hills[dir].index(map[current])
            visited.add(current)
            next_directions = [
                (i, npos in visited)
                for i, di in enumerate(directions)
                for npos in [addt(current, di)]
                if npos in map and map[npos] != "#"
            ]

        # junction reached
        if way == 1:
            # headed "forward"
            di_graph.add_edge(begin, current, cost=length)
        else:
            # headed "backwards" so add it reversed
            di_graph.add_edge(current, begin, cost=length)

        # part 2 where direction doesn't matter
        graph.add_edge(begin, current, cost=length)  # for part 2

        # add options into the queue
        for di, already_visited in next_directions:
            if not (already_visited):
                q.append((current, di))

    return di_graph, graph


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/23.txt"
filename = puzzle

map, start, end = parse_input(filename)
directed_graph, graph = build_graphs(map, start, end)

paths = nx.all_simple_paths(directed_graph, start, end)
max_length = max([nx.path_weight(directed_graph, path, "cost") for path in paths])
print("Part 1:", max_length)

paths = nx.all_simple_paths(graph, start, end)
max_length = max([nx.path_weight(graph, path, "cost") for path in paths])
print("Part 2:", max_length)
