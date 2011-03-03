import pygame
from pygame.locals import*
from sys import exit


class Screen:
    def __init__(self):

        self.caminho = {"Background":"ChronoTrigger.jpg","Esfera":"esfera.gif"}
        self.pos_esfera = (310,410)

    def carregarImagens(self, screen):
        screen.blit(pygame.image.load("ChronoTrigger.jpg").convert(),(0,0))
        screen.blit(pygame.image.load("esfera.gif").convert,(self.pos_esfera))

    def carregarTexto(self, screen):
        screen.blit(pygame.font.SysFont("arial black",28).render("Start", True, (255,255,255),(360,400))
        screen.blit(pygame.font.SysFont("arial black",28).render("Exit", True, (255,255,255), (360,430))

    def Looping(self,screen):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()    
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.pos_esfera = (330,440)
                    if event.key == K_UP:
                        self.pos_esfera = (330,410)

            carregarImagens(screen)
            carregarTexto(screen)
            pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("Starting Pygame RPG Battle")

tela = Screen()
tela.Looping(screen)
