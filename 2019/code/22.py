class Deck:
    def __init__(self, deck_size):
        self.size = deck_size
        self.cards = [i for i in range(0, deck_size)]

    def deal_into_new_stack(self):
        self.cards.reverse()

    def cut(self, n):
        if n > 0:
            cut_point = n
        else:
            cut_point = self.size - abs(n)
        top = self.cards[:cut_point]
        bottom = self.cards[cut_point:]
        self.cards = bottom + top

    def deal_with_increment(self, n):
        new_deck = [0] * self.size
        step = 0
        for i in range(self.size):
            new_deck[step % self.size] = self.cards[i]
            step += n
        self.cards = new_deck

    def shuffle(self, instructions):
        for instruction, n in instructions:
            if 'cut' in instruction:
                self.cut(int(n))
            elif 'increm' in instruction:
                self.deal_with_increment(int(n))
            elif 'stack' in instruction:
                self.deal_into_new_stack()

def parse_input(filename):
    with open(filename, 'r') as f:
        raw_instructions = [line.rstrip() for line in f]
    instruction_list = []
    options = ('cut', 'deal with increment', 'deal into new stack')
    for line in raw_instructions:
        for o in options:
            if line.startswith(o):
                instruction_list.append((o, line.replace(o, '').strip()))
    return instruction_list

filename = 'test.txt'
filename = '2019/inputs/22.txt'
instructions = parse_input(filename)
my_deck = Deck(10007)
my_deck.shuffle(instructions)
print('Part 1 Answer:',my_deck.cards.index(2019))


n = 119315717514047
c = 2020

a, b = 1, 0

with open(filename, 'r') as f:
    raw_instructions = [line for line in f]

for l in raw_instructions:
    if l == 'deal into new stack\n':
        la, lb = -1, -1
    elif l.startswith('deal with increment '):
        la, lb = int(l[len('deal with increment '):]), 0
    elif l.startswith('cut '):
        la, lb = 1, -int(l[len('cut '):])
    a = (la * a) % n
    b = (la * b + lb) % n

M = 101741582076661
def inv(a, n): return pow(a, n-2, n)
Ma = pow(a, M, n)
Mb = (b * (Ma - 1) * inv(a-1, n)) % n
print('Part 2 Answer:',((c - Mb) * inv(Ma, n)) % n)