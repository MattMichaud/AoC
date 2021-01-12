class Example():
    def __init__(self, instuction, before, after):
        self.instruction = instuction
        self.before = before
        self.after = after
        self.op_results = {}
        self.valid_ops = set()
        self.perform_ops()

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
            if op == 'addr':
                result[self.instruction[3]] = register_A + register_B
                self.op_results['addr'] = result
                if result == self.after: self.valid_ops.add('addr')
            elif op == 'addi':
                result[self.instruction[3]] = register_A + value_B
                self.op_results['addi'] = result
                if result == self.after: self.valid_ops.add('addi')
            elif op == 'mulr':
                result[self.instruction[3]] = register_A * register_B
                self.op_results['mulr'] = result
                if result == self.after: self.valid_ops.add('mulr')
            elif op == 'muli':
                result[self.instruction[3]] = register_A * value_B
                self.op_results['muli'] = result
                if result == self.after: self.valid_ops.add('muli')
            elif op == 'setr':
                result[self.instruction[3]] = register_A
                self.op_results['setr'] = result
                if result == self.after: self.valid_ops.add('setr')
            elif op == 'seti':
                result[self.instruction[3]] = value_A
                self.op_results['seti'] = result
                if result == self.after: self.valid_ops.add('seti')
            elif op == 'banr':
                result[self.instruction[3]] = register_A & register_B
                self.op_results['banr'] = result
                if result == self.after: self.valid_ops.add('banr')
            elif op == 'bani':
                result[self.instruction[3]] = register_A & value_B
                self.op_results['bani'] = result
                if result == self.after: self.valid_ops.add('bani')
            elif op == 'borr':
                result[self.instruction[3]] = register_A | register_B
                self.op_results['borr'] = result
                if result == self.after: self.valid_ops.add('borr')
            elif op == 'bori':
                result[self.instruction[3]] = register_A | value_B
                self.op_results['bori'] = result
                if result == self.after: self.valid_ops.add('bori')
            elif op == 'gtir':
                if value_A  > register_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['gtir'] = result
                if result == self.after: self.valid_ops.add('gtir')
            elif op == 'gtri':
                if register_A  > value_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['gtri'] = result
                if result == self.after: self.valid_ops.add('gtri')
            elif op == 'gtrr':
                if register_A  > register_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['gtrr'] = result
                if result == self.after: self.valid_ops.add('gtrr')
            elif op == 'eqir':
                if value_A  == register_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['eqir'] = result
                if result == self.after: self.valid_ops.add('eqir')
            elif op == 'eqri':
                if register_A  == value_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['eqri'] = result
                if result == self.after: self.valid_ops.add('eqri')
            elif op == 'eqrr':
                if register_A  == register_B:
                    result[self.instruction[3]] = 1
                else:
                    result[self.instruction[3]] = 0
                self.op_results['eqrr'] = result
                if result == self.after: self.valid_ops.add('eqrr')

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

def part1(filename):
    examples = parse_input(filename)
    three_or_more = 0
    for ex in examples:
        #ex.display()
        if len(ex.valid_ops) >= 3: three_or_more += 1
    print('Part 1 Answer:',three_or_more)


input_file = '2018_16_input_1.txt'
#input_file = 'test.txt'
part1(input_file)