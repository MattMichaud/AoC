import sys

sys.path.append(".")
from utils import data_import


def parse_input(filename):
    with open(filename, "r") as f:
        data = f.read().splitlines()
    return data


def group_into_elves(input_list):
    elves = []
    current_sum = 0
    for c in input_list:
        if c == "":
            elves.append(current_sum)
            current_sum = 0
        else:
            current_sum += int(c)
    elves.append(current_sum)
    return elves


def part1(filename):
    calories = parse_input(filename)
    elves = group_into_elves(calories)
    print("Part 1 Answer:", max(elves))


def part2(filename):
    calories = parse_input(filename)
    elves = group_into_elves(calories)
    elves.sort(reverse=True)
    print("Part 2 Answer:", sum(elves[0:3]))


# inp = "2022/inputs/test.txt"
inp = "2022/inputs/01.txt"
part1(inp)
part2(inp)
