import numpy as np

class Cart():
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction
        if self.direction in '><': self.track_under = '-'
        else: self.track_under = '|'
        self.turns_made = 0
        self.active = True

    def next_turn(self):
        turns = ['left','straight','right']
        next_turn = turns[self.turns_made % 3]
        return(next_turn)

    def get_move_offset(self):
        offsets = {'>':(1,0), '<':(-1,0), '^':(0,-1), 'v':(0,1)}
        return(offsets[self.direction])

    def update_direction(self, new_track):
        if new_track == '+':
            rotation = self.next_turn()
            self.turns_made += 1
            if (rotation == 'right' and self.direction == '>') or (rotation == 'left' and self.direction == '<'): self.direction = 'v'
            elif (rotation == 'right' and self.direction == '<') or (rotation == 'left' and self.direction == '>'): self.direction = '^'
            elif (rotation == 'right' and self.direction == '^') or (rotation == 'left' and self.direction == 'v'): self.direction = '>'
            elif (rotation == 'right' and self.direction == 'v') or (rotation == 'left' and self.direction == '^'): self.direction = '<'
        else:
            if (self.direction == '>' and new_track == '\\') or (self.direction == '<' and new_track == '/'): self.direction = 'v'
            elif (self.direction == '>' and new_track == '/') or (self.direction == '<' and new_track == '\\'): self.direction = '^'
            elif (self.direction == '^' and new_track == '/') or (self.direction == 'v' and new_track == '\\'): self.direction = '>'
            elif (self.direction == '^' and new_track == '\\') or (self.direction == 'v' and new_track == '/'): self.direction = '<'

class Track():
    def __init__(self, filename):
        self.cart_list = []
        with open(filename, 'r') as f:
            data = f.read().splitlines()
        self.width = len(data[0])
        self.height = len(data)
        self.tracks = np.empty(shape=(self.width,self.height), dtype=str)
        for x,y in [(x,y) for x in range(self.width) for y in range(self.height)]:
            self.tracks[(x,y)] = data[y][x]
            if data[y][x] in '><^v':
                new_cart = Cart((x,y), data[y][x])
                self.cart_list.append(new_cart)
        self.current_tick = 0
        self.sort_carts()

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.tracks[(x,y)], end='')
            print()
        print()
        print(len(self.cart_list))
        print()

    def sort_carts(self):
        self.cart_list = sorted(self.cart_list, key=lambda element: (element.location[1], element.location[0]))

    def complete_tick(self, stop_on_collision=True):
        self.sort_carts()
        crash_detected = False
        for cart in self.cart_list:
            if cart.active:
                offset = cart.get_move_offset()
                loc = cart.location
                new_loc = tuple(map(sum, zip(offset, loc)))
                dest_track = self.tracks[new_loc]
                if dest_track in '-|\\/+':
                    self.tracks[loc] = cart.track_under
                    cart.track_under = self.tracks[new_loc]
                    cart.update_direction(self.tracks[new_loc])
                    self.tracks[new_loc] = cart.direction
                    cart.location = new_loc
                elif dest_track in '><v^':
                    crash_detected = True
                    self.deactivate_cart(loc)
                    self.deactivate_cart(new_loc)
                    if stop_on_collision: break
        if crash_detected:
            return(new_loc)
        else:
            return

    def active_carts(self):
        active_carts = []
        for cart in self.cart_list:
            if cart.active: active_carts.append(cart)
        return(active_carts)

    def deactivate_cart(self, loc):
        for cart in self.cart_list:
            if cart.location == loc:
                cart.active = False
                self.tracks[loc] = cart.track_under

def part1(filename):
    my_track = Track(filename)
    collision_location = None
    while not collision_location:
        collision_location = my_track.complete_tick()
    print('Part 1 Answer:', str(collision_location[0])+','+str(collision_location[1]))

def part2(filename):
    my_track = Track(filename)
    while len(my_track.active_carts()) > 1:
        my_track.complete_tick(False)
    last_cart_location = my_track.active_carts()[0].location
    print('Part 2 Answer:', str(last_cart_location[0])+','+str(last_cart_location[1]))

input_file = '2018/inputs/2018_13_input.txt'
part1(input_file)
part2(input_file)