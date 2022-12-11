import math
import re


def parse_input(filename):
    res = {}
    data = open(filename, "r").read().strip().split("\n")
    cleaned_data = [line for line in data if line != ""]
    for i in range(len(cleaned_data) // 6):
        offset = i * 6
        inv = list(map(int, re.findall("\d+", cleaned_data[offset + 1])))
        operation = cleaned_data[offset + 2].replace("  Operation: new = ", "")
        func = eval("lambda old: " + operation)
        div = int(cleaned_data[offset + 3].replace("  Test: divisible by ", ""))
        t = int(cleaned_data[offset + 4].replace("    If true: throw to monkey ", ""))
        f = int(cleaned_data[offset + 5].replace("    If false: throw to monkey ", ""))
        res[i] = Monkey(inv, func, div, t, f)
    return res


class Monkey:
    def __init__(
        self, starting_items, operation, test_divisor, true_monkey, false_monkey
    ):
        self.items = starting_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.items_inspected = 0

    def add_item(self, item):
        self.items.append(item)

    def process_items(self, mkeys, factor=None):
        for i in range(len(self.items)):
            self.items_inspected += 1
            item = self.items.pop(0)
            item = self.operation(item)
            if factor == None:
                item = item // 3
            else:
                item = item % factor
            if item % self.test_divisor == 0:
                mkeys[self.true_monkey].add_item(item)
            else:
                mkeys[self.false_monkey].add_item(item)


test_input = "test.txt"
puzzle_input = "2022/inputs/11.txt"
current_input = puzzle_input

ml = parse_input(current_input)
part2 = False
for r in range(20):
    for m in ml.values():
        m.process_items(ml)
inspected = sorted([m.items_inspected for m in ml.values()])
print("Part 1:", inspected[-1] * inspected[-2])

ml = parse_input(current_input)
part2 = True
lcm = math.prod(set(m.test_divisor for m in ml.values()))
for r in range(10000):
    for m in ml.values():
        m.process_items(ml, lcm)
inspected = sorted([m.items_inspected for m in ml.values()])
print("Part 2:", inspected[-1] * inspected[-2])
