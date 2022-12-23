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


def clear_in_direction(els, loc, dir):
    offsets = NEIGHBOR_LOCS[dir]
    x, y = loc
    res = all((x + dx, y + dy) not in els.values() for dx, dy in offsets)
    return res


def part1(el, part1_rounds):
    # print("== INITIAL STATE ==")
    # display_elves(elf_locs, (-3, -2), (10, 9))
    check_order = ["N", "S", "W", "E"]
    check_index = 0
    elves_moved = 1
    round = 0
    while elves_moved > 0:
        elves_moved = 0
        round = round + 1
        # if round % 100 == 0:
        #     print("Round", round)
        proposed_locs = []
        for e, l in el.items():
            # check neighbors to see if move needed
            all_clear = all(clear_in_direction(el, l, d) for d in check_order)
            if all_clear:
                # all clear so elf stays put
                proposed_locs.append(l)
            else:
                # set proposed move based on move order
                found_move = False
                for dir_offset in range(4):
                    check_dir = check_order[(check_index + dir_offset) % 4]
                    if clear_in_direction(el, l, check_dir):
                        new_loc = tuple_add(l, MOVE_OFFSETS[check_dir])
                        found_move = True
                        break
                # no clear move, stay put
                proposed_locs.append(new_loc if found_move else l)

        # determine valid moves
        # accomplish valid moves
        for e, l in el.items():
            proposed = proposed_locs[e - 1]
            if proposed_locs.count(proposed) < 2:
                el[e] = proposed
                if proposed != l:
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
curr_inp = puzzle_inp

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
