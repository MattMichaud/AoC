import sys

sys.path.append(".")
from utils import data_import


def parse_input(filename):
    data = open(filename, "r").read().strip()
    data = data.split("\n\n")
    seeds_line = data[0]
    map_lines = [l.split("\n") for l in data[1:]]

    seeds = seeds_line.replace("seeds: ", "").split()

    maps = {}
    for ml in map_lines:
        source = ml[0][: ml[0].find("-to-")]
        destination = ml[0].replace(source + "-to-", "").replace(" map:", "")
        map_dict = {}
        map_dict["dest"] = destination
        rules = []
        for r in ml[1:]:
            d_start, s_start, length = r.split()
            rules.append((int(d_start), int(s_start), int(length)))
        map_dict["rules"] = rules

        maps[source] = map_dict

    return (seeds, maps)


def part1(seeds, maps):
    locations = []
    for s in seeds:
        source = "seed"
        value = int(s)
        while source != "location":
            new_value = None
            destination = maps[source]["dest"]
            for d_start, s_start, length in maps[source]["rules"]:
                if (s_start <= value) and (value < (s_start + length)):
                    new_value = value - (s_start - d_start)
            if not new_value:
                new_value = value
            source = destination
            value = new_value
        locations.append(value)
    return min(locations)


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/05.txt"
current_file = puzzle_file
s, m = parse_input(current_file)
print("Part 1 Answer:", part1(s, m))
