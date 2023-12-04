def scratch_cards(filename):
    with open(filename, "r") as f:
        data = f.read().splitlines()

    p1 = 0
    Cards = {}
    for line in data:
        card_num = int(line.split()[1][:-1])
        line = line.split()[2:]
        winners = [int(x) for x in line[: line.index("|")]]
        numbers = [int(x) for x in line[line.index("|") + 1 :]]
        matches = sum(item in winners for item in numbers)
        score = int(2 ** (matches - 1) * (matches > 0))
        Cards[card_num] = {"copies": 1, "matches": matches, "score": score}

    for c in range(1, max(Cards.keys()) + 1):
        for offset in range(Cards[c]["matches"]):
            Cards[c + 1 + offset]["copies"] += Cards[c]["copies"]

    p1 = sum(v["score"] for v in Cards.values())
    p2 = sum(v["copies"] for v in Cards.values())
    print("Part 1 Answer:", p1)
    print("Part 2 Answer:", p2)
    return


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/04.txt"
current_file = puzzle_file
inp = scratch_cards(current_file)
