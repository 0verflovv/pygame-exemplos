""" objman.py 
    man object
"""

import pygame, gameEngine, keyframe

class Man(gameEngine.SuperSpriteAnim):
    def __init__(self, scene):
        gameEngine.SuperSpriteAnim.__init__(self, scene)
        self.scene = scene
        #self.imgSize = (66, 114)
        rSize = (66,114)
        self.addState('idleL', 'data/idleL.png', rSize, 8, 4, 41, 1, None)
        self.addState('idleR', 'data/idleR.png', rSize, 8, 4, 41, 1, None)
        self.addState('walkL', 'data/walkL.png', rSize, 6, 4, 31, 1, None)
        self.addState('walkR', 'data/walkR.png', rSize, 6, 4, 31, 1, None)
        self.addState('turnL', 'data/turnL.png', rSize, 4, 4, 15, 1, 'walkL')
        self.addState('turnR', 'data/turnR.png', rSize, 4, 4, 15, 1, 'walkR')
        self.addState('runL', 'data/runL.png', rSize, 5, 4, 29, 2, None)
        self.addState('runR', 'data/runR.png', rSize, 5, 4, 29, 2, None)
        self.addState('jumpL', 'data/jumpL.png', rSize, 4, 4, 23, 2, 'idleL')
        self.addState('jumpR', 'data/jumpR.png', rSize, 4, 4, 23, 2, 'idleR')
        self.addState('deathL', 'data/deathL.png', (114,108), 8, 4, 43, 2, 'hold')
        self.addState('deathR', 'data/deathR.png', (114,108), 8, 4, 43, 2, 'hold')
        self.isJumping = True
        self.isHit = False         # is the user is a hit state?
        self.runSndPlaying = False # is the running sound playing?
        self.hitCount = 0          # number of times man has been hit 
        self.alpha = 255           # global alpha setting
        self.AIR_DRAG = 0.1
        self.GROUND_DRAG = 0.8
        self.JUMP_VEL = 10
        self.JUMP_HOLD_VEL = 0.5   # bigger numbers = longer hold
        self.MAX_JUMP_VEL = 20
        self.WALK_VEL = 1
        self.MAX_WALK_VEL = 10
        self.RUN_THRESH = 8
        self.MAX_HITS = 2          # maximum number of times man can be hit
        self.reset()

    def reset(self):
        self.setState('idleR')
        self.hitCount = 0
        self.isHit = False
        self.alpha = 255

    def update(self):
        gameEngine.SuperSpriteAnim.update(self)
        # make sure man's feet touch the ground
        self.rect.inflate_ip(0,-1)
        # play the running sound if needed
        if self.getState() == 'runL' or \
        self.getState() == 'runR':
            if self.runSndPlaying == False:
                self.runSndPlaying = True
                self.scene.runSnd.play(-1)
        else:
            if self.runSndPlaying == True:
                self.runSndPlaying = False
                self.scene.runSnd.stop()

    def jump(self):
        if self.isJumping == False:
            self.dy = -self.JUMP_VEL
            self.y -= 10
            self.isJumping = True
            self.scene.jumpSnd.play()
        elif self.isJumping == True and self.dy < 0:
            self.dy -= self.JUMP_HOLD_VEL             

    def hit(self):
        if self.isHit == False:
            self.isHit = True
            self.hitCount += 1
            if (self.hitCount >= self.MAX_HITS):
                self.scene.startDeath()
            else:
                hitKeyframe = keyframe.ManHitKeyframe(self, self.scene.frames, self.scene.frames + 100)
                self.scene.keyframes.append(hitKeyframe)
                self.scene.damageSnd.play()
    
    def die(self):
        if self.getState() == 'idleL' or \
        self.getState() == 'walkL'or \
        self.getState() == 'runL' or \
        self.getState() == 'jumpL' or \
        self.getState() == 'turnL': self.setState('deathL')
        if self.getState() == 'idleR' or \
        self.getState() == 'walkR'or \
        self.getState() == 'runR' or \
        self.getState() == 'jumpR' or \
        self.getState() == 'turnR': self.setState('deathR')
    
    def doDrag(self):
        drag = 0
        if self.isJumping == True: 
            drag = self.AIR_DRAG
        else:
            drag = self.GROUND_DRAG

        if self.dx > drag:
            self.dx -= drag       
        elif self.dx < -drag:     
            self.dx += drag       
        else:
            self.dx = 0
     
    def handleLeft(self):
        if self.getState() == 'idleL': self.setState('walkL')
        elif self.getState() == 'idleR': self.setState('idleL')
        elif self.getState() == 'walkR': self.setState('turnL')
        elif self.getState() == 'walkL' and self.dx < -self.RUN_THRESH:
            self.setState('runL')
        elif self.getState() == 'runR': self.setState('turnL')
        elif self.getState() == 'jumpR': self.setState('jumpL')
        if self.getState() != 'deathL' and \
            self.getState() != 'deathR':
            if self.dx > -self.MAX_WALK_VEL:
                self.dx -= self.WALK_VEL
        
    def handleRight(self):   
        if self.getState() == 'idleR': self.setState('walkR')
        elif self.getState() == 'idleL': self.setState('idleR')
        elif self.getState() == 'walkL': self.setState('turnR')
        elif self.getState() == 'walkR' and self.dx > self.RUN_THRESH:
            self.setState('runR')
        elif self.getState() == 'runL': self.setState('turnR')
        elif self.getState() == 'jumpL': self.setState('jumpR')
        if self.getState() != 'deathL' and \
            self.getState() != 'deathR':
            if self.dx < self.MAX_WALK_VEL:
                self.dx += self.WALK_VEL
          
    def handleNoInput(self):        
        if self.getState() == 'walkL': self.setState('idleL')
        elif self.getState() == 'walkR': self.setState('idleR')
        elif self.getState() == 'runL': self.setState('idleL')
        elif self.getState() == 'runR': self.setState('idleR')
        elif self.getState() == 'jumpL': self.setState('idleL')
        elif self.getState() == 'jumpR': self.setState('idleR')

    def handleJump(self):
        if self.getState() == 'idleL' or \
        self.getState() == 'turnL' or \
        self.getState() == 'walkL' or \
        self.getState() == 'runL':
            self.setState('jumpL')
        if self.getState() == 'idleR' or \
        self.getState() == 'turnR' or \
        self.getState() == 'walkR' or \
        self.getState() == 'runR':
            self.setState('jumpR')
        self.jump()

    def checkPlatformCollisions(self):
        """ check collisions with platforms """
        if self.collidesGroup(self.scene.platformGroup) == False: return
        m = self.rect
        self.isJumping = True
        for platform in self.scene.level.platforms:        
            if self.collidesWith(platform): 
                collisionSide = self.getCollisionSide(platform)
                self.platformCollide(platform, collisionSide)
        if (self.y >= self.scene.screen.get_height() - 50) and \
        self.scene.frames > 100:
            # man hit bottom of screen
            self.scene.startDeath()
        self.updateVector()        
        self.rect.center = (self.x, self.y)

    def checkCoinCollisions(self):
        """ check collisions with coins """
        if self.collidesGroup(self.scene.coinGroup) == False: return
        for coin in self.scene.level.coins:        
            if self.collidesWith(coin):                     
                coin.hit()

    def checkGoombaCollisions(self):
        """ check collisions with goombas """
        if self.collidesGroup(self.scene.goombaGroup) == False: return
        for goomba in self.scene.level.goombas:        
            if goomba.getState() == 'die': continue
            if self.collidesWith(goomba):                     
                collisionSide = self.getCollisionSide(goomba)
                if (collisionSide == 0): 
                    goomba.hit()
                    self.isJumping = False
                    self.handleJump()
                else:
                    self.hit()

    def checkStarCollisions(self):
        """ check collisions with stars """
        if self.collidesGroup(self.scene.starGroup) == False: return
        for star in self.scene.level.stars:        
            if self.collidesWith(star):                     
                star.hit()

    def checkBlockCollisions(self):
        """ check collisions with blocks """
        if self.collidesGroup(self.scene.blockGroup) == False: return
        m = self.rect
        for block in self.scene.level.blocks:        
            if self.collidesWith(block): 
                collisionSide = self.getCollisionSide(block)
                self.blockCollide(block, collisionSide)
            else:
                block.untouch()
        self.updateVector()        
        self.rect.center = (self.x, self.y)

    def checkPitCollisions(self):
        """ check collisions with pits """
        if self.collidesGroup(self.scene.pitGroup) == False: return
        for pit in self.scene.level.pits:        
            if self.collidesWith(pit):                     
                self.scene.startDeath()

    def checkWarpCollisions(self):
        """ check collisions with warp """
        if self.collidesGroup(self.scene.warpGroup) == False: return
        for warp in self.scene.level.warps:        
            if self.collidesWith(warp):                     
                self.scene.nextLevel()
        
    def platformCollide(self, platform, collisionSide):
        """ handle a platform collision """
        p = platform.rect
        if collisionSide == 0:
            # go up
            self.y = p.top - (self.rect.height /2) + 1
            self.dy = 0
            self.isJumping = False
        elif collisionSide == 2:
            # go down
            self.y = p.bottom + (self.rect.height /2) - 1
            self.dy = 0
            self.isJumping = True
        elif collisionSide == 1:
            # go left
            self.x = p.left - (self.rect.width /2) + 1
            self.dx = 0
            self.isJumping = True
        elif collisionSide == 3:
            # go right
            self.x = p.right + (self.rect.width /2) - 1
            self.dx = 0
            self.isJumping = True
        elif collisionSide == 4:
            # inside the boundary
            #self.y = p.bottom + (self.rect.height /2)
            self.isJumping = True        

    def blockCollide(self, block, collisionSide):
        """ handle a block collision """
        p = block.rect
        if collisionSide == 0:
            # go up
            self.y = p.top - (self.rect.height /2) 
            self.dy = 0
            self.isJumping = False
            block.touch()
        elif collisionSide == 2:
            # go down
            self.y = p.bottom + (self.rect.height /2) - 1
            self.dy = 0
            self.isJumping = True
            block.hit()
        elif collisionSide == 1:
            # go left
            self.x = p.left - (self.rect.width /2) + 1
            self.dx = 0
            self.isJumping = True
        elif collisionSide == 3:
            # go right
            self.x = p.right + (self.rect.width /2) - 1
            self.dx = 0
            self.isJumping = True
        elif collisionSide == 4:
            # inside the boundary
            self.isJumping = True        



        