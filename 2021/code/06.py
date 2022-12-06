import collections as cl

input_file = "test.txt"
input_file = "2021/inputs/06.txt"
lanternfish = cl.Counter(
    int(fish) for fish in open(input_file, "r").read().strip().split(",")
)


def population_change(fish, days):
    for _ in range(days):
        new_fish = cl.Counter()
        for age, number in fish.items():
            if age <= 0:
                new_fish[6] += number
                new_fish[8] += number
            else:
                new_fish[age - 1] += number
        fish = new_fish
    return fish


part1 = population_change(lanternfish, 80)
print("Part 1:", sum(part1.values()))
# to figure out 256 days worth, just need to go forward 256 - 80 days since we've done 80 already
part2 = population_change(part1, (256 - 80))
print("Part 2:", sum(part2.values()))
