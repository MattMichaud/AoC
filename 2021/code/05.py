import re
import collections as cl

input_file = "test.txt"
input_file = "2021/inputs/05.txt"
lines = [
    tuple(map(int, re.findall(r"\d+", line)))
    for line in open(input_file).read().split("\n")
][:-1]
h_lines = [ln for ln in lines if ln[1] == ln[3]]
v_lines = [ln for ln in lines if ln[0] == ln[2]]
d_lines = [ln for ln in lines if (ln[0] != ln[2]) and (ln[1] != ln[3])]

intersects = cl.defaultdict(int)
for (x1, y1, x2, y2) in h_lines:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        intersects[x, y1] += 1

for (x1, y1, x2, y2) in v_lines:
    for y in range(min(y1, y2), max(y1, y2) + 1):
        intersects[x1, y] += 1

print("Part 1:", sum(x > 1 for x in intersects.values()))

for (x1, y1, x2, y2) in d_lines:
    dx = (x2 > x1) - (x1 > x2)
    dy = (y2 > y1) - (y1 > y2)
    for d in range(abs(x2 - x1) + 1):
        intersects[x1 + dx * d, y1 + dy * d] += 1

print("Part 2:", sum(x > 1 for x in intersects.values()))
