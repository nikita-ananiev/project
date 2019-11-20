import pygame
# инициализация Pygame:
pygame.init()
# размеры окна:

# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode((500, 500))


fps = 120
clock = pygame.time.Clock()
screen.fill((250, 0, 0))
pygame.draw.circle(screen, pygame.Color('white'), (0, 0), 100)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

