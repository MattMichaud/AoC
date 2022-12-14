def tuple_add(a, b):
    return tuple(map(sum, zip(a, b)))


def parse_input(filename, start_loc, with_floor=False, floor_width=20):
    input_lines = open(filename, "r").read().strip().split("\n")
    structures = []
    for line in input_lines:
        tuples = [eval(item) for item in line.split(" -> ")]
        structures.append(tuples)
    rock_locs = set()
    for struct in structures:
        for i in range(len(struct) - 1):
            start_x = min(struct[i][0], struct[i + 1][0])
            start_y = min(struct[i][1], struct[i + 1][1])
            end_x = max(struct[i][0], struct[i + 1][0])
            end_y = max(struct[i][1], struct[i + 1][1])
            for y in range(start_y, end_y + 1):
                for x in range(start_x, end_x + 1):
                    rock_locs.add((x, y))
    c = build_cave(rock_locs, start_loc, with_floor, floor_width)
    c[start_loc] = "+"
    return c


def build_empty_cave(top_left, bottom_right):
    coords = {}
    min_x, min_y = top_left
    max_x, max_y = bottom_right
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            coords[(x, y)] = "."
    return coords


def get_dims(c):
    tl = (min(x for x, _ in c), min(y for _, y in c))
    br = (max(x for x, _ in c), max(y for _, y in c))
    return tl, br


def build_cave(rocks, start, with_floor, floor_width):
    all_locs = rocks
    all_locs.add(start)
    floor_left = -1 * (floor_width // 2)
    floor_right = floor_width // 2
    floor_depth = get_dims(rocks)[1][1] + 2
    floor_locs = [
        (start[0] + x, floor_depth) for x in range(floor_left, floor_right + 1)
    ]
    if with_floor:
        all_locs = list(all_locs) + floor_locs
    top_left, bottom_right = get_dims(all_locs)
    temp_cave = build_empty_cave(top_left, bottom_right)
    for r in rocks:
        temp_cave[r] = "#"
    if with_floor:
        for loc in floor_locs:
            temp_cave[loc] = "F"
    return temp_cave


def display(c, display_vals=["#", "o", "+"]):
    used_locs = [(x, y) for x, y in c.keys() if c[(x, y)] in display_vals]
    top_left, bottom_right = get_dims(used_locs)
    min_x, min_y = top_left
    max_x, max_y = bottom_right
    for y in range(min_y, max_y + 1):
        row = [c.get((x, y), " ") for x in range(min_x, max_x + 1)]
        print("".join(row))


def drop_sand(cave, drop_loc):
    at_rest = False
    off_edge = False
    current_sand_loc = drop_loc
    movements = {"D": (0, 1), "DL": (-1, 1), "DR": (1, 1)}
    while not at_rest and not off_edge:
        sand_moved = False
        for direction in ["D", "DL", "DR"]:
            if not sand_moved:
                check_loc = tuple_add(current_sand_loc, movements.get(direction))
                check_val = cave.get(check_loc, "ABYSS")
                if check_val == ".":
                    current_sand_loc = check_loc
                    sand_moved = True
                elif check_val == "ABYSS":
                    off_edge = True
                    sand_moved = True
        if not off_edge and not sand_moved:
            at_rest = True
            cave[current_sand_loc] = "o"
    return off_edge


test_input = "test.txt"
puzzle_input = "2022/inputs/14.txt"
current_file = puzzle_input

start_loc = (500, 0)
part1_cave = parse_input(current_file, start_loc)
while not drop_sand(part1_cave, start_loc):
    next
print("Part 1:", len([v for v in part1_cave.values() if v == "o"]))

floor_width = 500
part2_cave = parse_input(current_file, start_loc, True, floor_width)
while part2_cave[start_loc] == "+":
    drop_sand(part2_cave, start_loc)
print("Part 2:", len([v for v in part2_cave.values() if v == "o"]))
