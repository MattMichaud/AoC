import sys

sys.path.append(".")
from utils import lcm


def parse_input(filename):
    data = open(filename, "r").read().strip().split("\n")
    lines = [[int(x) for x in line.split()] for line in data]
    return lines


def predict_next(li):
    diffs = [li[i + 1] - li[i] for i in range(len(li) - 1)]
    return li[-1] + (0 if all(v == 0 for v in diffs) else predict_next(diffs))


def predict_prev(li):
    diffs = [li[i + 1] - li[i] for i in range(len(li) - 1)]
    return li[0] - (0 if all(v == 0 for v in diffs) else predict_prev(diffs))


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/09.txt"
lines = parse_input(puzzle_file)
print("Part 1:", sum(predict_next(l) for l in lines))
print("Part 2:", sum(predict_prev(l) for l in lines))
