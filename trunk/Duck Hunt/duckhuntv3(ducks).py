#-------------------------------------------------------------------------------
# Name:        Duck Hunt v3
# Purpose:     Coloca um pato passando na frente da background
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

preto = (0, 0, 0)

screen = pygame.display.set_mode((890, 550), 0, 32)

# variaveis que armazenarao a posicao em que o mouse se encontra
x = 0
y = 0

x_duck = 0
y_duck = randint(0, 550)

while True:
    for event in pygame.event.get():
        # se ele capturar um evento de fechar a tela (clicar no botao "X" no topo da janela), o programa eh fechado
        if event.type == QUIT:
            exit()
        if event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()


    posicao = (x, y)

    x_duck += 1

    if x_duck > 890:
        x_duck = 0
        y_duck = randint(0, 550)

    # colore o fundo de preto, deve sempre vir antes de desenharmos os objetos, no caso o circulo, pois se nao, tudo vai ficar preto!
    screen.fill(preto)
    pygame.mouse.set_visible(False)

    # o blit do background deve vir anter do blit da mira, pois assim o background sera desenhado
    # primeiro e a mira depois, ficando o background atras da mira e nao o contrario!
    screen.blit(pygame.image.load("background.png"), (0, 0))
    screen.blit(pygame.image.load("greenduck.gif"), (x_duck, y_duck))
    screen.blit(pygame.image.load("mira.gif").convert(), posicao)

    pygame.display.update()