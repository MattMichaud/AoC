import sys

sys.path.append(".")
from utils import tuple_add
from collections import deque


OFFSETS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}


def parse_input(filename):
    data = open(filename, "r").read().strip()
    lines = data.split("\n")
    grid = [[int(c) for c in l] for l in lines]
    return grid


def find_pathways(grid, debug=False, out_count=1000):
    rows = len(grid)
    cols = len(grid[0])
    visited_states = {}
    # (heat_loss, r, c, direction, consecutive_straight)
    initial_state = (0, 0, 0, "X", 0)
    q = deque()
    q.append(initial_state)
    step_num = 0
    while q:
        step_num += 1
        if debug and step_num % out_count == 0:
            print("Step", step_num, "Queue size:", len(q))
        heat_loss, r, c, dir, cons = q.popleft()
        if (r, c, dir, cons) in visited_states:
            if visited_states[(r, c, dir, cons)] > heat_loss:
                visited_states[(r, c, dir, cons)] = heat_loss
            else:
                continue

        visited_states[(r, c, dir, cons)] = heat_loss
        # try all directions
        opposite_direction = {"N": "S", "S": "N", "E": "W", "W": "E"}.get(dir, "X")
        for new_direction in "NSEW":
            if new_direction != opposite_direction:  # can't go backwards
                row_offset, col_offset = OFFSETS[new_direction]
                new_row = r + row_offset
                new_col = c + col_offset
                in_grid = (0 <= new_row < rows) and (0 <= new_col < cols)
                new_cons = 1 if new_direction != dir else cons + 1

                if in_grid and new_cons <= 3:
                    new_state = (
                        heat_loss + grid[new_row][new_col],
                        new_row,
                        new_col,
                        new_direction,
                        new_cons,
                    )
                    q.append(new_state)
    final_heat_loss = []
    for key, value in visited_states.items():
        r, c, _, _ = key
        if r == rows - 1 and c == cols - 1:
            final_heat_loss.append(value)
    return min(final_heat_loss)


def find_pathways_ultra(grid, debug=False, out_count=1000):
    rows = len(grid)
    cols = len(grid[0])
    visited_states = {}
    # (heat_loss, r, c, direction, consecutive_straight)
    initial_state = (0, 0, 0, "X", -1)
    q = deque()
    q.append(initial_state)
    step_num = 0
    while q:
        step_num += 1
        if debug and step_num % out_count == 0:
            print("Step", step_num, "Queue size:", len(q))
        heat_loss, r, c, dir, cons = q.popleft()
        if (r, c, dir, cons) in visited_states:
            if visited_states[(r, c, dir, cons)] > heat_loss:
                visited_states[(r, c, dir, cons)] = heat_loss
            else:
                continue

        visited_states[(r, c, dir, cons)] = heat_loss
        # try all directions
        opposite_direction = {"N": "S", "S": "N", "E": "W", "W": "E"}.get(dir, "X")
        for new_direction in "NSEW":
            if new_direction != opposite_direction:  # can't go backwards
                row_offset, col_offset = OFFSETS[new_direction]
                new_row = r + row_offset
                new_col = c + col_offset
                in_grid = (0 <= new_row < rows) and (0 <= new_col < cols)
                new_cons = 1 if new_direction != dir else cons + 1

                if (
                    in_grid
                    and new_cons <= 10  # can't go more than 10 in a row
                    and (
                        new_direction == dir or cons >= 4 or cons == -1
                    )  # still going straight, or have gone at least 4, or just started puzzle
                ):
                    new_state = (
                        heat_loss + grid[new_row][new_col],
                        new_row,
                        new_col,
                        new_direction,
                        new_cons,
                    )
                    q.append(new_state)
    final_heat_loss = []
    for key, value in visited_states.items():
        r, c, _, _ = key
        if r == rows - 1 and c == cols - 1:
            final_heat_loss.append(value)
    return min(final_heat_loss)


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/17.txt"
filename = puzzle

city = parse_input(filename)
print("Part 1:", find_pathways(city, False, 1000000))
print("Part 2:", find_pathways_ultra(city, False, 1000000))
