import sys

sys.path.append(".")
from utils import data_import


def calibration_value(inp):
    sum = 0
    for l in inp:
        digits = ""
        for c in l[0]:
            if c.isdigit():
                digits += c
        two_digit = digits[0] + digits[len(digits) - 1]
        sum += int(two_digit)
    return sum


def part1(inp):
    print("Part 1 Answer:", calibration_value(inp))


def part2(inp):
    num_strings = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
    ]
    cleaned_input = []
    for l in inp:
        string = l[0]
        print(string)
        for number, num_txt in enumerate(num_strings):
            string = string.replace(num_txt, str(number + 1))
        print(string)
        cleaned_input.append([string])

    sum = calibration_value(cleaned_input)

    print("Part 2 Answer: ", sum)


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/01.txt"
lines = data_import(test_file, str, " ")
# part1(lines)
part2(lines)
