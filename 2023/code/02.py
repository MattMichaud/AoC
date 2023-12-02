import sys

sys.path.append(".")
from utils import data_import


def parse_input(filename):
    with open(filename, "r") as f:
        data = f.read().splitlines()
    sum = 0
    part2 = 0
    for l in data:
        game_index = int(l[5 : l.find(":")])
        possible = True
        min_red = min_green = min_blue = 0
        pulls = l[l.find(":") + 2 :].split("; ")
        for p in pulls:
            balls = p.split(", ")
            for b in balls:
                parts = b.split(" ")
                count = int(parts[0])
                color = parts[1]
                if (
                    (color == "red" and count > 12)
                    or (color == "green" and count > 13)
                    or (color == "blue" and count > 14)
                ):
                    possible = False
                if color == "red" and count > min_red:
                    min_red = count
                if color == "green" and count > min_green:
                    min_green = count
                if color == "blue" and count > min_blue:
                    min_blue = count
        if possible:
            sum += game_index
        power = min_red * min_green * min_blue
        part2 += power
    print(sum, part2)
    return data


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/02.txt"
current_file = puzzle_file
inp = parse_input(current_file)
