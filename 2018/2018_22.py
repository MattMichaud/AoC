def build_cave(depth, target, max_size=None):
    cave = {}

    if max_size is None:
        max_size = target

    for i in range(0, max_size[0] + 1):
        for j in range(0, max_size[1] + 1):
            if i == target[0] and j == target[1]:
                cave[i, j] = {'index': 0}
            elif i == 0:
                cave[i, j] = {'index': 48271 * j}
            elif j == 0:
                cave[i, j] = {'index': 16807 * i}
            else:
                cave[i, j] = {'index': cave[i-1, j]['level'] * cave[i, j-1]['level']}

            cave[i, j]['level'] = (cave[i, j]['index'] + depth) % 20183
            cave[i, j]['erosion'] = cave[i,j]['level'] % 3

    return cave

elts = {0: '.', 1: '=', 2: '|'}

def show_cave(cave, target):
    for j in range(0, target[0] + 1):
        line = ''
        for i in range(0, target[1] + 1):
            if i == 0 and j == 0: line += 'M'
            elif (i, j) == target: line += 'T'
            else: line += elts[cave[i, j]['erosion']]
        print(line)

def part1(depth, target):
    cave = build_cave(depth, target)
    res = sum(
        cave[i, j]['erosion']
        for i in range(target[0] + 1)
        for j in range(target[1] + 1)
    )
    return res

TORCH = 1
CLIMB = 2
NEITHER = 3

ROCKY = 0
WET = 1
NARROW = 2

ALLOWED_TOOLS = {
    ROCKY: (TORCH, CLIMB),
    WET: (CLIMB, NEITHER),
    NARROW: (TORCH, NEITHER),
}

def part2(depth, target):

    if target[0] > target[1]:
        max_size = (target[0] * 2, target[1] * 5)
    else:
        max_size = (target[0] * 5, target[1] * 2)

    cave = {
        key: value['erosion']
        for key, value in build_cave(depth, target, max_size).items()
    }

    target = (target[0], target[1], TORCH)

    distances = {}

    todo = {((0, 0, TORCH), 0)}

    while todo:
        cell, distance = todo.pop()
        if cell in distances and distance > distances[cell]:
            continue

        distances[cell] = distance

        if target in distances and distance > distances[target]:
            continue

        tool = cell[2]

        for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if cell[0] + i < 0 or cell[1] + j < 0:
                continue
            if cell[0] + i > max_size[0] or cell[1] + j > max_size[1]:
                continue
            if tool in ALLOWED_TOOLS[cave[cell[0] + i, cell[1] + j]]:
                todo.add(((cell[0] + i, cell[1] + j, tool), distance + 1))

        if cave[cell[:2]] == ROCKY:
            if tool == TORCH:
                tool = CLIMB
            else:
                tool = TORCH
        elif cave[cell[:2]] == WET:
            if tool == CLIMB:
                tool = NEITHER
            else:
                tool = CLIMB
        elif cave[cell[:2]] == NARROW:
            if tool == TORCH:
                tool = NEITHER
            else:
                tool = TORCH

        todo.add(((cell[0], cell[1], tool), distance + 7))

    return distances[target]


depth = 6969
target = (9, 796)
print('Part 1 Answer:', part1(depth, target))
print('Part 2 Answer:', part2(depth, target))