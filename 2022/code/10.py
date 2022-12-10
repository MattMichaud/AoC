test_input = "test.txt"
puzzle_input = "2022/inputs/10.txt"
current_file = puzzle_input

instructions = open(current_file, "r").read().strip().split("\n")
curr_register = 1
register_results = [curr_register]
for inst in instructions:
    if inst == "noop":
        register_results.append(curr_register)
    elif inst.startswith("addx"):
        val = int(inst.split(" ")[1])
        register_results.append(curr_register)
        register_results.append(curr_register)
        curr_register += val

i = 0
signal_strength = 0
while (20 + i * 40) < len(register_results):
    signal_strength += (20 + i * 40) * register_results[(20 + i * 40)]
    i += 1

print("Part 1:", signal_strength)

CRT = []
for row in range(6):
    CRT_row = []
    for pixel_pos in range(40):
        reg = ((40 * row) + pixel_pos) + 1
        sprite_pos = register_results[reg]
        if pixel_pos in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            out_char = "#"
        else:
            out_char = " "
        CRT_row.append(out_char)
    CRT.append("".join(CRT_row))

print("Part 2:")
for row in CRT:
    print(row)
