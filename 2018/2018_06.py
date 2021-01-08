def get_coordinates(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    points = []
    for item in data:
        x,y = item.split(', ')
        points.append((int(x),int(y)))
    return(points)

def get_dimensions(points):
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    return(min(x_vals), max(x_vals), min(y_vals), max(y_vals))

def build_grid(min_x, max_x, min_y, max_y, buffer = 5):
    grid = {}
    for (x,y) in [(x,y) for x in range(min_x - buffer, max_x + buffer + 1) for y in range(min_y - buffer, max_y + buffer + 1)]:
        grid[(x,y)] = '.'
    return(grid)

def add_points(grid, points):
    for index, p in enumerate(points):
        grid[p] = '*' + str(index) + '*'

def distance(x1, y1, x2, y2):
    dist = abs(x1 - x2) + abs(y1 - y2)
    return(dist)

def update_distances(grid, points):
    for x,y in grid:
        if grid[(x,y)] == '.':
            min_distance = None
            distances = [distance(x,y,px,py) for px,py in points]
            min_distance = min(distances)
            if distances.count(min_distance) == 1:
                grid[(x,y)] = 'd' + str(distances.index(min_distance))
    return

def non_infinite_points(grid, points):
    infinite_points = set()
    min_x, max_x, min_y, max_y = get_dimensions(grid)
    for y in range(min_y, max_y+1):
        infinite_points.add(grid[(min_x, y)])
        infinite_points.add(grid[(max_x, y)])
    for x in range(min_x, max_x+1):
        infinite_points.add(grid[(x, min_y)])
        infinite_points.add(grid[(x, max_y)])
    if '.' in infinite_points:
        infinite_points.remove('.')
    good_points = set(range(len(points)))
    for item in infinite_points:
        good_points.remove(int(item[1:]))
    return(good_points)

def find_area(grid, point_num):
    area = sum([1 for val in grid.values() if val == 'd' + str(point_num)]) + 1
    return(area)

def max_area(grid, points):
    biggest_area = 0
    for p in non_infinite_points(grid, points):
        point_area = find_area(grid, p)
        biggest_area = max(biggest_area, point_area)
    return(biggest_area)

def part1(filename):
    points = get_coordinates(input_file)
    min_x, max_x, min_y, max_y = get_dimensions(points)
    buffer = 1
    grid = build_grid(min_x, max_x, min_y, max_y, buffer)
    add_points(grid, points)
    update_distances(grid, points)
    print('Part 1 Answer:',max_area(grid, points))

def mark_safe_points(grid, points, mindist):
    safe_count = 0
    for x,y in grid:
        if grid[(x,y)] == '.':
            distances = [distance(x,y,px,py) for px,py in points]
            if sum(distances) < mindist:
                grid[(x,y)] = '#'
                safe_count += 1
    return(safe_count)

def part2(filename, mindist):
    points = get_coordinates(input_file)
    min_x, max_x, min_y, max_y = get_dimensions(points)
    buffer = 1
    grid = build_grid(min_x, max_x, min_y, max_y, buffer)
    safe = mark_safe_points(grid, points, mindist)
    print('Part 2 Answer:',safe)

input_file = '2018_06_input.txt'
part1(input_file)
part2(input_file, 10000)