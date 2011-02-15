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

# Desenhando circulos(parametros = screen,color,position,radius)

pygame.init()
cor = (230, 170, 0)
screen = pygame.display.set_mode((640, 360), 0, 32)
# meio da tela
posicao = (300, 176)
raio = 60

while True:
    for event in pygame.event.get():
        # se ele capturar um evento de fechar a tela (clicar no botao "X" no topo da janela), o programa eh fechado
        if event.type == QUIT:
            exit()

    pygame.draw.circle(screen, cor, posicao, raio)
    pygame.display.update()

#O exercicio sera, desenhar outro circulo dentro do que ja foi feito!

