# get input
test_file = "test.txt"
puzzle_file = "2022/inputs/17.txt"
current_file = puzzle_file
wind_list = list(open(current_file, "r").read().strip().split()[0])

rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, -2), (0, -1), (1, -1), (2, -1), (1, 0)],
    [(2, -2), (2, -1), (0, 0), (1, 0), (2, 0)],
    [(0, -3), (0, -2), (0, -1), (0, 0)],
    [(0, -1), (1, -1), (0, 0), (1, 0)],
]

move_offsets = {"<": (-1, 0), ">": (1, 0), "D": (0, 1)}
LEFT_WALL = 0
RIGHT_WALL = 8
FLOOR_HEIGHT = 0


def move_rock(r, d):
    return [(loc[0] + d[0], loc[1] + d[1]) for loc in r]


def get_row(t, r):
    row = "".join([t.get((x, r), ".") for x in range(LEFT_WALL, RIGHT_WALL + 1)])
    return row


def display_tower(t, h, start_height=FLOOR_HEIGHT):
    for y in range(h, start_height + 1):
        row = "".join([t.get((x, y), ".") for x in range(LEFT_WALL, RIGHT_WALL + 1)])
        print(y, row, row == "|###.###|")


def add_rock(t, r, mh):
    for loc in r:
        t[loc] = "#"
        mh = min(mh, loc[1])
    return t, mh


def init_tower(height):
    t = {}
    for x in range(LEFT_WALL, RIGHT_WALL + 1):
        t[(x, FLOOR_HEIGHT)] = "-"
    for y in range(height):
        t[(LEFT_WALL, -1 * y)] = "|"
        t[(RIGHT_WALL, -1 * y)] = "|"
    return t, 0


# init variables
current_rock_index = 0
current_wind_index = 0
total_rocks = 2022

# build initial tower space
tower, curr_max_height = init_tower(100000)

for r in range(total_rocks):
    current_rock = rocks[current_rock_index]
    current_rock_index = (current_rock_index + 1) % 5
    # place rock in initial spot
    bottom_left = (3, curr_max_height - 4)
    current_rock = move_rock(current_rock, bottom_left)
    rock_placed = False
    # keep doing the next until it can't move DOWN
    while not rock_placed:
        # try to push with win
        current_wind = wind_list[current_wind_index]
        current_wind_index = (current_wind_index + 1) % len(wind_list)
        test_locs = move_rock(current_rock, move_offsets[current_wind])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs

        # try to drop one place
        test_locs = move_rock(current_rock, move_offsets["D"])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs
        else:
            rock_placed = True

    # try to push by wind
    # try to move down
    tower, curr_max_height = add_rock(tower, current_rock, curr_max_height)
# display_tower(tower, curr_max_height - 5)
print("Part 1:", curr_max_height * -1)


### PART 2 ###

# init variables
current_rock_index = 0
current_wind_index = 0
total_rocks = 4000

# build initial tower space
tower, curr_max_height = init_tower(100000)

for r in range(total_rocks):
    current_rock = rocks[current_rock_index]
    current_rock_index = (current_rock_index + 1) % 5
    # place rock in initial spot
    bottom_left = (3, curr_max_height - 4)
    current_rock = move_rock(current_rock, bottom_left)
    rock_placed = False
    # keep doing the next until it can't move DOWN
    while not rock_placed:
        # try to push with win
        current_wind = wind_list[current_wind_index]
        current_wind_index = (current_wind_index + 1) % len(wind_list)
        test_locs = move_rock(current_rock, move_offsets[current_wind])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs

        # try to drop one place
        test_locs = move_rock(current_rock, move_offsets["D"])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs
        else:
            rock_placed = True

    # try to push by wind
    # try to move down
    tower, curr_max_height = add_rock(tower, current_rock, curr_max_height)


# find a repeating pattern
def tower_as_list(t, h):
    res_list = []
    for y in range(-1 * h, FLOOR_HEIGHT + 1):
        row = "".join([t.get((x, y), ".") for x in range(LEFT_WALL, RIGHT_WALL + 1)])
        res_list.append(row)
    return res_list


def cycle(list, min_length=0):
    shortest = []
    if len(list) <= 1:
        return list
    if len(set(list)) == len(list):
        return list
    for x in range(min_length, len(list) - min_length):
        if list[0:x] == list[x : 2 * x]:
            shortest = list[0:x]
    return shortest


tower_list = tower_as_list(tower, curr_max_height * -1)
tower_list = tower_list[::-1]
cycle_start = 0
cycle_found = False
while not cycle_found:
    test_list = tower_list[cycle_start:]
    if len(test_list) < 5:
        break
    c = cycle(tower_list[cycle_start:], 5)
    if len(c) > 0:
        cycle_found = True
    else:
        cycle_start += 1

start_row_index = -1 * cycle_start
start_row_pattern = get_row(tower, start_row_index)

target_row_index = -1 * (cycle_start + len(c))
target_row_pattern = get_row(tower, target_row_index)

# drop rocks and count until we get matching patterns

# init variables
current_rock_index = 0
current_wind_index = 0
rock_counter = 0
start_match = end_match = False

# build initial tower space
tower, curr_max_height = init_tower(100000)

while start_match == False or end_match == False:
    current_rock = rocks[current_rock_index]
    current_rock_index = (current_rock_index + 1) % 5
    # place rock in initial spot
    bottom_left = (3, curr_max_height - 4)
    current_rock = move_rock(current_rock, bottom_left)
    rock_placed = False
    # keep doing the next until it can't move DOWN
    while not rock_placed:
        # try to push with win
        current_wind = wind_list[current_wind_index]
        current_wind_index = (current_wind_index + 1) % len(wind_list)
        test_locs = move_rock(current_rock, move_offsets[current_wind])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs

        # try to drop one place
        test_locs = move_rock(current_rock, move_offsets["D"])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs
        else:
            rock_placed = True

    tower, curr_max_height = add_rock(tower, current_rock, curr_max_height)
    rock_counter += 1
    if get_row(tower, start_row_index) == start_row_pattern and not start_match:
        start_match = True
        start_rocks_dropped = rock_counter
        start_max_height = curr_max_height
    if get_row(tower, target_row_index) == target_row_pattern:
        end_match = True
        end_rocks_dropped = rock_counter
        end_max_height = curr_max_height


rocks_dropped_in_cycle = end_rocks_dropped - start_rocks_dropped
cycle_height = (-1 * end_max_height) - (-1 * start_max_height)


big_rock_target = 1000000000000
full_cycles = (big_rock_target - start_rocks_dropped) // rocks_dropped_in_cycle
remainder_rocks = (big_rock_target - start_rocks_dropped) % rocks_dropped_in_cycle

# drop start rocks, one cycle rocks, remainder rocks

# init variables
current_rock_index = 0
current_wind_index = 0
total_rocks = start_rocks_dropped + rocks_dropped_in_cycle + remainder_rocks

# build initial tower space
tower, curr_max_height = init_tower(100000)

for r in range(total_rocks):
    current_rock = rocks[current_rock_index]
    current_rock_index = (current_rock_index + 1) % 5
    # place rock in initial spot
    bottom_left = (3, curr_max_height - 4)
    current_rock = move_rock(current_rock, bottom_left)
    rock_placed = False
    # keep doing the next until it can't move DOWN
    while not rock_placed:
        # try to push with win
        current_wind = wind_list[current_wind_index]
        current_wind_index = (current_wind_index + 1) % len(wind_list)
        test_locs = move_rock(current_rock, move_offsets[current_wind])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs

        # try to drop one place
        test_locs = move_rock(current_rock, move_offsets["D"])
        invalid_loc = any((x, y) in tower.keys() for x, y in test_locs)
        if not invalid_loc:
            current_rock = test_locs
        else:
            rock_placed = True

    tower, curr_max_height = add_rock(tower, current_rock, curr_max_height)

dropped_in_cycles = big_rock_target - total_rocks
cycles = dropped_in_cycles // rocks_dropped_in_cycle
total_height = (-1 * curr_max_height) + cycles * cycle_height
print("Part 2:", total_height)
