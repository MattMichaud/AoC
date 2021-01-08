def get_polymer(filename):
    with open(filename) as f:
        polymer = f.read()
    polymer = polymer.replace('\n','')
    return(polymer)

def stack_redcution(polymer):
    stack = []
    for c in polymer:
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    new_polymer = ''.join(stack)
    return(new_polymer)

def part1(filename):
    polymer = get_polymer(filename)
    print('Part 1 Answer:', len(stack_redcution(polymer)))

def part2(filename):
    polymer = get_polymer(filename)
    from string import ascii_lowercase
    shortest = min([len(stack_redcution(polymer.replace(c,'').replace(c.upper(),''))) for c in ascii_lowercase])
    print('Part 2 Answer:', shortest)

input_file = '2018_05_input.txt'
part1(input_file)
part2(input_file)
