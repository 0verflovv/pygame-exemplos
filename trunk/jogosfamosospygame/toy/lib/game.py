""" game.py 
    test game engine
"""

import pygame, gameEngine, menucredits
from objman import *
from level import *
from menupause import *
from keyframe import *

class Game(gameEngine.Scene):
    def __init__(self, levelNum, prevScene=0):
        gameEngine.Scene.__init__(self)
        self.setCaption("Game")
        self.prevScene = prevScene
        self.level = Level(self, levelNum)
        self.levelNum = levelNum
        pygame.mixer.init(44100, -16, 2, 100)
        self.loadSounds()
        self.bg0 = pygame.image.load("data/level%dbg0.png" % levelNum)
        self.bg1 = pygame.image.load("data/level%dbg1.png" % levelNum)
        self.fg0 = pygame.image.load("data/level%dfg0.png" % levelNum)
        self.bg0offset = [0,0]
        self.gravity = 0.75
        self.levelNum = levelNum
        self.man = Man(self)
        self.sprites = [self.man]
        self.reset(isInit=True)

    def playMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("data/level%d.ogg" % self.levelNum)
        pygame.mixer.music.play(-1)
    
    def loadSounds(self):
        self.jumpSnd = pygame.mixer.Sound("data/jump.ogg")
        self.jumpSnd.set_volume(0.3)
        self.runSnd = pygame.mixer.Sound("data/run.ogg")
        self.runSnd.set_volume(0.2)
        self.damageSnd = pygame.mixer.Sound("data/damage.ogg")
        self.damageSnd.set_volume(0.3)
        self.dieSnd = pygame.mixer.Sound("data/die.ogg")
        self.dieSnd.set_volume(0.3)
        self.goombaDieSnd = pygame.mixer.Sound("data/goombadie.ogg")
        self.goombaDieSnd.set_volume(0.3)
        self.blockDieSnd = pygame.mixer.Sound("data/blockdie.ogg")
        self.blockDieSnd.set_volume(0.3)
        self.coinSnd = pygame.mixer.Sound("data/coin.ogg")
        self.coinSnd.set_volume(0.2)
        self.coinSnd2 = pygame.mixer.Sound("data/coin2.ogg")
        self.coinSnd2.set_volume(0.2)
        self.coinSnd3 = pygame.mixer.Sound("data/coin3.ogg")
        self.coinSnd3.set_volume(0.2)
        self.starSnd = pygame.mixer.Sound("data/star.ogg")
        self.starSnd.set_volume(0.3)
        self.warpSnd = pygame.mixer.Sound("data/warp.ogg")
        self.warpSnd.set_volume(0.5)
            
    def initSpriteGroups(self):
        self.coinGroup = ()
        self.platformGroup = ()
        self.goombaGroup = ()
        self.starGroup = ()
        self.blockGroup = ()
        self.pitGroup = ()
        self.warpGroup = ()
    
    def createSpriteGroups(self, isInit):
        if isInit == True: self.initSpriteGroups()
        self.coinGroup = self.createSpriteGroup(self.coinGroup, self.level.coins, isInit)
        self.platformGroup = self.createSpriteGroup(self.platformGroup, self.level.platforms, isInit)
        self.goombaGroup = self.createSpriteGroup(self.goombaGroup, self.level.goombas, isInit)
        self.starGroup = self.createSpriteGroup(self.starGroup, self.level.stars, isInit)
        self.blockGroup = self.createSpriteGroup(self.blockGroup, self.level.blocks, isInit)
        self.pitGroup = self.createSpriteGroup(self.pitGroup, self.level.pits, isInit)
        self.warpGroup = self.createSpriteGroup(self.warpGroup, self.level.warps, isInit)

    def createSpriteGroup(self, spriteGroup, spriteList, isInit):
        if isInit == False: spriteGroup.empty()
        spriteGroup = self.makeSpriteGroup(spriteList)
        self.addGroup(spriteGroup)
        return spriteGroup
            
    def reset(self, isInit):
        self.playMusic()
        self.frames = 0          # current frame
        self.deathStartFrame = 0 # frame where death animation began
        self.background = pygame.image.load("data/level%dback.png" % self.levelNum)
        self.bg0offset = [0,0]
        if isInit == False: self.level.reset()
        self.man.setPosition((self.level.manbounds[0], self.level.manbounds[3]))            
        self.createSpriteGroups(isInit)
        self.man.reset()
        self.keyframes = []
        fadeInKey = SurfaceFadeKeyframe(self.background, 0, 20, 0, 255)        
        self.keyframes.append(fadeInKey)
    
    def update(self):
        self.checkManCollisions()
        self.checkGoombaCollisions()   
        # handle player drag
        self.man.doDrag()
        # handle keypresses
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_ESCAPE]:
            self.stop()   
            if self.prevScene:        
                self.prevScene.start()
        if keys[pygame.K_RETURN]:
            self.pause()           
        if keys[pygame.K_DELETE]:
            pass                
        if keys[pygame.K_SPACE]:
            self.man.handleJump()
        if keys[pygame.K_LEFT]:
            self.man.handleLeft()
        elif keys[pygame.K_RIGHT]:
            self.man.handleRight()
        else: 
            self.man.handleNoInput()
        #add force of gravity
        if self.man.isJumping == True:
            self.man.dy += self.gravity
        self.man.updateVector()        
        self.shiftSprites()
        self.updateDeath()
        #print self.clock.get_fps()

    def shiftSprites(self):
        # adjust camera to get player centered on screen
        manX = self.screen.get_width() / 2
        manY = self.screen.get_height() / 2 + 100
        # the main character)
        shiftX = self.man.x - manX 
        shiftY = self.man.y - manY 
        self.man.setPosition([manX, manY])
        # shift other sprites    
        self.shiftSpriteList(self.level.platforms, shiftX, shiftY)
        self.shiftSpriteList(self.level.coins, shiftX, shiftY)
        self.shiftSpriteList(self.level.goombas, shiftX, shiftY)
        self.shiftSpriteList(self.level.stars, shiftX, shiftY)
        self.shiftSpriteList(self.level.blocks, shiftX, shiftY)
        self.shiftSpriteList(self.level.pits, shiftX, shiftY)
        self.shiftSpriteList(self.level.warps, shiftX, shiftY)
        # shift bg0
        self.bg0offset = [self.bg0offset[0] - shiftX, self.bg0offset[1] - shiftY]

    def shiftSpriteList(self, spriteList, shiftX, shiftY):
        for sprite in spriteList:
            sprite.x -= shiftX
            sprite.y -= shiftY
    
    def checkManCollisions(self):
        self.man.checkPlatformCollisions()
        self.man.checkCoinCollisions()
        self.man.checkGoombaCollisions()
        self.man.checkStarCollisions()
        self.man.checkBlockCollisions()
        self.man.checkPitCollisions()
        self.man.checkWarpCollisions()        

    def checkGoombaCollisions(self):
        for goomba in self.level.goombas:       
            goomba.checkPlatformCollisions()
            goomba.checkBlockCollisions()
            goomba.checkGoombaCollisions()
            goomba.checkPitCollisions()

    def debug(self):
        print "----------------------------------------------------------------"
        print "bg0offset: %s" % self.bg0offset
        
        print "man === x: %d, y: %d, top: %d, bottom: %d, left: %d, right: %d" % \
        (self.man.x, self.man.y, self.man.rect.top, self.man.rect.bottom, \
        self.man.rect.left, self.man.rect.right)
        print "        dx: %d, dy: %d, width: %d, height: %d, isJumping: %s" % \
        (self.man.dx, self.man.dy, self.man.rect.width, self.man.rect.height,\
        self.man.isJumping)
        print self.clock.get_fps()
        """
        print "platform === x: %d, y: %d, top: %d, bottom: %d, left: %d, right: %d" % \
        (self.platform.x, self.platform.y, self.platform.rect.top, self.platform.rect.bottom, \
        self.platform.rect.left, self.platform.rect.right)
        print "        dx: %d, dy: %d, width: %d, height: %d" % \
        (self.platform.dx, self.platform.dy, self.platform.rect.width, self.platform.rect.height)
        """
        
    def pause(self):
        prevScr = self.screen.copy()
        self.pauseMenu = PauseMenu(self, prevScr)
        self.stop()
        self.pauseMenu.start()      
    
    def startDeath(self):
        if self.deathStartFrame <= 0: 
            self.deathStartFrame = self.frames
            self.man.die()
            fadeOutKey = SurfaceFadeKeyframe(self.background, self.frames, self.frames + 20, 255, 0)        
            self.keyframes.append(fadeOutKey)
            pygame.mixer.music.stop()
            self.dieSnd.play()

    def updateDeath(self):
        if self.deathStartFrame != 0 and \
        self.frames - self.deathStartFrame > 86:
            self.reset(isInit=False)

    def nextLevel(self):             
        self.stop()
        if self.levelNum < 2: 
            self.game = Game(self.levelNum+1, self.prevScene)
            self.game.warpSnd.play()
            self.game.start()   
        else:
            self.runSnd.stop()
            self.credits = menucredits.CreditsMenu(self.prevScene)
            self.credits.start()