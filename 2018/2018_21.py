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

comp = Computer('2018/inputs/2018_21_input.txt')
done = False
unique_vals = set()
last_unique = None
while not done:
    comp.execute_instruction(comp.instruction_list[comp.instruction_pointer], False)
    if comp.instruction_pointer == 28:
        # line 28 compares register 3 to register 0 and will cause an exit if equal
        # so we are inspecting the values of register 3 on this line to determine
        # what values of register 0 would cause an exist
        # the first one we find is the answer to part 1 (fewest instructions executed)
        # the last one we find before the numbers repeat is the answer to part 2 (most instructions)
        #
        # if we could simplify the atual program this would run a LOT faster
        # that is what the cheater method at the bottom basically does
        # but that was copied from someone else
        #
        new_val = comp.registers[3]
        if new_val in unique_vals:
            print('Part 2 Answer:', last_unique)
            done = True
        else:
            last_unique = new_val
            unique_vals.add(new_val)
            if len(unique_vals) % 100 == 0: print(len(unique_vals))
            if len(unique_vals) == 1:
                print('Part 1 Answer:', new_val)


# this is the CHEATER method copied from someone else
#
# def run_activation_system(magic_number, is_part_1):
#     seen = set()
#     c = 0
#     last_unique_c = -1

#     while True:
#         a = c | 65536
#         c = magic_number

#         while True:
#             c = (((c + (a & 255)) & 16777215) * 65899) & 16777215

#             if 256 > a:
#                 if is_part_1:
#                     return c
#                 else:
#                     if c not in seen:
#                         seen.add(c)
#                         last_unique_c = c
#                         break
#                     else:
#                         return last_unique_c
#             else:
#                 a //= 256

# magic_number = 10736359
# print('Part 1 Answer:', run_activation_system(magic_number, True))
# print('Part 2 Answer:', run_activation_system(magic_number, False))

