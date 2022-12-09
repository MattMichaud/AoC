from itertools import chain


def sign(x):
    return (x > 0) - (x < 0)


def get_moves(filename):
    data = open(filename, "r").read().strip().split("\n")
    head_moves = []
    for dir, len in [d.split() for d in data]:
        for _ in range(int(len)):
            head_moves.append(dir)
    return head_moves


def track_tail(moves, num_knots):
    knots = [(0, 0)] * num_knots
    tail_locs = set()
    for m in moves:
        dx, dy = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}.get(m)
        knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
        for t in range(1, num_knots):
            gap_x = knots[t - 1][0] - knots[t][0]
            gap_y = knots[t - 1][1] - knots[t][1]
            if (gap_x == 0 and gap_y in [2, -2]) or (
                gap_y == 0 and gap_x in [2, -2]
            ):  # 2 apart horizontal or vertical
                knots[t] = (knots[t][0] + gap_x // 2, knots[t][1] + gap_y // 2)
            elif abs(gap_x) <= 1 and abs(gap_y) <= 1:  # adjacent
                next
            else:  # diagonal move
                knots[t] = (knots[t][0] + sign(gap_x), knots[t][1] + sign(gap_y))
        tail_locs.add(knots[num_knots - 1])
    return tail_locs


head_moves = get_moves("2022/inputs/09.txt")
print("Part 1:", len(track_tail(head_moves, 2)))
print("Part 2:", len(track_tail(head_moves, 10)))
