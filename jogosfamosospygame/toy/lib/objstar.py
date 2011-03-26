""" objstar.py 
    star object
"""

import pygame, gameEngine

class Star(gameEngine.SuperSpriteAnim):
    def __init__(self, scene, position):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        x = position[0] + (self.rect.width /2) - 40
        y = position[1] + (self.rect.height /2) - 10
        self.setPosition((x,y))
        rSize = (50,48)
        self.addState('idle', 'data/star.png', rSize, 12, 4, 61, 1, None)
        self.addState('kill', 'data/star.png', rSize, 12, 4, 61, -8, None)
        #self.addState('idle', 'data/rock.png', (46,42), 1, 1, 1, 1, 'hold')
        #self.addState('kill', 'data/rock-die.png', (136,112), 1, 4, 6, 1, 'hold')
        self.setState('idle')
        self.killTick = 0
        self.KILL_FRAMES = 15

    def hit(self):
        self.setState('kill')
        self.scene.starSnd.play()

    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        if self.getState() == 'kill':
            self.killTick += 1
            if self.killTick > self.KILL_FRAMES: 
                self.kill()
                self.scene.level.stars.remove(self)
            self.image.set_alpha(100)
