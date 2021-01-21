import numpy as np
from matplotlib import pyplot as plt

def part1(data, width, height):
    layers = int(len(data) / (width * height))
    shape = (layers, height, width)
    arr = np.array(data).reshape(shape)
    min_zero = min(arr, key=lambda x: len(x[x == 0]))
    ones = len(min_zero[min_zero == 1])
    twos = len(min_zero[min_zero == 2])
    print('Part 1 Answer:', ones * twos)

def find_value(n):
    index = 0
    while n[index] == 2: index += 1
    return n[index]

def part2(data, width, height):
    layers = int(len(data) / (width * height))
    shape = (layers, height, width)
    arr = np.array(data).reshape(shape)
    message = np.apply_along_axis(find_value, 0, arr)
    plt.imshow(message)
    plt.show()


filename = '2019/inputs/08.txt'
with open(filename, 'r') as f:
    data = f.read()
data = [int(c) for c in data]
width = 25
height = 6
part1(data, width, height)
part2(data, width, height)