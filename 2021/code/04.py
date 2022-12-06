filename = "2021/inputs/04.txt"
calls, *boards = open(filename).read().strip().split("\n\n")
calls = [int(c) for c in calls.split(",")]
boards = [
    [[int(el) for el in ln.split()] for ln in board.strip().split("\n")]
    for board in boards
]


def score(board, calls):
    score = (
        sum(
            board[i][j] if board[i][j] not in calls else 0
            for i in range(5)
            for j in range(5)
        )
        * calls[-1]
    )
    return score


winners = {}
for i in range(len(calls)):
    called = set(calls[:i])

    for j, board in enumerate(boards):
        if j in winners.keys():
            continue  # already a winner

        # winner?
        if any(all(board[k][l] in called for k in range(5)) for l in range(5)) or any(
            all(board[l][k] in called for k in range(5)) for l in range(5)
        ):
            winners[j] = i

first = min(winners, key=winners.get)
last = max(winners, key=winners.get)

print("Part 1:", score(boards[first], calls[: winners[first]]))
print("Part 1:", score(boards[last], calls[: winners[last]]))
