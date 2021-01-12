import sys
sys.path.append('.')
from linked_list import CircularDoublyLinkedList
from linked_list import Node


class Recipes():
    def __init__(self):
        self.recipe_list = CircularDoublyLinkedList()
        self.elf1_current = Node(3)
        self.elf2_current = Node(7)
        self.recipe_list.insert_at_end(self.elf1_current)
        self.recipe_list.insert_at_end(self.elf2_current)
        self.recipe_count = 2

    def add_new_recipes(self):
        recipe_sum = [int(c) for c in str(self.elf1_current.data + self.elf2_current.data)]
        for r in recipe_sum:
            self.recipe_list.insert_at_end(Node(r))
            self.recipe_count += 1

    def update_currents(self):
        self.elf1_current = self.elf1_current.traverse_forward(1 + self.elf1_current.data)
        self.elf2_current = self.elf2_current.traverse_forward(1 + self.elf2_current.data)

    def display(self):
        print(self.elf1_current, self.elf2_current, end=' -- ')
        self.recipe_list.display()

    def iteration(self, verbose=False):
        self.add_new_recipes()
        self.update_currents()
        if verbose: self.display()

    def get_tail(self, length=1):
        if self.recipe_count < length:
            return('')
        else:
            answer = ''
            current = self.recipe_list.first.prev
            for i in range(length):
                answer = str(current.data) + answer
                current = current.prev
            return(answer)

def part1(puzzle_input):
    recipes = Recipes()
    while recipes.recipe_count < puzzle_input + 10:
        recipes.iteration()
    extras = recipes.recipe_count - (puzzle_input + 10)
    end_of_list = recipes.recipe_list.first.prev
    for i in range(extras): end_of_list = end_of_list.prev
    answer = ''
    for i in range(10):
        answer = str(end_of_list.data) + answer
        end_of_list = end_of_list.prev
    print('Part 1 Answer:', answer)

def part2(puzzle_input):
    puzzle_input = str(puzzle_input)
    input_length = len(puzzle_input)
    recipes = Recipes()
    tail = ''
    while puzzle_input not in tail:
        recipes.iteration()
        tail = recipes.get_tail(input_length+1)
    recent1 = tail[:input_length]
    recent2 = tail[1:]
    result = recipes.recipe_count - input_length
    if recent1 == puzzle_input:
        result -= 1
    print('Part 2 Answer:', result)

part1(635041)
part2(635041)