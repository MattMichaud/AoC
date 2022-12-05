import sys

sys.path.append(".")
from utils import data_import


def get_start_end(pair):
    hyphen_loc = pair.find("-")
    start = int(pair[:hyphen_loc])
    end = int(pair[hyphen_loc + 1 :])
    return start, end


def part1(pairs):
    count = 0
    for p1, p2 in pairs:
        p1_start, p1_end = get_start_end(p1)
        p2_start, p2_end = get_start_end(p2)
        if (p1_start >= p2_start and p1_end <= p2_end) or (
            p2_start >= p1_start and p2_end <= p1_end
        ):
            count += 1
    print("Part 1 Answer:", count)


def part2(pairs):
    count = 0
    for p1, p2 in pairs:
        p1_start, p1_end = get_start_end(p1)
        p2_start, p2_end = get_start_end(p2)
        if (
            (p1_start >= p2_start and p1_start <= p2_end)
            or (p1_end >= p2_start and p1_end <= p2_end)
            or (p2_start >= p1_start and p2_start <= p1_end)
            or (p2_end >= p1_start and p2_end <= p1_end)
        ):
            count += 1
    print("Part 2 Answer:", count)


input_file = "2022/inputs/test.txt"
input_file = "2022/inputs/04.txt"
data = data_import(input_file, split_char=",")
part1(data)
part2(data)
