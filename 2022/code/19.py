import re
import collections as cl


def parse_input(file):
    return [
        tuple(map(int, re.findall(r"\d+", line)))
        for line in open(file, "r").read().strip().split("\n")
    ]


# blueprint format:
# (
#   blue_print_number,
#   ore_robot_ore_cost,
#   clay_robot_clay_cost,
#   obs_robot_ore_cost, obs_robot_clay_cost
#   geo_robot_ore_cost, geo_robot_obs_cost
# )


def find_max_geodes(
    ore_rob_ore_cost,
    cla_rob_ore_cost,
    obs_rob_ore_cost,
    obs_rob_cla_cost,
    geo_rob_ore_cost,
    geo_rob_obs_cost,
    max_time=24,
):
    system_states = cl.deque()
    # state format: time, tuple(ore, clay, obs, geo, ore_robs, cla_robs, obs_robs, geo_robs)
    initial_state = (0, (0, 0, 0, 0, 1, 0, 0, 0))  # start with 1 ore robot
    system_states.append(initial_state)
    previous_processed_states = set()

    most_geodes_made = 0
    while len(system_states) > 0:
        elapsed_time, (
            ore,
            cla,
            obs,
            geo,
            ore_robs,
            cla_robs,
            obs_robs,
            geo_robs,
        ) = system_states.popleft()
        most_geodes_made = max(most_geodes_made, geo)

        # check if we've already processed this state, if so move on, if not add it to ones we've processed
        if (
            ore,
            cla,
            obs,
            geo,
            ore_robs,
            cla_robs,
            obs_robs,
            geo_robs,
        ) in previous_processed_states or elapsed_time == max_time:
            continue
        previous_processed_states.add(
            (ore, cla, obs, geo, ore_robs, cla_robs, obs_robs, geo_robs)
        )

        time_remaining = max_time - elapsed_time
        # get the max geodes possible if we were to buy one geode robot per turn remaining
        max_geo_possible = (
            geo
            + time_remaining * geo_robs
            + (time_remaining * (time_remaining + 1) // 2)
        )
        # if we can't get enough to beat the max, move on from this scenario
        if max_geo_possible < most_geodes_made:
            continue

        # buy geode robot (always best option if affordable)
        if obs >= geo_rob_obs_cost and ore >= geo_rob_ore_cost:
            system_states.append(
                (
                    elapsed_time + 1,
                    (
                        ore + ore_robs - geo_rob_ore_cost,  # spend ore
                        cla + cla_robs,
                        obs + obs_robs - geo_rob_obs_cost,  # spend obs
                        geo + geo_robs,
                        ore_robs,
                        cla_robs,
                        obs_robs,
                        geo_robs + 1,  # add geo robot
                    ),
                )
            )
        else:  # consider buying other robots or advancing time

            # buy ore robot?
            max_ore_cost = max(
                ore_rob_ore_cost, cla_rob_ore_cost, obs_rob_ore_cost, geo_rob_ore_cost
            )
            if (
                # can afford and haven't reached max output
                ore >= ore_rob_ore_cost
                and ore_robs < max_ore_cost
                and ore + time_remaining * ore_robs < time_remaining * max_ore_cost
            ):
                # buy one ore robot
                system_states.append(
                    (
                        elapsed_time + 1,
                        (
                            ore + ore_robs - ore_rob_ore_cost,  # spend ore
                            cla + cla_robs,
                            obs + obs_robs,
                            geo + geo_robs,
                            ore_robs + 1,  # add ore robot
                            cla_robs,
                            obs_robs,
                            geo_robs,
                        ),
                    )
                )
            # buy one clay robot?
            if (
                # can afford and haven't reached max output
                ore >= cla_rob_ore_cost
                and cla_robs < obs_rob_cla_cost
                and cla + time_remaining * cla_robs < time_remaining * obs_rob_cla_cost
            ):
                # buy one clay robot
                system_states.append(
                    (
                        elapsed_time + 1,
                        (
                            ore + ore_robs - cla_rob_ore_cost,  # spend ore
                            cla + cla_robs,
                            obs + obs_robs,
                            geo + geo_robs,
                            ore_robs,
                            cla_robs + 1,  # add clay robot
                            obs_robs,
                            geo_robs,
                        ),
                    )
                )
            # buy one obsidian robot?
            if (
                # can afford and haven't reached max output
                ore >= obs_rob_ore_cost
                and cla >= obs_rob_cla_cost
                and obs_robs < geo_rob_obs_cost
                and obs + time_remaining * obs_robs < time_remaining * geo_rob_obs_cost
            ):
                # buy one obsidisan robot
                system_states.append(
                    (
                        elapsed_time + 1,
                        (
                            ore + ore_robs - obs_rob_ore_cost,  # spend ore
                            cla + cla_robs - obs_rob_cla_cost,  # spend clay
                            obs + obs_robs,
                            geo + geo_robs,
                            ore_robs,
                            cla_robs,
                            obs_robs + 1,  # add obsidian robot
                            geo_robs,
                        ),
                    )
                )
            # don't buy anything and just let robots work
            system_states.append(
                (
                    elapsed_time + 1,
                    (
                        ore + ore_robs,
                        cla + cla_robs,
                        obs + obs_robs,
                        geo + geo_robs,
                        ore_robs,
                        cla_robs,
                        obs_robs,
                        geo_robs,
                    ),
                )
            )

    return most_geodes_made


test = "test.txt"
puzzle = "2022/inputs/19.txt"
curr_file = puzzle

blueprints = parse_input(curr_file)

# part 1 - sum quality level of all blueprints
total_quality_level = 0
for bp in blueprints:
    bp_num = bp[0]
    bp_info = bp[1:]
    mg = find_max_geodes(*bp_info)
    quality_level = bp_num * mg
    # print("BP:", bp_num, "MAX:", mg, "QL:", quality_level)
    total_quality_level += quality_level
print("Part 1:", total_quality_level)

# part 2 - product of max geodes for first 3 blueprints
mgp = 1
for bp in blueprints[:3]:
    bp_num = bp[0]
    bp_info = bp[1:]
    mg = find_max_geodes(*bp_info, max_time=32)
    quality_level = bp_num * mg
    # print("BP:", bp_num, "MAX:", mg, "QL:", quality_level)
    mgp = mgp * mg
print("Part 2:", mgp)
