test_input = "test.txt"
puzzle_input = "2022/inputs/09.txt"
filename = puzzle_input

data = open(filename, "r").read().strip().split("\n")
head_moves = []
for dir, len in [d.split() for d in data]:
    [head_moves.append(dir) for _ in range(int(len))]


def sign(x):
    return (x > 0) - (x < 0)


head = (0, 0)
tail = (0, 0)
tail_visited = {}

dir_lookup = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

for m in head_moves:
    dx, dy = dir_lookup[m]
    head = (head[0] + dx, head[1] + dy)
    gap_x = head[0] - tail[0]
    gap_y = head[1] - tail[1]
    if gap_x == 0 and gap_y in [2, -2]:
        tail = (tail[0], tail[1] + gap_y // 2)
    elif gap_y == 0 and gap_x in [2, -2]:
        tail = (tail[0] + gap_x // 2, tail[1])
    elif abs(gap_x) <= 1 and abs(gap_y) <= 1:
        next
    else:
        tail = (tail[0] + sign(gap_x), tail[1] + sign(gap_y))
    tail_visited[tail] = True


total_visited = sum(1 for k in tail_visited.keys())
print("Part 1:", total_visited)

knots = [(0, 0)] * 10
tail_visited = {}

for m in head_moves:
    dx, dy = dir_lookup[m]
    knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
    for t in range(1, 10):
        gap_x = knots[t - 1][0] - knots[t][0]
        gap_y = knots[t - 1][1] - knots[t][1]

        if gap_x == 0 and gap_y in [2, -2]:
            knots[t] = (knots[t][0], knots[t][1] + gap_y // 2)
        elif gap_y == 0 and gap_x in [2, -2]:
            knots[t] = (knots[t][0] + gap_x // 2, knots[t][1])
        elif abs(gap_x) <= 1 and abs(gap_y) <= 1:
            next
        else:
            knots[t] = (knots[t][0] + sign(gap_x), knots[t][1] + sign(gap_y))
    tail_visited[knots[9]] = True

total_visited = sum(1 for k in tail_visited.keys())
print("Part 2:", total_visited)
