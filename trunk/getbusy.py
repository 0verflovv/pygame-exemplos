import pygame
from pygame.locals import *
from sys import exit

pygame.init()

pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play()

screen = pygame.display.set_mode((800, 600), 0, 32)
branco = (255, 255, 255)

while pygame.mixer.music.get_busy():
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	screen.blit(pygame.font.SysFont("arial", 58).render("Musica sendo executada...", True, branco), (80, 200))
	pygame.display.update()
    
