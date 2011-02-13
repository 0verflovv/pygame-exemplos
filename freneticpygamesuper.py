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
numberiter = 0

while True:

    #pygame.event.get() retornara o evento esperado,ou seja,o evento executado pelo usuario
    for event in pygame.event.get():
        #se o evento esperado for fechar a tela, entao o pygame sai o programa
        if event.type == QUIT:
            pygame.quit()
            exit()


    color = (randint(0, 255), randint(0, 255), randint(0, 255))

    numberiter = numberiter + 0.007


    screen.fill((0, 0, 0))

    for i in range(numberiter):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        pygame.draw.circle(screen, color,(randint(0, 800), randint(0, 600)), radius)
        pygame.draw.rect(screen, color, Rect((randint(0, 800), randint(0, 600)), (100, 100)))

    pygame.display.flip()

#O exercicio sera, desenhar outro circulo dentro do que ja foi feito!
