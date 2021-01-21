import sys
sys.path.append('.')
from utils import data_import
from itertools import permutations

POSITION = '0'
IMMEDIATE = '1'

def intcode_compuer(program, inp, print_out=False, starting_ip=0):
    terminated = False
    ip = starting_ip
    last_output = None
    while not terminated:
        inst = str(program[ip]).zfill(5)
        p1_mode = inst[2]
        p2_mode = inst[1]
        p3_mode = inst[0]
        opcode = int(inst[-2:])
        if opcode in (1,2):
            A = program[ip + 1] if p1_mode == IMMEDIATE else program[program[ip + 1]]
            B = program[ip + 2] if p2_mode == IMMEDIATE else program[program[ip + 2]]
            write_address = program[ip + 3]
            if opcode == 1:
                program[write_address] = A + B
            elif opcode == 2:
                program[write_address] = A * B
            ip += 4
        elif opcode == 3:
            if len(inp) == 0:
                # we will have to exit the program and wait until we have an input to resume
                return last_output, ip, False
                pass
            current_inp = inp.pop(0)
            write_address = program[ip + 1]
            program[write_address] = current_inp
            ip += 2
        elif opcode == 4:
            A = program[ip + 1] if p1_mode == IMMEDIATE else program[program[ip + 1]]
            if print_out: print('Output:', A, 'at position', ip)
            last_output = A
            ip += 2
        elif opcode in (5,6):
            A = program[ip + 1] if p1_mode == IMMEDIATE else program[program[ip + 1]]
            B = program[ip + 2] if p2_mode == IMMEDIATE else program[program[ip + 2]]
            if opcode == 5 and A != 0: ip = B
            elif opcode == 6 and A == 0: ip = B
            else: ip += 3
        elif opcode in (7,8):
            A = program[ip + 1] if p1_mode == IMMEDIATE else program[program[ip + 1]]
            B = program[ip + 2] if p2_mode == IMMEDIATE else program[program[ip + 2]]
            write_address = program[ip + 3]
            if opcode == 7 and A < B:program[write_address] = 1
            elif opcode == 8 and A == B: program[write_address] = 1
            else: program[write_address] = 0
            ip += 4
        elif opcode == 99:
            terminated = True
            return last_output, ip, True
    return last_output, ip, True


def sequence_result(amp_program, num_amps, phase_settings):
    current_amp = 1
    current_signal = 0
    while current_amp <= num_amps:
        current_program = amp_program.copy()
        current_inputs = [phase_settings[current_amp - 1], current_signal]
        current_signal, _, _ = intcode_compuer(current_program, current_inputs, False)
        current_amp += 1
    return(current_signal)

def part1(filename):
    program = data_import(filename, int, ',')[0]
    print('Part 1 Answer:', max([sequence_result(program, 5, t) for t in permutations(range(5), 5)]))

def part2(filename):
    program = data_import(filename, int, ',')[0]
    tuples = list(permutations(range(5,10), 5))
    max_signal = 0
    num_amps = 5
    for t in tuples:
        current_signal = 0
        final_result = False
        amps = []
        for i in range(num_amps):
            amps.append({'program':program.copy(), 'ip':0, 'inputs':[t[i]]})
        while not final_result:
            for i in range(num_amps):
                amps[i]['inputs'].append(current_signal)
                current_signal, amps[i]['ip'], final_result = intcode_compuer(amps[i]['program'], amps[i]['inputs'], False, amps[i]['ip'])
        max_signal = max(current_signal, max_signal)
    print('Part 2 Answer:',max_signal)


filename = '2019/inputs/07.txt'
#filename = 'test.txt'
part1(filename)
part2(filename)