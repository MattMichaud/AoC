def snafu2dec(s):
    res = 0
    for index, digit in enumerate(s[::-1]):
        if digit == "-":
            num = -1
        elif digit == "=":
            num = -2
        else:
            num = int(digit)
        place = 5**index
        res += num * place
    return res


def dec2snafu(d):
    if d == 0:
        return ""
    else:
        return dec2snafu((d + 2) // 5) + "012=-"[d % 5]


test_inp = "test.txt"
puzz_inp = "2022/inputs/25.txt"
curr_inp = puzz_inp

input = open(curr_inp, "r").read().strip().split("\n")
total_dec = sum(snafu2dec(n) for n in input)
total_snafu = dec2snafu(total_dec)
print("Part 1:", total_snafu)
