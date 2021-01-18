def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return(data)

def part1(li):
    from collections import Counter
    exactly_two_count = 0
    exactly_three_count = 0
    for boxID in li:
        #print(boxID)
        counter = Counter(boxID)
        if 2 in counter.values(): exactly_two_count += 1
        if 3 in counter.values(): exactly_three_count += 1
    return(exactly_two_count * exactly_three_count)

def nearly_equal(string1, string2):
    if len(string1) != len(string2):
        return False
    else:
        result = ''
        count_diffs = 0
        for a, b in zip(string1, string2):
            if a != b:
                count_diffs += 1
            else:
                result += a
        if count_diffs == 1:
            return(result)
    return(False)

def part2(li):
    for index, boxID in enumerate(li):
        remaining_IDs = li[index+1:]
        for compareID in remaining_IDs:
            test = nearly_equal(boxID, compareID)
            if test: return(test)


data = parse_input('2018/inputs/2018_02_input.txt')
print('Part 1 Answer:',part1(data))
print('Part 2 Answer:',part2(data))


