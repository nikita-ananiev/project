import pygame
import copy
import random
import math

pygame.init()


# size = int(input()), int(input())


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.corner = 0
        self.coords = [499, 499]
        self.array = []

    def create_array(self):
        for i in range(self.height):
            string = []
            if 0 < i < self.height - 1:
                for j in range(self.width):
                    if 0 < j < self.width - 1:
                        string.append(0)
                    else:
                        string.append(1)
            else:
                for j in range(self.width):
                    string.append(1)
            self.array.append(string)


map = Field(1000, 1000)
map.create_array()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
moves = []
running = True
v = 10
keys = {'W': False, 'A': False, 'S': False, 'D': False}
pressed = False


def delete(sp, char):
    for i in sp:
        if char in i:
            del sp[sp.index(i)]


def is_true(sp):
    for elem in sp:
        if elem:
            return True
    return False


cos, sin = 0, 0
last_x = 0
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pressed = True
            if event.key == pygame.K_w:
                keys['W'] = True
            if event.key == pygame.K_a:
                keys['A'] = True
            if event.key == pygame.K_d:
                keys['D'] = True
            if event.key == pygame.K_s:
                keys['S'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys['W'] = False
                delete(moves, 'W')
            if event.key == pygame.K_a:
                keys['A'] = False
                delete(moves, 'A')
            if event.key == pygame.K_d:
                keys['D'] = False
                delete(moves, 'D')
            if event.key == pygame.K_s:
                keys['S'] = False
                delete(moves, 'S')
        if event.type == pygame.MOUSEMOTION:
            x1, y1 = event.pos
            dif = x1 - last_x
            last_x = x1
            map.corner += dif / 2
    cos_w = math.cos(map.corner / 180 * math.pi)
    sin_w = math.sin(map.corner / 180 * math.pi)
    cos_a = math.cos((map.corner - 90) / 180 * math.pi)
    sin_a = math.sin((map.corner - 90) / 180 * math.pi)
    cos_s = math.cos((map.corner + 180) / 180 * math.pi)
    sin_s = math.sin((map.corner + 180) / 180 * math.pi)
    cos_d = math.cos((map.corner + 90) / 180 * math.pi)
    sin_d = math.sin((map.corner + 90) / 180 * math.pi)
    for i in keys.keys():
        if i == 'W' and keys[i]:
            move = cos_w, sin_w, 'W'
            moves.append(move)
        elif i == 'A' and keys[i]:
            move = cos_a, sin_a, 'A'
            moves.append(move)
        elif i == 'D' and keys[i]:
            move = cos_d, sin_d, 'D'
            moves.append(move)
        elif i == 'S' and keys[i]:
            move = cos_s, sin_s, 'S'
            moves.append(move)
    if is_true(keys.values()):
        for i in moves:
            if map.array[int(map.coords[0])][int(map.coords[1])] != 1:
                map.coords[0] += i[0] / 10
                map.coords[1] += i[1] / 10
    else:
        moves = []
    x2, y2 = map.coords
    x3 = x2 + cos_w * 100
    y3 = y2 + sin_w * 100
    pygame.draw.line(screen, (255, 255, 255), (x2, y2), (round(x3), round(y3)), 5)
    pygame.draw.circle(screen, (255, 0, 0), (int(map.coords[0]), int(map.coords[1])), 10)
    pygame.display.flip()
    clock.tick(100)
