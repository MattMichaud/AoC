test = "test.txt"
puzzle = "2022/inputs/18.txt"
current = puzzle

droplets = open(current, "r").read().strip().split("\n")
droplets = set(tuple(map(int, droplet.split(","))) for droplet in droplets)


def tuple_add(a, b):
    return tuple(map(sum, zip(a, b)))


def get_neighbors(d):
    offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    n = set(tuple_add(d, o) for o in offsets)
    return n


exposed_faces = 0
for current_droplet in droplets:
    neighbors = get_neighbors(current_droplet)
    for n in neighbors:
        if n not in droplets:
            exposed_faces += 1

print("Part 1:", exposed_faces)

# think about it like spreading lava in minecraft :D

# pick locations for lava source block that are on the outside
min_x = min(x for x, *_ in droplets) - 1
max_x = max(x for x, *_ in droplets) + 1
min_y = min(y for _, y, _ in droplets) - 1
max_y = max(y for _, y, _ in droplets) + 1
min_z = min(z for *_, z in droplets) - 1
max_z = max(z for *_, z in droplets) + 1

lava_source1 = (min_x, min_y, min_z)
lava_source2 = (max_x, max_y, max_z)

lava_blocks = set()
lava_blocks.add(lava_source1)
lava_blocks.add(lava_source2)

# expand each source block into its neighbors, unless
# the neighbor is outside the boundary, or is a droplet
added_blocks = True
while added_blocks:
    new_lava_blocks = set()
    for lb in lava_blocks:
        neighbors = get_neighbors(lb)
        for n in neighbors:
            if (
                n not in droplets
                and min_x <= n[0] <= max_x
                and min_y <= n[1] <= max_y
                and min_z <= n[2] <= max_z
            ):
                new_lava_blocks.add(n)
    # if we aren't adding any new blocks, then we are done filling
    if new_lava_blocks.issubset(lava_blocks):
        added_blocks = False
    lava_blocks = lava_blocks.union(new_lava_blocks)


# now just check each droplet's neighbors and count if they are in the lava
touching_lava = 0
for droplet in droplets:
    for n in get_neighbors(droplet):
        if n in lava_blocks:
            touching_lava += 1

print("Part 2:", touching_lava)
