""" objblock.py 
    breakable block object
"""

import pygame, gameEngine, random

class Block(gameEngine.SuperSpriteAnim):
    def __init__(self, scene, position, kind):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        x = position[0] + (self.rect.width /2) - 30
        y = position[1] + (self.rect.height /2) + 10
        self.setPosition((x,y))
        self.kind = kind
        if kind == 'norm':
            self.addState('idle', 'data/block-touch.png', (46,42), 1, 1, 1, 1, 'hold')
            self.addState('kill', 'data/block-die.png', (136,112), 1, 4, 6, -1, 'hold')
            self.addState('touch', 'data/block-touch.png', (46,42), 18, 4, 91, 1, 'hold')
            self.addState('untouch', 'data/block-touch.png', (46,42), 18, 4, 91, 1, 'hold', False)
        elif kind == 'coin':
            self.addState('idle', 'data/coinblock-touch.png', (46,42), 1, 1, 1, 1, 'hold')
            self.addState('kill', 'data/coinblock-die.png', (136,112), 4, 4, 25, 1, 'hold')
            self.addState('touch', 'data/coinblock-touch.png', (46,42), 4, 4, 21, 1, 'touch')
            self.addState('untouch', 'data/coinblock-touch.png', (46,42), 1, 1, 1, 1, 'hold')
        self.setState('idle')
        self.killTick = 0
        self.KILL_FRAMES = 15

    def hit(self):
        self.setState('kill')
        if self.kind == 'coin':
            snd = random.randint(0,2)
            if snd == 0:
                self.scene.coinSnd.play()
            elif snd == 1:
                self.scene.coinSnd2.play()
            elif snd == 2:
                self.scene.coinSnd3.play()
            self.scene.blockDieSnd.play()
        else:
            self.scene.blockDieSnd.play()

    def touch(self):
        self.setState('touch')

    def untouch(self):
        if self.getState() == 'touch':
            self.setState('untouch')

    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        if self.getState() == 'kill':
            self.killTick += 1
            if self.killTick > self.KILL_FRAMES: 
                self.kill()
                self.scene.level.blocks.remove(self)
            self.image.set_alpha(100)

        
