import pygame
pygame.init()
size = int(input()), int(input())
screen = pygame.display.set_mode((800, 800))
screen2 = pygame.Surface(screen.get_size())
running = True
x = 0
v = 10
fps = 120
clock = pygame.time.Clock()
screen.fill((0, 0, 0))

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (x * self.cell_size + self.left,
                                y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def get_cell(self, pos):
        x, y = pos
        x -= self.left
        y -= self.top
        return x // self.cell_size, y // self.cell_size

    def on_click(self, cell_coord):
        if cell_coord[0] < size[0] and cell_coord[1] < size[1] and cell_coord[0] >= 0 and cell_coord[1] >= 0:
            print(cell_coord[0] + 1, cell_coord[1] + 1)
        else:
            print(None)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

board = Board(size[0], size[1])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
    clock.tick(100)
    pygame.display.flip()