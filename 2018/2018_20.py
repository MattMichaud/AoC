import numpy as np
import re
from collections import deque
import operator

door_offsets = {'N':(0,-1), 'S':(0,1), 'E': (1,0), 'W':(-1,0)}
room_offsets = {'N':(0,-2), 'S':(0,2), 'E': (2,0), 'W':(-2,0)}

class NotFound(Exception): pass

def tuple_add(a, b):
    return(tuple(map(sum, zip(a, b))))

class RoomMap():
    def __init__(self, expression):
        self.start_loc = (0,0)
        self.rooms = set([self.start_loc])
        self.doors = set()
        self.process_regex(expression)
        self.room_graph = self.build_room_graph()
        self.room_distances = {}
        self.update_room_distances()

    def add_room(self, current_loc, direction):
        new_room_loc = tuple_add(current_loc, room_offsets[direction])
        self.rooms.add(new_room_loc)
        self.doors.add(tuple_add(current_loc, door_offsets[direction]))
        return(new_room_loc)

    def add_room_string(self, start_loc, directions):
        current_loc = start_loc
        for d in directions:
            current_loc = self.add_room(current_loc, d)
        return(current_loc)

    def display(self):
        print('Current Map:')
        room_xs = [t[0] for t in self.rooms]
        room_ys = [t[1] for t in self.rooms]
        min_x = min(room_xs) - 1
        max_x = max(room_xs) + 1
        min_y = min(room_ys) - 1
        max_y = max(room_ys) + 1
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        grid = np.empty(shape=(width, height), dtype=str)
        grid[:] = ' '
        offset = (-1 * min_x, -1 * min_y)
        neighbor_offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for r in self.rooms:
            r_offset = tuple_add(r, offset)
            grid[r_offset] = '.'
            for neighbor in neighbor_offsets:
                grid[tuple_add(r_offset, neighbor)] = '#'
        for d in self.doors:
            if d[0] % 2 == 0:
                grid[tuple_add(d, offset)] = '-'
            else:
                grid[tuple_add(d, offset)] = '|'
        grid[tuple_add(self.start_loc, offset)] = 'X'

        for y in range(height):
            for x in range(width):
                print(grid[(x,y)], end='')
            print()
        print()

    def process_regex(self, expression, start_locs=[(0,0)]):
        char_index = 0
        done = False
        current_locs = start_locs.copy()
        branch_starts = []
        branch_ends = []
        next_character = ''
        while next_character != '$':
            next_character = expression[char_index]
            if next_character == '(':
                branch_starts.append(current_locs.copy())
                branch_ends.append([])
            elif next_character == '|':
                for item in current_locs:
                    branch_ends[-1].append(item)
                current_locs = branch_starts[-1].copy()
            elif next_character == ')':
                for item in current_locs:
                    branch_ends[-1].append(item)
                branch_starts.pop()
                current_locs = branch_ends.pop()
                current_locs = list(set(current_locs))
            elif next_character in ('NSEW'):
                for index, loc in enumerate(current_locs):
                    current_locs[index] = self.add_room(loc, next_character)
            char_index += 1

    def build_room_graph(self):
        room_graph = {}
        for r in self.rooms:
            room_graph[r] = []
            for c in 'NSEW':
                possible_door_loc = tuple_add(r, door_offsets[c])
                if possible_door_loc in self.doors:
                    room_loc = tuple_add(r, room_offsets[c])
                    room_graph[r].append(room_loc)
        return(room_graph)

    def bfs_search(self, start, goal):
        visited = {start: None}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == goal:
                path = []
                while node is not None:
                    path.append(node)
                    node = visited[node]
                return path[::-1]
            for neighbour in self.room_graph[node]:
                if neighbour not in visited:
                    visited[neighbour] = node
                    queue.append(neighbour)
        raise NotFound('No path from {} to {}'.format(start, goal))

    def update_room_distances(self):
        room_index = 1
        for r in self.rooms:
            room_index += 1
            shortest_path = self.bfs_search(self.start_loc, r)
            distance = len(shortest_path) - 1
            self.room_distances[r] = distance

    def furthest_room(self):
        furthest_room = max(self.room_distances.items(), key=operator.itemgetter(1))[0]
        return(self.room_distances[furthest_room])

    def distant_rooms(self, distance):
        room_count = 0
        for r in self.rooms:
            if self.room_distances[r] >= distance:
                room_count += 1
        return(room_count)

with open('2018_20_input.txt','r') as f:
    room_regex = f.read()

my_map = RoomMap(room_regex)
print('Part 1 Answer:', my_map.furthest_room())
print('Part 2 Answer:', my_map.distant_rooms(1000))