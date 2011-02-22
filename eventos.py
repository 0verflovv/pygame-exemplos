import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
branco = (255, 255, 255)
preto = (0, 0, 0)

mensagem = ""

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            mensagem = "KEYDOWN"
        elif event.type == KEYUP:
            mensagem = "KEYUP"
        elif event.type == MOUSEMOTION:
            mensagem = "MOUSEMOTION"
        elif event.type == MOUSEBUTTONDOWN:
            mensagem = "MOUSEBUTTONDOWN"

    screen.fill(preto)
    screen.blit(pygame.font.SysFont("arial", 72).render(mensagem, True, branco), (80, 200))
    pygame.display.update()