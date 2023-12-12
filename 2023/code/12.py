def parse_input(filename):
    data = [line.strip() for line in open(filename, "r").readlines()]
    springs = []
    for line in data:
        pattern, groups = line.split()
        groups = tuple(int(x) for x in groups.split(","))
        springs.append((pattern, groups))
    return springs


cached_results = {}


def count_possibles(pattern, groups):
    # check cache for result
    if (pattern, groups) in cached_results.keys():
        return cached_results[(pattern, groups)]

    # if pattern done check that groups are done
    if pattern == "":
        return len(groups) == 0

    # if groups done check that no more '#' in pattern
    if groups == ():
        return "#" not in pattern

    count = 0
    # treat first character as '.' and move on
    if pattern[0] == "." or pattern[0] == "?":
        count += count_possibles(pattern[1:], groups)

    # treat first character as '#' (start the group)
    # check if enough space to finish group (length and no '.' in the way)
    # if not finishing the pattern, make sure the next char after group isn't '#'
    if (
        (pattern[0] == "#" or pattern[0] == "?")
        and groups[0] <= len(pattern)
        and "." not in pattern[: groups[0]]
        and (groups[0] == len(pattern) or pattern[groups[0]] != "#")
    ):
        # finish the group and continue
        count += count_possibles(pattern[groups[0] + 1 :], groups[1:])

    # cache result to speed up future calls
    cached_results[(pattern, groups)] = count
    return count


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/12.txt"
input = parse_input(puzzle)

print("Part 1:", sum(count_possibles(pattern, groups) for pattern, groups in input))
print(
    "Part 2:",
    sum(
        count_possibles("?".join([pattern] * 5), groups * 5)
        for pattern, groups in input
    ),
)
