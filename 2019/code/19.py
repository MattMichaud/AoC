import sys
sys.path.append('.')
from intcode import IntCodeComputer, parse_intcode
from utils import tuple_add

def inbeam_gen(program):
    def inbeam(point):
        comp = IntCodeComputer(program)
        comp.add_input(point[0])
        comp.add_input(point[1])
        comp.compute()
        return comp.pop_output()
    return inbeam

def part1(program, grid_size=50):
    inbeam = inbeam_gen(program)
    return sum(inbeam((x,y)) for x in range(grid_size) for y in range(grid_size))

def part2(program, bottom_left=(0,10), ship_size=100):
    inbeam = inbeam_gen(program)
    coord_diff = ship_size - 1

    while True:
        if inbeam(bottom_left):
            top_right = tuple_add(bottom_left, (coord_diff, -coord_diff))
            if inbeam(top_right):
                top_left = tuple_add(bottom_left, (0, -coord_diff))
                return 10000 * top_left[0] + top_left[1]

            bottom_left = tuple_add(bottom_left, (0,1)) # move down
        else:
            bottom_left = tuple_add(bottom_left, (1,0)) # move right

code = parse_intcode('2019/inputs/19.txt')
print(f'Part 1 Answer: {part1(code)}')
print(f'Part 2 Answer: {part2(code)}')
