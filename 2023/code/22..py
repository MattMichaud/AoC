def parse_input(filename):
    data = open(filename, "r").read().splitlines()
    blocks = []
    for line in data:
        block = []
        start, end = line.split("~")
        start_x, start_y, start_z = (int(c) for c in start.split(","))
        end_x, end_y, end_z = (int(c) for c in end.split(","))
        block = [
            (x, y, z)
            for z in range(start_z, end_z + 1)
            for y in range(start_y, end_y + 1)
            for x in range(start_x, end_x + 1)
        ]
        blocks.append(block)
    return blocks


def drop_blocks(blocks):
    keep_dropping = True
    unique_dropped = set()  # for part 2
    any_dropped = True
    while any_dropped:
        # initialize state
        any_dropped = False
        occupied = set()
        for block in blocks:
            for x, y, z in block:
                occupied.add((x, y, z))

        # try to move each block in the list
        for i, block in enumerate(blocks):
            # make sure all points are either not at the bottom and won't hit another block
            if all(
                z != 1 and ((x, y, z - 1) not in occupied or (x, y, z - 1) in block)
                for x, y, z in block
            ):
                any_dropped = True  # need to keep trying to drop
                unique_dropped.add(i)  # for part 2
                # move each point down one
                for x, y, z in block:
                    occupied.discard((x, y, z))
                    occupied.add((x, y, z - 1))
                # update the list of where the blocks are
                blocks[i] = [(x, y, z - 1) for x, y, z in block]

    return unique_dropped


def solve(blocks):
    drop_blocks(blocks)
    safe_to_move = chain_reactions = 0
    for i in range(len(blocks)):
        moved = len(drop_blocks(blocks[0:i] + blocks[i + 1 :]))
        if moved == 0:
            safe_to_move += 1
        chain_reactions += moved
    print("Part 1:", safe_to_move)
    print("Part 2:", chain_reactions)


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/22.txt"
filename = puzzle

solve((parse_input(filename)))
