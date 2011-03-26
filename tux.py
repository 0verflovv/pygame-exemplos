import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

preto = (0, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 255, 0)
cinza = (25, 25, 25)
cinzaclaro = (230, 230, 230)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	# corpo
	pygame.draw.circle(screen, cinza, (400, 450), 420)
	# pelo
	pygame.draw.circle(screen, cinzaclaro, (400, 680), 380)
	# olho esquerda
	pygame.draw.circle(screen, branco, (245, 265), 150)
	# olho direita
	pygame.draw.circle(screen, branco, (535, 265), 150)
	# pupila esquerda
	pygame.draw.circle(screen, preto, (345, 265), 40)
	# pupila direita
	pygame.draw.circle(screen, preto, (435, 265), 30)
	# bico
	pygame.draw.polygon(screen, amarelo, [(280, 350), (400, 500), (515, 350)])
	pygame.display.update()

	
