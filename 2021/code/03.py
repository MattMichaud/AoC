import sys

sys.path.append(".")
from utils import data_import

data = data_import("2021/inputs/03.txt")

gamma = "".join(max(x, key=x.count) for x in zip(*data))
epsilon = "".join(min(x, key=x.count) for x in zip(*data))
print("Part 1:", int(gamma, 2) * int(epsilon, 2))


pos = 0
while len(data) > 1:
    filter_bit = "".join(n[pos] for n in data)
    bit_criteria = "0" if filter_bit.count("0") > filter_bit.count("1") else "1"
    data = [n for n in data if n[pos] == bit_criteria]
    pos += 1
oxygen_generator_rating = int(data[0], 2)

data = data_import("2021/inputs/03.txt")
pos = 0
while len(data) > 1:
    filter_bit = "".join(n[pos] for n in data)
    bit_criteria = "0" if filter_bit.count("0") <= filter_bit.count("1") else "1"
    data = [n for n in data if n[pos] == bit_criteria]
    pos += 1
co2_scrubber_rating = int(data[0], 2)

print("Part 2:", oxygen_generator_rating * co2_scrubber_rating)
