#-------------------------------------------------------------------------------
# Name:        Frenetic
# Purpose:
#
# Author:      Johann
#
# Created:     13/02/2011
# Copyright:   (c) Johann 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import*
from sys import exit

from random import randint

pygame.init()

screen = pygame.display.set_mode((1280, 800),0,32)
numberiter = 0
Fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                Fullscreen = not Fullscreen
                if Fullscreen:
                    screen = pygame.display.set_mode((1280, 800), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((1280, 800), 0, 32)

    pygame.mouse.set_visible(False)
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    numberiter = numberiter + 0.007
    screen.fill((0, 0, 0))

    for i in range(numberiter):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        pygame.draw.circle(screen, color,(randint(0, 1280), randint(0, 800)), 60)
        pygame.draw.rect(screen, color, Rect((randint(0, 1280), randint(0, 800)), (100, 100)))

    pygame.display.flip()

