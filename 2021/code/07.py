import sys

sys.path.append(".")
from utils import data_import

test_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
filename = "2021/inputs/07.txt"
actual_input = [int(x) for x in open(filename, "r").read().strip().split(",")]
crab_locations = actual_input


def first_n_sum(n):
    return int(n * (n + 1) / 2)


min_fuel = None
for pos in range(min(crab_locations), max(crab_locations) + 1):
    fuel_needed = 0
    for loc in crab_locations:
        fuel_needed += abs(loc - pos)
    if min_fuel == None or fuel_needed < min_fuel:
        min_fuel = fuel_needed

print("Part 1:", min_fuel)

min_fuel = None
for pos in range(min(crab_locations), max(crab_locations) + 1):
    fuel_needed = 0
    for loc in crab_locations:
        fuel_needed += first_n_sum(abs(loc - pos))
    if min_fuel == None or fuel_needed < min_fuel:
        min_fuel = fuel_needed

print("Part 2:", min_fuel)
