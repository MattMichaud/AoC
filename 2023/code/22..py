from collections import defaultdict
from copy import deepcopy


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


def drop_all_blocks(blocks):
    keep_dropping = True
    unique_dropped = set()  # for part 2
    while keep_dropping:
        blocks_dropped = 0

        # initialize occupied set
        occupied = set()
        for block in blocks:
            for x, y, z in block:
                occupied.add((x, y, z))

        # try to move each block in the list
        for i, block in enumerate(blocks):
            can_move = True
            for x, y, z in block:
                if z == 1:
                    # already at the bottom - don't drop
                    can_move = False
                if (x, y, z - 1) in occupied and (x, y, z - 1) not in block:
                    # would hit another block - don't drop
                    can_move = False
            if can_move:
                blocks_dropped += 1
                unique_dropped.add(i)  # for part 2
                # move each point down one
                for x, y, z in block:
                    occupied.discard((x, y, z))
                    occupied.add((x, y, z - 1))
                # update the list of where the blocks are
                blocks[i] = [(x, y, z - 1) for x, y, z in block]

        # if nothing fell, stop dropping and return
        if blocks_dropped == 0:
            keep_dropping = False
    return blocks, unique_dropped


def count_safely_movable(blocks):
    critical_blocks = set()
    # figure out which blocks are below each block
    for i, block in enumerate(blocks):
        blocks_below = set()
        for x, y, z in block:
            for j, jblock in enumerate(blocks):
                if i != j and (x, y, z - 1) in jblock:
                    blocks_below.add(j)
        # if only one block below, that block is critical
        if len(blocks_below) == 1:
            critical_blocks.add(blocks_below.pop())
    # total - critical = safe to move
    return len(blocks) - len(critical_blocks)


def biggest_chain_reaction(blocks):
    total = 0
    for i in range(len(blocks)):
        # remove the block
        temp_blocks = deepcopy(blocks)
        temp_blocks = temp_blocks[0:i] + temp_blocks[i + 1 :]
        # drop blocks
        _, uniques = drop_all_blocks(temp_blocks)
        # count uniques that fell
        total += len(uniques)
    return total


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/22.txt"
filename = puzzle

blocks, _ = drop_all_blocks(parse_input(filename))
print("Part 1:", count_safely_movable(blocks))
print("Part 2:", biggest_chain_reaction(blocks))
