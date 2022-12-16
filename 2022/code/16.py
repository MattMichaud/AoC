import re

test_file = "test.txt"
puzzle_file = "2022/inputs/16.txt"
current_file = puzzle_file

MAX_PATHS = 20000


def parse_input(filename):
    file_data = open(filename, "r").read()
    loc_data_raw = re.findall(r"Valve (\w\w).*?rate=(\d+).*?valves? (.*)", file_data)
    flow_rates = dict((loc, int(rate)) for loc, rate, _ in loc_data_raw)
    tunnels = dict(
        (loc, dests.replace(" ", "").split(",")) for loc, _, dests in loc_data_raw
    )
    return tunnels, flow_rates


def part1(t, r, sl):
    # paths is a list of tuples containing (pressure, path as list, opened as set)
    paths = [(0, [sl], set())]
    for time in range(1, 31):
        # slim down paths
        if len(paths) > MAX_PATHS:
            paths.sort(reverse=True)
            paths = paths[:MAX_PATHS]
        # print("time:", time, "path count:", len(paths))
        new_paths = []
        for total_pressure, path, open_valves in paths:
            current_loc = path[-1]
            pressure = sum(r[ov] for ov in open_valves)
            total_pressure += pressure
            # either move or open
            for loc in t[current_loc]:
                new_paths.append((total_pressure, path + [loc], open_valves.copy()))
            if r[current_loc] > 0 and current_loc not in open_valves:
                new_paths.append((total_pressure, path, open_valves | {current_loc}))
        paths = new_paths
    return max(paths)


def get_moves_valves(t, r, curr_loc, pth, ovs):
    # return list of options to either open valve or use tunnel
    res = []
    for loc in t[curr_loc]:
        res.append((pth + [loc], ovs.copy()))
    if r[curr_loc] > 0 and curr_loc not in ovs:
        res.append((pth, ovs | {curr_loc}))
    return res


# part 2 is similar but essentially 2 people (me, elephant) operating each second for 26 seconds
def part2(t, r, sl):
    # paths is a list of tuples containing (total pressure, path as list of tuples, opened as set)
    paths = [(0, ([sl], [sl]), set())]
    for time in range(1, 27):
        # slim down paths
        if len(paths) > MAX_PATHS:
            paths.sort(reverse=True)
            paths = paths[:MAX_PATHS]
        # print("time:", time, "path count:", len(paths))
        new_paths = []
        for total_pressure, path, open_valves in paths:
            me_loc = path[0][-1]
            ele_loc = path[1][-1]
            pressure = sum(r[ov] for ov in open_valves)
            total_pressure += pressure
            # either move or open for me and ele
            for loc_me, open_me in get_moves_valves(t, r, me_loc, path[0], open_valves):
                for loc_ele, open_ele in get_moves_valves(
                    t, r, ele_loc, path[1], open_me
                ):
                    new_paths.append((total_pressure, ([loc_me, loc_ele]), open_ele))
        paths = new_paths
    return max(paths)


tunnels, rates = parse_input(current_file)

max_pressure, *_ = part1(tunnels, rates, "AA")
print("Part 1:", max_pressure)

pressure, *_ = part2(tunnels, rates, "AA")
print("Part 2:", pressure)
