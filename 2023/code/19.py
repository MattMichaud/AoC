from collections import deque


def parse_input(fname):
    data = open(fname, "r").read().strip()
    flows, parts = data.split("\n\n")
    workflows = {}
    for flow in flows.split("\n"):
        name = flow[: flow.find("{")]
        rules = flow[flow.find("{") + 1 : -1].split(",")
        workflows[name] = rules

    part_ratings = []
    for p in parts.split("\n"):
        p = p[1:-1].split(",")
        p_dict = {}
        for item in p:
            letter, value = item.split("=")
            p_dict[letter] = int(value)
        part_ratings.append(p_dict)

    return workflows, part_ratings


def process_part(part, workflows):
    curr_wf_name = "in"  # start with 'in' workflow
    completed = False
    while not completed:
        workflow = workflows[curr_wf_name]
        for rule in workflow:
            # figure out rule type and apply
            # use break to finish out a workflow and go on to next workflow
            if ":" in rule:  # comparison rule
                category = rule[0]
                operator = rule[1]
                comp_value = int(rule[2 : rule.find(":")])
                new_flow = rule[rule.find(":") + 1 :]
                if operator == ">":
                    if part[category] > comp_value:
                        curr_wf_name = new_flow
                        break
                elif operator == "<":
                    if part[category] < comp_value:
                        curr_wf_name = new_flow
                        break
            else:  # statement rule
                curr_wf_name = rule
                break
        if curr_wf_name in ["A", "R"]:
            completed = True
    return curr_wf_name


def part2(workflows):
    # similar to the other day when we had to send ranges through rules
    start_ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    start_flow = "in"
    flow_step_and_ranges = deque()
    flow_step_and_ranges.append((start_flow, start_ranges))
    total_combinations = 0
    while flow_step_and_ranges:
        flow_name, ranges = flow_step_and_ranges.popleft()
        # check for any invalid ranges
        for key, r in ranges.items():
            if r[0] > r[1]:
                print("INVALID RANGE", key, r)
            continue

        if flow_name == "A":  # count up combinations that were accepted
            combos = (
                (ranges["x"][1] - ranges["x"][0] + 1)
                * (ranges["m"][1] - ranges["m"][0] + 1)
                * (ranges["a"][1] - ranges["a"][0] + 1)
                * (ranges["s"][1] - ranges["s"][0] + 1)
            )
            total_combinations += combos
            continue  # done with this combination

        elif flow_name == "R":
            continue  # done with this combination

        else:
            workflow = workflows[flow_name]
            # process each rule of the workflow
            # split the ranges and append to the flow_step_and_ranges

            for rule in workflow:
                if ":" in rule:  # comparison rule
                    category = rule[0]  # which rating category
                    operator = rule[1]  # which type of operation (< or >)
                    comp_value = int(rule[2 : rule.find(":")])  # value to split on
                    new_flow = rule[rule.find(":") + 1 :]  # worflow to pass on
                    cr_low, cr_high = ranges[category]  # current range
                    if operator == ">":
                        # split range into two sections: pass_on and keep
                        pass_on_low = max(cr_low, comp_value + 1)
                        pass_on_high = cr_high
                        keep_low = cr_low
                        keep_high = min(cr_high, comp_value)
                        pass_on_ranges = ranges.copy()
                        pass_on_ranges[category] = (pass_on_low, pass_on_high)
                        flow_step_and_ranges.append(
                            (new_flow, pass_on_ranges)
                        )  # pass_on gets added to queue with the new flow_step
                        ranges[category] = (
                            keep_low,
                            keep_high,
                        )  # keep becomes new range to continue with rules for this flow
                    elif operator == "<":
                        # split range into two sections: pass_on and keep
                        pass_on_low = cr_low
                        pass_on_high = min(cr_high, comp_value - 1)
                        keep_low = max(cr_low, comp_value)
                        keep_high = cr_high
                        pass_on_ranges = ranges.copy()
                        pass_on_ranges[category] = (pass_on_low, pass_on_high)
                        flow_step_and_ranges.append(
                            (new_flow, pass_on_ranges)
                        )  # pass_on gets added to queue with the new flow_step
                        ranges[category] = (
                            keep_low,
                            keep_high,
                        )  # keep becomes new range to continue with rules for this flow

                else:
                    # statement rule
                    # add back into queue with new flow name
                    flow_step_and_ranges.append((rule, ranges))

    return total_combinations


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/19.txt"
filename = puzzle

wfs, prs = parse_input(filename)
total_ratings = 0
for part in prs:
    if process_part(part, wfs) == "A":
        total_ratings += sum(part.values())
print("Part 1:", total_ratings)
print("Part 2:", part2(wfs))
