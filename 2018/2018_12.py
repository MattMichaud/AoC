from itertools import groupby
def all_equal(iterable):
    g = groupby(iterable)
    return(next(g, True) and not next(g, False))

class PottedPlants():
    def __init__(self):
        self.growth_rules = None
        self.current_state = None
        self.current_gen = 0
        self.first_plant = 0

    def init_from_file(self, filename):
        with open(filename, 'r') as f:
            data = f.read().splitlines()
        self.current_state = data[0].replace('initial state: ','')
        self.first_plant = self.current_state.find('#')
        self.current_state = self.current_state[self.first_plant:]
        self.current_gen = 0
        rules = data[2:]
        self.growth_rules = {}
        for rule in rules:
            pattern = rule[:5]
            result = rule[-1]
            self.growth_rules[pattern] = result

    def display(self):
        display_string = 'Time: ' + str(self.current_gen) + '\t\tMin Plant: ' + str(self.first_plant) + '\t\t' + self.current_state
        print(display_string)

    def trim_state(self, state):
        return(state.replace('.',' ').strip().replace(' ','.'))

    def advance_generation(self):
        padding = '.....'
        self.current_state = padding + self.current_state + padding
        new_state = ''
        for index in range(2,len(self.current_state)-2):
            pattern = self.current_state[index-2:index+3]
            if pattern in self.growth_rules:
                new_plant = self.growth_rules[pattern]
            else:
                new_plant = '.'
            new_state += new_plant
        self.first_plant += new_state.find('#') - 3
        self.current_gen += 1
        self.current_state = self.trim_state(new_state)
        return

    def advance_multiple(self, generations, verbose=False):
        for i in range(generations):
            self.advance_generation()
            if verbose: self.display()

    def advance_multiple_big(self, generations, verbose=False, consistency_threshold=5):
        diffs = [0] * consistency_threshold
        previous_sum = self.sum_plants()
        consistent = False
        while not consistent:
            self.advance_generation()
            new_sum = self.sum_plants()
            diffs.pop(0)
            diffs.append(new_sum - previous_sum)
            consistent = all_equal(diffs)
            previous_sum = new_sum
        still_need = generations - self.current_gen
        additional_index_sums = diffs[-1] * still_need
        result = new_sum + additional_index_sums
        return(result)

    def sum_plants(self):
        import re
        plants = [m.start() + self.first_plant for m in re.finditer('#', self.current_state)]
        return(sum(plants))

def part1():
    input_file = '2018/inputs/2018_12_input.txt'
    plants = PottedPlants()
    plants.init_from_file(input_file)
    plants.advance_multiple(20)
    print('Part 1 Answer:', plants.sum_plants())

def part2():
    input_file = '2018/inputs/2018_12_input.txt'
    plants = PottedPlants()
    plants.init_from_file(input_file)
    print('Part 2 Answer:', plants.advance_multiple_big(50000000000))

part1()
part2()