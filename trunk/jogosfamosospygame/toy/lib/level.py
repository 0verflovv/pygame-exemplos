""" level.py 
    game level
"""

import pygame, gameEngine
from objman import *
from objplatform import *
from objcoin import *
from objgoomba import *
from objstar import *
from objblock import *
from objpit import *
from objwarp import *

class Level():
    def __init__(self, scene, levelNum):
        self.levelNum = levelNum
        self.scene = scene
        self.reset()

    def reset(self):
        self.platforms = []
        self.coins = []
        self.goombas = []
        self.stars = []
        self.blocks = []
        self.pits = []
        self.warps = []
        self.manbounds = [0,0,0,0]

        # load the level
        file = open("data/level%d.txt" % self.levelNum, 'r')
        section = ""
       
        sectionNames = ['Man', 'Platforms', 'Coins', 'Goombas', 'Stars', 'Blocks', \
        'CoinBlocks', 'Pits', 'Warps']
       
        while 1:
            # per line
            line = file.readline()
            if line == '':
                break
            else:
                line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            doContinue = False
            for name in sectionNames:
                if line.startswith(name):
                    section = name.lower()
                    doContinue = True
                    break
            if doContinue: continue
            
            if section == "man":
               self.manbounds = self.parseBounds(line)    
            if section == "platforms":
                bounds = self.parseBounds(line)
                self.platforms.append(Platform(self.scene, bounds))
            if section == "coins":
                bounds = self.parseBounds(line)
                self.coins.append(Coin(self.scene, (bounds[0], bounds[1])))
            if section == "goombas":
                bounds = self.parseBounds(line)
                self.goombas.append(Goomba(self.scene, (bounds[0], bounds[1])))
            if section == "stars":
                bounds = self.parseBounds(line)
                self.stars.append(Star(self.scene, (bounds[0], bounds[1])))
            if section == "blocks":
                bounds = self.parseBounds(line)
                self.blocks.append(Block(self.scene, (bounds[0], bounds[1]), "norm"))
            if section == "coinblocks":
                bounds = self.parseBounds(line)
                self.blocks.append(Block(self.scene, (bounds[0], bounds[1]), "coin"))
            if section == "pits":
                bounds = self.parseBounds(line)
                self.pits.append(Pit(self.scene, bounds))
            if section == "warps":
                bounds = self.parseBounds(line)
                self.warps.append(Warp(self.scene, bounds))
                
    def prepareBounds(self, b):
        if b: return int(b.strip())
    
    def parseBounds(self, bounds):
        bounds = map(self.prepareBounds, bounds.split("px"))
        bounds.pop()
        return bounds
        
