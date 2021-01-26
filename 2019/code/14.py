import math

def create_reactions(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    reactions = {}
    for line in data:
        [input_chemicals, output_chemical] = line.split(' => ')
        input_chemicals = input_chemicals.split(', ')
        inputs = []
        for x in input_chemicals:
            x = x.split(' ')
            quantity = int(x[0])
            chem = x[1]
            inputs.append((quantity, chem))
        output_chemical = output_chemical.split(' ')
        output_name = output_chemical[1]
        output_quantity = int(output_chemical[0])
        reactions[output_name] = {'inputs': inputs, 'quantity': output_quantity}
    return reactions

class Problem:
    def __init__(self, filename):
        self.reactions = create_reactions(filename)
        self.on_hand = {}
        self.clear_on_hand()

    def clear_on_hand(self):
        for key in self.reactions:
            for _, chem in self.reactions[key]['inputs']:
                self.on_hand[chem] = 0
        self.on_hand['FUEL'] = 0

    def ore_needed(self, name, quantity):
        ore_count = 0
        stack = [(quantity, name)]

        while stack:
            q, n = stack.pop()
            if n == 'ORE':
                ore_count += q
            else:
                # use any on-hand first
                if self.on_hand[n] > 0 and self.on_hand[n] >= q:
                    self.on_hand[n] -= q
                    q = 0
                elif self.on_hand[n] > 0 and self.on_hand[n] < q:
                    q -= self.on_hand[n]
                    self.on_hand[n] = 0

                # perform reaction number of times needed
                if q > 0:
                    multiplier = math.ceil(q / self.reactions[n]['quantity'])
                    left_over = multiplier * self.reactions[n]['quantity'] - q
                    self.on_hand[n] += left_over
                    for dep_q, dep_n in self.reactions[n]['inputs']:
                        stack.append((multiplier * dep_q, dep_n))
        return ore_count

    def max_fuel(self, ore_on_hand):
        ore_needed_for_one_fuel = self.ore_needed('FUEL', 1)
        self.clear_on_hand()
        increment = current_try = ore_on_hand // ore_needed_for_one_fuel
        result = 0
        while not (increment == 1 and result > ore_on_hand):
            if result > ore_on_hand:
                current_try -= increment
                increment //= 2
            else:
                current_try += increment
            result = self.ore_needed('FUEL', current_try)
            self.clear_on_hand()
        return current_try - 1

filename = '2019/inputs/14.txt'
prob = Problem(filename)
print('Part 1 Answer: {}'.format(prob.ore_needed('FUEL', 1)))
print('Part 2 Answer: {}'.format(prob.max_fuel(1000000000000)))
