def isUniqueChars(st):
    if len(set(st)) == len(st):
        return True
    else:
        return False


def findStartOfPacketMarker(buffer, packet_length):
    for i in range(packet_length, len(buffer)):
        test_packet = buffer[i - packet_length : i]
        if isUniqueChars(test_packet):
            return i
    return -1


filename = "2022/inputs/06.txt"
puzzle_input = open(filename, "r").readline()
print("Part 1 Answer:", findStartOfPacketMarker(puzzle_input, 4))
print("Part 2 Answer:", findStartOfPacketMarker(puzzle_input, 14))
