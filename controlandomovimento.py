import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

sonic_x = 10
sonic_y = 280

direcmov = 0
movcima = 0

sprite = "sonicdireita.gif"

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                direcmov = +10
            elif event.key == K_LEFT:
                direcmov = -10
            elif event.key == K_UP:
                movcima = -5
                sprite = "sonicball.gif"
        elif event.type == KEYUP:
            direcmov = 0
            movcima = 0

    sonic_x += direcmov
    sonic_y += movcima

    if sonic_y < 180:
        movcima = +5

    if sonic_y == 280:
        movcima = 0

    if direcmov == 10:
        if movcima == 5 or movcima == -5:
            sprite = "sonicball.gif"
        else:
            sprite = "sonicdireita.gif"
    elif direcmov == -10:
        if movcima == 5 or movcima == -5:
            sprite = "sonicball.gif"
        else:
            sprite = "sonicesquerda.gif"


    screen.blit(pygame.image.load("greenhill.png").convert(), (0, 0))
    screen.blit(pygame.image.load(sprite).convert(), (sonic_x, sonic_y))

    pygame.display.update()