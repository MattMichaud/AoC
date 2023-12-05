def parse_input(filename):
    seeds, *maps = open(filename, "r").read().strip().split("\n\n")
    seeds = [int(x) for x in seeds.split()[1:]]
    rule_sets = []
    for map in maps:
        lines = map.split("\n")[1:]
        rules = [[int(x) for x in line.split()] for line in lines]
        rule_sets.append(rules)
    return seeds, rule_sets


def apply_rule(inp, rules):
    for dest, source, size in rules:
        if source <= inp < source + size:
            return inp + (dest - source)
    return inp


def apply_all_rules(inp, rule_sets):
    for rules in rule_sets:
        inp = apply_rule(inp, rules)
    return inp


def apply_rule_to_ranges(ranges, rules):
    added_ranges = []
    for dest, source, size in rules:
        source_end = source + size
        new_ranges = []
        while ranges:
            (start, end) = ranges.pop()
            left = (start, min(end, source))
            middle = (max(start, source), min(source_end, end))
            right = (max(source_end, start), end)
            if left[1] > left[0]:
                new_ranges.append(left)
            if middle[1] > middle[0]:
                added_ranges.append(
                    (middle[0] - source + dest, middle[1] - source + dest)
                )
            if right[1] > right[0]:
                new_ranges.append(right)
        ranges = new_ranges
    return ranges + added_ranges


def apply_all_rules_to_ranges(ranges, rule_sets):
    for rules in rule_sets:
        ranges = apply_rule_to_ranges(ranges, rules)
    return ranges


def part1(seeds, rule_sets):
    return min([apply_all_rules(s, rule_sets) for s in seeds])


def part2(seeds, rule_sets):
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    return min(
        [
            min(apply_all_rules_to_ranges([(start, end)], rule_sets))[0]
            for start, end in seed_ranges
        ]
    )


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/05.txt"
current_file = puzzle_file
s, r = parse_input(current_file)
print("Part 1:", part1(s, r))
print("Part 2:", part2(s, r))
