""" keyframe.py 
    keyframe objects
"""

import pygame, gameEngine

class Keyframe():
    """ generic keyframe"""
    def __init__(self, start=0, end=100, x1=0, x2=255):
        self.start = start            # beginning frame number
        self.end = end                # ending frame number
        self.x1 = x1                  # start value
        self.x2 = x2                  # end value
        self.frames = 0
        self.totalF = end - start - 1 # how many frames total?

    def getNextValue(self):
        value = (float(self.frames) / self.totalF * (self.x2 - self.x1)) + self.x1
        self.frames += 1
        return value

class AlphaKeyframe(Keyframe):
    """ alpha adjustment keyframe 
        sprite: SuperSprite object
        x1: integer, start alpha
        x2: integer, end alpha """
    def __init__(self, sprite, start, end, x1, x2):
        Keyframe.__init__(self, start, end, x1, x2)
        self.sprite = sprite

    def process(self):
        alpha = self.getNextValue()
        self.sprite.imageMaster.set_alpha(alpha)                        
        self.sprite.update()
        self.sprite.alpha = alpha

class SurfaceFadeKeyframe(Keyframe):
    """ fade in/out surface keyframe 
        sprite: surface object
        x1: integer, start alpha
        x2: integer, end alpha """
    def __init__(self, surface, start, end, x1, x2):
        Keyframe.__init__(self, start, end, x1, x2)
        self.surface = surface
        self.origImg = surface.copy()
        self.black = surface.copy()
        self.black.fill((0,0,0))

    def process(self):
        alpha = self.getNextValue()
        if alpha > 250:
            self.surface.blit(self.origImg, (0,0))
        else:           
            self.black.set_alpha(255 - alpha)                        
            self.surface.blit(self.origImg, (0,0))
            self.surface.blit(self.black, (0,0))

class MoveKeyframe(Keyframe):
    """ movement keyframe 
        sprite: SuperSprite object
        x1: 2-tuple of ints, start position
        x2: 2-tuple of ints, end position """
    def __init__(self, sprite, start, end, x1, x2):
        Keyframe.__init__(self, start, end, x1, x2)
        self.xKeyframe = Keyframe(start, end, x1[0], x2[0])
        self.yKeyframe = Keyframe(start, end, x1[1], x2[1])
        self.sprite = sprite

    def process(self):
        x = self.xKeyframe.getNextValue()
        y = self.yKeyframe.getNextValue()
        self.sprite.setPosition((x,y))
        self.sprite.update()

class RotoZoomKeyframe(Keyframe):
    """ rotozoom keyframe
        sprite: SuperSprite object
        x1: 2-tuple of floats, (start angle, start scale)
        x2: 2-tuple of floats, (end angle, end scale) """
    def __init__(self, sprite, start, end, x1, x2):
        Keyframe.__init__(self, start, end, x1, x2)
        self.angleKeyframe = Keyframe(start, end, x1[0], x2[0])
        self.scaleKeyframe = Keyframe(start, end, x1[1], x2[1])
        self.sprite = sprite
        self.origImg = self.sprite.imageMaster.copy()
        self.transColor = self.sprite.imageMaster.get_at((1, 1))

    def process(self):
        angle = self.angleKeyframe.getNextValue()
        scale = self.scaleKeyframe.getNextValue()
        self.sprite.imageMaster = pygame.transform.rotozoom(self.origImg, angle, scale)
        self.sprite.imageMaster.set_colorkey(self.transColor)
        self.sprite.update()  

class ResetKeyframe(Keyframe):
    # currently unused
    """ reset keyframe - reset the game scene after x frames """
    def __init__(self, scene, totalF):        
        Keyframe.__init__(self, scene.frames, totalF + scene.frames, 0, 1)                  
        self.alphaKey = Keyframe(self.start, self.end, 255, 0)
        self.scene = scene
    
    def process(self):
        alpha = self.alphaKey.getNextValue()
        scene.screen.set_alpha(alpha)
        if self.getNextValue() == 1: scene.reset(isInit=False)
            
class ManHitKeyframe(Keyframe):
    """ temporary man hit state keyframe """
    def __init__(self, man, start, end):        
        Keyframe.__init__(self, start, end, 0, 1)                  
        self.man = man

    def process(self):
        if self.getNextValue() >= 1: 
            self.man.isHit = False   
            self.man.alpha = 255
        else:
            self.man.isHit = True
            amin = 40
            if self.man.alpha != 255: self.man.alpha = 255
            else: self.man.alpha = amin

class SetStateKeyframe(Keyframe):            
    """ change state of SuperSpriteAnim"""
    def __init__(self, scene, sprite, state, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene
        self.state = state
        self.sprite = sprite

    def process(self):
        if self.getNextValue() == 0: 
            self.sprite.setState(self.state)

class AssignVarKeyframe(Keyframe):            
    """ assign a variable to another """
    def __init__(self, scene, var1, var2, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene
        self.var1 = var1
        self.var2 = var2

    def process(self):
        if self.getNextValue() == 0: 
            self.var1 = self.var2
            print "assigning var"