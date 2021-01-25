import sys
sys.path.append('.')
from utils import IntCodeComputer
import pygame

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def part1(filename):
    data = [int(c) for c in open(filename).read().split(",")]
    comp = IntCodeComputer(data)
    comp.compute()
    output_groups = list(zip(*(iter(comp.output_array),) * 3))
    screen = {}
    for g in output_groups: screen[(g[0], g[1])] = g[2]
    print('Part 1 Answer {}'.format(list(screen.values()).count(BLOCK)))

def part2(filename):
    pygame.init()
    box_x = box_y = 20
    screen_x = 38 * box_x
    screen_y = 21 * box_y
    screen = pygame.display.set_mode([screen_x, screen_y])

    data = [int(c) for c in open(filename).read().split(",")]
    comp = IntCodeComputer(data, 0)
    comp.set_single_memory_address(0, 2)
    comp.compute()
    output_array = comp.get_output()
    ball_pos_x = paddle_pos_x = 0
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        paddle_input = 0
        if ball_pos_x > paddle_pos_x: paddle_input = 1
        elif ball_pos_x < paddle_pos_x: paddle_input = -1
        comp.add_input(paddle_input)
        comp.compute()
        for i in range(0, len(output_array), 3):
            if output_array[i] == -1 and output_array[i + 1] == 0: score = output_array[i + 2]
            else:
                color = (255, 255, 255)
                if output_array[i+2] == EMPTY:
                    color = (161, 228, 255)
                elif output_array[i+2] == WALL:
                    color = (204, 131, 108)
                elif output_array[i+2] == BLOCK:
                    color = (108, 126, 204)
                elif output_array[i+2] == PADDLE:
                    color = (35, 57, 153)
                    paddle_pos_x = output_array[i]
                elif output_array[i+2] == BALL:
                    color = (250, 187, 149)
                    ball_pos_x = output_array[i]
                pygame.draw.rect(screen, color, [output_array[i] * box_x, output_array[i+1] * box_y, box_x, box_y])
        pygame.display.flip()
        if comp.finished:
            running = False
            print('Part 2 Answer: {}'.format(score))

filename = '2019/inputs/13.txt'
part1(filename)
part2(filename)