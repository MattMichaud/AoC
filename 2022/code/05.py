import sys

sys.path.append(".")
from utils import data_import


def parse_moves(li):
    res = []
    for l in li:
        l = l.replace("move ", "").replace(" from ", ",").replace(" to ", ",")
        l = l.split(",")
        l = [eval(i) for i in l]
        res.append(l)
    return res


def accomplish_moves(crates, moves):
    for m in moves:
        qty = m[0]
        source = m[1]
        dest = m[2]
        for i in range(qty):
            crate = crates[source].pop()
            crates[dest].append(crate)
    return crates


def accomplish_moves_multiple(crates, moves):
    for m in moves:
        qty = m[0]
        source = m[1]
        dest = m[2]
        moved = crates[source][-1 * qty :]
        crates[source] = crates[source][: -1 * qty]
        crates[dest] = crates[dest] + moved
    return crates


def part1(crates, moves):
    crates = accomplish_moves(crates, moves)
    res = ""
    for stack in crates[1:]:
        res += stack[-1]
    print("Part 1 Answer:", res)


def part2(crates, moves):
    crates = accomplish_moves_multiple(crates, moves)
    res = ""
    for stack in crates[1:]:
        res += stack[-1]
    print("Part 2 Answer:", res)


# input_file = "2022/inputs/test.txt"
input_file = "2022/inputs/05.txt"

test_crates = [[], ["Z", "N"], ["M", "C", "D"], ["P"]]
crates = [
    [],
    ["C", "Z", "N", "B", "M", "W", "Q", "V"],
    ["H", "Z", "R", "W", "C", "B"],
    ["F", "Q", "R", "J"],
    ["Z", "S", "W", "H", "F", "N", "M", "T"],
    ["G", "F", "W", "L", "N", "Q", "P"],
    ["L", "P", "W"],
    ["V", "B", "D", "R", "G", "C", "Q", "J"],
    ["Z", "Q", "N", "B", "W"],
    ["H", "L", "F", "C", "G", "T", "J"],
]

data = data_import(input_file)
moves = parse_moves(data)
part1(crates, moves)

test_crates = [[], ["Z", "N"], ["M", "C", "D"], ["P"]]
crates = [
    [],
    ["C", "Z", "N", "B", "M", "W", "Q", "V"],
    ["H", "Z", "R", "W", "C", "B"],
    ["F", "Q", "R", "J"],
    ["Z", "S", "W", "H", "F", "N", "M", "T"],
    ["G", "F", "W", "L", "N", "Q", "P"],
    ["L", "P", "W"],
    ["V", "B", "D", "R", "G", "C", "Q", "J"],
    ["Z", "Q", "N", "B", "W"],
    ["H", "L", "F", "C", "G", "T", "J"],
]
part2(crates, moves)
