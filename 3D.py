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
            if 5 < i < self.height - 5:
                for j in range(self.width):
                    if 445 <= j <= 450:
                        string.append(1)
                    elif 5 < j < self.width - 5:
                        string.append(0)
                    else:
                        string.append(1)
            else:
                for j in range(self.width):
                    string.append(1)
            self.array.append(string)

    def draw_walls(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.array[i][j] == 1:
                    screen2.set_at((j, i), (155, 155, 155))


map = Field(1000, 1000)
map.create_array()
screen = pygame.display.set_mode((1000, 1000))
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
moves = []
running = True
v = 10
keys = {'W': False, 'A': False, 'S': False, 'D': False}
pressed = False


def algoritm(x0, y0, x1, y1):
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    delta_erry = delta_y
    delta_errx = delta_x
    y = y0
    x = x0
    dir_y = y1 - y0
    dir_y = 1 if dir_y > 0 else -1
    dir_x = x1 - x0
    dir_x = 1 if dir_x > 0 else -1
    if delta_x > delta_y:
        for x in range(x0, x1, dir_x):
            if map.array[y][x] == 1:
                return
            screen.set_at((x, y), (255, 255, 255))
            error += delta_erry
            if 2 * error >= delta_erry:
                y += dir_y
                error -= delta_x
    elif delta_x < delta_y:
        for y in range(y0, y1, dir_y):
            if map.array[y][x] == 1:
                return
            screen.set_at((x, y), (255, 255, 255))
            error += delta_errx
            if 2 * error >= delta_errx:
                x += dir_x
                error -= delta_y


def is_x(kor):
    return True if kor[0] != 0 else False


def poz(num):
    return -1 if num > 0 else 1


def delete(sp, char):
    for i in sp:
        if char in i:
            del sp[sp.index(i)]


def check(sp, char):
    for i in sp:
        if char in i:
            return True
    return False


def is_true(sp):
    for elem in sp:
        if elem:
            return True
    return False


def is_corner(sp, x, y, r):
    if sp[x - r][y] == 1 and sp[x][y - r] == 1\
            or sp[x + r][y] == 1 and sp[x][y - r] == 1\
            or sp[x - r][y] == 1 and sp[x][y + r] == 1\
            or sp[x + r][y] == 1 and sp[x][y + r] == 1:
        return True
    return False


stop = False
move_y = False
move_x = False
offset = [(10, 0), (0, -10), (-10, 0), (0, 10)]
cos, sin = 0, 0
last_x = 0
map.draw_walls()
while running:
    screen.fill((0, 0, 0))
    screen.blit(screen2, (0, 0))
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
            if event.key == pygame.K_s and len(moves) == 0:
                keys['S'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys['W'] = False
            if event.key == pygame.K_a:
                keys['A'] = False
            if event.key == pygame.K_d:
                keys['D'] = False
            if event.key == pygame.K_s:
                keys['S'] = False
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
            if check(moves, 'W'):
                delete(moves, 'W')
            move = cos_w, sin_w, 'W'
            moves.append(move)
        elif i == 'A' and keys[i]:
            if check(moves, 'A'):
                delete(moves, 'A')
            move = cos_a, sin_a, 'A'
            moves.append(move)
        elif i == 'D' and keys[i]:
            if check(moves, 'D'):
                delete(moves, 'D')
            move = cos_d, sin_d, 'D'
            moves.append(move)
        elif i == 'S' and keys[i]:
            if check(moves, 'S'):
                delete(moves, 'S')
            move = cos_s, sin_s, 'S'
            moves.append(move)
    if is_true(keys.values()):
        for i in moves:
            if map.array[int(map.coords[1] + i[1] + 10)][int(map.coords[0] + i[0] + 10)] != 1 and \
                    map.array[int(map.coords[1] + i[1] - 10)][int(map.coords[0] + i[0] + 10)] != 1 and \
                    map.array[int(map.coords[1] + i[1] - 10)][int(map.coords[0] + i[0] - 10)] != 1 and \
                    map.array[int(map.coords[1] + i[1] + 10)][int(map.coords[0] + i[0] - 10)] != 1:
                map.coords[0] += i[0]
                map.coords[1] += i[1]
            else:
                for j in offset:
                    if map.array[int(map.coords[1] + i[1] + j[1])][int(map.coords[0] + i[0] + j[0])] == 1:
                        if not(is_corner(map.array, int(map.coords[1]), int(map.coords[0]), 11)):
                            if is_x(j):
                                map.coords[1] -= poz(i[1])
                                break
                            else:
                                map.coords[0] -= poz(i[0])
                                break
                        else:
                            pass

    moves = []
    x2, y2 = map.coords
    x3 = x2 + cos_w * 1000
    y3 = y2 + sin_w * 1000
    algoritm(round(x2), round(y2), round(x3), round(y3))
    # pygame.draw.line(screen, (255, 255, 255), (x2, y2), (round(x3), round(y3)), 5)
    pygame.draw.circle(screen, (255, 0, 0), (int(map.coords[0]), int(map.coords[1])), 10)
    pygame.display.flip()
    clock.tick(100)
