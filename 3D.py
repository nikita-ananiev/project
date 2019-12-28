import pygame
import copy
import random
import math

pygame.init()

# size = int(input()), int(input())

wall_width = 10


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.corner = 0
        self.coords = [250, 250]
        self.array = []

    def create_array(self):
        for i in range(self.height):
            string = []
            if 10 < i < self.height - 10:
                for j in range(self.width):
                    if 10 < j < self.width - 10:
                        string.append(0)
                    else:
                        string.append(((i//10)*j%255)+1)
            else:
                if i <= 10:
                    for j in range(self.width):
                        string.append(((j//100)*i%255)+1)
                        # string.append(3)
                elif i >= self.height - 10:
                    for j in range(self.width):
                        string.append(((j//20)*i%255)+1)
                        # string.append(2)
            self.array.append(string)

    def draw_walls(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.array[i][j] == 1:
                    screen2.set_at((j, i), (155, 155, 155))

    def add_wall(self, x1, y1, x2, y2):
        d_x = 10 if x2 - x1 >= 0 else -10
        d_y = 10 if y2 - y1 >= 0 else -10
        for y in range(y1 * 10, y2 * 10 + d_y):
            for x in range(x1 * 10, x2 * 10 + d_x):
                self.array[y][x] = 1



map = Field(500, 500)
map.create_array()
screen = pygame.display.set_mode((500, 500))
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
moves = []
running = True
v = 10
keys = {'W': False, 'A': False, 'S': False, 'D': False}
pressed = False


def algoritm(x1, y1, x2, y2, dont_draw):
    start_x = x1
    start_y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dir_x = 1 if x2 - x1 > 0 else -1
    dir_y = 1 if y2 - y1 > 0 else -1
    step = 1
    x = x1 + 1
    y = y1 + 1
    last_x = x
    last_y = y
    dif = 0
    k = (dy + 1) / (dx + 1)
    if dx >= dy:
        while True:
            dif += 1
            x = x1 + step * dif * dir_x
            y = y1 + step * dif * k * dir_y
            if map.array[round(y)][round(x)] != 0:
                c1, c2 = round(y), round(x)
                x = last_x
                y = last_y
                if step == 1:
                    if not(dont_draw):
                        pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (x, y), 1)
                    return math.sqrt((x - start_x)**2 + (y - start_y)**2), map.array[c1][c2]
                step = 1
                x1 = x
                y1 = y
                dif = 0
            last_x = x
            last_y = y
    else:
        k = 1/k
        while True:
            dif += 1
            y = y1 + step * dif * dir_y
            x = x1 + step * dif * k * dir_x
            if map.array[round(y)][round(x)] != 0:
                c1, c2 = round(y), round(x)
                x = last_x
                y = last_y
                if step == 1:
                    if not (dont_draw):
                        pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (x, y), 1)
                    return math.sqrt((x - start_x) ** 2 + (y - start_y) ** 2), map.array[c1][c2]
                step = 1
                x1 = x
                y1 = y
                dif = 0
            last_x = x
            last_y = y

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
    if sp[x - r][y] != 0 and sp[x][y - r] != 0 \
            or sp[x + r][y] != 0 and sp[x][y - r] != 0 \
            or sp[x - r][y] != 0 and sp[x][y + r] != 0 \
            or sp[x + r][y] != 0 and sp[x][y + r] != 0:
        return True
    return False


stop = False
move_y = False
move_x = False
offset = [(10, 0), (0, -10), (-10, 0), (0, 10)]
cos, sin = 0, 0
last_x = 0
is_map = False
map.add_wall(10, 10, 40, 10)
map.draw_walls()

k = 90 / 1000
while running:
    screen.fill((0, 0, 0))
    if is_map:
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
            if event.key == pygame.K_m:
                is_map = True if not is_map else False
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
            if map.array[int(map.coords[1] + i[1] + 10)][int(map.coords[0] + i[0] + 10)] == 0 and \
                    map.array[int(map.coords[1] + i[1] - 10)][int(map.coords[0] + i[0] + 10)] == 0 and \
                    map.array[int(map.coords[1] + i[1] - 10)][int(map.coords[0] + i[0] - 10)] == 0 and \
                    map.array[int(map.coords[1] + i[1] + 10)][int(map.coords[0] + i[0] - 10)] == 0:
                map.coords[0] += i[0]
                map.coords[1] += i[1]
            else:
                for j in offset:
                    if map.array[int(map.coords[1] + i[1] + j[1])][int(map.coords[0] + i[0] + j[0])] != 0:
                        if not (is_corner(map.array, int(map.coords[1]), int(map.coords[0]), 11)):
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
    if is_map:
        x3 = x2 + cos_w * 1500
        y3 = y2 + sin_w * 1500
        tg = math.tan(map.corner / 180 * math.pi)
        s = algoritm(round(x2), round(y2), round(x3), round(y3), False)
        # print(s)
        # pygame.draw.line(screen, (255, 255, 255), (x2, y2), (round(x3), round(y3)), 5)
        pygame.draw.circle(screen, (255, 0, 0), (int(map.coords[0]), int(map.coords[1])), 10)
    else:
        angle = map.corner - 45
        for pix in range(500):
            cos = math.cos(angle / 180 * math.pi)
            sin = math.sin(angle / 180 * math.pi)
            tg = math.tan(angle / 180 * math.pi)
            x3 = x2 + cos * 1500
            y3 = y2 + sin * 1500
            distance, color = algoritm(round(x2), round(y2), round(x3), round(y3), True)
            # print(color)
            wall_height = round(30000 / distance)
            wall_top = (500 - wall_height) / 2
            wall_bottom = wall_top + wall_height
            pygame.draw.line(screen, (90, 90, 160), (pix, 0), (pix, wall_top), 1)  # ceiling
            pygame.draw.line(screen, (color, 90, 90), (pix, wall_top), (pix, wall_bottom), 1)  # wall
            pygame.draw.line(screen, (90, 160, 90), (pix, wall_bottom), (pix, 1000), 1)  # floor
            angle += k

    pygame.display.flip()
    clock.tick(100)
