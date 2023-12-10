import sys

sys.path.append(".")
from utils import tuple_add
from collections import deque

# if you are moving in a direction, what pipes are valid in next spot
dirs = {
    "n": {"valid_next": ["|", "F", "7", "S"], "move_offset": (-1, 0)},
    "s": {"valid_next": ["|", "L", "J", "S"], "move_offset": (1, 0)},
    "e": {"valid_next": ["-", "7", "J", "S"], "move_offset": (0, 1)},
    "w": {"valid_next": ["-", "F", "L", "S"], "move_offset": (0, -1)},
}
new_dirs = {
    "|": {"n": "n", "s": "s"},
    "-": {"e": "e", "w": "w"},
    "L": {"s": "e", "w": "n"},
    "J": {"s": "w", "e": "n"},
    "7": {"n": "w", "e": "s"},
    "F": {"n": "e", "w": "s"},
}
three_bys = {
    "S": ["...", ".#.", "..."],
    "|": [".#.", ".#.", ".#."],
    "-": ["...", "###", "..."],
    "L": [".#.", ".##", "..."],
    "J": [".#.", "##.", "..."],
    "7": ["...", "##.", ".#."],
    "F": ["...", ".##", ".#."],
    ".": ["...", "...", "..."],
}


def parse_input(filename):
    field = open(filename, "r").read().splitlines()
    width = len(field[0])
    length = len(field)
    pipes = {}
    for r in range(length):
        for c in range(width):
            if field[r][c] in ["|", "-", "L", "J", "7", "F"]:
                pipes[(r, c)] = field[r][c]
            elif field[r][c] == "S":
                start_pos = (r, c)
    return pipes, start_pos


def find_loop(pipes, start, debug=False):
    # from start, check each direction until you find a loop
    for dir in dirs.keys():
        pos = start
        if debug:
            print("testing", dir)
        loop = [start]
        curr_dir = dir
        stop = False
        while not stop:
            next_loc = tuple_add(pos, dirs[curr_dir]["move_offset"])
            next_pipe = pipes.get(next_loc, ".")
            if next_loc == start:
                loop.append(next_loc)
                if debug:
                    print("loop complete")
                    print(loop)
                stop = True
                return loop
            elif next_pipe in dirs[curr_dir]["valid_next"]:
                loop.append(next_loc)
                next_dir = new_dirs[next_pipe][curr_dir]
                if debug:
                    print(next_loc, next_pipe, next_dir)
                pos = next_loc
                curr_dir = next_dir
            else:
                # dead end
                if debug:
                    print("dead end at", pos)
                    print("looking", curr_dir, "at", next_loc)
                    print("found", next_pipe)
                stop = True
    return


def part2(loop, debug=False):
    # blow up each spot to a 3x3
    max_row = max(x for x, _ in loop)
    max_col = max(y for _, y in loop)
    min_row = min(x for x, _ in loop)
    min_col = min(y for _, y in loop)
    top_left = tuple_add((-1, -1), (min_row, min_col))
    bottom_right = tuple_add((1, 1), (max_row, max_col))

    # fill in the new grid
    new_grid = {}
    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            pipe = pipes.get((r, c)) if (r, c) in loop else "."
            if (r, c) == start:
                pipe = "S"
            replacement = three_bys[pipe]
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    set_loc = (r * 3 + row_offset, c * 3 + col_offset)
                    char = replacement[row_offset + 1][col_offset + 1]
                    assert set_loc not in new_grid.keys()
                    new_grid[set_loc] = char

    # fix the start point
    start_translated = (start[0] * 3, start[1] * 3)
    if new_grid[tuple_add(start_translated, (-2, 0))] == "#":
        new_grid[tuple_add(start_translated, (-1, 0))] = "#"
    if new_grid[tuple_add(start_translated, (2, 0))] == "#":
        new_grid[tuple_add(start_translated, (1, 0))] = "#"
    if new_grid[tuple_add(start_translated, (0, -2))] == "#":
        new_grid[tuple_add(start_translated, (0, -1))] = "#"
    if new_grid[tuple_add(start_translated, (0, 2))] == "#":
        new_grid[tuple_add(start_translated, (0, 1))] = "#"

    # print grid for testing
    if debug:
        print("\nstarting grid")
        for r in range((top_left[0] * 3) - 1, (bottom_right[0] * 3 + 2)):
            row = ""
            for c in range((top_left[1] * 3) - 1, bottom_right[1] * 3 + 2):
                row += new_grid[(r, c)]
            print(row)

    # start filling from top left translated to 3x3
    dq = deque()
    dq.append((top_left[0] * 3, top_left[1] * 3))
    visited = set()

    while dq:
        row, col = dq.popleft()
        new_grid[(row, col)] = "O"  # O for filled space
        # try to fill up, down, left, right
        for row_offset, col_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + row_offset
            new_col = col + col_offset
            if (
                (new_row, new_col) in new_grid.keys()  # valid location
                and (new_row, new_col) not in visited  # haven't been there yet
                and new_grid[(new_row, new_col)] == "."  # is empty
            ):
                dq.append((new_row, new_col))  # add to list to check
                visited.add((new_row, new_col))  # add to list checked

    # print grid for testing
    if debug:
        print("\nfilled grid")
        for r in range((top_left[0] * 3) - 1, (bottom_right[0] * 3 + 2)):
            row = ""
            for c in range((top_left[1] * 3) - 1, bottom_right[1] * 3 + 2):
                row += new_grid[(r, c)]
            print(row)

    # count empty 3x3s
    empties = 0
    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            mid = (r * 3, c * 3)
            tests = []
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    tests.append(
                        new_grid[tuple_add(mid, (row_offset, col_offset))] == "."
                    )
            if all(tests):
                empties += 1
    return empties


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/10.txt"
pipes, start = parse_input(puzzle)
loop = find_loop(pipes, start)
print("Part 1:", len(loop) // 2)
print("Part 2:", part2(loop, False))
