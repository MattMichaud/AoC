from collections import defaultdict


def parse_input(filename):
    data = open(filename, "r").read().splitlines()
    hands = []
    for d in data:
        hand, bid = d.split()
        hands.append((hand, int(bid)))
    return hands


def hand_rank(hand, joker=False):
    cards = defaultdict(int)
    jokers = 0
    if joker and "J" in hand:
        new_hand = ""
        for card in hand:
            if card == "J":
                jokers += 1
            else:
                new_hand += card
        hand = new_hand
    for card in hand:
        cards[card] += 1
    counts = sorted(cards.values(), reverse=True)
    if jokers == 5:
        return 6  # five of a kind
    elif counts[0] + jokers == 5:
        return 6  # five of a kind
    elif counts[0] + jokers == 4:
        return 5  # four of a kind
    elif counts[0] + jokers == 3 and counts[1] == 2:
        return 4  # full house
    elif counts[0] + jokers == 3:
        return 3  # three of a kind
    elif counts[0] == 2 and counts[1] == 2:
        return 2  # two pair
    elif counts[0] + jokers == 2:
        return 1  # one pair
    else:
        return 0  # high card


def hand_sort_value(hand, joker=False):
    sv = []
    vals = {"A": "14", "K": "13", "Q": "12", "J": "11", "T": "10"}
    if joker:
        vals["J"] = "01"
    for card in hand:
        if card.isdigit():
            sv.append("0" + card)
        else:
            sv.append(vals[card])
    return "".join(sv)


def sorted_ranked_hands(hands, joker=False):
    ranked_hands = [
        (h, b, float(str(hand_rank(h, joker)) + "." + hand_sort_value(h, joker)))
        for h, b in hands
    ]
    ranked_hands.sort(key=lambda x: x[2])
    return ranked_hands


def calc_winnings(hand_list):
    return sum([(i + 1) * b for i, (_, b, _) in enumerate(hand_list)])


test_file = "2023/inputs/test.txt"
puzzle_file = "2023/inputs/07.txt"
current_file = puzzle_file
hands = parse_input(current_file)
print("Part 1 Answer:", calc_winnings(sorted_ranked_hands(hands)))
print("Part 2 Answer:", calc_winnings(sorted_ranked_hands(hands, True)))
