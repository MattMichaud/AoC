import sys
sys.path.append('.')
from utils import data_import

def run_program(program):
    terminated = False
    ip = 0
    while not terminated:
        current_instruction = program[ip]
        if current_instruction in (1, 2):
            position_A = program[ip + 1]
            position_B = program[ip + 2]
            position_C = program[ip + 3]
            A = program[position_A]
            B = program[position_B]
            if current_instruction == 1:
                C = A + B
            elif current_instruction == 2:
                C = A * B
            program[position_C] = C
            ip += 4
            continue
        if current_instruction == 99:
            terminated = True
        ip += 1

def execute_code(code, noun, verb):
    code[1] = noun
    code[2] = verb
    run_program(code)
    return(code[0])

def part1(filename):
    program = data_import(filename, int, ',')[0]
    print('Part 1 Answer:', execute_code(program, 12, 2))

def part2(filename, target):
    prog = data_import(filename, int, ',')[0]
    for noun in range(100):
        for verb in range(100):
            p = prog.copy()
            if execute_code(p, noun, verb) == target:
                print('Part 2 Answer:', 100 * noun + verb)

input_file = '2019/inputs/02.txt'
part1(input_file)
part2(input_file, 19690720)