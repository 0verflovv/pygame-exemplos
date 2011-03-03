import pygame
from pygame.locals import *
from sys import exit

from Crono import Crono
from Frog import Frog
from Alien import Alien

class Main():
    def __init__(self):
        self.crono = Crono()
        self.frog = Frog()
        self.alien = Alien()
        self.local = {"CRONO" : "crono.gif", "FROG" : "frog.gif", "ALIEN" :\
                      "alien.gif", "BACKGROUND" : "background.jpg"}
        self.pos_seta = (20, 500)
        
    def carregarCenario(self, screen):
        screen.blit(pygame.image.load("background.jpg").convert(), (0, 0))
        for caract in (self.crono, self.frog, self.alien):
            screen.blit(pygame.image.load(self.local[caract.nome]).convert(), \
                        caract.posicao)
            
    def carregarTextos(self, screen):
        screen.blit(pygame.font.SysFont("arial", 32).render("Attack", True, \
                    (255, 255, 255)), (50, 500)) 
	screen.blit(pygame.font.SysFont("arial", 32).render("Run", True, \
                    (255, 255, 255)), (50, 530)) 
	screen.blit(pygame.font.SysFont("arial", 32).render(">", True, \
                    (0, 0, 0)), self.pos_seta)
        
    def loop(self,screen):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                            self.pos_seta = (20, 530)
                    elif event.key == K_UP:
                            self.pos_seta = (20, 500)
                    elif event.key == K_SPACE:
                            # seta esta em 'attack'
                            if self.pos_seta == (20, 500):
                                    pass
                            # seta esta em 'run'
                            elif self.pos_seta == (20, 530):
                                    pass
            self.carregarCenario(screen)
            self.carregarTextos(screen)
            pygame.display.update()
            
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("PyGame RPG Battle Sample")

main = Main()
main.loop(screen)

