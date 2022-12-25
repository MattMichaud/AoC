from collections import defaultdict


def parse_input(file):
    data = open(file, "r").read()
    lines = [x for x in data.split("\n")]
    res = set()
    for r, row in enumerate(lines):
        for c, sym in enumerate(row):
            if sym == "#":
                res.add((r, c))
    return res


def solve(elves):
    dir_list = ["N", "S", "W", "E"]
    any_moved = True
    round = 0
    while any_moved:
        round += 1
        any_moved = False
        proposed = defaultdict(list)
        for (r, c) in elves:
            has_neighbor = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if ((dr, dc) != (0, 0)) and (r + dr, c + dc) in elves:
                        has_neighbor = True
            if not has_neighbor:
                continue

            moved = False
            for d in dir_list:
                if (
                    d == "N"
                    and (not moved)
                    and (r - 1, c) not in elves
                    and (r - 1, c - 1) not in elves
                    and (r - 1, c + 1) not in elves
                ):
                    proposed[(r - 1, c)].append((r, c))
                    moved = True
                elif (
                    d == "S"
                    and (not moved)
                    and (r + 1, c) not in elves
                    and (r + 1, c - 1) not in elves
                    and (r + 1, c + 1) not in elves
                ):
                    proposed[(r + 1, c)].append((r, c))
                    moved = True
                elif (
                    d == "W"
                    and (not moved)
                    and (r, c - 1) not in elves
                    and (r - 1, c - 1) not in elves
                    and (r + 1, c - 1) not in elves
                ):
                    proposed[(r, c - 1)].append((r, c))
                    moved = True
                elif (
                    d == "E"
                    and (not moved)
                    and (r, c + 1) not in elves
                    and (r - 1, c + 1) not in elves
                    and (r + 1, c + 1) not in elves
                ):
                    proposed[(r, c + 1)].append((r, c))
                    moved = True

        dir_list = dir_list[1:] + [dir_list[0]]

        for key, value in proposed.items():
            if len(value) == 1:
                any_moved = True
                elves.discard(value[0])
                elves.add(key)

        if not any_moved:
            print("Part 2:", round)
            break

        if round == 10:
            x_min, *_, x_max = sorted(x for x, _ in elves)
            y_min, *_, y_max = sorted(y for _, y in elves)
            total_ground = (x_max - x_min + 1) * (y_max - y_min + 1)
            total_elves = len(elves)
            empty_ground = total_ground - total_elves
            print("Part 1:", empty_ground)


test_file = "test.txt"
puzzle_file = "2022/inputs/23.txt"
curr_file = puzzle_file

elves = parse_input(curr_file)
solve(elves)
