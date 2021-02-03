import sys
sys.path.append('.')
from intcode_2 import Intcode


class NetIntcode:

    def __init__(self, program: list, address: int, target_address: int, network: list):
        self.packet_queue = []
        self.vm = Intcode(program)
        self.vm.input_val = address
        self.target_address = target_address
        self.network = network
        self.vm.run_until_input_or_done()
        self.vm.input_val = -1
        self.idle = False

    def run_until_io(self) -> int or None:
        if not self.packet_queue:
            self.vm.input_val = -1
        else:
            self.vm.input_val = self.packet_queue[0][0]  # provide X from next packet
        output = self.vm.run_until_io_or_done()
        if self.vm.stopped_on_input:
            if self.packet_queue:
                x, y = self.packet_queue.pop(0)
                self.vm.input_val = y
                self.vm.run_until_input_or_done()
            else:
                self.idle = True
        else:
            self.idle = False
            dest_address = output
            x = self.vm.run_until_io_or_done()
            y = self.vm.run_until_io_or_done()
            if dest_address == self.target_address:
                return dest_address, x, y
            self.network[dest_address].packet_queue.append((x, y))