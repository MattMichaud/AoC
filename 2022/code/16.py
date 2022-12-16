import re


MAX_SCENARIOS = 15000  # 10k wasn't enough for part 2 ... wrong answer


def parse_input(filename):
    file_data = open(filename, "r").read()
    loc_data_raw = re.findall(r"Valve (\w\w).*?rate=(\d+).*?valves? (.*)", file_data)
    flow_rates = dict((loc, int(rate)) for loc, rate, _ in loc_data_raw)
    tunnels = dict(
        (loc, dests.replace(" ", "").split(",")) for loc, _, dests in loc_data_raw
    )
    return tunnels, flow_rates


def get_paths_valves_opts(t, r, curr_loc, pth, ovs):
    # return list of options to either add to path (move) or open a valve
    res = []
    for loc in t[curr_loc]:
        res.append((pth + [loc], ovs.copy()))
    if r[curr_loc] > 0 and curr_loc not in ovs:
        res.append((pth, ovs | {curr_loc}))
    return res


def part1(tunnels, rates, start_loc):
    # scenarios is a list of tuples containing (pressure, paths as list, opened valves as set)
    scenarios = [(0, [start_loc], set())]
    for time in range(1, 31):
        # slim down scenarios
        if len(scenarios) > MAX_SCENARIOS:
            scenarios.sort(reverse=True)
            scenarios = scenarios[:MAX_SCENARIOS]
        updated_scenarios = []
        for total_pressure, path, open_valves in scenarios:
            current_loc = path[-1]
            pressure = sum(rates[ov] for ov in open_valves)
            total_pressure += pressure
            # either move or open
            for new_path, new_open in get_paths_valves_opts(
                tunnels, rates, current_loc, path, open_valves
            ):
                updated_scenarios.append((total_pressure, new_path, new_open))
        scenarios = updated_scenarios
    return max(scenarios)


# part 2 is similar but essentially 2 people (me, elephant) operating each second for 26 seconds
def part2(tunnels, rates, start_loc):
    # scenarios is a list of tuples containing (total pressure, me & ele paths as list of tuples, opened valves as set)
    scenarios = [(0, ([start_loc], [start_loc]), set())]
    for time in range(1, 27):
        # slim down scenarios
        if len(scenarios) > MAX_SCENARIOS:
            scenarios.sort(reverse=True)
            scenarios = scenarios[:MAX_SCENARIOS]
        updated_scenarios = []
        for total_pressure, path, open_valves in scenarios:
            me_loc = path[0][-1]
            ele_loc = path[1][-1]
            pressure = sum(rates[ov] for ov in open_valves)
            total_pressure += pressure
            # either move or open for me, then move or open for and ele (with new valves I opened)
            for new_path_me, new_open_me in get_paths_valves_opts(
                tunnels, rates, me_loc, path[0], open_valves
            ):
                for new_path_ele, new_open_ele in get_paths_valves_opts(
                    tunnels, rates, ele_loc, path[1], new_open_me
                ):
                    updated_scenarios.append(
                        (total_pressure, (new_path_me, new_path_ele), new_open_ele)
                    )
        scenarios = updated_scenarios
    return max(scenarios)


test_file = "test.txt"
puzzle_file = "2022/inputs/16.txt"
current_file = puzzle_file
puzzle_tunnels, puzzle_rates = parse_input(current_file)

max_pressure, *_ = part1(puzzle_tunnels, puzzle_rates, "AA")
print("Part 1:", max_pressure)

pressure, *_ = part2(puzzle_tunnels, puzzle_rates, "AA")
print("Part 2:", pressure)
