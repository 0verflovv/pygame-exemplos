""" objwarp.py 
    warp object
"""

import pygame, gameEngine

class Warp(gameEngine.SuperSprite):
    def __init__(self, scene, bounds):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setBoundAction(self.STOP)        
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        x = bounds[0] + (width /2)
        y = bounds[1] + (height /2)
        self.imageMaster = pygame.Surface((width, height))
        self.imageMaster.fill((0,0, 0))                
        self.imageMaster.set_colorkey((0,0,0))
        self.imageMaster = self.imageMaster.convert()        
        self.x = x
        self.y = y