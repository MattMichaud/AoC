import sys
sys.path.append('.')
from intcode import IntCodeComputer

from collections import namedtuple

PathState = namedtuple('PathState',
                       ('pos', 'dir', 'can_turn', 'seen', 'prefix'))

CompressState = namedtuple('CompressState', ('main', 'programs', 'index'))


class Scaffold(object):
    def __init__(self, filename):
        self.field, self.pos, self.dir = set(), None, None

        code = [int(c) for c in open(filename, 'r').read().split(',')]
        comp = IntCodeComputer(code, empty_space=10000)
        comp.compute()

        for y, line in enumerate(''.join(map(chr, comp.output_array)).split('\n')):
            for x, char in enumerate(line):
                if char == '#':
                    self.field.add((x, y))
                elif char == '<':
                    self.pos = x, y
                    self.dir = -1, 0
                elif char == '>':
                    self.pos = x, y
                    self.dir = 1, 0
                elif char == '^':
                    self.pos = x, y
                    self.dir = 0, -1
                elif char == 'v':
                    self.pos = x, y
                    self.dir = 0, 1
        self.crossings = {
            (x, y)
            for x, y in self.field
            if sum(((x - 1, y) in self.field, (x, y - 1) in self.field,
                    (x, y + 1) in self.field, (x + 1, y) in self.field)) > 2
        }

    def paths(self):
        stack = [
            PathState(pos=self.pos,
                      dir=self.dir,
                      can_turn=True,
                      seen=set(),
                      prefix=[])
        ]
        while stack:
            state = stack.pop()
            x, y = state.pos
            dx, dy = state.dir
            can_turn = state.can_turn
            seen = state.seen
            prefix = state.prefix
            consecutive = 0
            while True:
                if can_turn:
                    next_prefix = prefix + [str(consecutive)
                                            ] if consecutive > 0 else prefix
                    stack.extend((PathState(pos=(x, y),
                                            dir=(dy, -dx),
                                            can_turn=False,
                                            seen=set(seen),
                                            prefix=next_prefix + ['L']),
                                  PathState(pos=(x, y),
                                            dir=(-dy, dx),
                                            can_turn=False,
                                            seen=set(seen),
                                            prefix=next_prefix + ['R'])))
                else:
                    can_turn = True
                consecutive += 1
                x += dx
                y += dy
                if (x, y) not in self.field:
                    break
                if (x, y) in seen and (x, y) not in self.crossings:
                    break
                seen.add((x, y))
                if len(seen) == len(self.field):
                    yield prefix + [str(consecutive)]


def part1(filename):
    return sum(
        x * y
        for x, y in Scaffold(filename).crossings)


def compress(path):
    stack = [CompressState(main=[], programs=[], index=0)]
    while stack:
        main, programs, index = stack.pop()
        if index >= len(path):
            yield [
                ','.join(main), *(','.join(program) for program in programs)
            ]
        if len(main) < 10:
            for id, program in zip('ABC', programs):
                if path[index:index + len(program)] == program:
                    stack.append(
                        CompressState(main=main + [id],
                                      programs=programs,
                                      index=index + len(program)))
        if len(programs) < 3:
            for end in range(index + 1, len(path)):
                if sum(map(len, path[index:end])) + end - index - 1 > 20:
                    break
                stack.append(
                    CompressState(main=main + ['ABC'[len(programs)]],
                                  programs=programs + [path[index:end]],
                                  index=end))


def part2(filename):
    scaffold = Scaffold(filename)
    input = '\n'.join(
        next(result for path in scaffold.paths() for result in compress(path)))
    code = [int(c) for c in open(filename, 'r').read().split(',')]
    code[0] = 2
    comp = IntCodeComputer(code, empty_space=2000)
    for item in [ord(c) for c in f'{input}\nn\n']:
        comp.add_input(item)
    comp.compute()
    return comp.output_array.pop()

filename = '2019/inputs/17.txt'
print(f'Part 1 Answer: {part1(filename)}')
print(f'Part 2 Answer: {part2(filename)}')