import pygame
from pygame.locals import*
from sys import exit

pygame.init()

preto = (0, 0, 0)
verde = (0, 255, 0)

screen = pygame.display.set_mode((640, 360), 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill(preto)

    pygame.draw.rect(screen, verde, Rect((300, 120), (140, 70)))

    pygame.display.update()
