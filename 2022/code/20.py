import sys

sys.path.append(".")
from utils import data_import
from linked_list import CircularDoublyLinkedList, Node


def parse_input(f):
    return [int(line) for line in open(f, "r").read().strip().split("\n")]


def part1(inp):

    number_list = CircularDoublyLinkedList()
    node_pointers = {}
    for i, n in enumerate(inp):
        new_node = Node(n)
        number_list.insert_at_end(new_node)
        node_pointers[i] = new_node
        if n == 0:
            zero_node_loc = i

    for i in range(len(inp)):
        node_to_move = node_pointers[i]
        node_value = node_to_move.data
        move_dist = abs(node_value) % (len(input) - 1)
        if node_value < 0:
            number_list.remove(node_to_move)
            ref_node = node_to_move.traverse_back(move_dist)
            number_list.insert_before(ref_node, node_to_move)
        elif node_value > 0:
            number_list.remove(node_to_move)
            ref_node = node_to_move.traverse_forward(move_dist)
            number_list.insert_after(ref_node, node_to_move)
        else:  # no movement
            next

    # find 0 node
    zero_node = node_pointers[zero_node_loc]
    return sum(zero_node.traverse_forward(i * 1000).data for i in [1, 2, 3])


def part2(inp, key, mixes):

    number_list = CircularDoublyLinkedList()
    node_pointers = {}
    for i, n in enumerate(inp):
        new_node = Node(n * key)
        number_list.insert_at_end(new_node)
        node_pointers[i] = new_node
        if n == 0:
            zero_node_loc = i

    for mix in range(mixes):
        for i in range(len(inp)):
            node_to_move = node_pointers[i]
            node_value = node_to_move.data
            move_dist = abs(node_value) % (len(input) - 1)
            if node_value < 0:
                number_list.remove(node_to_move)
                ref_node = node_to_move.traverse_back(move_dist)
                number_list.insert_before(ref_node, node_to_move)
            elif node_value > 0:
                number_list.remove(node_to_move)
                ref_node = node_to_move.traverse_forward(move_dist)
                number_list.insert_after(ref_node, node_to_move)
            else:  # no movement
                next

    # find 0 node
    zero_node = node_pointers[zero_node_loc]
    return sum(zero_node.traverse_forward(i * 1000).data for i in [1, 2, 3])


test = "test.txt"
puzzle = "2022/inputs/20.txt"
curr_file = puzzle

input = parse_input(curr_file)
print("Part 1:", part1(input))
print("Part 2:", part2(input, 811589153, 10))
