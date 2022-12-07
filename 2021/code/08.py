test_file = "test.txt"
puzzle_file = "2021/inputs/08.txt"
input_file = puzzle_file

displays = [x.split(" | ") for x in open(input_file).read().strip().split("\n")]
input_displays = [display[0].split() for display in displays]
output_displays = [display[1].split() for display in displays]

print(
    "Part 1:",
    sum(
        sum(len(digits) in [2, 3, 4, 7] for digits in display)
        for display in output_displays
    ),
)

# in 2 = TOP_RIGHT or BOTTOM_RIGHT
# in 3 but not 2 = TOP_MIDDLE
# in 4 but not 2 = MIDDLE_MIDDLE or TOP_LEFT
# same as digits of 4 but with TOP_MIDDLE and one more = number 9 = one more is BOTTOM_MIDDLE
