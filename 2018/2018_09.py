import sys
sys.path.append('.')
from linked_list import CircularDoublyLinkedList
from linked_list import Node

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