from math import sqrt, floor, ceil


def parse_input(filename):
    times, distances = open(filename, "r").read().strip().split("\n")
    times = [int(t) for t in times.split()[1:]]
    distances = [int(d) for d in distances.split()[1:]]
    return times, distances


def list_to_int(li):
    return int("".join([str(l) for l in li]))


def quadratic_roots(a, b, c):
    return [
        (-b + sqrt(b**2 - (4 * a * c))) / (2 * a),
        (-b - sqrt(b**2 - (4 * a * c))) / (2 * a),
    ]


def count_winning_times(t, d):
    roots = sorted(quadratic_roots(-1, t, -(d + 0.000000000001)))
    return floor(roots[1]) - ceil(roots[0]) + 1


def part1(times, distances):
    total_times = [count_winning_times(t, d) for t, d in list(zip(times, distances))]
    result = 1
    for t in total_times:
        result = result * t
    return result


def part2(times, distances):
    t = float(list_to_int(times))
    d = float(list_to_int(distances))
    return count_winning_times(t, d)


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/06.txt"
current_file = puzzle_file
t, d = parse_input(current_file)
print("Part 1:", part1(t, d))
print("Part 2:", part2(t, d))
