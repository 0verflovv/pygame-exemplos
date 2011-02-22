import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
branco = (255, 255, 255)
preto = (0, 0, 0)
posicao = ""

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            posicao = str(pygame.mouse.get_pressed())

    screen.fill(preto)
    screen.blit(pygame.font.SysFont("arial", 72).render(posicao, True, branco), (80, 200))
    pygame.display.update()