#-------------------------------------------------------------------------------
# Name:        Duck Hunt v5
# Purpose:     Faz o pato desaparecer se for acertado
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
azul = (0, 255, 0)

screen = pygame.display.set_mode((890, 550), 0, 32)

# variaveis que armazenarao a posicao em que o mouse se encontra
x_pos = 0
y_pos = 0

# variaveis que armazenarao a posicao em que um clique no mouse foi efetuado
x_clique = 0
y_clique = 0

# variaveis que armazenarao a posicao em que o pato se encontra
x_duck = 0
y_duck = randint(0, 550)

pontos = 0

duckacertado = False

while True:
    for event in pygame.event.get():
        # se ele capturar um evento de fechar a tela (clicar no botao "X" no topo da janela), o programa eh fechado
        if event.type == QUIT:
            exit()
        if event.type == MOUSEMOTION:
            x_pos, y_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            x_clique, y_clique = pygame.mouse.get_pos()


    posicao = (x_pos, y_pos)

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
    screen.blit(pygame.font.SysFont("arial", 72).render("Pontos: " + str(pontos), True, azul), (500, 450))

    if duckacertado == False:
        # para serem contabilizados pontos, a posicao do clique deve estar mais ou menos onde o pato esta exatamente,
        # por conta desse mais ou menos usamos a funcao range
        if x_clique + 50 in range(x_duck - 30, x_duck + 30) and y_clique + 50 in range(y_duck - 30, y_duck + 30):
            pontos += 1
            duckacertado = True
        screen.blit(pygame.image.load("greenduck.gif"), (x_duck, y_duck))

    screen.blit(pygame.image.load("mira.gif").convert(), posicao)

    pygame.display.update()