import sys

sys.path.append(".")
from utils import data_import


def translate_command(command):
    direction, distance = command.split(" ")
    distance = int(distance)
    if direction == "forward":
        return distance, 0
    if direction == "down":
        return 0, distance
    if direction == "up":
        return 0, -1 * distance


def move_sub(horizontal_start, depth_start, commands):
    h, d = horizontal_start, depth_start
    for comm in commands:
        dh, dd = translate_command(comm)
        h += dh
        d += dd
    return h, d


def part1(commands):
    h, d = move_sub(0, 0, commands_input)
    print("Part 1:", h * d)


def move_sub_with_aim(horizontal_start, depth_start, aim_start, commands):
    h, d, a = horizontal_start, depth_start, aim_start
    for comm in commands:
        horizontal_distance, aim_change = translate_command(comm)
        a += aim_change
        h += horizontal_distance
        d += a * horizontal_distance
    return h, d


def part2(commands):
    h, d = move_sub_with_aim(0, 0, 0, commands)
    print("Part 2:", h * d)


commands_input = data_import("test.txt")
commands_input = data_import("2021/inputs/02.txt")
part1(commands_input)
part2(commands_input)
