def parse_input(filename):
    data = open(filename, "r").read().strip().split("\n")
    grid = [[c for c in row] for row in data]
    return grid


def display(grid):
    for row in range(len(grid)):
        print("".join(grid[row]))
    print()


def tilt(grid):
    rows = len(grid)
    cols = len(grid[0])
    for c in range(cols):
        done = False
        while not done:
            rocks_moved = 0
            for r in range(rows):
                if r > 0 and grid[r][c] == "O" and grid[r - 1][c] == ".":
                    rocks_moved += 1
                    grid[r - 1][c] = "O"
                    grid[r][c] = "."
            if rocks_moved == 0:
                done = True
    return grid


def calc_load(grid):
    load = 0
    rows = len(grid)
    cols = len(grid[0])
    for c in range(cols):
        for r in range(rows):
            if grid[r][c] == "O":
                load += rows - r
    return load


def cycle(grid):
    # using https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
    for _ in range(4):
        # tilt then rotate 90 degrees clockwise
        grid = tilt(grid)
        grid = [list(i) for i in list(zip(*grid[::-1]))]
    return grid


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/14.txt"
filename = puzzle

print("Part 1:", calc_load(tilt(parse_input(filename))))

pattern = parse_input(filename)
seen_patterns = {}
max_cycles = 1000000000
current_cycle = 0
while current_cycle < max_cycles:
    current_cycle += 1
    pattern = cycle(pattern)
    # make it hashable for dict key (immutable)
    pattern_key = tuple(tuple(row) for row in pattern)
    if pattern_key in seen_patterns.keys():
        # how long did the repeat take
        length = current_cycle - seen_patterns[pattern_key]
        # how many whole version of those can we do
        repeats = (max_cycles - current_cycle) // length
        # advance to that cycle and continue
        current_cycle += repeats * length
    seen_patterns[pattern_key] = current_cycle
print("Part 2:", calc_load(pattern))
