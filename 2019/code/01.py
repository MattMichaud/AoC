import sys
sys.path.append('.')
from utils import data_import


def part1(masses):
    fuel = [(mass // 3) - 2 for mass in masses]
    print('Part 1 Answer:', sum(fuel))

def part2(masses):
    fuel = []
    while masses:
        current_mass = masses.pop()
        new_fuel = (current_mass // 3) - 2
        if new_fuel > 0:
            fuel.append(new_fuel)
            masses.append(new_fuel)
    print('Part 2 Answer:',sum(fuel))

masses = data_import('2019/inputs/01.txt', int)
part1(masses)
part2(masses)