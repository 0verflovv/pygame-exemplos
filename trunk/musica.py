import pygame
from pygame.locals import *
from sys import exit

pygame.init()

pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play()

screen = pygame.display.set_mode((800, 600), 0, 32)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()


