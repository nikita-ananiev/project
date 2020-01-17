import pygame
import copy
import random
import os
import math
from collections import namedtuple

WallInfo = namedtuple('WallInfo', 'color')
WallIntersection = namedtuple('WallIntersection', 'point distance wall')

walls = []

pygame.init()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.corner = 0
        self.coords = [500, 500]
        self.array = []

    def create_array(self):
        for i in range(self.height):
            string = []
            if 10 < i < self.height - 10:
                for j in range(self.width):
                    if 10 < j < self.width - 10:
                        string.append(0)
                    else:
                        string.append(((i // 10) * j % 255) + 1)
            else:
                if i <= 10:
                    for j in range(self.width):
                        string.append(((j // 100) * i % 255) + 1)
                        # string.append(3)
                elif i >= self.height - 10:
                    for j in range(self.width):
                        string.append(((j // 20) * i % 255) + 1)
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


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Wall:
    def __init__(self, id, segment, color):
        self.segment = segment
        self.id = id
        self.color = color


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Hero:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle


class Monster(pygame.sprite.Sprite):
    image = load_image("monster.png", -1)
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, group, x, y, r):
        super().__init__(group)
        self.image = Monster.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, s):
        self.image = pygame.transform.scale(Monster.image, (100 // s, 100 // s))
        self.rect = self.image.get_rect()


Monster(all_sprites, 500, 550, 5)
return_steps = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def find_monster(x1, y1, x2, y2, hero_angle):
    hero_angle %= 360
    dy = y1 - y2
    hyp = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    katet = x1 - x2
    cos = katet / hyp
    angle = math.acos(cos)
    angle = (angle / math.pi * 180)
    if dy < 0:
        angle = -angle
    angle %= 360
    need_angle = angle - hero_angle
    # need_angle %= 360
    pix = 500 + need_angle * 1 / 0.09
    if -500 <= pix <= 1500:
        return pix, hyp * math.cos(need_angle * math.pi / 180)
    else:
        return None


def draw_sky(hero_angle):
    angle = hero_angle
    image = load_image("sky.jpg")
    image = pygame.transform.scale(image, (1000, 500))
    if angle > 0:
        pixels_cut = angle * 3
        image_cut_left = image.subsurface(pygame.Rect((pixels_cut), 0, 1000 - pixels_cut, 500))
        image_cut_right = image.subsurface(pygame.Rect(0, 0, pixels_cut, 500))
        screen.blit(image_cut_right, (1000 - pixels_cut, 0))
        screen.blit(image_cut_left, (0, 0))

    elif angle < 0:
        pixels_cut = -angle * 3
        image_cut_left = image.subsurface(pygame.Rect(0, 0, 1000 - pixels_cut, 500))
        image_cut_right = image.subsurface(pygame.Rect((1000 - pixels_cut), 0, pixels_cut, 500))
        screen.blit(image_cut_left, (pixels_cut, 0))
        screen.blit(image_cut_right, (0, 0))


# def draw_grass(hero_angle):
#     pos_x = int(pos_x)
#     pos_y = int(pos_y)
#     angle = hero_angle
#     image = load_image("grass.jpg")
#     image = pygame.transform.scale(image, (1000, 500))
#
#     pixels_gorizont = pos_x
#     image_cut_gorizont_left = image.subsurface(pygame.Rect((pixels_gorizont), 0, 1000 - pixels_gorizont, 500))
#     image_cut_gorizont_right = image.subsurface(pygame.Rect(0, 0, pixels_gorizont, 500))
#     screen.blit(image_cut_gorizont_right, (1000 - pixels_gorizont, 500))
#     screen.blit(image_cut_gorizont_left, (0, 500))
#
#     pixels_vertical = int(pos_y / 1.7)
#     image_cut_vertical_top = image.subsurface(pygame.Rect(0, 500 - pixels_vertical, 1000, pixels_vertical))
#     image_cut_vertical_bott = image.subsurface(pygame.Rect(0, 0, 1000, 500 - pixels_vertical))
#     screen.blit(image_cut_vertical_top, (0, 500))
#     screen.blit(image_cut_vertical_bott, (0, 500 + pixels_vertical))
#
#     if angle > 0:
#         pixels_cut = angle * 3
#         image_cut_left = image.subsurface(pygame.Rect((pixels_cut), 0, 1000 - pixels_cut, 500))
#         image_cut_right = image.subsurface(pygame.Rect(0, 0, pixels_cut, 500))
#         screen.blit(image_cut_right, (1000 - pixels_cut, 500))
#         screen.blit(image_cut_left, (0, 500))
#
#     elif angle < 0:
#         pixels_cut = -angle * 3
#         image_cut_left = image.subsurface(pygame.Rect(0, 0, 1000 - pixels_cut, 500))
#         image_cut_right = image.subsurface(pygame.Rect((1000 - pixels_cut), 0, pixels_cut, 500))
#         screen.blit(image_cut_left, (pixels_cut, 500))
#         screen.blit(image_cut_right, (0, 500))


def add_wall(x1, y1, x2, y2, color):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    segment = Segment(p1, p2)
    wall = Wall(len(walls) + 1, segment, color)
    walls.append(wall)


def make_walls():
    add_wall(0, 50, 1000, 51, (255, 50, 50))
    add_wall(50, 0, 51, 1000, (50, 255, 50))
    add_wall(950, 0, 951, 1000, (50, 50, 255))
    add_wall(0, 950, 1000, 951, (255, 255, 50))
    add_wall(500, 500, 600, 501, (255, 255, 50))
    # add_wall(200, 200, 801, 601, (50, 255, 255))
    # add_wall(200, 800, 601, 201, (50, 50, 50))


def get_segment_intersection(segment1, segment2):
    a1 = segment1.p1.y - segment1.p2.y
    b1 = segment1.p2.x - segment1.p1.x
    c1 = segment1.p1.x * segment1.p2.y - segment1.p2.x * segment1.p1.y
    a2 = segment2.p1.y - segment2.p2.y
    b2 = segment2.p2.x - segment2.p1.x
    c2 = segment2.p1.x * segment2.p2.y - segment2.p2.x * segment2.p1.y
    check = lambda x, y: min(segment1.p1.x, segment1.p2.x) <= x <= max(segment1.p1.x, segment1.p2.x) and \
                         min(segment1.p1.y, segment1.p2.y) <= y <= max(segment1.p1.y, segment1.p2.y) and \
                         min(segment2.p1.y, segment2.p2.y) <= y <= max(segment2.p1.y, segment2.p2.y) and \
                         min(segment2.p1.x, segment2.p2.x) <= x <= max(segment2.p1.x, segment2.p2.x)
    if b1 * a2 - b2 * a1 and a1:
        y = (c2 * a1 - c1 * a2) / (b1 * a2 - b2 * a1)
        x = (-c1 - b1 * y) / a1
        if check(x, y):
            return Point(x, y)
        else:
            return None
    elif b1 * a2 - b2 * a1 and a2:
        y = (c2 * a1 - c1 * a2) / (b1 * a2 - b2 * a1)
        x = (-c2 - b2 * y) / a2
        if check(x, y):
            return Point(x, y)
        else:
            return None
    else:
        return None


def get_point_distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def get_nearest_wall_intersection(hero_position, hero_look):
    hero_segment = Segment(hero_position, hero_look)
    nearest_wall_intersection = None  # WallIntersection type
    for wall in walls:
        current_wall_intersection_point = get_segment_intersection(hero_segment, wall.segment)
        if current_wall_intersection_point is None:
            continue
        distance_to_current_wall = get_point_distance(hero_position, current_wall_intersection_point)
        if nearest_wall_intersection is None or distance_to_current_wall < nearest_wall_intersection.distance:
            nearest_wall_intersection = WallIntersection(current_wall_intersection_point, distance_to_current_wall,
                                                         wall)

    return nearest_wall_intersection


make_walls()
# map = Field(500, 500)
# map.create_array()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.toggle_fullscreen()
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
moves = []
running = True
v = 10

keys = {'W': False, 'A': False, 'S': False, 'D': False}
pressed = False

hero = Hero(Point(450, 400), 90)


def look_around(coords):
    point1 = Point(coords.x, coords.y + 1000000)
    point2 = Point(coords.x, coords.y - 1000000)
    point3 = Point(coords.x + 1000000, coords.y)
    point4 = Point(coords.x - 1000000, coords.y)
    print(point1, point2, point3, point4)
    return point1, point2, point3, point4


def is_wall(points):
    num = 0
    for point in points:
        nearest_wall_intersection = get_nearest_wall_intersection(hero.position, point)
        if nearest_wall_intersection:
            if nearest_wall_intersection.distance <= 10:
                return True, num
        num += 1
    return False, num


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


def draw_walls():
    for wall in walls:
        pygame.draw.line(screen2,
                         wall.color,
                         (wall.segment.p1.x, wall.segment.p1.y),
                         (wall.segment.p2.x, wall.segment.p2.y),
                         1)


coords = 500, 500
stop = False
move_y = False
move_x = False
offset = [(10, 0), (0, -10), (-10, 0), (0, 10)]
cos, sin = 0, 0
last_x = None
is_map = True
# map.add_wall(10, 10, 40, 10)
# map.draw_walls()
draw_walls()
flag = False

while running:
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
            dif = x1 - last_x if last_x else 0
            last_x = x1
            hero.angle += dif / 2
            # print(hero.angle)
    cos_w = math.cos(hero.angle / 180 * math.pi)
    sin_w = math.sin(hero.angle / 180 * math.pi)
    cos_a = math.cos((hero.angle - 90) / 180 * math.pi)
    sin_a = math.sin((hero.angle - 90) / 180 * math.pi)
    cos_s = math.cos((hero.angle + 180) / 180 * math.pi)
    sin_s = math.sin((hero.angle + 180) / 180 * math.pi)
    cos_d = math.cos((hero.angle + 90) / 180 * math.pi)
    sin_d = math.sin((hero.angle + 90) / 180 * math.pi)
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
            points = look_around(hero.position)
            flag, j = is_wall(points)
            if not (flag):
                hero.position.x += i[0]
                hero.position.y += i[1]
            else:
                hero.position.x += return_steps[j][0]
                hero.position.y += return_steps[j][1]

    moves = []

    # x2, y2 = map.coords
    if is_map:
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        look_x = hero.position.x + cos_w * 1000000
        look_y = hero.position.y + sin_w * 1000000
        tg = math.tan(hero.angle / 180 * math.pi)
        nearest_wall_intersection = get_nearest_wall_intersection(hero.position, Point(look_x, look_y))
        if nearest_wall_intersection:
            look_x = nearest_wall_intersection.point.x
            look_y = nearest_wall_intersection.point.y
        pygame.draw.line(screen,
                         (255, 255, 255),
                         (round(hero.position.x), round(hero.position.y)),
                         (round(look_x), round(look_y)),
                         1)
        pygame.draw.circle(screen, (255, 0, 0), (round(hero.position.x), round(hero.position.y)), 10)
    else:
        draw_sky(hero.angle)
        # draw_grass(hero.angle)
        # pygame.draw.rect(screen, (90, 90, 160), (0, 0, 1000, 500))
        pygame.draw.rect(screen, (90, 160, 90), (0, 500, 1000, 500))
        angle = hero.angle - 45
        current_wall_id = 0
        wall_height = 0
        count = 1
        start_wall_height = None
        color = None
        for pix in range(1000):
            cos = math.cos(angle / 180 * math.pi)
            sin = math.sin(angle / 180 * math.pi)
            x3 = hero.position.x + cos * 1000000
            y3 = hero.position.y + sin * 1000000
            nearest_wall_intersection = get_nearest_wall_intersection(hero.position, Point(x3, y3))
            # if nearest_wall_intersection is None:
            #     wall_height = 0
            # else:
            #     wall_height = round(
            #             30000 / nearest_wall_intersection.distance / math.cos((angle - hero.angle) / 180 * math.pi))
            #     wall_top = (1000 - wall_height) / 2
            #     wall_bottom = wall_top + wall_height
            #     abs_x = pix
            #     pygame.draw.line(screen, nearest_wall_intersection.wall.color, (abs_x, wall_top), (abs_x, wall_bottom), 1)

            if nearest_wall_intersection is None:
                wall_height = 0
            else:
                if nearest_wall_intersection.wall.id != current_wall_id or pix == 999:
                    prev_start_height = start_wall_height
                    prev_color = color
                    start_wall_height = round(
                        30000 / nearest_wall_intersection.distance / math.cos((angle - hero.angle) / 180 * math.pi))
                    color = nearest_wall_intersection.wall.color
                    if current_wall_id == 0:
                        current_wall_id = nearest_wall_intersection.wall.id
                        angle += 0.09
                        continue
                    if not prev_start_height:
                        angle += 0.09
                        continue
                    dy = (wall_height - prev_start_height) / 2
                    dx = count
                    k = dy / dx
                    x = 1
                    for _ in range(count):
                        y = x * k
                        h = 2 * y + prev_start_height
                        wall_top = (1000 - h) / 2
                        wall_bottom = wall_top + h
                        abs_x = pix - count + x
                        pygame.draw.line(screen, prev_color, (abs_x, wall_top), (abs_x, wall_bottom), 1)
                        x += 1
                    count = 1
                    current_wall_id = nearest_wall_intersection.wall.id

                count += 1
                wall_height = round(
                    30000 / nearest_wall_intersection.distance / math.cos((angle - hero.angle) / 180 * math.pi))
            angle += 0.09

    # find and draw monsters
    found = find_monster(450, 500, hero.position.x, hero.position.y, hero.angle)
    # if found:
    #     pygame.draw.circle(screen, (0, 0, 0), (round(found[0]), 500), 5000 // round(found[1]))

    pygame.display.flip()
    clock.tick(100)
