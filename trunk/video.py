import pygame
from pygame.locals import *
from sys import exit

pygame.init()

video = pygame.movie.Movie('video.mpg')

# eh criada uma tela do tamanho da resolucao do filme, para caber perfeitamente
screen = pygame.display.set_mode(video.get_size(), 0, 32)

# a tela eh associada ao filme, dizemos entao ao PyGame onde queremos que o filme apareca
video.set_display(pygame.display.get_surface())

# o video eh executado
video.play()

while video.get_busy():
    for event in pygame.event.get():
		if event.type == QUIT:
			exit()
