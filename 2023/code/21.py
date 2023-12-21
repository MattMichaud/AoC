from collections import deque
from copy import deepcopy

OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse_input(filename):
    data = open(filename, "r").read().strip()
    lines = data.split("\n")
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] == "S":
                start_pos = (r, c)
    return lines, start_pos


def part_one(map, start, num_steps):
    rows = len(map)
    cols = len(map[0])
    next_q = deque()
    next_q.append(start)
    for _ in range(num_steps):
        current_q = deepcopy(next_q)
        visited = set(current_q)
        next_q = deque()
        while current_q:
            curr_loc = current_q.popleft()
            for dir in OFFSETS:
                new_row = curr_loc[0] + dir[0]
                new_col = curr_loc[1] + dir[1]
                if (
                    0 <= new_row < rows  # valid row
                    and 0 <= new_col < cols  # valid column
                    and (new_row, new_col) not in visited  # haven't added already
                    and map[new_row][new_col] != "#"  # not a wall
                ):
                    visited.add((new_row, new_col))
                    next_q.append((new_row, new_col))
    return len(next_q)


def part_two(map, start, total_steps=26501365):
    rows = len(map)
    cols = len(map[0])
    offset = total_steps % rows
    evals = [0, 1, 2]
    results = []
    for n in evals:
        steps_n = offset + (rows * n)
        next_q = deque()
        next_q.append(start)
        for _ in range(steps_n):
            current_q = deepcopy(next_q)
            visited = set(current_q)
            next_q = deque()
            while current_q:
                curr_loc = current_q.popleft()
                for dir in OFFSETS:
                    new_row, new_col = curr_loc[0] + dir[0], curr_loc[1] + dir[1]
                    if (new_row, new_col) not in visited and map[new_row % rows][
                        new_col % cols
                    ] != "#":
                        visited.add((new_row, new_col))
                        next_q.append((new_row, new_col))
        results.append((n, len(next_q)))

    x = (total_steps - offset) / rows
    return int(quadratic_extrapolation(*results, x))


def quadratic_extrapolation(pt1, pt2, pt3, x):
    x0, y0 = pt1
    x1, y1 = pt2
    x2, y2 = pt3
    c = y0
    b = (y1 - y0) / (x1 - x0)
    a = ((y2 - y1) / (x2 - x1) - b) / (x2 - x0)
    return a * (x - x1) * (x - x0) + b * (x - x0) + c


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/21.txt"
filename = puzzle

map, start = parse_input(filename)
steps = 6 if filename == test else 64
print("Part 1:", part_one(map, start, steps))
print("Part 2:", part_two(map, start, 26501365))
# part 2 method doesn't work on test case
# probably because it doesn't have clear paths N-S and E-W from start
# methodology is to see how much you can cover in steps to get to edge of first square (n=0)
# then how much if you go out one full square from that (n=1), then one more (n=2)
# those results will form a quadratic because of how they are arranged in concentric diamonds
