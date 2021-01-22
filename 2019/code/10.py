import math

def init_asteroids(filename):
    with open(filename, 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, a in enumerate(line):
                if a == '#':
                    yield (x, y)

def angle(start, end):
    result = math.atan2(end[0] - start[0], start[1] - end[1]) * 180 / math.pi
    if result < 0:
        return 360 + result
    return result

def find_station(asteroids):
    station = None
    max_count = 0
    for asteroid in asteroids:
        count = len({angle(asteroid, target) for target in asteroids if asteroid != target})
        if count > max_count:
            max_count = count
            station = asteroid
    print('Part 1 Answer:',max_count)
    return station

def vaporize(station, asteroids, target_count):
    asteroids.remove(station)
    angles = sorted(
        ((angle(station, target), target) for target in asteroids), key=lambda x: (x[0], abs(station[0] - x[1][0]) + abs(station[1] - x[1][1]))
    )

    idx = 0
    last_target = angles.pop(idx)
    last_angle = last_target[0]
    vaporized_count = 1

    while vaporized_count < target_count and angles:
        if idx >= len(angles):
            idx = 0
            last_angle = None
        if last_angle == angles[idx][0]:
            idx += 1
            continue
        last_target = angles.pop(idx)
        last_angle = last_target[0]
        vaporized_count += 1
    print('Part 2 Answer:', last_target[1][0] * 100 + last_target[1][1])
    return last_target[1]

filename = '2019/inputs/10.txt'
asteroids = list(init_asteroids(filename))
station = find_station(asteroids)
vaporize(station, asteroids, 200)