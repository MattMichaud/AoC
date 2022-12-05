import sys

sys.path.append(".")
from utils import data_import

# A = ROCK, B = PAPER, C = SCISSORS
# X = ROCK, Y = PAPER, Z = SCISSORS


def outcome_score(opp, you):
    if (
        (opp == "A" and you == "X")
        or (opp == "B" and you == "Y")
        or (opp == "C" and you == "Z")
    ):
        return 3
    elif (
        (opp == "A" and you == "Y")
        or (opp == "B" and you == "Z")
        or (opp == "C" and you == "X")
    ):
        return 6
    else:
        return 0


def shape_score(shape):
    if shape == "A" or shape == "X":
        return 1
    elif shape == "B" or shape == "Y":
        return 2
    else:
        return 3


def part1(turn_list):
    score = 0
    for a, b in turn_list:
        round_score = outcome_score(a, b) + shape_score(b)
        score += round_score
    print("Part 1 Answer", score)


def part2(turn_list):
    score = 0
    for them, desired_outcome in turn_list:
        if desired_outcome == "X":
            # need to lose
            if them == "A":
                you = "Z"
            elif them == "B":
                you = "X"
            elif them == "C":
                you = "Y"
        if desired_outcome == "Y":
            # need to draw
            if them == "A":
                you = "X"
            elif them == "B":
                you = "Y"
            elif them == "C":
                you = "Z"
        if desired_outcome == "Z":
            # need to win
            if them == "A":
                you = "Y"
            elif them == "B":
                you = "Z"
            elif them == "C":
                you = "X"
        turn_score = outcome_score(them, you) + shape_score(you)
        score += turn_score
    print("Part 2 Answer", score)


inp_file = "2022/inputs/test.txt"
inp_file = "2022/inputs/02.txt"
turns = data_import(inp_file, str, " ")
part1(turns)
part2(turns)
