class Example():
    def __init__(self, instruction, before, after):
        self.instruction = instruction
        self.before = before
        self.after = after
        self.op_results = {}
        self.valid_ops = set()
        self.perform_ops()
        self.op_number = instruction[0]

    def display(self):
        print('Before:',self.before)
        print('Inst  :',self.instruction)
        print('After :',self.after)

    def perform_ops(self):
        op_list = ['addr', 'addi', 'mulr', 'muli','setr','seti','banr','bani','borr','bori','gtir','gtri','gtrr','eqir','eqri','eqrr']
        register_A = self.before[self.instruction[1]]
        value_A = self.instruction[1]
        register_B = self.before[self.instruction[2]]
        value_B = self.instruction[2]
        for op in op_list:
            result = self.before.copy()
            inst = [op] + self.instruction[1:]
            result = execute_instruction(inst, self.before)
            self.op_results[op] = result
            if result == self.after: self.valid_ops.add(op)

def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    data = data.split('\n\n')
    examples = []
    for inst in data:
        inst = inst.split('\n')
        before = [int(c) for c in inst[0].replace('Before: [','').replace(']','').split(',')]
        instruction = [int(c) for c in inst[1].split()]
        after = [int(c) for c in inst[2].replace('After:  [','').replace(']','').split(',')]
        examples.append(Example(instruction, before, after))
    return(examples)

def parse_input_program(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    prog = []
    for line in data:
        line = [int(c) for c in line.split()]
        prog.append(line)
    return(prog)

def part1(filename):
    examples = parse_input(filename)
    three_or_more = 0
    for ex in examples:
        #ex.display()
        if len(ex.valid_ops) >= 3: three_or_more += 1
    print('Part 1 Answer:',three_or_more)

def find_actual_opcodes(examples):
    ops = {}
    for i in range(16):
        ops[i] = set()
    for ex in examples:
        for opcode in ex.valid_ops:
            ops[ex.op_number].add(opcode)
    reduction_done = True
    while reduction_done:
        reduction_done = False
        for key, value in ops.items():
            if len(value) == 1:
                remove_code = list(value)[0]
                #print('trying to remove',remove_code)
                for k in ops:
                    if k != key and remove_code in ops[k]:
                        ops[k].remove(remove_code)
                        reduction_done = True
    return(ops)

def execute_instruction(instruction, registers, opcode_map=None):
    register_A = registers[instruction[1]]
    value_A = instruction[1]
    register_B = registers[instruction[2]]
    value_B = instruction[2]
    if opcode_map == None: op = instruction[0]
    else: op = list(opcode_map[instruction[0]])[0]
    result = registers.copy()
    if op == 'addr': result[instruction[3]] = register_A + register_B
    elif op == 'addi': result[instruction[3]] = register_A + value_B
    elif op == 'mulr': result[instruction[3]] = register_A * register_B
    elif op == 'muli': result[instruction[3]] = register_A * value_B
    elif op == 'setr': result[instruction[3]] = register_A
    elif op == 'seti': result[instruction[3]] = value_A
    elif op == 'banr': result[instruction[3]] = register_A & register_B
    elif op == 'bani': result[instruction[3]] = register_A & value_B
    elif op == 'borr': result[instruction[3]] = register_A | register_B
    elif op == 'bori': result[instruction[3]] = register_A | value_B
    elif op == 'gtir':
        if value_A  > register_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    elif op == 'gtri':
        if register_A  > value_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    elif op == 'gtrr':
        if register_A  > register_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    elif op == 'eqir':
        if value_A  == register_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    elif op == 'eqri':
        if register_A  == value_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    elif op == 'eqrr':
        if register_A  == register_B: result[instruction[3]] = 1
        else: result[instruction[3]] = 0
    return(result)

def part2(examples_filename, program_fileame):
    examples = parse_input(examples_filename)
    program = parse_input_program(program_fileame)
    opcode_map = find_actual_opcodes(examples)
    current_registers = [0,0,0,0]
    for inst in program:
        current_registers = execute_instruction(inst, current_registers, opcode_map)
    print('Part 2 Answer:', current_registers[0])

part1('2018/inputs/2018_16_input_1.txt')
part2('2018/inputs/2018_16_input_1.txt', '2018/inputs/2018_16_input_2.txt')