import networkx as netx

def get_data(filename):
    with open(filename, "r") as f:
        data = f.read().rstrip()

    return [tuple(map(int, line.split(","))) for line in data.splitlines()]

def mandist(s, t):
    return sum(abs(x - y) for x, y in zip(s, t))

def part1(points):
    g = netx.Graph()
    for point in points:
        for otherpoint in points:
            if mandist(point, otherpoint) <= 3:
                g.add_edge(point, otherpoint)

    return netx.number_connected_components(g)

input_file = '2018/inputs/2018_25_input.txt'
print('Part 1 Answer:', part1(get_data(input_file)))