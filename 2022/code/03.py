import sys

sys.path.append(".")
from utils import data_import


def priority(c):
    num = ord(c)
    if num >= 97:  # lowercase
        out = ord(c) - 96
    else:  # uppercase
        out = ord(c) - 64 + 26
    return out


def string_split(input_string):
    mid = len(input_string) // 2
    first_half = input_string[:mid]
    second_half = input_string[mid:]
    return first_half, second_half


def part1(rucksacks):
    priority_sum = 0
    for sack in rucksacks:
        c1, c2 = string_split(sack)
        same = list(set(c1).intersection(c2))[0]
        priority_sum += priority(same)
    print("Part 1 Answer:", priority_sum)


def part2(rucksacks):
    total_priority = 0
    groups = len(rucksacks) // 3
    for i in range(groups):
        sack1 = set(rucksacks[(i * 3) + 0])
        sack2 = set(rucksacks[(i * 3) + 1])
        sack3 = set(rucksacks[(i * 3) + 2])
        set1 = sack1.intersection(sack2)
        result_set = set1.intersection(sack3)
        badge = list(result_set)[0]
        total_priority += priority(badge)
    print("Part 2 Answer:", total_priority)


input_file = "2022/inputs/test.txt"
input_file = "2022/inputs/03.txt"
data = data_import(input_file)
part1(data)
part2(data)
