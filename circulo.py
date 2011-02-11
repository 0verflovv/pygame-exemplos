#-------------------------------------------------------------------------------
# Name:        C�rculo
# Purpose:     Um C�rculo em PyGame
#
# Author:      Fernanda
#
# Created:     11/02/2011
# Copyright:   (c) Fernanda 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import*
from sys import exit

#Desenhando circulos(parametros = screen,color,position,radius)

pygame.init()

screen = pygame.display.set_mode((640,360),0,32)
color = (230,170,0)
position = (300,176) #Meio da tela
radius = (60)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.lock()

    pygame.draw.circle(screen,color,position,radius)
    
    screen.unlock()

    pygame.display.update()

#O exerc�cio ser�, desenhar outro c�rculo dentro do que j� foi feito!
    
