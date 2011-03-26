""" objcoin.py 
    coin object
"""

import pygame, gameEngine, random

class Coin(gameEngine.SuperSpriteAnim):
    def __init__(self, scene, position):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        x = position[0] + (self.rect.width /2) - 40
        y = position[1] + (self.rect.height /2) - 10
        self.setPosition((x,y))
        #self.imgSize = (40, 40)
        rSize = (40,40)
        self.addState('idle', 'data/coin.png', rSize, 8, 4, 40, 1, None)
        self.addState('kill', 'data/coin.png', rSize, 8, 4, 40, -8, None)
        self.setState('idle')
        self.killTick = 0
        self.KILL_FRAMES = 15

    def hit(self):
        self.setState('kill')
        snd = random.randint(0,2)
        if snd == 0:
            self.scene.coinSnd.play()
        elif snd == 1:
            self.scene.coinSnd2.play()
        elif snd == 2:
            self.scene.coinSnd3.play()

    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        if self.getState() == 'kill':
            self.killTick += 1
            if self.killTick > self.KILL_FRAMES: 
                self.kill()
                self.scene.level.coins.remove(self)
            self.image.set_alpha(100)
