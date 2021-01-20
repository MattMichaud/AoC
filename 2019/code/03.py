import sys
import numpy as np
sys.path.append('.')
from utils import data_import, tuple_add

def build_wire(wire_instructions):
    offsets = {'R':(1,0), 'L':(-1,0), 'U':(0,1), 'D':(0,-1)}
    current_loc = (0,0)
    wire = []
    for inst in wire_instructions:
        direction = inst[0]
        distance = int(inst[1:])
        for i in range(distance):
            current_loc = tuple_add(current_loc, offsets[direction])
            wire.append(current_loc)
    return(wire)

def part1(filename, print_result=True):
    wire_instructions = data_import(filename, str, ',')
    wires = []
    wires_list = []
    for wire_instruction in wire_instructions:
        w = build_wire(wire_instruction)
        wires.append(set(w))
        wires_list.append(w)
    intersections = set.intersection(*wires)
    distances = [abs(x) + abs(y) for x,y in intersections]
    if print_result: print('Part 1 Answer:', min(distances))
    return(wires_list, intersections)

def part2(filename):
    wires, intersections = part1(filename, True)
    signal_delays = []
    for intersection in intersections:
        delay = 0
        for wire in wires:
            delay += wire.index(intersection) + 1
        signal_delays.append(delay)
    print('Part 2 Answer:',min(signal_delays))

filename = '2019/inputs/03.txt'
part2(filename)