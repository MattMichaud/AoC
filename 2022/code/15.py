import re

test_input = "test.txt"
puzzle_input = "2022/inputs/15.txt"
current_input = puzzle_input
TARGET_ROW = 2000000
MAX_X = MAX_Y = 4000000

sensor_data = [
    list(map(int, re.findall("-?\d+", line)))
    for line in open(current_input, "r").read().strip().split("\n")
]


def m_distance(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


def count_no_beacons(sensors, row):
    no_beacon_sets = []  # tuples of (from_x, to_x) marking spots with no beacons
    for sensor_x, sensor_y, beacon_x, beacon_y in sensors:
        # find spots on target_row that can't be beacons
        beacon_dist = m_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
        dist_to_target_row = m_distance((sensor_x, sensor_y), (sensor_x, row))
        extra_length = beacon_dist - dist_to_target_row
        if extra_length > 0:
            no_beacon_sets.append(
                set(range(sensor_x - extra_length, sensor_x + extra_length + 1))
            )
    beacons_on_target_row = set([bx for sx, sy, bx, by in sensors if by == row])
    no_beacon_count = len(set.union(*no_beacon_sets) - beacons_on_target_row)
    return no_beacon_count


part1 = count_no_beacons(sensor_data, TARGET_ROW)
print("Part 1:", part1)


sensors_with_radius = [
    (sx, sy, m_distance((sx, sy), (bx, by))) for sx, sy, bx, by in sensor_data
]
for sensor in sensors_with_radius:
    sx, sy, radius = sensor
    # find points just outside sensor range
    border_points = set()
    for dx in range(radius + 2):
        dy = radius + 1 - dx
        border_points.add((sx + dx, sy + dy))
        border_points.add((sx - dx, sy + dy))
        border_points.add((sx + dx, sy - dy))
        border_points.add((sx - dx, sy - dy))
    border_points = set(
        (x, y) for x, y in border_points if 0 <= x <= MAX_X and 0 <= y <= MAX_Y
    )
    # check those points if they are in another sensor
    for x, y in border_points:
        in_other_sensor_range = all(
            m_distance((x, y), (sx, sy)) > r for sx, sy, r in sensors_with_radius
        )
        if in_other_sensor_range:
            tuning_frequency = x * 4000000 + y
            print("Part 2:", tuning_frequency)
            exit()
