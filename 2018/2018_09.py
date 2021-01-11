class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def traverse_forward(self, index):
        result = self
        for _ in range(index):
            result = result.next
        return(result)

    def traverse_back(self, index):
        result = self
        for _ in range(index):
            result = result.prev
        return(result)

    def display_all(self):
        current = self
        while True:
            print(current.data, end = ' ')
            current = current.next
            if current == self:
                print()
                break

    def __str__(self):
        return(str(self.data))

class CircularDoublyLinkedList():
    def __init__(self):
        self.first = None

    def get_node(self, index):
        current = self.first
        for i in range(index):
            current = current.next
            if current == self.first:
                return None
        return(current)

    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node, new_node):
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node):
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)

    def insert_at_beg(self, new_node):
        self.insert_at_end(new_node)
        self.first = new_node

    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next

    def display(self):
        if self.first == None:
            return
        else:
            current = self.first
            while True:
                print(current.data, end = ' ')
                current = current.next
                if current == self.first:
                    print()
                    break


class Game():
    def __init__(self, num_players):
        self.num_players = num_players
        self.marbles = CircularDoublyLinkedList()
        self.current_player = 1
        self.current_marble = Node(0)
        self.marbles.insert_at_beg(self.current_marble)
        self.scores = [0] * (num_players + 1)
        self.lowest_available = 1

    def display(self):
        print('Current Player:', self.current_player, 'Current Marble:', self.current_marble)
        print('Marble Circle:', end=' ')
        self.marbles.display()

    def take_turn(self, verbose=False):
        new_marble = Node(self.lowest_available)
        if new_marble.data % 23 == 0:
            remove_marble = self.current_marble.traverse_back(7)
            self.current_marble = remove_marble.next
            self.marbles.remove(remove_marble)
            self.scores[self.current_player] += new_marble.data + remove_marble.data
        else:
            self.marbles.insert_after(self.current_marble.next, new_marble)
            self.current_marble = new_marble
        if verbose: self.display()
        self.current_player = (self.current_player % self.num_players) + 1
        self.lowest_available += 1

    def winning_score(self):
        return(max(self.scores))

def play_game(players, last_marble, verbose=False):
    game = Game(players)
    for turn in range(last_marble):
        game.take_turn(verbose)
    return(game.winning_score())

print('Part 1 Answer:',play_game(452, 70784))
print('Part 2 Answer:',play_game(452, 7078400))