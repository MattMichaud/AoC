def parse_input(filename):
    data = open(filename, "r").read().strip().split("\n\n")
    patterns = []
    for group in data:
        pattern = [[char for char in row] for row in group.split("\n")]
        patterns.append(pattern)
    return patterns


def score_pattern(p):
    summary_p1 = 0  # no mismatches
    summary_p2 = 0  # exactly 1 mismatch
    rows = len(p)
    cols = len(p[0])
    # find vertical symmetry
    for c in range(cols - 1):  # don't check the last column
        mismatches = 0
        for delta in range(cols):
            left_col_check = c - delta
            right_col_check = c + 1 + delta
            # make sure they are valid and within bounds
            if (
                0 <= left_col_check
                and left_col_check < right_col_check
                and right_col_check < cols
            ):
                # check elements of all rows in those cols against each other
                for r in range(rows):
                    if p[r][left_col_check] != p[r][right_col_check]:
                        mismatches += 1
        if mismatches == 0:
            summary_p1 += c + 1  # row nums are 1-indexed in problem
        elif mismatches == 1:
            summary_p2 += c + 1  # row nums are 1-indexed in problem
    # find horizontal symmetry
    for r in range(rows - 1):  # don't check the last row
        mismatches = 0
        for delta in range(rows):
            top_row_check = r - delta
            bottom_row_check = r + 1 + delta
            # make sure they are valid and within bounds
            if (
                0 <= top_row_check
                and top_row_check < bottom_row_check
                and bottom_row_check < rows
            ):
                # check elements of all cols in those rows against each other
                for c in range(cols):
                    if p[top_row_check][c] != p[bottom_row_check][c]:
                        mismatches += 1
        if mismatches == 0:
            summary_p1 += 100 * (r + 1)  # col nums are 1-indexed in problem
        elif mismatches == 1:
            summary_p2 += 100 * (r + 1)  # col nums are 1-indexed in problem
    return (summary_p1, summary_p2)


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/13.txt"
patterns = parse_input(puzzle)
summaries = [score_pattern(p) for p in patterns]
print("Part 1:", sum(s[0] for s in summaries))
print("Part 2:", sum(s[1] for s in summaries))
