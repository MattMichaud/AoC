
def build_pattern(base_pattern, digit_number):
    new_pattern = []
    for c in base_pattern:
        for _ in range(digit_number):
            new_pattern.append(c)
    return new_pattern


def complete_phase(original, base_pattern):
    res = ''
    for i in range(len(original)):
        pattern = build_pattern(base_pattern, i + 1)
        pattern_i = 1
        new_digit = 0
        for j in range(len(original)):
            new_digit += int(original[j]) * pattern[pattern_i]
            pattern_i = (pattern_i + 1) % (len(pattern))
        res = res + str(abs(new_digit) % 10)
    return res

def multiple_phases(original, base_pattern, num_phases):
    current = original
    for _ in range(num_phases):
        current = complete_phase(current, base_pattern)
    return current

base_pattern = [0, 1, 0, -1]
test_input = '80871224585914546619083218645595'
actual_input = '59709511599794439805414014219880358445064269099345553494818286560304063399998657801629526113732466767578373307474609375929817361595469200826872565688108197109235040815426214109531925822745223338550232315662686923864318114370485155264844201080947518854684797571383091421294624331652208294087891792537136754322020911070917298783639755047408644387571604201164859259810557018398847239752708232169701196560341721916475238073458804201344527868552819678854931434638430059601039507016639454054034562680193879342212848230089775870308946301489595646123293699890239353150457214490749319019572887046296522891429720825181513685763060659768372996371503017206185697'
output = multiple_phases(actual_input, base_pattern, 100)
print('Part 1 Answer: {}'.format(output[:8]))

from itertools import cycle, accumulate

# with open("data/day16.txt") as f:
#     s = f.read().strip()
s = actual_input
offset = int(s[:7])
digits = [int(i) for i in s]
# If `rep` is `digits` repeated 10K times, construct:
#     arr = [rep[-1], rep[-2], ..., rep[offset]]
l = 10000 * len(digits) - offset
i = cycle(reversed(digits))
arr = [next(i) for _ in range(l)]
# Repeatedly take the partial sums mod 10
for _ in range(100):
    arr = [n % 10 for n in accumulate(arr)]
print('Part 2 Answer: {}'.format("".join(str(i) for i in arr[-1:-9:-1])))