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
    done = False
    hit_bottom = False
    current_sand_loc = drop_loc
    sand_moved = False
    while not done:
        sand_moved = False
        for direction in ["D", "DL", "DR"]:
            offset = {"D": (0, 1), "DL": (-1, 1), "DR": (1, 1)}.get(direction)
            if not sand_moved:
                check_loc = (
                    current_sand_loc[0] + offset[0],
                    current_sand_loc[1] + offset[1],
                )
                if check_loc[1] >= bottom:
                    done = True
                    hit_bottom = True
                    sand_moved = True
                elif check_loc not in c.keys():
                    current_sand_loc = check_loc
                    sand_moved = True
        if not hit_bottom and not sand_moved:
            done = True
    if floor or not hit_bottom:
        c[current_sand_loc] = "o"

    return hit_bottom


def display_cave(c, top_left, bottom_right):
    for y in range(top_left[1], bottom_right[1] + 1):
        row = "".join(
            c.get((x, y), ".") for x in range(top_left[0], bottom_right[0] + 1)
        )
        print(row)


test_input = "test.txt"
puzzle_input = "2022/inputs/14.txt"
current_file = puzzle_input

start_loc = (500, 0)
part1_cave = build_cave(current_file, start_loc)
while not drop_sand(part1_cave, start_loc):
    next
print("Part 1:", len([v for v in part1_cave.values() if v == "o"]))

part2_cave = build_cave(current_file, start_loc)
floor_depth = max(y for x, y in part2_cave.keys()) + 2
while part2_cave[start_loc] == "+":
    drop_sand(part2_cave, start_loc, floor=True, bottom=floor_depth)
print("Part 2:", len([v for v in part2_cave.values() if v == "o"]))
