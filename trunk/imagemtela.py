import pygame
from pygame.locals import*
from sys import exit

pygame.init()

preto = (0, 0, 0)

screen = pygame.display.set_mode((640, 360), 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill(preto)

    # pygame.image.load recebe uma string com o endereco da imagem, carregando-a
    # o .convert() converte essa imagem carregada para o tipo Surface, possibilitando que ela apareca na tela
    screen.blit(pygame.image.load("imagem.jpg").convert(), (130, 20))
    pygame.display.update()
