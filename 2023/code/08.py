import sys

sys.path.append(".")
from utils import lcm


def parse_input(filename):
    inst, node_lines = open(filename, "r").read().strip().split("\n\n")
    nodes = {}
    for node in node_lines.split("\n"):
        name, leftright = node.split(" = ")
        leftright = leftright.replace("(", "").replace(")", "")
        left, right = leftright.split(", ")
        nodes[name] = {"L": left, "R": right}
    return inst, nodes


def count_steps(inst, nodes, start_loc="AAA", dest_locs=["ZZZ"]):
    step = 0
    max_steps = 1000000
    curr_loc = start_loc
    while curr_loc not in dest_locs and step < max_steps:
        dir = inst[step % len(inst)]
        curr_loc = nodes[curr_loc][dir]
        step += 1
    return step


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/08.txt"
current_file = puzzle_file
inst, nodes = parse_input(current_file)
print("Part 1:", count_steps(inst, nodes))
start_nodes = [k for k in nodes.keys() if k.endswith("A")]
end_nodes = [k for k in nodes.keys() if k.endswith("Z")]
convergence = lcm([count_steps(inst, nodes, sn, end_nodes) for sn in start_nodes])
print("Part 2:", convergence)
