def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return(data)

def parse_instructions(li):
    unique_steps = set()
    instructions = {}
    clean_instructions = []
    for inst in li:
        inst = inst.replace('Step ','').replace(' must be finished before step ','')[:2]
        step = inst[1]
        prereq = inst[0]
        clean_instructions.append((step,prereq))
        for c in inst:
            unique_steps.add(c)
    for step in unique_steps:
        instructions[step] = {'prereqs':set(), 'duration':ord(step)-4}
    for inst in clean_instructions:
        instructions[inst[0]]['prereqs'].add(inst[1])
    return(instructions)

def get_ready_list(instructions, completed_list, available_list=None):
    ready_list = []
    if available_list == None: available_list = instructions
    for step in available_list:
        if instructions[step]['prereqs'].issubset(completed_list) and step not in completed_list:
            ready_list.append(step)
    ready_list.sort()
    return(ready_list)

def get_next_step(instructions, completed_list):
    ready_list = get_ready_list(instructions, completed_list)
    return(ready_list[0])

def part1(filename):
    instruction_list = parse_input(input_file)
    instructions = parse_instructions(instruction_list)
    completed_list = []
    while len(completed_list) < len(instructions):
        completed_list.append(get_next_step(instructions,completed_list))
    print('Part 1 Answer:',''.join(completed_list))

def part2(filename, total_workers):
    instruction_list = parse_input(input_file)
    instructions = parse_instructions(instruction_list)
    completed_list = set()
    available = set(instructions)
    in_process_list = set()
    time = 0
    workers = [(None,0)] * total_workers
    while completed_list != set(instructions):
        for index, w in enumerate(workers):
            if w[1] <= time:
                if w[0] != None: completed_list.add(w[0])
                if w[0] in in_process_list: in_process_list.remove(w[0])
                possible_steps = get_ready_list(instructions, completed_list, available)
                if len(possible_steps) > 0:
                    new_step = possible_steps[0]
                    available.remove(new_step)
                    new_ready_time = time + instructions[new_step]['duration']
                else:
                    new_step = None
                    new_ready_time = time
                workers[index] = (new_step, new_ready_time)
        time += 1
    print('Part 2 Answer:', time-1)


input_file = '2018_07_input.txt'
#input_file = 'test.txt'
part1(input_file)
part2(input_file, 5)