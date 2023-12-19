from math import gcd


def data_import(filename, cast=str, split_char=None, rstrip=False):
    data = []
    with open(filename) as file:
        line = file.readline()
        while line:
            if rstrip and line.rstrip() or line.strip():
                if split_char is not None:
                    line = line.split(split_char)
                    data.append([cast(item.strip()) for item in line])
                else:
                    data.append(cast(rstrip and line.rstrip() or line.strip()))

            line = file.readline()
    return data


def tuple_add(a, b):
    return tuple(map(sum, zip(a, b)))


def read_intcode(file) -> list:
    with open(file) as f:
        return list(map(int, f.read().split(",")))


def read_map(file) -> list:
    with open(file) as f:
        return [list(line.rstrip("\n")) for line in f.readlines()]


def lcm(li):
    lcm = li[0]
    for i in li[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def shoelace_area(coords):
    # uses shoelace formula and pick's theorem
    # to calculate points in the area and perimeter
    area = 0
    perim = 0
    # shoelace formula (trapezoid version)
    for i in range(1, len(coords)):
        x1, y1 = coords[i - 1]
        x2, y2 = coords[i]
        area += (y1 + y2) * (x1 - x2)
        perim += abs(x1 - x2) + abs(y1 - y2)
    area = abs(area) // 2
    # pick's theorem
    interior = area - (perim) // 2 + 1
    # total points indside and on perimeter
    return interior + perim
