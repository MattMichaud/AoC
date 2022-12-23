def parse_input(file):
    data = open(file, "r").read().strip().split("\n")
    e = {}
    n = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "#":
                n += 1
                e[n] = (x, y)
    return e


def tuple_add(a, b):
    return tuple(map(sum, zip(a, b)))


def display_elves(el, topLeft=None, bottomRight=None):
    x_min, *_, x_max = sorted(x for x, _ in el.values())
    y_min, *_, y_max = sorted(y for _, y in el.values())
    if topLeft:
        x_min, y_min = topLeft
    if bottomRight:
        x_max, y_max = bottomRight
    # print("top left:", (x_min, y_min))
    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            if (x, y) in el.values():
                row += "#"
            else:
                row += "."
        print("".join(row))


def count_empty_ground(el):
    x_min, *_, x_max = sorted(x for x, _ in el.values())
    y_min, *_, y_max = sorted(y for _, y in el.values())
    total_ground = (x_max - x_min + 1) * (y_max - y_min + 1)
    total_elves = len(el)
    empty_ground = total_ground - total_elves
    return empty_ground


# def clear_in_direction(els, loc, dir):
#     offsets = NEIGHBOR_LOCS[dir]
#     x, y = loc
#     res = all((x + dx, y + dy) not in els.values() for dx, dy in offsets)
#     return res


def get_empty_neighbors(els, loc):
    # offsets (0=NW, 1=N, 2=NE, 3=W, 5=Self, 6=E, 7=SW, 8=S, 9=SE)
    offsets = [
        (-1, -1),  # 0 = NW
        (0, -1),  # 1 = N
        (1, -1),  # 2 = NE
        (-1, 0),  # 3 = W
        (1, 0),  # 4 = E
        (-1, 1),  # 5 = SW
        (0, 1),  # 6 = S
        (1, 1),  # 7 = SE
    ]
    x, y = loc
    empty_neighbors = [(x + dx, y + dy) not in els.values() for dx, dy in offsets]
    return empty_neighbors


def part1(el, part1_rounds):
    # print("== INITIAL STATE ==")
    # display_elves(elf_locs, (-3, -2), (10, 9))
    check_order = ["N", "S", "W", "E"]
    check_index = 0
    elves_moved = 1
    round = 0
    dir_indices = {"N": [0, 1, 2], "S": [5, 6, 7], "W": [0, 3, 5], "E": [2, 4, 7]}
    while elves_moved > 0:
        elves_moved = 0
        round = round + 1
        if round % 10 == 0:
            print("Round", round)
        proposed_moves_locs = []
        proposed_moves_elf_nums = []
        for e, l in el.items():
            # check neighbors to see if move needed
            empty_neighbors = get_empty_neighbors(el, l)
            all_clear = all(empty_neighbors)
            if not all_clear:
                # set proposed move based on move order
                found_move = False
                for dir_offset in range(4):
                    check_dir = check_order[(check_index + dir_offset) % 4]
                    dir_neighbors = [empty_neighbors[n] for n in dir_indices[check_dir]]
                    if all(dir_neighbors):
                        new_loc = tuple_add(l, MOVE_OFFSETS[check_dir])
                        found_move = True
                        break
                # no clear move, stay put
                if found_move:
                    proposed_moves_locs.append(new_loc)
                    proposed_moves_elf_nums.append(e)

        valid_locs = [
            (x, y)
            for (x, y) in proposed_moves_locs
            if proposed_moves_locs.count((x, y)) < 2
        ]
        for index, elf_num in enumerate(proposed_moves_elf_nums):
            if proposed_moves_locs[index] in valid_locs:
                el[elf_num] = proposed_moves_locs[index]
                elves_moved += 1

        # update move order
        check_index = (check_index + 1) % 4
        # print("\n== End of Round", round + 1, "==")
        # display_elves(elf_locs, (-3, -2), (10, 9))
        if round == part1_rounds:
            print("Part 1:", count_empty_ground(el))
    print("Part 2:", round)


test_inp = "test.txt"
puzzle_inp = "2022/inputs/23.txt"
curr_inp = test_inp

NEIGHBOR_LOCS = {
    "N": [(-1, -1), (0, -1), (1, -1)],
    "S": [(-1, 1), (0, 1), (1, 1)],
    "W": [(-1, -1), (-1, 0), (-1, 1)],
    "E": [(1, -1), (1, 0), (1, 1)],
}

MOVE_OFFSETS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

elf_locs = parse_input(curr_inp)
# display_elves(elf_locs, (0, 0), (4, 6))
part1(elf_locs, 10)
