POSITION = '0'
IMMEDIATE = '1'
RELATIVE = '2'

def intcode_computer(program, inp, memory_multiplier=1, print_out=False):

    # initialize computer
    terminated = False
    ip = 0
    last_output = None
    relative_base = 0
    program = program + ([0] * (len(program) * memory_multiplier))
    outputs = []

    while not terminated:

        inst = str(program[ip]).zfill(5)
        p1_mode = inst[2]
        p2_mode = inst[1]
        p3_mode = inst[0]
        opcode = int(inst[-2:])

        opcodes_using_A = (1,2,4,5,6,7,8,9)
        opcodes_using_B = (1,2,5,6,7,8)

        # set the first input
        if opcode in opcodes_using_A:
            if p1_mode == IMMEDIATE:
                position = ip + 1
            elif p1_mode == POSITION:
                position = program[ip + 1]
            elif p1_mode == RELATIVE:
                position = relative_base + program[ip + 1]
            A = program[position]

        # set the second input
        if opcode in opcodes_using_B:
            if p2_mode == IMMEDIATE:
                position = ip + 2
            elif p2_mode == POSITION:
                position = program[ip + 2]
            elif p2_mode == RELATIVE:
                position = relative_base + program[ip + 2]
            B = program[position]

        # set the write location appropriately
        if opcode in (1,2,7,8) and p3_mode == RELATIVE: write_address = relative_base + program[ip + 3]
        if opcode in (1,2,7,8) and p3_mode != RELATIVE: write_address = program[ip + 3]
        if opcode == 3 and p1_mode == RELATIVE: write_address = relative_base + program[ip + 1]
        if opcode == 3 and p1_mode != RELATIVE: write_address = program[ip + 1]

        # execute opcodes
        if opcode in (1,2):
            if opcode == 1:
                program[write_address] = A + B
            elif opcode == 2:
                program[write_address] = A * B
            ip += 4

        elif opcode == 3:
            val = inp.pop(0)
            program[write_address] = val
            ip += 2

        elif opcode == 4:
            if print_out: print('Output:', A)
            outputs.append(A)
            ip += 2

        elif opcode in (5,6):
            if opcode == 5 and A != 0: ip = B
            elif opcode == 6 and A == 0: ip = B
            else: ip += 3

        elif opcode in (7,8):
            if opcode == 7 and A < B: program[write_address] = 1
            elif opcode == 8 and A == B: program[write_address] = 1
            else: program[write_address] = 0
            ip += 4

        elif opcode == 9:
            relative_base += A
            ip += 2

        elif opcode == 99:
            terminated = True

    return(outputs)

with open('2019/inputs/09.txt', 'r') as f:
    data = f.read()
actual_input = [int(c) for c in data.split(',')]
print('Part 1 Answer:',intcode_computer(actual_input, [1], 1, False)[0])
print('Part 2 Answer:',intcode_computer(actual_input, [2], 1, False)[0])

