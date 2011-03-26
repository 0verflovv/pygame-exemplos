""" menucredits.py 
    credits menu
"""

import pygame, gameEngine
from keyframe import *
from game import *

class CreditsMenu(gameEngine.Scene):
    def __init__(self, prevScene):
        gameEngine.Scene.__init__(self)
        self.setCaption("Credits Menu")
        self.prevScene = prevScene
        self.selectSnd = pygame.mixer.Sound("data/menuselect.ogg")
        self.selectSnd.set_volume(0.5)
        self.sprites = []
        self.reset()
            
    def reset(self):
        self.background.set_alpha(0)
        self.frames = 0                           # current frame
        self.background = pygame.image.load("data/menucredits.png")
        self.keyframes = []
        self.createKeys()
    
    def createKeys(self):
        # fade in 
        fade = 100
        newKey = SurfaceFadeKeyframe(self.background, 0, fade, 0, 255)        
        self.keyframes.append(newKey)        
        
    def update(self):
        pass
    
    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE \
            or event.key == pygame.K_RETURN:
                self.selectSnd.play()
                self.stop() 
                self.prevScene.start()

                    