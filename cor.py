import pygame
# importa constantes necessarias ao PyGame
from pygame.locals import *
from sys import exit

# constroi a janela no tamanho 800 x 600 e coloca o objeto (surface) que a representa em uma variavel
screen = pygame.display.set_mode((800, 600), 0, 32)
azulclaro = (120, 50, 255)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        screen.fill(azulclaro)
        pygame.display.update()
