import z3
import operator

test_input = "test.txt"
puzzle_input = "2022/inputs/21.txt"
curr = puzzle_input

input_lines = [line for line in open(curr, "r").read().strip().split("\n")]
ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

s1 = z3.Solver()
s2 = z3.Solver()
for line in input_lines:
    name, expr = line.split(": ")
    expr = expr.split()
    if len(expr) == 1:  # and name != "humn":
        s1.add(z3.Real(name) == int(expr[0]))
        if name != "humn":
            s2.add(z3.Real(name) == int(expr[0]))

    elif len(expr) == 3:
        left, op, right = expr
        s1.add(z3.Real(name) == ops.get(op)(z3.Real(left), z3.Real(right)))
        if name != "root":
            s2.add(z3.Real(name) == ops.get(op)(z3.Real(left), z3.Real(right)))
        else:
            s2.add(z3.Real(left) == z3.Real(right))

assert s1.check() == z3.sat
model = s1.model()
part1 = model.eval(z3.Real("root"))
print("Part 1:", part1)

assert s2.check() == z3.sat
m2 = s2.model()
part2 = m2[z3.Real("humn")].as_long()
print("Part 2:", part2)
