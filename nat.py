class NAT:
    def __init__(self, network):
        self.network = network
        self.packet = None
        self.last_y_delivered = None

    def is_network_idle(self):
        for computer in self.network:
            if not computer.idle:
                return False
        return True

    def has_packet(self):
        return self.packet is not None

    def is_repeated_y(self):
        return self.packet[1] == self.last_y_delivered

    def send_packet(self):
        self.last_y_delivered = self.packet[1]
        self.network[0].packet_queue.append(self.packet)
        self.packet = None