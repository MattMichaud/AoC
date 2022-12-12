# --- Day 12: Hill Climbing Algorithm ---
import networkx as nx

test_input = "test.txt"
puzzle_input = "2022/inputs/12.txt"
current_input = puzzle_input

# Read Input, Get start_loc, end_loc, convert into elevations
input = [list(l) for l in open(current_input, "r").read().strip().split("\n")]
width = len(input[0])
height = len(input)
for y in range(height):
    for x in range(width):
        if input[y][x] == "S":
            start_loc = (x, y)
            input[y][x] = "a"
        elif input[y][x] == "E":
            end_loc = (x, y)
            input[y][x] = "z"
        input[y][x] = ord(input[y][x]) - 96

# Build directed graph DG
DG = nx.DiGraph()
offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
for y in range(height):
    for x in range(width):
        curr_elevation = input[y][x]
        curr_loc = (x, y)
        DG.add_node(curr_loc, height=curr_elevation)
        for dx, dy in offsets:
            if x + dx in range(width) and y + dy in range(height):
                test_elevation = input[y + dy][x + dx]
                test_loc = (x + dx, y + dy)
                if test_elevation <= curr_elevation + 1:
                    DG.add_edge(curr_loc, test_loc)

# find shortest path from start to end
part1 = nx.shortest_path_length(DG, start_loc, end_loc)
print("Part 1:", part1)

# find shortest path for each node with height 1
distances = [
    nx.shortest_path_length(DG, x, end_loc)
    for x, y in DG.nodes(data=True)
    if y["height"] == 1 and nx.has_path(DG, x, end_loc)
]
print("Part 2:", min(distances))
