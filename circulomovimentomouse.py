#-------------------------------------------------------------------------------
# Name:        circulomovimentomouse
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

pygame.init()

amarelo = (230, 170, 0)
preto = (0, 0, 0)

screen = pygame.display.set_mode((640, 360), 0, 32)
raio = 60
x = 0
y = 0

while True:
    for event in pygame.event.get():
        # se ele capturar um evento de fechar a tela (clicar no botao "X" no topo da janela), o programa eh fechado
        if event.type == QUIT:
            exit()
        if event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()


    posicao = (x, y)

    # colore o fundo de preto, deve sempre vir antes de desenharmos os objetos, no caso o circulo, pois se nao, tudo vai ficar preto!
    screen.fill(preto)
    pygame.draw.circle(screen, amarelo, posicao, raio)

    pygame.display.update()