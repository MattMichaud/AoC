def parse_input(filename):
    """Function to parse puzzle input for day 1, returns a list of frequency changes

    Args:
        filename (str): name of file to be parsed
    """
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return(data)

def part1(li):
    """Function to complete part 1

    Args:
        li (list): list of frequency changes
    """
    result = sum([int(i) for i in li])
    return(result)

def part2(li):
    """Function to complete part 2

    Args:
        li (list): list of frequency changes (as strings)
    """
    li = [int(i) for i in li]
    freqs = {0}
    current_frequency = 0
    result = None
    index = 0
    while result == None:
        current_frequency += li[index]
        if current_frequency in freqs: 
            result = current_frequency
        else:
            freqs.add(current_frequency)
        index = (index + 1) % len(li)
    return(result)

data = parse_input('2018_01_input.txt')
print('Part 1 Answer:',part1(data))
print('Part 2 Answer:',part2(data))

