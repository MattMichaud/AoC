
def validate_pwd(num: int, comparison_function) -> bool:
    num = str(num)
    if len(num) != 6 or any(num[i] < num[i-1] for i in range(1, len(num))): return False
    groups = [num.count(n) for n in set(num)]
    return any(comparison_function(x) for x in groups)

def part1(lower, upper):
    valid_count = sum(validate_pwd(x, lambda x: x>=2) for x in range(lower, upper+1))
    print('Part 1 Answer:', valid_count)

def part2(lower, upper):
    valid_count = sum(validate_pwd(x, lambda x: x==2) for x in range(lower, upper+1))
    print('Part 1 Answer:', valid_count)

part1(183564, 657474)
part2(183564, 657474)
