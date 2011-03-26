import pygame
from pygame.locals import *
from sys import exit

from datetime import datetime

pygame.init()

preto = (0, 0, 0)
branco = (255, 255, 255)

screen = pygame.display.set_mode((370, 80))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    screen.fill(preto)

    # blit jogando a string datahora na tela
    screen.blit(pygame.font.SysFont("calibri", 35).render(str(datetime.now()), True, branco), (20, 20))
    
    pygame.display.update()
