""" levelintro.py 
    level intro screen
"""

import pygame, gameEngine
from keyframe import *
from game import *

class LevelIntro(gameEngine.Scene):
    def __init__(self, prevScene, levelNum):
        gameEngine.Scene.__init__(self)
        self.setCaption("Level Intro")
        self.prevScene = prevScene
        self.levelNum = levelNum
        self.title = LevelTitle(self)
        self.sprites = [self.title]
        pygame.mixer.music.stop()
        self.reset()
            
    def reset(self):
        self.background.set_alpha(0)
        self.frames = 0                           # current frame
        self.background = pygame.image.load("data/levelintro.png")
        self.keyframes = []
        self.createKeys()
    
    def createKeys(self):
        # bg fades
        newKey = SurfaceFadeKeyframe(self.background, 0, 50, 0, 255)        
        self.keyframes.append(newKey)        
        newKey = SurfaceFadeKeyframe(self.background, 110, 130, 255, 0)        
        self.keyframes.append(newKey)        
        # level title fades
        newKey = AlphaKeyframe(self.title, 0, 90, 0, 255)     
        self.keyframes.append(newKey)
        newKey = AlphaKeyframe(self.title, 105, 120, 255, 0)     
        self.keyframes.append(newKey)
        # load game
        newKey = LoadGameKeyframe(self, 130)        
        self.keyframes.append(newKey)        
        
    def update(self):
        pass
               
class LevelTitle(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("data/levelintro-1-1.png")
        x = scene.screen.get_width() / 2
        y = scene.screen.get_height() / 2
        self.setPosition((x, y))    

class LoadGameKeyframe(Keyframe):
    """ load the game """
    def __init__(self, scene, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene

    def process(self):
        if self.getNextValue() == 0: 
            self.scene.stop()
            self.scene.game = Game(self.scene.levelNum, self.scene.prevScene)
            self.scene.game.start()                    