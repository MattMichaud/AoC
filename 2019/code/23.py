import sys
sys.path.append('.')
from net_intcode import NetIntcode
from utils import read_intcode
from nat import NAT


def init_network(program: list, num_computers: int, nat_address: int) -> list:
    network = []
    for address in range(num_computers):
        network.append(NetIntcode(program, address, nat_address, network))
    return network


def part_one(filename: str, num_computers: int, target_address: int) -> int:
    network = init_network(read_intcode(filename), num_computers, target_address)
    while True:
        for computer in network:
            packet = computer.run_until_io()
            if packet is not None and packet[0] == target_address:
                return packet[2]  # Y value


def part_two(filename: str, num_computers: int, nat_address: int) -> int or None:
    network = init_network(read_intcode(filename), num_computers, nat_address)
    nat = NAT(network)
    while True:
        for computer in network:
            packet = computer.run_until_io()
            if packet is not None and packet[0] == nat_address:
                nat.packet = (packet[1], packet[2])
        if nat.is_network_idle() and nat.has_packet():
            if nat.is_repeated_y():
                return nat.last_y_delivered
            else:
                nat.last_y_delivered = None
            nat.send_packet()


filename = '2019/inputs/23.txt'
print(f'Part 1 Answer {part_one(filename, 50, 255)}')
print(f'Part 2 Answer {part_two(filename, 50, 255)}')