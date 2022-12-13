test_file = "test.txt"
puzzle_file = "2022/inputs/13.txt"
current_file = puzzle_file

pairs = open(current_file, "r").read().strip().split("\n\n")
pairs = [p.split("\n") for p in pairs]
packet_pairs = []
for pair in pairs:
    packet_pairs.append([eval(i) for i in pair])


def compare(left, right):
    left_int = isinstance(left, int)
    right_int = isinstance(right, int)
    if left_int and right_int:
        if left < right:
            return "RIGHT"
        elif left == right:
            return "CONTINUE"
        else:
            return "WRONG"
    elif left_int and not right_int:
        return compare([left], right)
    elif not left_int and right_int:
        return compare(left, [right])
    else:
        i = 0
        status = "CONTINUE"
        while status == "CONTINUE":
            if i + 1 > len(left) and i + 1 > len(right):
                return status
            elif i + 1 > len(left):
                return "RIGHT"
            elif i + 1 > len(right):
                return "WRONG"
            else:
                status = compare(left[i], right[i])
            i += 1

        return status


print(
    "Part 1:",
    sum(i for i, (l, r) in enumerate(packet_pairs, 1) if compare(l, r) == "RIGHT"),
)

divider_packets = [[[2]], [[6]]]
all_packets = [] + divider_packets
for pair in packet_pairs:
    for p in pair:
        all_packets.append(p)


def bubble_sort(items):
    n = len(items)
    for i in range(n):
        fully_sorted = True
        for j in range(n - i - 1):
            if compare(items[j], items[j + 1]) == "WRONG":
                items[j], items[j + 1] = items[j + 1], items[j]
                fully_sorted = False
        if fully_sorted:
            break
    return items


sorted_packets = bubble_sort(all_packets)
divider_packet_indices = [
    i for i, packet in enumerate(sorted_packets, 1) if packet in divider_packets
]
decoder_key = divider_packet_indices[0] * divider_packet_indices[1]
print("Part 2:", decoder_key)
