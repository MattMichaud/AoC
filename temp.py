class MarbleGame():
    def __init__(self, num_players):
        self.num_players = num_players
        self.marble_circle = [0]
        self.current_player = 1
        self.current_marble_loc = 0
        self.scores = [0] * (num_players + 1)
        self.lowest_available = 1
    
    def take_turn(self, verbose=False):
        new_marble = self.lowest_available
        if new_marble % 23 == 0:
            remove_loc = self.current_marble_loc - 7
            if remove_loc < 0: remove_loc = len(self.marble_circle) + remove_loc
            removed_marble = self.marble_circle.pop(remove_loc)
            self.scores[self.current_player] += new_marble + removed_marble
            self.current_marble_loc = remove_loc
        else:
            insert_loc = (self.current_marble_loc + 2) % len(self.marble_circle)
            if insert_loc == 0:
                self.marble_circle.append(new_marble)
                self.current_marble_loc = len(self.marble_circle) - 1
            else:
                self.marble_circle.insert(insert_loc, new_marble)
                self.current_marble_loc = insert_loc

        if verbose: 
            print('Player',self.current_player,'added marble',new_marble)
            print('Ending Circle:',self.marble_circle)
            print('Scores:', self.scores)
            print()

        self.current_player = (self.current_player % self.num_players) + 1
        self.lowest_available += 1
        return
    
    def display(self):
        print('Current Player:', self.current_player)
        print('Marble Circle:', self.marble_circle)
        
    def winning_score(self):
        return(max(self.scores))

players = 452
last_marble = 70784 * 100

game = MarbleGame(players)
for turn in range(last_marble):
    game.take_turn(False)
    if turn % 10000 == 0: print('Turn',turn,'completed!')
game.winning_score()
