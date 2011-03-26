""" intro.py 
    intro engine
"""

import pygame, gameEngine
from keyframe import *
from menumain import *

class Intro(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.setCaption("Intro")
        self.bear = IntroBear(self)
        self.FRAME_OFFSET = 10   # keyframe starting offset 
        
        pygame.mixer.init(44100, -16, 2, 100)
        pygame.mixer.music.load("data/intro-bg.ogg")
        self.bearSnd = {}
        self.bearSnd['1'] = pygame.mixer.Sound("data/bear1.ogg")
        self.bearSnd['2'] = pygame.mixer.Sound("data/bear2.ogg")
        self.bearSnd['3'] = pygame.mixer.Sound("data/bear3.ogg")
        self.bearSnd['4'] = pygame.mixer.Sound("data/bear4.ogg")
        self.bearSnd['5'] = pygame.mixer.Sound("data/bear5.ogg")
        self.view = IntroView(self)
        self.text = IntroText(self)

        self.sprites = [self.bear, self.view, self.text]
        self.reset()
            
    def reset(self):
        self.frames = 0                           # current frame
        self.cycle = 0                            # sync cycle frame counter
        self.startTicks = pygame.time.get_ticks() # number of ticks since reset
        #self.background = pygame.image.load("data/level%dback.png" % self.levelNum)
        self.keyframes = []
        self.createKeys()
    
    def createKeys(self):
        # create music keyframe
        newKey = StartMusicKeyframe(self, self.getFrame(0))
        self.keyframes.append(newKey)

        # create bear keyframes
        bearStart = [0,350,563,851,1061]
        bearAudio = [0,350,560,850,1060]
        i = 0
        for frame in bearStart:
            i += 1
            newKey = SetStateKeyframe(self, self.bear, "%d" % i, self.getFrame(frame))
            self.keyframes.append(newKey)
        i = 0
        for frame in bearAudio:
            i += 1
            newKey = StartBearAudioKeyframe(self, "%d" % i, self.getFrame(frame))
            self.keyframes.append(newKey)
        
        # create view keyframes
        viewFadeIn = [[360,450], [570,670], [810,830], [856,956]]
        viewFadeOut = [[500,560], [760,780], [835,840], [1150,1230]]
        viewSwap = [0,565,785,841]

        for frames in viewFadeIn:
            newKey = AlphaKeyframe(self.view, self.getFrame(frames[0]), self.getFrame(frames[1]), 0, 255)     
            self.keyframes.append(newKey)
        for frames in viewFadeOut:
            newKey = AlphaKeyframe(self.view, self.getFrame(frames[0]), self.getFrame(frames[1]), 255, 0)     
            self.keyframes.append(newKey)
        i = 0
        for frame in viewSwap:
            i += 1
            newKey = SwapViewKeyframe(self, i, self.getFrame(frame))
            self.keyframes.append(newKey)        

        # create text keyframes
        textFadeIn = [[133,153], [260, 280], [350, 370], [500, 520], [570, 590], \
        [690, 710], [740, 770], [780, 810], [1200, 1220], [1250, 1270]]
        textFadeOut = [[240,250], [330, 340], [480, 490], [550, 560], [670, 680], \
        [725, 735], [775, 778], [860, 880], [1240, 1250], [1315, 1330]]
        textSwap = [0, 255, 345, 495, 565, 685, 736, 779, 881, 1251]

        for frames in textFadeIn:
            newKey = AlphaKeyframe(self.text, self.getFrame(frames[0]), self.getFrame(frames[1]), 0, 200)     
            self.keyframes.append(newKey)
        for frames in textFadeOut:
            newKey = AlphaKeyframe(self.text, self.getFrame(frames[0]), self.getFrame(frames[1]), 200, 0)     
            self.keyframes.append(newKey)
        i = 0
        for frame in textSwap:
            newKey = SwapTextKeyframe(self, i, self.getFrame(frame))
            self.keyframes.append(newKey)   
            i += 1
    
        # create main menu load keyframe
        newKey = LoadMenuKeyframe(self, self.getFrame(1315))
        self.keyframes.append(newKey)
    
    def getFrame(self, frame):
        mul = 4
        return (self.FRAME_OFFSET+frame)*mul
    
    def update(self):
        # handle keypresses
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
            self.stop()
            pygame.mixer.stop()
            mainMenu = MainMenu()
            mainMenu.start()  
        #print self.getFrame(self.frames), self.getFrame(800)

class IntroBear(gameEngine.SuperSpriteAnim):
    def __init__(self, scene):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.setPosition((320,400))
        rSize = (76,70)
        self.addState('0', 'data/intro-bear1.png', rSize, 1, 1, 1, 1, 'hold')
        self.addState('1', 'data/intro-bear1.png', rSize, 70, 4, 350, 5, 'hold')
        self.addState('2', 'data/intro-bear2.png', rSize, 41, 4, 210, 5, 'hold')
        self.addState('3', 'data/intro-bear3.png', rSize, 57, 4, 290, 5, 'hold')
        self.addState('4', 'data/intro-bear4.png', rSize, 41, 4, 210, 5, 'hold')
        self.addState('5', 'data/intro-bear5.png', rSize, 44, 4, 223, 5, 'hold')
        self.setState('0')

    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        pass

class IntroView(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.scene = scene
        self.views = {}
        for i in range(1,5):
            self.preloadView(i)
        self.swapView(1)

    def preloadView(self, viewNum):
        self.views[viewNum] = pygame.image.load("data/intro-view%d.png" % viewNum)
        self.views[viewNum] = self.views[viewNum].convert()
            
    def swapView(self, viewNum):
        self.imageMaster = self.views[viewNum]
        self.setPosition((320, 180))
        self.imageMaster.set_alpha(0)
        self.update()

class IntroText(gameEngine.SuperSpriteAnim):
    def __init__(self, scene):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        self.setPosition((320, 455))
        rSize = (606,36)
        self.addState('1', 'data/intro-text.png', rSize, 3, 4, 10, 999999, None)
        self.setState('1')
        self.alpha = 0
            
    def setFrame(self, frame):
        self.frame = frame
        
        
class StartMusicKeyframe(Keyframe):
    """ start the music """
    def __init__(self, scene, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene

    def process(self):
        if self.getNextValue() == 0: 
            pygame.mixer.music.play()
            pass

class StartBearAudioKeyframe(Keyframe):            
    """ start the bear audio """
    def __init__(self, scene, stateNum, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene
        self.stateNum = stateNum

    def process(self):
        if self.getNextValue() == 0: 
            self.scene.bearSnd[self.stateNum].play()
            print "starting audio: %s" % self.stateNum

class SwapViewKeyframe(Keyframe):            
    """ swap the current view image """
    def __init__(self, scene, stateNum, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene
        self.stateNum = stateNum

    def process(self):
        if self.getNextValue() == 0: 
            self.scene.view.swapView(self.stateNum)
            
class SwapTextKeyframe(Keyframe):
    """ set the text frame """
    def __init__(self, scene, frame, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene
        self.frame= frame

    def process(self):
        if self.getNextValue() == 0: 
            self.scene.text.setFrame(self.frame)

class LoadMenuKeyframe(Keyframe):
    """ load the main menu """
    def __init__(self, scene, start):        
        Keyframe.__init__(self, start, start+10, 0, 1)                  
        self.scene = scene

    def process(self):
        if self.getNextValue() == 0: 
            self.scene.stop()
            mainMenu = MainMenu()
            mainMenu.start()                                 