import numpy as np

def get_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level = power_level * rack_id
    power_level = (power_level // 100) % 10
    power_level -= 5
    return(power_level)

def create_cs_grid(size, serial_number):
    grid = np.zeros((301,301))
    for x,y in [(x,y) for x in range(1,size+1) for y in range(1,size+1)]:
        grid[x,y] = get_power_level(x, y, serial_number)
    cs_grid = grid.cumsum(axis=0, dtype=int).cumsum(axis=1, dtype=int)
    return(cs_grid)

def square_sum(table, x, y, size):
    Cx = Ax = x - 1
    By = Ay = y - 1
    Dx = Bx = Ax + size
    Dy = Cy = Ay + size
    res = table[Dx,Dy] + table[Ax,Ay] - table[Bx,By] - table[Cx,Cy]
    return(res)

def max_sum(table, size):
    r = range(1, 301-size)
    max_power = max_x = max_y = None
    for x,y in [(x,y) for x in r for y in r]:
        loc_power = square_sum(table, x, y, size)
        if max_power == None or loc_power > max_power:
            max_power = loc_power
            max_x = x
            max_y = y
    return(max_power, max_x, max_y)

def part1(serial_number):
    cs_grid = create_cs_grid(300, serial_number)
    max_power, max_x, max_y = max_sum(cs_grid, 3)
    print('Part 1 Answer:',str(max_x)+','+str(max_y))

def part2(serial_number):
    cs_grid = create_cs_grid(300, serial_number)
    max_power = None
    for s in range(1,301):
        size_pow, size_x, size_y = max_sum(cs_grid, s)
        if max_power is None or (size_pow is not None and size_pow > max_power):
            max_power = size_pow
            max_x = size_x
            max_y = size_y
            max_size = s
    print('Part 2 Answer:',str(max_x)+','+str(max_y)+','+str(max_size))

serial_number = 4151
part1(serial_number)
part2(serial_number)