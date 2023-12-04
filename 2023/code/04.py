with open("2023/inputs/04.txt", "r") as f:
    data = f.read().splitlines()
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
print("Part 1 Answer:", sum(v["score"] for v in Cards.values()))
print("Part 2 Answer:", sum(v["copies"] for v in Cards.values()))
