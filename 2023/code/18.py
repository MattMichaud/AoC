import sys

sys.path.append(".")
from utils import tuple_add, shoelace_area
from collections import deque

OFFSETS = {
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1),
}


def parse_input(filename):
    return [l.split() for l in open(filename, "r").read().splitlines()]


# ended up switching part 1 to the same method as part 2, so this goes unused
def dig_trench(plan):
    t = {}
    loc = (0, 0)
    for dir, dist, hex in plan:
        for i in range(int(dist)):
            loc = tuple_add(loc, OFFSETS[dir])
            t[loc] = hex
    return t


# ended up switching part 1 to the same method as part 2, so this goes unused
def dig_interior(trench, start_pos=(1, 1)):
    q = deque()
    q.append(start_pos)
    visited = set()
    while q:
        loc = q.popleft()
        trench[loc] = "#"
        for dir in "UDLR":
            new_loc = tuple_add(loc, OFFSETS[dir])
            if new_loc not in visited and new_loc not in trench.keys():
                q.append(new_loc)
                visited.add(new_loc)
    return trench


def convert_plan(plan):
    new_plan = []
    for _, _, hex in plan:
        dist = int(hex[2:7], 16)
        dir_offset = hex[-2:-1]
        dir = {"0": "R", "1": "D", "2": "L", "3": "U"}[dir_offset]
        new_plan.append([dir, dist, hex])
    return new_plan


def plan_to_coords(plan):
    coords = [(0, 0)]
    curr_pos = (0, 0)
    for dir, dist, hex in plan:
        offset = OFFSETS[dir]
        offset = (offset[0] * int(dist), offset[1] * int(dist))
        new_pos = tuple_add(curr_pos, offset)
        coords.append(new_pos)
        curr_pos = new_pos
    return coords


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/18.txt"

filename = puzzle
dig_plan = parse_input(filename)
print("Part 1:", shoelace_area(plan_to_coords(dig_plan)))
print("Part 2:", shoelace_area(plan_to_coords(convert_plan(dig_plan))))

# OLD PART 1 METHOD - DIDN'T SCALE
# trench = dig_interior(dig_trench(dig_plan))
# print("Part 1:", len(trench.keys()))
