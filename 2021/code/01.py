import sys

sys.path.append(".")
from utils import data_import


def count_increases(depths):
    return sum(depths[i] > depths[i - 1] for i in range(1, len(depths)))


def count_window_increasses(depths):
    return sum(depths[i] > depths[i - 3] for i in range(3, len(depths)))


report = data_import("test.txt", int)
report = data_import("2021/inputs/01.txt", int)
print("Part 1:", count_increases(report))
print("Part 2:", count_window_increasses(report))
