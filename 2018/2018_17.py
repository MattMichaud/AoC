import numpy as np

def get_clay_locs(filename):
    with open(filename, 'r') as f:
        raw_data = f.read().splitlines()
    points = []
    for line in raw_data:
        if line[0] == 'x': #vertical line
            x = int(line[2:line.find(',')])
            y_list = [int(c) for c in line[line.find(' ')+3:].split('..')]
            y_range = range(y_list[0], y_list[1]+1)
            for y in y_range:
                points.append((x,y))
        else: #horizontal line
            y = int(line[2:line.find(',')])
            x_list = [int(c) for c in line[line.find(' ')+3:].split('..')]
            x_range = range(x_list[0], x_list[1]+1)
            for x in x_range:
                points.append((x,y))
    return(points)

class Sandbox():
    def __init__(self, filename, water_source_x):
        self.clay_points = get_clay_locs(filename)
        clay_x = [p[0] for p in self.clay_points]
        clay_y = [p[1] for p in self.clay_points]
        self.water_source = (water_source_x, min(clay_y) - 1)
        padding = 1
        self.min_x = min(clay_x) - padding
        self.max_x = max(clay_x) + padding + 1
        self.min_y = min(clay_y)
        self.max_y = max(clay_y) + 1
        self.grid = np.empty(shape=(self.max_x, self.max_y), dtype=str)
        self.grid[:] = '.'
        for point in self.clay_points:
            self.grid[point] = '#'
        self.grid[self.water_source] = '+'

    def display(self):
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                print(self.grid[(x,y)], end='')
            print()
        print()

    def drop_water(self, source=None):
        if source == None: source = self.water_source
        filled_row = False
        source_x = source[0]
        source_y = source[1]
        point_below = (source_x, source_y + 1)
        while point_below[1] < self.max_y and self.grid[point_below] not in '#~':
            self.grid[point_below] = '|'
            point_below = move_point(point_below, 'D')
        if point_below[1] >= self.max_y: return(filled_row)                                 # passed off the bottom
        start = move_point(point_below, 'U')
        if start == source: return(filled_row)                                              # nowhere to drop
        test_point = move_point(start, 'L')                                                 # flow water left
        while self.grid[test_point] in '.|' and self.grid[move_point(test_point, 'D')] in '~#':
            self.grid[test_point] = '|'
            test_point = move_point(test_point, 'L')
        left_end = test_point
        test_point = move_point(start,'R')                                                  # flow water right
        while self.grid[test_point] in '.|' and self.grid[move_point(test_point, 'D')] in '~#':
            self.grid[test_point] = '|'
            test_point = move_point(test_point, 'R')
        right_end = test_point
        if self.grid[left_end] == '#' and self.grid[right_end] == '#':                      # row to fill with standing water
            fill_point = move_point(left_end, 'R')
            while fill_point != right_end:
                self.grid[fill_point] = '~'
                fill_point = move_point(fill_point, 'R')
            self.drop_water(source)
            filled_row = True

        if self.grid[left_end] == '.':                                                      # drop water off left side
            filled_row = self.drop_water(left_end)
            self.grid[left_end] = '|'
        if self.grid[right_end] == '.':                                                     # drop water off right side
            filled_row = self.drop_water(right_end)
            self.grid[right_end] = '|'

        if filled_row: self.drop_water(source)
        return(filled_row)

    def count_water(self):
        unique, counts = np.unique(self.grid, return_counts=True)
        count_dict = dict(zip(unique, counts))
        return(count_dict)

def move_point(point, direction):
    offsets = {'R':(1,0), 'L':(-1,0), 'D':(0,1), 'U':(0,-1)}
    offset = offsets[direction]
    return(tuple(map(sum, zip(point, offset))))

def both_parts(filename):
    sandbox = Sandbox(filename, 500)
    sandbox.drop_water()
    count_dict = sandbox.count_water()
    print('Part 1 Answer:', count_dict['~'] + count_dict['|'])
    print('Part 2 Answer:', count_dict['~'])

input_file = '2018/inputs/2018_17_input.txt'
both_parts(input_file)