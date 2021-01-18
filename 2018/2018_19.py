class Computer():
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.read().splitlines()
        self.ip_location = int(data[0].replace('#ip ',''))
        self.instruction_list = []
        for line in data[1:]:
            line = line.split()
            inst = [line[0]] + [int(c) for c in line[1:]]
            self.instruction_list.append(inst)
        self.registers = [0,0,0,0,0,0]
        self.instruction_pointer = self.registers[self.ip_location]

    def execute_instruction(self, instruction, verbose=False):
        op = instruction[0]
        result = self.registers.copy()
        result[self.ip_location] = self.instruction_pointer
        if verbose: print('ip=',self.instruction_pointer, result, instruction, end=' ')
        if op == 'addr': result[instruction[3]] = result[instruction[1]] + result[instruction[2]]
        elif op == 'addi': result[instruction[3]] = result[instruction[1]] + instruction[2]
        elif op == 'mulr': result[instruction[3]] = result[instruction[1]] * result[instruction[2]]
        elif op == 'muli': result[instruction[3]] = result[instruction[1]] * instruction[2]
        elif op == 'setr': result[instruction[3]] = result[instruction[1]]
        elif op == 'seti': result[instruction[3]] = instruction[1]
        elif op == 'banr': result[instruction[3]] = result[instruction[1]] & result[instruction[2]]
        elif op == 'bani': result[instruction[3]] = result[instruction[1]] & instruction[2]
        elif op == 'borr': result[instruction[3]] = result[instruction[1]] | result[instruction[2]]
        elif op == 'bori': result[instruction[3]] = result[instruction[1]] | instruction[2]
        elif op == 'gtir':
            if instruction[1]  > result[instruction[2]]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0
        elif op == 'gtri':
            if result[instruction[1]]  > instruction[2]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0
        elif op == 'gtrr':
            if result[instruction[1]]  > result[instruction[2]]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0
        elif op == 'eqir':
            if instruction[1]  == result[instruction[2]]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0
        elif op == 'eqri':
            if result[instruction[1]]  == instruction[2]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0
        elif op == 'eqrr':
            if result[instruction[1]]  == result[instruction[2]]: result[instruction[3]] = 1
            else: result[instruction[3]] = 0

        self.registers = result
        self.instruction_pointer = self.registers[self.ip_location] + 1
        if verbose: print(result,'new ip=', self.instruction_pointer)

        return()

    def run_program(self, verbose=False):
        while self.instruction_pointer in range(len(self.instruction_list)):
            self.execute_instruction(self.instruction_list[self.instruction_pointer], verbose)

def sum_factors(num):
    sum = 0
    for i in range(1, num+1):
        if num % i == 0:
            sum += i
    return(sum)

def part1(filename):
    comp = Computer(filename)
    comp.run_program(False)
    print('Part 1 Answer:', comp.registers[0])

def part2(filename):
    comp = Computer(filename)
    comp.registers[0] = 1
    prev_inst_pointer = comp.instruction_pointer
    while comp.instruction_pointer >= prev_inst_pointer:
        prev_inst_pointer = comp.instruction_pointer
        comp.execute_instruction(comp.instruction_list[comp.instruction_pointer], False)
    max_reg = max(comp.registers)
    print('Part 2 Answer:',sum_factors(max_reg))

input_file = '2018/inputs/2018_19_input.txt'
part1(input_file)
part2(input_file)