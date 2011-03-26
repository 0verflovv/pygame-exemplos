""" objgoomba.py 
    Goomba object
"""

import pygame, gameEngine, math

class Goomba(gameEngine.SuperSpriteAnim):
    def __init__(self, scene, position):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        x = position[0] + (self.rect.width /2) - 25
        y = position[1] + (self.rect.height /2) + 10
        self.setPosition((x,y))
        rSize = (52,40)
        self.addState('walkL', 'data/duck-walkL.png', rSize, 8, 4, 41, 1, None)
        self.addState('walkR', 'data/duck-walkR.png', rSize, 8, 4, 41, 1, None)
        self.addState('turnL', 'data/duck-turnL.png', rSize, 8, 4, 41, -2, 'walkL')
        self.addState('turnR', 'data/duck-turnR.png', rSize, 8, 4, 41, -2, 'walkR')
        self.addState('dieL', 'data/duck-turnR.png', rSize, 8, 4, 41, -8, 'dieR')
        self.addState('dieR', 'data/duck-turnL.png', rSize, 8, 4, 41, -8, 'dieL')
        self.setState('walkL')
        self.killTick = 0
        self.KILL_FRAMES = 25
        self.GRAVITY = 0.8
        self.gravity = 0
        self.velocity = 3
        self.moving = False 
        self.reset()

    def hit(self):
        self.die()

    def die(self):
        if self.getState() == 'walkL' or \
        self.getState() == 'turnL':
            self.setState('dieL')
        if self.getState() == 'walkR' or \
        self.getState() == 'turnR':
            self.setState('dieR')            
        self.scene.level.goombas.remove(self)
        self.scene.goombaDieSnd.play()

    def reset(self):
        self.setState('walkL')
        self.dx = -self.velocity
        self.updateVector()
        
    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        if self.getState() == 'dieL' or \
        self.getState() == 'dieR':
            self.killTick += 1
            if self.killTick > self.KILL_FRAMES: self.kill()
            self.image.set_alpha(100)
        # don't move until the player is near
        if math.fabs(self.scene.man.x - self.x) > 420:
            self.dx = 0
        else:
            if self.moving == False: 
                self.moving = True
                self.dx = -self.velocity   
                self.gravity = self.GRAVITY  
        self.updateVector()            
        self.setPosition((self.x,self.y))

    def checkPlatformCollisions(self):
        """ check collisions with platforms """
        landed = False
        for platform in self.scene.level.platforms:        
            if self.collidesWith(platform): 
                collisionSide = self.getCollisionSide(platform)
                # top or bottom hack
                if collisionSide == -1 or \
                collisionSide == 4: 
                    collisionSide = 0
                self.platformCollide(platform, collisionSide)
                if collisionSide == 0: 
                    landed = True
        if landed == False:
            self.dy += self.gravity          
        self.updateVector()        
        self.rect.center = (self.x, self.y)

    def checkGoombaCollisions(self):
        """ check collisions with goombas """
        for goomba in self.scene.level.goombas:        
            if self.collidesWith(goomba) and \
            self != goomba: 
                self.goombaCollide()

    def checkBlockCollisions(self):
        """ check collisions with blocks """
        if self.collidesGroup(self.scene.blockGroup) == False: return
        m = self.rect
        for block in self.scene.level.blocks:        
            if self.collidesWith(block): 
                collisionSide = self.getCollisionSide(block)
                self.blockCollide(block, collisionSide)
        self.updateVector()        
        self.rect.center = (self.x, self.y)

    def checkPitCollisions(self):
        """ check collisions with pits """
        if self.collidesGroup(self.scene.pitGroup) == False: return
        for pit in self.scene.level.pits:        
            if self.collidesWith(pit):                     
                self.die()
        
    def platformCollide(self, platform, collisionSide):
        """ handle a platform collision """
        p = platform.rect
        if collisionSide == 0:
            # go up
            if p.top == 0 and p.left == 0: return # wierd bug            
            self.y = p.top - (self.rect.height /2) + 1
            self.dy = 0
        elif collisionSide == 2:
            # go down
            self.y = p.bottom + (self.rect.height /2) - 1
            self.dy = 0
        elif collisionSide == 1:
            # go left
            self.x = p.left - (self.rect.width /2) + 1
            self.turnAround()
        elif collisionSide == 3:
            # go right
            self.x = p.right + (self.rect.width /2) - 1
            self.turnAround()
        elif collisionSide == 4:
            # inside the boundary
            pass

    def blockCollide(self, block, collisionSide):
        """ handle a block collision """
        p = block.rect
        if collisionSide == 0:
            # go up
            if block.getState() == "kill":
                self.die()
            else:
                self.y = p.top - (self.rect.height /2) + 1 
                self.dy = 0
        elif collisionSide == 2:
            # go down
            self.y = p.bottom + (self.rect.height /2) - 1
            self.dy = 0
            block.hit()
        elif collisionSide == 1:
            # go left
            self.x = p.left - (self.rect.width /2) + 1
            self.dx = 0
        elif collisionSide == 3:
            # go right
            self.x = p.right + (self.rect.width /2) - 1
            self.dx = 0
        elif collisionSide == 4:
            # inside the boundary
            self.y = p.top - (self.rect.height /2) + 1

    def goombaCollide(self):
        """ handle a goomba collision """
        self.turnAround()

    def turnAround(self):
        self.dx = -self.dx
        if self.getState() == 'walkL': 
            self.setState('turnR')
        elif self.getState() == 'walkR': 
            self.setState('turnL')
