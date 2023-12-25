import sys

sys.path.append(".")
from itertools import combinations
from utils import tuple_add as addt
from z3 import *


def parse_input(filename):
    data = open(filename, "r").read().splitlines()
    hailstones = []
    for line in data:
        coords, velocity = line.split("@ ")
        (x, y, z) = (int(c) for c in coords.split(", "))
        (dx, dy, dz) = (int(c) for c in velocity.split(", "))
        hailstones.append((x, y, z, dx, dy, dz))
    return hailstones


def line(p1, p2):
    A = p1[1] - p2[1]
    B = p2[0] - p1[0]
    C = p1[0] * p2[1] - p2[0] * p1[1]
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def count_valid_intersections(hailstones, min, max):
    index_pairs = combinations(range(len(hailstones)), 2)
    valid_intersections = 0
    for i, j in index_pairs:
        pt1 = (hailstones[i][0], hailstones[i][1])
        velocity1 = (hailstones[i][3], hailstones[i][4])
        pt2 = addt(pt1, velocity1)
        line1 = line(pt1, pt2)
        pt3 = (hailstones[j][0], hailstones[j][1])
        velocity2 = (hailstones[j][3], hailstones[j][4])
        pt4 = addt(pt3, velocity2)
        line2 = line(pt3, pt4)
        intersect = intersection(line1, line2)
        if intersect:
            x, y = intersect
            future_a = (x > pt1[0]) == (pt2[0] > pt1[0])
            future_b = (x > pt3[0]) == (pt4[0] > pt3[0])
            if min <= x <= max and min <= y <= max and future_a and future_b:
                valid_intersections += 1
    return valid_intersections


def part2(hailstones):
    # use z3 solver to solve system of linear equations
    total_hail = len(hailstones)
    # initialize variables for z3 to solve for
    x, y, z, dx, dy, dz = Int("x"), Int("y"), Int("z"), Int("dx"), Int("dy"), Int("dz")
    # time variable for when each hailstone collides with our new hailstone
    T = [Int(f"T{i}") for i in range(total_hail)]
    SOLVE = Solver()
    # for each hailstone, at some time, our new hailstone will have the same position
    # our new hailstone is at (x + time * dx, y + time * dy, z + time * dz)
    # existing hailstone is at (x1 + time * v1, y1 + time * v2, z1 + time * v3)
    for i in range(total_hail):
        SOLVE.add((x + T[i] * dx) - (hailstones[i][0] + T[i] * hailstones[i][3]) == 0)
        SOLVE.add((y + T[i] * dy) - (hailstones[i][1] + T[i] * hailstones[i][4]) == 0)
        SOLVE.add((z + T[i] * dz) - (hailstones[i][2] + T[i] * hailstones[i][5]) == 0)
    # solve and save model
    res = SOLVE.check()
    M = SOLVE.model()
    return M.eval(x + y + z)


def part1_z3(hailstones, min, max):
    # using z3 for part1, but it is super slow
    # sticking with original method of calculations
    index_pairs = combinations(range(len(hailstones)), 2)
    valid_intersections = 0
    for i, j in index_pairs:
        t1, t2 = Real("t1"), Real("t2")
        x, y = Real("x"), Real("y")
        SOLVE = Solver()
        SOLVE.add(x - (hailstones[i][0] + t1 * hailstones[i][3]) == 0)
        SOLVE.add(x - (hailstones[j][0] + t2 * hailstones[j][3]) == 0)
        SOLVE.add(y - (hailstones[i][1] + t1 * hailstones[i][4]) == 0)
        SOLVE.add(y - (hailstones[j][1] + t2 * hailstones[j][4]) == 0)
        SOLVE.add(t1 > 0)
        SOLVE.add(t2 > 0)
        res = SOLVE.check()
        if res != unsat:
            M = SOLVE.model()
            xpos = M.eval(x).as_fraction()
            xpos = xpos.numerator / xpos.denominator
            ypos = M.eval(y).as_fraction()
            ypos = ypos.numerator / ypos.denominator
            if min <= xpos <= max and min <= ypos <= max:
                valid_intersections += 1
    print(valid_intersections)


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/24.txt"
filename = puzzle

hail = parse_input(filename)
min = 200000000000000 if filename == puzzle else 7
max = 400000000000000 if filename == puzzle else 27
print("Part 1:", count_valid_intersections(hail, min, max))
print("Part 2:", part2(hail))
# part1_z3(hail, min, max)
