import pygame
from pygame.locals import *
from sys import exit

def carregarImagens(screen):
	screen.blit(pygame.image.load("background.jpg").convert(), (0, 0))
	screen.blit(pygame.image.load("crono.gif").convert(), (140, 275))
	screen.blit(pygame.image.load("frog.gif").convert(), (75, 360))
	screen.blit(pygame.image.load("alien.gif").convert(), (600, 335))

def carregarTextos(screen, pos_seta):
	screen.blit(pygame.font.SysFont("arial", 32).render("Attack", True, (255, 255, 255)), (50, 500)) 
	screen.blit(pygame.font.SysFont("arial", 32).render("Run", True, (255, 255, 255)), (50, 530)) 
	screen.blit(pygame.font.SysFont("arial", 32).render(">", True, (255, 255, 255)), pos_seta) 

def atacar(screen):
	pos_x = 600
	pos_y = 335
	
	screen.blit(pygame.image.load("alien.gif").convert(), (pos_x, pos_y))
	pygame.display.update()

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)

pygame.display.set_caption("PyGame RPG Battle Sample")

pos_seta = (20, 500)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == KEYDOWN:
			if event.key == K_DOWN:
				pos_seta = (20, 530)
			elif event.key == K_UP:
				pos_seta = (20, 500)
			elif event.key == K_SPACE:
				# seta esta em 'attack'
				if pos_seta == (20, 500):
					atacar(screen)
				# seta esta em 'run'
				elif pos_seta == (20, 530):
					correr(screen)
	carregarImagens(screen)
	carregarTextos(screen, pos_seta)
	pygame.display.update()
