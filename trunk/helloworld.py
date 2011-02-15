#-------------------------------------------------------------------------------
# Name:        Hello World
# Purpose:     Um Hello World em PyGame
#
# Author:      Johann
#
# Created:     11/02/2011
# Copyright:   (c) Johann 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit

# inicializa a pygame engine
pygame.init()
# coloca a cor branco em uma variavel
branco = (255, 255, 255)
# constroi a janela no tamanho 800 x 600 e coloca o objeto (surface) que a representa em uma variavel
screen = pygame.display.set_mode((800, 600))

while True:
    # o for esta sempre capturando eventos
    for event in pygame.event.get():
        # se ele capturar um evento de fechar a tela (clicar no botao "X" no topo da janela), o programa eh fechado
        if event.type == QUIT:
            exit()
    # joga a fonte na posicao x=100, y=50 da tela
    screen.blit(pygame.font.SysFont("arial", 120).render("Hello World!", True, branco), (130, 200))
    # atualiza a tela constantemente
    pygame.display.flip()