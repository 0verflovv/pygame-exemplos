""" menumain.py 
    main menu
"""

import pygame, gameEngine
from keyframe import *
from menucredits import *
from levelintro import *

class MainMenu(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.setCaption("Main Menu")
        pygame.mixer.init(44100, -16, 2, 100)
        pygame.mixer.music.load("data/menumain.ogg")
        pygame.mixer.music.play()
        self.viewSnd = pygame.mixer.Sound("data/menuview.ogg")
        self.viewSnd.set_volume(0.2)
        self.selectSnd = pygame.mixer.Sound("data/menuselect.ogg")
        self.selectSnd.set_volume(0.5)
        self.startLnk = MenuLink(self, "data/menumain-start%d.png", 1, (408, 241), 1)
        self.creditsLnk = MenuLink(self, "data/menumain-credits%d.png", 1, (408, 315), 0)
        self.quitLnk = MenuLink(self, "data/menumain-quit%d.png", 1, (408, 395), 0)
        self.sel = 0   # selected item
        self.sprites = [self.startLnk, self.creditsLnk, self.quitLnk]
        self.reset()
            
    def reset(self):
        self.background.set_alpha(0)
        self.frames = 0                           # current frame
        self.cycle = 0                            # sync cycle frame counter
        self.startTicks = pygame.time.get_ticks() # number of ticks since reset
        self.background = pygame.image.load("data/menumain.png")
        self.keyframes = []
        self.createKeys()
    
    def createKeys(self):
        # fade in 
        fade = 100
        newKey = SurfaceFadeKeyframe(self.background, 0, fade, 0, 255)        
        self.keyframes.append(newKey)        
        fade = 200
        newKey = AlphaKeyframe(self.startLnk, 0, fade, 0, 255)     
        self.keyframes.append(newKey)
        newKey = AlphaKeyframe(self.creditsLnk, 0, fade, 0, 255)     
        self.keyframes.append(newKey)
        newKey = AlphaKeyframe(self.quitLnk, 0, fade, 0, 255)     
        self.keyframes.append(newKey)
        
    def update(self):
        pass
    
    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop() 
            if event.key == pygame.K_RETURN:
                if self.sel == 0:
                    self.selectSnd.play()
                    self.stop()
                    self.levelIntro = LevelIntro(self, 1)
                    self.levelIntro.start()
                elif self.sel == 1:
                    self.selectSnd.play()
                    self.stop()
                    self.credits = CreditsMenu(self)
                    self.credits.start()
                elif self.sel == 2:                              
                    self.selectSnd.play()
                    self.stop()
            if event.key == pygame.K_UP:
                self.sel = (self.sel - 1) % 3
                self.updateMenu()
            if event.key == pygame.K_DOWN:
                self.sel = (self.sel + 1) % 3
                self.updateMenu()

    def updateMenu(self):
        self.viewSnd.play()
        # update menu link
        if self.sel == 0:
            self.startLnk.swapView(1)
            self.creditsLnk.swapView(0)
            self.quitLnk.swapView(0)
        elif self.sel == 1:
            self.startLnk.swapView(0)
            self.creditsLnk.swapView(1)
            self.quitLnk.swapView(0)
        elif self.sel == 2:                  
            self.startLnk.swapView(0)
            self.creditsLnk.swapView(0)
            self.quitLnk.swapView(1)
            
class MenuLink(gameEngine.SuperSprite):
    def __init__(self, scene, filePattern, total, position, view):
        gameEngine.SuperSprite.__init__(self, scene)
        self.scene = scene
        self.filePattern = filePattern
        self.setPosition(position)
        self.views = {}
        for i in range(0,total + 1):
            self.preloadView(i)
        self.swapView(view)
        self.imageMaster.set_alpha(0)

    def preloadView(self, viewNum):
        self.views[viewNum] = pygame.image.load(self.filePattern % viewNum)
        self.views[viewNum] = self.views[viewNum].convert()
            
    def swapView(self, viewNum):
        self.imageMaster = self.views[viewNum]
        self.update() 
                    