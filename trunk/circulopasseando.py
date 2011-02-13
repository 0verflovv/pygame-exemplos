#-------------------------------------------------------------------------------
# Name:        Circulo
# Purpose:     Um Circulo em PyGame
#
# Author:      Fernanda
#
# Created:     11/02/2011
# Copyright:   (c) Fernanda 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import*
from sys import exit

#Desenhando circulos(parametros = screen,color,position,radius)

pygame.init()

screen = pygame.display.set_mode((800, 600),0,32)
color = (230,170,0)
radius = (60)

# x e y sao as posicoes iniciais na tela
x = 0
y = 0

while True:

    #pygame.event.get() retornara o evento esperado,ou seja,o evento executado pelo usuario
    for event in pygame.event.get():
        #se o evento esperado for fechar a tela, entao o pygame sai o programa
        if event.type == QUIT:
            pygame.quit()
            exit()

    x = x + 1
    y = y + 1

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen,color,(x, y),radius)

    pygame.display.flip()

#O exercicio sera, desenhar outro circulo dentro do que ja foi feito!

