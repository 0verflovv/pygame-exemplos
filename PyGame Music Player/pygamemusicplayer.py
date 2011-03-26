import pygame
from pygame.locals import *

from sys import exit
from os import getcwd, listdir

pygame.init()

class PyGameMusicPlayer:
    def __init__(self):
        self.branco = (255, 255, 255)
        self.preto = (0, 0, 0)

    def retornarTempoFormatado(self, tempo):
        try: tempo = int(str(tempo)[:-3])
        except ValueError: return "00:00"
        if tempo < 10:
            return "00:0" + str(tempo)
        elif tempo >= 10 and tempo < 60:
            return "00:" + str(tempo)
        elif tempo >= 60:
            if tempo % 60 < 10:
                return "0" + str(tempo / 60) + ":0" + str(tempo % 60)
            return "0" + str(tempo / 60) + ":" + str(tempo % 60)

    def criarPlaylist(self):
        return [musica for musica in listdir(getcwd()) if ".mp3" in musica\
        or ".ogg" in musica or ".mid" in musica or ".midi" in musica]

    def tratarClique(self, x, y):
        """Verifica onde foi efetuado o clique e efetua a acao esperada"""
        # botao de pause
        if x in range(110, 155) and y in range(120, 160):
            pygame.mixer.music.pause()
            return "Pause"
        # botao de play
        elif x in range(160, 200) and y in range(120, 160):
            pygame.mixer.music.unpause()
            return "Play"
        # botao de proximo
        elif x in range(260, 310) and y in range(120, 160):
            pygame.mixer.music.stop()
            return "Proximo"
		# botao de diminuir volume
        elif x in range(585, 625) and y in range(125, 155):
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
            return "Volume: " + str(pygame.mixer.music.get_volume())[:3]
		# botao de aumentar volume
        elif x in range (625, 665) and y in range(125, 155):
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
            return "Volume: " +  str(pygame.mixer.music.get_volume())[:3]

    def mostrarPainel(self):
        screen = pygame.display.set_mode((670, 165))
        clique_x, clique_y = 0, 0
        acaoexecutada = ""
        screen = pygame.display.set_mode((670, 165))
        playlist = self.criarPlaylist()
        for musica in playlist:
			# para cada musica da playlist, uma tela sera mostrada (um while pygame.mixer.music.get_busy())
            pygame.mixer.music.load(musica)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        clique_x, clique_y = pygame.mouse.get_pos()
                        acaoexecutada = self.tratarClique(clique_x, clique_y)

                screen.blit(pygame.image.load("painel.png").convert(), (0, 0))
                screen.blit(pygame.font.SysFont("arial", 40).render(musica + " - " \
                + self.retornarTempoFormatado(pygame.mixer.music.get_pos()), True, \
                self.branco), (20, 40))
                screen.blit(pygame.font.SysFont("arial", 14).render(acaoexecutada, True, self.branco), (20, 80))

                pygame.display.update()
        self.mostrarPainel()

def main():
    pgmp = PyGameMusicPlayer()
    pgmp.mostrarPainel()

if __name__ == '__main__':
    main()
