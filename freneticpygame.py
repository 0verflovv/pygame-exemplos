#-------------------------------------------------------------------------------
# Name:        module1
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

#Desenhando circulos(parametros = screen,color,position,radius)

pygame.init()

screen = pygame.display.set_mode((800, 600),0,32)
radius = (60)

# x e y sao as posicoes iniciais na tela
x = 0
y1 = 0
y2 = 0
y3 = 0
y4 = 0
y5 = 0
y6 = 0
z = 0

while True:

    #pygame.event.get() retornara o evento esperado,ou seja,o evento executado pelo usuario
    for event in pygame.event.get():
        #se o evento esperado for fechar a tela, entao o pygame sai o programa
        if event.type == QUIT:
            pygame.quit()
            exit()

    x = x + 1
    y1 = y1 + 1
    y2 = y2 + 1
    y3 = y3 + 1
    y4 = y4 + 1
    y5 = y5 + 1
    y6 = y6 + 1

    if x > 800:
        x = randint(0, 800)

    if y1 > 600:
        y1 = randint(0, 600)

    if y2 > 600:
        y2 = randint(0, 600)

    if y3 > 600:
        y3 = randint(0, 600)

    if y4 > 600:
        y4 = randint(0, 600)

    if y5 > 600:
        y5 = randint(0, 600)

    if y6 > 600:
        y6 = randint(0, 600)

    color = (randint(0, 255), randint(0, 255), randint(0, 255))


    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, color,(x, y1), radius)

    for i in (y1, y2, y3, y4, y5, y6):
        pygame.draw.rect(screen, color, Rect((x, i), (100, 100)))

    pygame.display.flip()

#O exercicio sera, desenhar outro circulo dentro do que ja foi feito!
