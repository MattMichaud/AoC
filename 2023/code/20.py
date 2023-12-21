import sys

sys.path.append(".")
from utils import lcm
from collections import deque, defaultdict


def parse_input(filename):
    data = open(filename, "r").read().strip().split("\n")
    modules = {}
    for line in data:
        source, destinations = line.split(" -> ")
        source_type = source[0] if source != "broadcaster" else source
        source_name = source[1:] if source != "broadcaster" else source
        destinations = [d for d in destinations.split(", ")]
        inputs = {}
        module = {
            "type": source_type,
            "inputs": inputs,
            "destinations": destinations,
            "state": "off",
        }
        modules[source_name] = module
    return modules


def initialize_inputs(module_list):
    for module in module_list.keys():
        # print(module)
        input_list = {}
        for key, value in module_list.items():
            if key != module and module in value["destinations"]:
                input_list[key] = "low"
        module_list[module]["inputs"] = input_list
        # print(module_list[module])
    return module_list


def push_the_button(max_presses, module_list, debug=False):
    # pulse is a tuple of (from, to, type)
    initial_pulse = ("button", "broadcaster", "low")
    pulses = deque()
    low_count = 0
    high_count = 0

    # needed for part 2
    watch_list = list(module_list["rs"]["inputs"].keys())  # which inputs feed into 'rs'
    previous_times = {}  # the last time each module received a 'low'
    counts = defaultdict(int)  # the number of times each module received a 'low'
    cycle_lengths = []  # the length between first and second 'low'

    for t in range(1, max_presses + 1):
        pulses.append(initial_pulse)
        while pulses:
            current_pulse = pulses.popleft()
            pulse_source, pulse_target, pulse_type = current_pulse

            # find cycles for part 2
            if pulse_type == "low":
                # for each input into our target 'rs', when it receives its second low, figure out its cycle time
                if (
                    pulse_target in previous_times
                    and counts[pulse_target] == 2
                    and pulse_target in watch_list
                ):
                    cycle_lengths.append(t - previous_times[pulse_target])
                previous_times[pulse_target] = t
                counts[pulse_target] += 1

            # check to see if we have enough cycle times (one for each input in watch_list)
            if len(cycle_lengths) == len(watch_list):
                # the LCM of the cycle times will be when we get one low pulse from 'rs'
                print("Part 2:", lcm(cycle_lengths))
                return

            # update pulse counts
            if pulse_type == "low":
                low_count += 1
            else:
                high_count += 1
            if debug:
                print(pulse_source, "-", pulse_type, "->", pulse_target)

            if pulse_target not in module_list.keys():
                continue

            target_module = module_list[pulse_target]
            target_type = target_module["type"]

            # print("target type", target_type)
            if target_type == "broadcaster":
                # pass pulse on to all destinations
                for dest in target_module["destinations"]:
                    # print("sent", pulse_type, "to", dest)
                    pulses.append((pulse_target, dest, pulse_type))

            elif target_type == "%":
                # Flip-flop module
                # ignore high pulse
                # low pulse flips state
                # if state was off, flip on and send high pulse
                # if state was on, flip to off and send low pulse
                if pulse_type == "high":
                    continue
                else:
                    if target_module["state"] == "off":
                        target_module["state"] = "on"
                        new_pulse_type = "high"
                    elif target_module["state"] == "on":
                        target_module["state"] = "off"
                        new_pulse_type = "low"
                    else:
                        print("ERROR STATE")
                    for dest in target_module["destinations"]:
                        # print("sent", new_pulse_type, "to", dest)
                        pulses.append((pulse_target, dest, new_pulse_type))

            elif target_type == "&":
                # Conjunction module
                # remembers type of pulse from most recent input
                # first update memory for source
                # if all remembered are high, send low pulse
                # otherwise send high pulse
                target_module["inputs"][pulse_source] = pulse_type
                new_pulse_type = (
                    "low"
                    if all(v == "high" for v in target_module["inputs"].values())
                    else "high"
                )
                for dest in target_module["destinations"]:
                    pulses.append((pulse_target, dest, new_pulse_type))

        # print out the answer at step 1000 for part 1
        if t == 1000:
            print("Part 1:", low_count * high_count)

    return low_count * high_count


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/20.txt"
filename = puzzle

modules = parse_input(filename)
modules = initialize_inputs(modules)

button_presses = 10**6
push_the_button(button_presses, modules, False)
