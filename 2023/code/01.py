import sys

sys.path.append(".")
from utils import data_import


def find_first(text, patterns):
    for i in range(len(text)):
        for p in patterns:
            if text[i : i + len(p[0])] == p[0]:
                return p[1]


def calibration_values_sum(inp, part2=False):
    search_for = [(str(c), int(c)) for c in range(10)]
    if part2:
        search_for += [
            ("one", 1),
            ("two", 2),
            ("three", 3),
            ("four", 4),
            ("five", 5),
            ("six", 6),
            ("seven", 7),
            ("eight", 8),
            ("nine", 9),
        ]
    search_for_reversed = [(p[0][::-1], p[1]) for p in search_for]
    return sum(
        [
            find_first(line, search_for) * 10
            + find_first(line[::-1], search_for_reversed)
            for line in inp
        ]
    )


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/01.txt"
current_file = puzzle_file
lines = [l[0] for l in data_import(current_file, str, " ")]
print("Part 1 Answer:", calibration_values_sum(lines))
print("Part 2 Answer:", calibration_values_sum(lines, True))
