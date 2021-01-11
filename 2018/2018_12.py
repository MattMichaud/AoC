def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    initial_state = data[0].replace('initial state: ','')
    rules = data[2:]
    rules_dict = {}
    for rule in rules:
        pattern = rule[:5]
        result = rule[-1]
        rules_dict[pattern] = result
    return (initial_state, rules_dict)

def advance_generation(start_state, first_pot_num, rules):
    base_state = '..' + start_state + '..'
    new_state = ''
    for i in range(0,len(base_state)-4):
        pattern = base_state[i:i+5]
        if pattern not in rules:
            added = '.'
        else:
            added = rules[pattern]
        new_state = new_state + added
        print('Checked pattern:', pattern, 'and added',added)
    new_first_pot = new_state.find('#') - 2
    return(new_state[first_pot_num+2:], new_first_pot)

def multiple_generations(start_state, num_generations, rules):
    first_pot = 0
    current_state = start_state
    for i in range(num_generations):
        print(i,':','starts at',first_pot,':', current_state)
        current_state, first_pot = advance_generation(current_state, first_pot, rules)
    print(num_generations,':','starts at',first_pot,':', current_state)
    return(current_state, first_pot)

input_file = '2018_12_input.py'
input_file = 'test.txt'
initial_state, rules = parse_input(input_file)
print(multiple_generations(initial_state, 3, rules))

# print((initial_state, 0))
# print(advance_generation(initial_state, 0, rules))