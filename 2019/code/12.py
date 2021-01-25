import sys
sys.path.append('.')
from utils import tuple_add
from typing import Tuple, List
from itertools import combinations
from math import gcd


class Moon:
    def __init__(self, name: str, position: Tuple[int, int, int]) -> None:
        self.name = name
        self.position = position
        self.velocity = [0, 0, 0]

    def __repr__(self) -> str:
        return '{:>8} ::: pos={} vel={}'.format(self.name, self.position, self.velocity)

    def potential_energy(self) -> int:
        return sum(abs(coord) for coord in self.position)

    def kinetic_energy(self) -> int:
        return sum(abs(coord) for coord in self.velocity)

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()


class PlanetSystem:
    def __init__(self, moon_list: List[Moon] = []) -> None:
        self.moons = []
        self.time = 0
        for moon in moon_list: self.add_moon(moon)

    def add_moon(self, moon: Moon) -> None:
        self.moons.append(moon)

    def display(self) -> None:
        print('After {} steps:'.format(self.time))
        for moon in self.moons: print(moon)
        print()

    def time_step(self) -> None:
        self.time += 1

        combos = combinations(self.moons, 2)
        for (moon1, moon2) in combos:
            for i in range(3):
                if moon1.position[i] < moon2.position[i]:
                    moon1.velocity[i] += 1
                    moon2.velocity[i] -= 1
                elif moon1.position[i] > moon2.position[i]:
                    moon1.velocity[i] -= 1
                    moon2.velocity[i] += 1

        for moon in self.moons:
            moon.position = tuple_add(moon.position, tuple(moon.velocity))

    def energy(self) -> int:
        return sum(moon.total_energy() for moon in self.moons)


def lcm(li: List[int]) -> int:
    lcm = li[0]
    for i in li[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return(lcm)


def part1():
    io = Moon('Io', (1, 3, -11))
    eurpoa = Moon('Eurpoa', (17, -10, -8))
    ganymede = Moon('Ganymede', (-1, -15, 2))
    callisto = Moon('Callisto', (12, -4, -4))
    jupiter = PlanetSystem([io, eurpoa, ganymede, callisto])
    steps = 1000
    for i in range(steps):
        jupiter.time_step()
    print('Part 1 Answer: {}'.format(jupiter.energy()))

def part2():
    cycle_lengths = []
    for i in range(3):
        io = Moon('Io', (1, 3, -11))
        eurpoa = Moon('Eurpoa', (17, -10, -8))
        ganymede = Moon('Ganymede', (-1, -15, 2))
        callisto = Moon('Callisto', (12, -4, -4))

        jupiter = PlanetSystem([io, eurpoa, ganymede, callisto])
        target_velocity = [0,0,0]
        target_pos = [moon.position[i] for moon in jupiter.moons]
        cycle_found = False
        while not cycle_found:
            jupiter.time_step()
            if [moon.position[i] for moon in jupiter.moons] == target_pos:
                if all(moon.velocity[i] == 0 for moon in jupiter.moons):
                    cycle_found = True
        cycle_lengths.append(jupiter.time)
    print('Part 2 Answer: {}'.format(lcm(cycle_lengths)))

part1()
part2()