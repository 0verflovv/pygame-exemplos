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

# coloca as cores preto e branco em variaveis
preto = (0, 0, 0)
branco = (255, 255, 255)

# coloca o objeto (font) que representa a fonte em uma variavel
fonte = pygame.font.SysFont("arial", 120)

# constroi a janela no tamanho 800 x 600 e coloca o objeto (surface) que a representa em uma variavel
screen = pygame.display.set_mode((800, 600))

while True:
    # pinta o fundo da tela de preto
    screen.fill(preto)

    # joga a fonte na posicao x=100, y=50 da tela
    screen.blit(fonte.render("Hello World!", True, branco), (130, 200))

    # atualiza a tela constantemente
    pygame.display.flip()