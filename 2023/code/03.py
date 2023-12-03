import sys

sys.path.append(".")
from utils import data_import
from utils import tuple_add
from collections import defaultdict


def parse_input(filename):
    nums = defaultdict(str)
    symbols = defaultdict(str)
    with open(filename, "r") as f:
        data = f.read().splitlines()

    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c != ".":
                if c.isdigit():
                    nums[(j, i)] = c
                else:
                    symbols[(j, i)] = c

    used_locs = []
    numbers = []
    for k, v in nums.items():
        if k not in used_locs:
            row = k[1]
            left_edge = k[0]

            x_offset = 0
            while tuple_add(k, (x_offset, 0)) in nums.keys():
                x_offset += 1

            value = ""
            for dx in range(x_offset):
                loc = tuple_add(k, (dx, 0))
                used_locs.append(loc)
                value += str(nums[loc])

            right_edge = left_edge + x_offset - 1
            numbers.append((int(value), row, left_edge, right_edge))

    total = 0
    for value, row, left, right in numbers:
        # get all the neighbors
        neighbors = []
        neighbors.append((left - 1, row))
        neighbors.append((right + 1, row))
        for x in range(left - 1, right + 2):
            neighbors.append((x, row - 1))
            neighbors.append((x, row + 1))
        if any(item in neighbors for item in symbols.keys()):
            total += value

    print("Part 1 Answer:", total)

    unique_nums = defaultdict(str)
    for i, (value, row, left, right) in enumerate(numbers):
        for x in range(left, right + 1):
            unique_nums[(x, row)] = (i, value)

    total_gear_ratio = 0
    for k, v in symbols.items():
        neighbor_nums = set()
        if v == "*":
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dx == 0 and dy == 0):
                        check_loc = tuple_add(k, (dx, dy))
                        if check_loc in unique_nums.keys():
                            neighbor_nums.add(unique_nums[check_loc])
            if len(neighbor_nums) == 2:
                gear_ratio = 1
                for _, v in neighbor_nums:
                    gear_ratio = gear_ratio * v
                total_gear_ratio += gear_ratio

    print("Part 2 Answer:", total_gear_ratio)

    return


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/03.txt"
current_file = puzzle_file
inp = parse_input(current_file)
