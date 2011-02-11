#-------------------------------------------------------------------------------
# Name:        Retângulo
# Purpose:     Um Retângulo em PyGame
#
# Author:      Fernanda
#
# Created:     11/02/2011
# Copyright:   (c) Fernanda 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame   #Importa a biblioteca Pygame dando acesso a todos os submodulos
from pygame.locals import *
from sys import exit

#inicializa cada um dos submodulos da biblioteca Pygame
pygame.init()

#Instanciando o objeto que sera uma janela Pygame em seu desktop,passando como parametro uma tupla que contem o tamanho da tela(height and width)
screen = pygame.display.set_mode((640,360),0,32)    

while True:
    #pygame.event.get() retornará o evento esperado,ou seja,o evento executado pelo usuario
    for event in pygame.event.get():
        #se o evento esperado for fechar a tela, entao o pygame sai o programa
        if event.type == QUIT:
            pygame.quit()
            exit()

    #Bloqueia a tela
    screen.lock()
    
    pygame.draw.rect(screen,(140,240,130), Rect((100,100),(130,170)))#Desenhando na tela,o primeiro parametro eh o objeto tela(screen)   
                                                                     #,o segundo eh a cor do retangulo,o ultimo parametro eh que objeto vc deseja desenhar
    #Desbloqueia a tela                                              #Dentro da funcao Rect() passam-se dois parametros,o primeiro e a posicao do seu retangulo e o segundo o tamanho                                        
    screen.unlock()                              

    #Refresh na tela                                      
    pygame.display.update()





