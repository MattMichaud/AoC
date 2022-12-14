def build_cave(filename, start_loc):
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
    temp_cave = {start_loc: "+"}
    for r in rock_locs:
        temp_cave[r] = "#"
    return temp_cave


def drop_sand(c, drop_loc, floor=False, bottom=0):
    if not floor:
        bottom = max(y for x, y in c if c[(x, y)] == "#") + 1
    current_sand_loc = drop_loc
    sand_moved = True
    hit_bottom = False
    while sand_moved:
        sand_moved = False
        for direction in ["D", "DL", "DR"]:
            offset = {"D": (0, 1), "DL": (-1, 1), "DR": (1, 1)}.get(direction)
            if not sand_moved and not hit_bottom:
                check_loc = (
                    current_sand_loc[0] + offset[0],
                    current_sand_loc[1] + offset[1],
                )
                if check_loc[1] >= bottom:
                    hit_bottom = True
                elif check_loc not in c.keys():
                    sand_moved = True
                    current_sand_loc = check_loc
    if floor or not hit_bottom:
        c[current_sand_loc] = "o"

    return hit_bottom


test_input = "test.txt"
puzzle_input = "2022/inputs/14.txt"
current_file = puzzle_input
start_loc = (500, 0)

cave = build_cave(current_file, start_loc)
while not drop_sand(cave, start_loc):
    next
print("Part 1:", len([v for v in cave.values() if v == "o"]))

cave = build_cave(current_file, start_loc)
floor_depth = max(y for x, y in cave.keys()) + 2
while cave[start_loc] == "+":
    drop_sand(cave, start_loc, floor=True, bottom=floor_depth)
print("Part 2:", len([v for v in cave.values() if v == "o"]))
