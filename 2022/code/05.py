import sys

sys.path.append(".")
from utils import data_import


def parse_input(filename):
    crate_lines = []
    move_lines = []
    with open(filename) as file:
        data = file.read().splitlines()
    for line in data:
        if line == "":
            continue
        elif line[0] == "m":
            move_lines.append(line)
        elif line[1] == "1":
            total_crates = int(
                line.lstrip().rstrip().replace("   ", ",").split(",")[-1]
            )
        else:
            crate_lines.append(line)
    moves = parse_moves(move_lines)
    crates = parse_crates(crate_lines, total_crates)
    return moves, crates


def parse_crates(crate_list, total):
    crates = [[] for i in range(total + 1)]
    crate_list.reverse()
    for l in crate_list:
        for i in range(total):
            c = l[(i * 4) + 1]
            if c != " ":
                crates[i + 1].append(c)
    return crates


def parse_moves(move_list):
    res = []
    for l in move_list:
        l = l.replace("move ", "").replace(" from ", ",").replace(" to ", ",")
        l = l.split(",")
        l = [eval(i) for i in l]
        res.append(l)
    return res


def accomplish_moves(crates, moves, keepOrder=False):
    for m in moves:
        qty, source, dest = m
        temp_list = []
        for i in range(qty):
            crate = crates[source].pop()
            temp_list.append(crate)
        if keepOrder:
            temp_list.reverse()
        crates[dest] = crates[dest] + temp_list
    return crates


def get_top_letters(crates):
    res = ""
    for stack in crates[1:]:
        res += stack[-1]
    return res


def part1(crates, moves):
    crates = accomplish_moves(crates, moves)
    print("Part 1 Answer:", get_top_letters(crates))


def part2(crates, moves):
    crates = accomplish_moves(crates, moves, True)
    print("Part 2 Answer:", get_top_letters(crates))


input_file = "2022/inputs/05.txt"
moves, crates = parse_input(input_file)
part1(crates, moves)
moves, crates = parse_input(input_file)
part2(crates, moves)
