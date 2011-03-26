""" menupause.py 
    pause menu
"""

import pygame, gameEngine, keyframe

class PauseMenu(gameEngine.Scene):
    def __init__(self, scene, prevScr):
        gameEngine.Scene.__init__(self)
        self.prevEngine = scene
        self.initBgSprite(prevScr)
        self.title = PauseTitle(self)
        self.sprites = [self.prevScrSprite, self.title]
        self.bgKey = keyframe.AlphaKeyframe(self.prevScrSprite, 0, 50, 0, 100)        
        self.titleRotoKey = keyframe.RotoZoomKeyframe(self.title, 0, 20, (343, 0), (0,1.0))        
        self.titleFadeKey = keyframe.AlphaKeyframe(self.title, 0, 20, 0, 255)        
        self.keyframes = [self.bgKey, self.titleRotoKey, self.titleFadeKey]
    
    def initBgSprite(self, prevScr):
        self.prevScrSprite = gameEngine.SuperSprite(self)
        self.prevScrSprite.imageMaster = prevScr
        x = self.screen.get_width() / 2
        y = self.screen.get_height() / 2
        self.prevScrSprite.setPosition((x,y))

    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.stop()     
                self.prevEngine.keepGoing = True
        
    def update(self):
        pass

class PauseTitle(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("data/menupause.png")
        x = scene.screen.get_width() / 2
        y = scene.screen.get_height() / 2
        self.setPosition((x, y))    
                    