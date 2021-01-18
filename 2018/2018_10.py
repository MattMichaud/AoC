class Point():
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.vel_x = velocity_x
        self.vel_y = velocity_y

    def advance_time(self, seconds=1):
        self.x = self.x + (seconds * self.vel_x)
        self.y = self.y + (seconds * self.vel_y)



class Sky():
    def __init__(self):
        self.points = []
        self.update_stats()
        self.current_time = 0
        self.unique_xs = None
        self.unique_ys = None

    def unique_dimensions(self):
        x_vals = set([p.x for p in self.points])
        y_vals = set([p.y for p in self.points])
        return(len(x_vals), len(y_vals))

    def update_stats(self):
        x_vals = [p.x for p in self.points]
        y_vals = [p.y for p in self.points]
        if len(x_vals) > 0:
            self.min_x = min(x_vals)
            self.max_x = max(x_vals)
            self.min_y = min(y_vals)
            self.max_y = max(y_vals)
        self.unique_xs, self.unique_ys = self.unique_dimensions()

    def add_point(self, new_point, update=True):
        self.points.append(new_point)
        if update: self.update_stats()

    def print_sky(self):
        self.update_stats()
        width = self.get_width()
        height = self.get_height()
        all_points = [(p.x, p.y) for p in self.points]
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                if (x,y) in all_points:
                    print('#', end='')
                else:
                    print(' ', end='')
            print()
        print()

    def advance_time(self, seconds=1):
        for p in self.points:
            p.advance_time(seconds)
        self.current_time += seconds
        self.update_stats()

    def get_width(self):
        return(self.max_x - self.min_x + 1)

    def get_height(self):
        return(self.max_y - self.min_y + 1)

    def get_area(self):
        return(self.get_width() * self.get_height())



def get_points(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    points = []
    for line in data:
        x_pos = int(line[line.find('<')+1:line.find(',')].strip())
        y_pos = int(line[line.find(',')+1:line.find('>')].strip())
        vline = line[line.find('>')+1:]
        x_vel = int(vline[vline.find('<')+1:vline.find(',')].strip())
        y_vel = int(vline[vline.find(',')+1:vline.find('>')].strip())
        points.append(Point(x_pos, y_pos, x_vel, y_vel))
    return(points)


my_sky = Sky()
original_points = get_points('2018/inputs/2018_10_input.txt')
for point in original_points:
    my_sky.add_point(new_point=point, update=False)
my_sky.update_stats()
curr_area = my_sky.get_area()
while True:
    my_sky.advance_time()
    new_area = my_sky.get_area()
    if new_area > curr_area:
        my_sky.advance_time(-1)
        break
    else:
        curr_area = new_area
print('Part 1 Answer:')
my_sky.print_sky()
print('Part 2 Answer:', my_sky.current_time, 'seconds')
