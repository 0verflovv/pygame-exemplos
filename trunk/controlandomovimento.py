import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

# posicao no eixo x do Sonic na tela
sonic_x = 10

# posicao no eixo y do Sonic na tela
sonic_y = 280

direcmov = 0
movcima = 0

sprite = "sonicdireita.gif"

pygame.mixer.music.load("hill.mid")
pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
				# pressionando seta para a direita, Sonic deve mover-se 10 pontos no eixo x para a direita
                direcmov = +10
            elif event.key == K_LEFT:
				# pressionando seta para a esquerda, Sonic deve mover-se 10 pontos no eixo x para a esquerda
                direcmov = -10
            elif event.key == K_UP:
				# pressionando seta para cima, Sonic deve mover-se 5 pontos para baixo no eixo y (isso faz ele "subir", nao descer...
				# pois a origem (0, 0) esta no topo da janela
                movcima = -5
                sprite = "sonicball.gif"
        elif event.type == KEYUP:
            direcmov = 0
            movcima = 0

	# a posicao do Sonic no eixo x deve ser iterada de acordo com o que aconteceu nos eventos, assim como a posicao y...
    sonic_x += direcmov
    sonic_y += movcima

    if sonic_y < 180:
        movcima = +5

    if sonic_y == 280:
        movcima = 0

    if direcmov == 10:
        if movcima == 5 or movcima == -5:
            sprite = "sonicball.gif"
        else:
            sprite = "sonicdireita.gif"
    elif direcmov == -10:
        if movcima == 5 or movcima == -5:
            sprite = "sonicball.gif"
        else:
            sprite = "sonicesquerda.gif"


    screen.blit(pygame.image.load("greenhill.png").convert(), (0, 0))
    screen.blit(pygame.image.load(sprite).convert(), (sonic_x, sonic_y))

    pygame.display.update()
