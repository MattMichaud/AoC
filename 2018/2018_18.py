import numpy as np

def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    #data = np.loadtxt(filename, delimiter='')'
    size = len(data)
    array = np.empty(shape=(size,size), dtype=str)
    for (x,y) in [(x,y) for x in range(size) for y in range(size)]:
        array[(x,y)] = data[y][x]
    return(array)


class LumberArea():
    def __init__(self, filename):
        self.current_state = parse_input(filename)
        self.width = self.current_state.shape[0]
        self.height = self.current_state.shape[1]
        self.elapsed_minutes = 0
        self.valid_locs = self.get_valid_indices()
        unique, counts = np.unique(self.current_state, return_counts=True)
        count_dict = dict(zip(unique, counts))
        self.tree_count = count_dict['|']
        self.yard_count = count_dict['#']
        self.neighbor_locs = self.build_neighbor_locs()

    def get_valid_indices(self):
        result = []
        row_index, col_index = self.current_state.nonzero()
        for row, col in zip(row_index, col_index):
            result.append((row, col))
        return(result)

    def neighbor_loc_list(self, loc):
        adjacent_offsets = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        res = []
        for offset in adjacent_offsets:
            neighbor = tuple(map(sum, zip(offset, loc)))
            if neighbor in self.valid_locs:
                res.append(neighbor)
        return(res)

    def build_neighbor_locs(self):
        neighbor_locs = {}
        for loc in self.valid_locs:
            neighbor_locs[loc] = self.neighbor_loc_list(loc)
        return(neighbor_locs)

    def display(self):
        if self.elapsed_minutes == 0:
            print('Initial state:')
        else:
            print('After',self.elapsed_minutes,'minute:')
        for y in range(self.height):
            for x in range(self.width):
                print(self.current_state[(x,y)], end='')
            print()
        print('Resource Value', self.resource_value())
        print()

    def neighbor_counts(self, loc):
        neighbors = self.neighbor_locs[loc]
        trees = yards = 0
        for neighbor in neighbors:
            value = self.current_state[neighbor]
            if value == '|': trees += 1
            elif value == '#': yards += 1
        return(trees, yards)

    def advance_one_minute(self):
        new_state = np.empty(shape=self.current_state.shape, dtype=str)
        for loc in self.valid_locs:
            current_value = self.current_state[loc]
            nearby_trees, nearby_yards = self.neighbor_counts(loc)
            if current_value == '.':
                if nearby_trees >= 3:
                    new_state[loc] = '|'
                    self.tree_count += 1
                else:
                    new_state[loc] = current_value
            elif current_value == '|':
                if nearby_yards >= 3:
                    new_state[loc] = '#'
                    self.tree_count -= 1
                    self.yard_count += 1
                else:
                    new_state[loc] = current_value
            elif current_value == '#':
                if nearby_yards >= 1 and nearby_trees >= 1:
                    new_state[loc] = '#'
                else:
                    new_state[loc] = '.'
                    self.yard_count -= 1
        self.current_state = new_state
        self.elapsed_minutes += 1

    def resource_value(self):
        return(self.tree_count * self.yard_count)

    def advance_time(self, minutes=1, verbose=False):
        for _ in range(minutes):
            self.advance_one_minute()
            if verbose: self.display()

def part1(filename, time=10, verbose=False):
    lumber = LumberArea(filename)
    if verbose: lumber.display()
    lumber.advance_time(time, verbose)
    print('Part 1 Answer:', lumber.resource_value())

def part2(filename, time=1000000000):
    lumber = LumberArea(filename)
    state_list = []
    cycle = False
    iteration = 0
    while not cycle:
        lumber.advance_one_minute()
        iteration += 1
        if any(np.array_equal(lumber.current_state, prev) for prev in state_list):
            cycle = True
            match_index = 0
            for index, arr in enumerate(state_list):
                if np.array_equal(lumber.current_state, arr):
                    match_index = index
                    break
            cycle_len = len(state_list) - match_index
        else:
            state_list.append(lumber.current_state.copy())
    while iteration + cycle_len <= time:
        iteration += cycle_len
        lumber.elapsed_minutes += cycle_len
    for _ in range(iteration, time):
        lumber.advance_one_minute()
    print('Part 2 Answer:',lumber.resource_value())

input_file = '2018/inputs/2018_18_input.txt'
part1(input_file)
part2(input_file)




