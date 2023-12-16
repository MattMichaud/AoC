import sys

sys.path.append(".")
from utils import tuple_add


OFFSETS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}

MIRRORS = {
    "/": {"N": "E", "S": "W", "E": "N", "W": "S"},
    "\\": {"N": "W", "S": "E", "E": "S", "W": "N"},
}


def parse_input(filename):
    data = open(filename, "r").read().splitlines()
    rows = len(data)
    cols = len(data[0])
    stuff = {}
    for r in range(rows):
        for c in range(cols):
            if data[r][c] in "/\\-|":
                stuff[(r, c)] = data[r][c]
    return stuff, rows, cols


def part1(grid, rows, cols, start_beam=((0, 0), "E")):
    # one beam at the start at (0, 0) heading E
    # beam is represented by a tuple (location, current direction)
    active_beams = [start_beam]
    energized_locs = set()
    processed_beams = set()  # there are LOOPS! uggh
    while len(active_beams) > 0:
        valid_beams = []
        for loc, dir in active_beams:
            x, y = loc
            if 0 <= x < rows and 0 <= y < cols and (loc, dir) not in processed_beams:
                valid_beams.append((loc, dir))
        active_beams = valid_beams
        if len(active_beams) > 0:
            # get the current location and direction
            loc, dir = active_beams.pop()
            # energize current location
            energized_locs.add(loc)
            # add to list of processed beeams (avoid loops)
            processed_beams.add((loc, dir))
            # find out what is at the current location and take actions
            object = grid.get(loc, ".")
            if object in MIRRORS.keys():
                # mirrors
                new_dir = MIRRORS[object][dir]
                new_loc = tuple_add(loc, OFFSETS[new_dir])
                active_beams.append((new_loc, new_dir))
            elif object == "-":
                # splitters
                if dir in "EW":
                    # just move through
                    new_loc = tuple_add(loc, OFFSETS[dir])
                    active_beams.append((new_loc, dir))
                else:
                    # split in two (E & W)
                    for d in "EW":
                        new_loc = tuple_add(loc, OFFSETS[d])
                        active_beams.append((new_loc, d))
            elif object == "|":
                # splitter
                if dir in "NS":
                    # just move through
                    new_loc = tuple_add(loc, OFFSETS[dir])
                    active_beams.append((new_loc, dir))
                else:
                    # split into (N & S)
                    for d in "NS":
                        new_loc = tuple_add(loc, OFFSETS[d])
                        active_beams.append((new_loc, d))
            else:
                # just move
                new_loc = tuple_add(loc, OFFSETS[dir])
                active_beams.append((new_loc, dir))
    return len(energized_locs)


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/16.txt"
filename = puzzle

contraption, height, width = parse_input(filename)
print("Part 1:", part1(contraption, height, width))

max_energized = 0
for r in range(height):
    from_left = part1(contraption, height, width, ((r, 0), "E"))
    from_right = part1(contraption, height, width, ((r, width - 1), "W"))
    max_energized = max(from_left, from_right, max_energized)
for c in range(width):
    from_top = part1(contraption, height, width, ((0, c), "S"))
    from_bottom = part1(contraption, height, width, ((height - 1, c), "N"))
    max_energized = max(from_top, from_bottom, max_energized)
print("Part 2:", max_energized)
