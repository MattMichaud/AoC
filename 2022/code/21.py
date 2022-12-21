import math


def parse_input(file):
    input_lines = [line for line in open(curr, "r").read().strip().split("\n")]
    jobs = {}
    for line in input_lines:
        words = line.split()
        monkey_name = words[0][:-1]
        expression = line.split(":")[1].split()
        jobs[monkey_name] = expression
    return jobs


def job_output(jobs, name, human_number):
    expression_parts = jobs[name]
    if name == "humn" and human_number >= 0:
        return human_number  # added for part 2 of problem

    # if we have a number, return it, otherwise do the expression indicated (recursive)
    if len(expression_parts) < 2:
        return int(expression_parts[0])
    else:
        expression_part1 = job_output(jobs, expression_parts[0], human_number)
        expression_part2 = job_output(jobs, expression_parts[2], human_number)
        op = expression_parts[1]
        if op == "+":
            return expression_part1 + expression_part2
        elif op == "-":
            return expression_part1 - expression_part2
        elif op == "*":
            return expression_part1 * expression_part2
        elif op == "/":
            return expression_part1 / expression_part2


test_input = "test.txt"
puzzle_input = "2022/inputs/21.txt"
curr = puzzle_input

monkey_jobs = parse_input(curr)
root_result = int(job_output(monkey_jobs, "root", -1))
print("Part 1:", root_result)

# for part 2, we need the first part of the root expression
# equal to second part of the human expression
root_exp1 = monkey_jobs["root"][0]
root_exp2 = monkey_jobs["root"][2]

# one of them isn't dependent on the input, figure out which one, and make sure that's set to root_exp2
if job_output(monkey_jobs, root_exp2, 0) != job_output(monkey_jobs, root_exp2, 1):
    root_exp1, root_exp2 = root_exp2, root_exp1
assert job_output(monkey_jobs, root_exp1, 0) != job_output(monkey_jobs, root_exp1, 1)
assert job_output(monkey_jobs, root_exp2, 0) == job_output(monkey_jobs, root_exp2, 1)


# try it both directions, only one should work and produce an output
expr1_goal = job_output(monkey_jobs, root_exp2, 0)
low = 0
high = int(1e20)
while low < high and abs(high - low) > 1:
    middle = (low + high) // 2
    current_result = expr1_goal - job_output(monkey_jobs, root_exp1, middle)
    if current_result < 0:
        low = middle
    elif current_result == 0:  # found correct input
        print("Part 2:", middle)
        break
    else:
        high = middle

# reset and try from the other direction
low = 0
high = int(1e20)
while low < high and abs(high - low) > 1:
    middle = (low + high) // 2
    current_result = expr1_goal - job_output(monkey_jobs, root_exp1, middle)
    if current_result < 0:
        high = middle
    elif current_result == 0:  # found correct input
        print("Part 2b:", middle)
        break
    else:
        low = middle
