#!/usr/bin/python

# fire.py : see docstring below for description of program
#
# Copyright (C) 2010  Sean McKean
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Fire demo.
See README.txt file for original source credits.
Controls --
  Press left/right mouse button to
  inflame/extinguish the area around the mouse.
  Press space key to send a blast of flame.
  Press 'c' key to clear most of the flames.
"""


import sys
import os
import pygame as pg
import numpy as np
from time import time

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if os.path.pardir not in sys.path:
    sys.path.append(os.path.pardir)
import main


black = (   0,   0,   0, 255 )
white = ( 255, 255, 255, 255 )


class Blast (object):

    def __init__(self, x, y, rec, expand_speed, max_radius):
        self.x, self.y = x, y
        self.xs, self.ys = rec.x, rec.y
        self.xe, self.ye = self.xs + rec.w, self.ys + rec.h
        self.expand_speed = expand_speed
        self.max_radius = max_radius
        self.radius = 0.0
        angle_range = np.arange(256) / 256.0 * 2.0 * np.pi
        self.x_ary = np.cos(angle_range)
        self.y_ary = np.sin(angle_range)


    def Update(self):
        self.radius += self.expand_speed
        if self.radius > self.max_radius:
            return True

        return False


    def Display(self, dst_ary):
        x_off_ary = (self.radius * self.x_ary + self.x).astype(np.int)
        y_off_ary = (self.radius * self.y_ary + self.y).astype(np.int)
        x_within = np.logical_and(x_off_ary >= self.xs, x_off_ary < self.xe)
        y_within = np.logical_and(y_off_ary >= self.ys, y_off_ary < self.ye)
        within = np.logical_and(x_within, y_within)
        inds = x_off_ary[within], y_off_ary[within]
        size = dst_ary[inds].size
        dst_ary[inds] = np.random.randint(96, 256, size)


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.preview = preview
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        pg.mouse.set_visible(True)

        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        self.rec = self.sfc.get_rect()

        # Set up output palette
        self.pal = []
        r_from, g_from, b_from = 0, 0, 0
        color_ranges = (
                (0, 0, 127, 24), (255, 0, 0, 24), (255, 255, 0, 16),
                (255, 255, 255, 64), (255, 255, 255, 128)
                )
        ind = 0
        for (r_to, g_to, b_to, rng) in color_ranges:
            for i in range(ind, ind + rng):
                factor = float(i - ind) / rng
                r = int(factor * (r_to - r_from) + r_from)
                g = int(factor * (g_to - g_from) + g_from)
                b = int(factor * (b_to - b_from) + b_from)
                self.pal.append((r, g, b))
            ind += rng
            r_from, g_from, b_from = r_to, g_to, b_to
        self.sfc.set_palette(self.pal)
        self.sfc.fill(0)

        self.image_ary = np.zeros((self.w, self.h), dtype=np.uint8)
        self.flaming = True
        self.x, self.y = None, None

        self.blasts = []

        self.start = self.displace_start = time()


    def Inflame(self, ary):
        randint = np.random.randint
        w, h = ary.shape

        # Add hot pixels from image array to output.
        areas = self.image_ary > 0
        size = self.image_ary[areas].size
        ary[areas] = randint(0, 256, size) & self.image_ary[areas]

        # Place flame above mouse if not currently extinguishing.
        if self.x is not None and self.flaming:
            x = slice(self.x - 1, self.x + 2)
            y = slice(self.y - 5, self.y - 2)
            ary[x, y] = randint(128, 256, ary[x, y].shape)

        # Display each individual blast.
        for blast in self.blasts:
            blast.Display(ary)

        # Finally, add hot pixels to bottom of output.
        for i in range(randint(0, 512)):
            x, y = randint(0, self.w), randint(self.h - 3, self.h)
            ary[x, y] = randint(0, 256)


    def DrawFrame(self):
        dst_ary = pg.surfarray.pixels2d(self.sfc)
        self.Inflame(dst_ary)

        temp_ary = dst_ary.astype(np.int16)
        # The array will be rolled (or shifted) in eight configurations,
        # totalled, averaged, and then subtracted from, to create an
        # upward-moving and decaying flame effect.
        # First, store right, middle, and left arrays.
        rolled_arrays = [
                temp_ary,
                np.roll(temp_ary, -1, axis=0),
                np.roll(temp_ary, +1, axis=0),
                ]
        # Store first sum into composite comp_ary, making sure not to
        # overwrite pixels at bottom of display.
        comp_ary = (rolled_arrays[1] + rolled_arrays[2])[..., : self.h - 2]
        # Sum the rest.
        for y in (1, 2):
            for ary in rolled_arrays:
                comp_ary += ary[..., y: self.h + y - 2]
        # Obtain an average by dividing by 8.
        comp_ary = (comp_ary >> 3)[..., : self.h - 3]
        # Store a diminished version into destination array.
        # Be sure to clip at 0.
        dst_ary[..., : self.h - 3] = np.maximum(0, comp_ary - 1)
        # Clear far left and right columns and bottom two rows to
        # control the flames.
        dst_ary[0: : self.w - 1, ...] = dst_ary[..., self.h - 2: ] = 0
        del dst_ary

        self.frames += 1

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

            x, y = pg.mouse.get_pos()
            x -= self.update_rec.x
            y -= self.update_rec.y
            if 0 <= x < self.w and 0 <= y < self.h:
                self.x, self.y = x, y
                self.flaming = True
                if pg.mouse.get_pressed()[0]:
                    # Set mouse position in image array.
                    self.image_ary[x, y] = 255
                elif pg.mouse.get_pressed()[2]:
                    # Clear a larger area around the mouse.
                    self.flaming = False
                    self.image_ary[x - 3: x + 4, y - 3: y + 4] = 0
            else:
                # Make sure the mouse is not displayed when outside
                # the bounds of the screen.
                self.x, self.y = None, None

            # Update each blast.
            i = 0
            while i < len(self.blasts):
                if self.blasts[i].Update():
                    del self.blasts[i]
                else:
                    i += 1

            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    return False
                elif evt.type == pg.KEYDOWN:
                    if evt.key == pg.K_ESCAPE:
                        return True
                    elif evt.key == pg.K_RETURN:
                        return True
                    elif evt.key == pg.K_F12:
                        if evt.mod & pg.KMOD_CTRL:
                            main.TakeSnapshot(sfc, __file__)
                    elif evt.key == pg.K_SPACE:
                        max_radius = np.random.rand() * 64.0 + 32.0
                        blast = Blast(x, y, self.rec, 1.0, max_radius)
                        self.blasts.append(blast)
                    elif evt.key == pg.K_c:
                        self.image_ary.fill(0)
                        self.blasts = []


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
