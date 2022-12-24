from collections import deque


def parse_input(file):
    data = open(file, "r").read().strip()
    data = [x for x in data.split("\n")]
    return data


def get_bliz_locs(g):
    # creates a dict with key of time (t)
    # contains locations of blizzards at next time (t + 1)
    # those are unsafe spots to move
    # because it will repeat, we only need enough entries for
    # the cycle which is height * width of area of field
    height = len(g)
    width = len(g[0])
    bliz_locs = {}
    for t in range(((height - 2) * (width - 2) + 1)):
        unsafe_locs = set()
        for row in range(height):
            for col in range(width):
                curr_item = g[row][col]
                if curr_item == ">":
                    unsafe_locs.add((row, 1 + ((col - 1 + t) % (width - 2))))
                elif curr_item == "<":
                    unsafe_locs.add((row, 1 + ((col - 1 - t) % (width - 2))))
                elif curr_item == "v":
                    unsafe_locs.add((1 + ((row - 1 + t) % (height - 2)), col))
                elif curr_item == "^":
                    unsafe_locs.add((1 + ((row - 1 - t) % (height - 2)), col))
        bliz_locs[t] = unsafe_locs
    return bliz_locs


test_inp = "test.txt"
puzz_inp = "2022/inputs/24.txt"
curr_inp = puzz_inp

grid = parse_input(curr_inp)
max_rows = len(grid)
max_cols = len(grid[0])

# populate bliz_locs dict
bliz_locs = get_bliz_locs(grid)

# find start location
r = 0
c = grid[r].index(".")

seen_states = set()
start_state = (r, c, 0, False, False)  # row, col, time, seen_end, seen_start
states = deque([start_state])
part1_finished = False
while states:
    (row, col, time, seen_end, seen_start) = states.popleft()
    # if it isn't a valid spot, ignore it
    # need this because we don't check when adding states
    if not (0 <= row < max_rows and 0 <= col < max_cols and grid[row][col] != "#"):
        continue
    # once we are at the end,
    # and have already been to the end and back to start,
    # we are done with part 2
    if row == max_rows - 1 and seen_start and seen_end:
        print("Part 2:", time)
        break
    # first time we reach the end, print result for part 1
    if row == max_rows - 1 and (not part1_finished):
        print("Part 1:", time)
        part1_finished = True
    # mark when we've seen the end
    if row == max_rows - 1:
        seen_end = True
    # if we have already seen the end, mark if we got back to start
    if row == 0 and seen_end:
        seen_start = True

    # keep track of states we have already processed to avoid duplicates
    if (row, col, time, seen_end, seen_start) in seen_states:
        continue
    seen_states.add((row, col, time, seen_end, seen_start))

    # get where blizzards will be at next time (time cycles by area of field)
    bliz_time = time % ((max_rows - 2) * (max_cols - 2))
    avoid_locs = bliz_locs[bliz_time + 1]

    # can we stay put?
    if (row, col) not in avoid_locs:
        states.append((row, col, time + 1, seen_end, seen_start))
    # can we move right?
    if (row, col + 1) not in avoid_locs:
        states.append((row, col + 1, time + 1, seen_end, seen_start))
    # can we move left?
    if (row, col - 1) not in avoid_locs:
        states.append((row, col - 1, time + 1, seen_end, seen_start))
    # can we move up?
    if (row - 1, col) not in avoid_locs:
        states.append((row - 1, col, time + 1, seen_end, seen_start))
    # can we move down?
    if (row + 1, col) not in avoid_locs:
        states.append((row + 1, col, time + 1, seen_end, seen_start))
