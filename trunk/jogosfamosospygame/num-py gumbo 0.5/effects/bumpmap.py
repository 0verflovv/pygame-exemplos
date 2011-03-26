#!/usr/bin/python

# bumpmap.py : see docstring below for description of program
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
Bumpmapping demo.
See README.txt file for original source and
image credits.
The mouse affects the light source when
the left mouse button is pressed.
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


def ComputeTable(sfc):
    """ Creates a 256x256 mapping table to translate an index and a
        brightness level into a 32-bit color. """

    size = 256
    ary = np.zeros((size, size), dtype=np.uint32)
    pal_ary = np.array([ q[: 3] for q in sfc.get_palette()[: size] ])

    x_ary, y_ary = np.indices(ary.shape)
    y_ary = y_ary.reshape((ary.shape + (1, )))
    temp_ary = pal_ary.reshape((size, 1, 3)) * y_ary / (size - 1)
    r = temp_ary[..., 0] << 16
    g = temp_ary[..., 1] << 8
    b = temp_ary[..., 2]
    ary[...] = r | g | b

    return ary


def ComputeLight(size):
    """ Creates a light array of the given size. Light level will be
        between 0 and 255. """

    x_ary, y_ary = np.indices((size, size)) - size / 2.0 + 0.5
    dis_ary = np.hypot(x_ary, y_ary) * 255.0 / (size / 2.0)

    return 255 - np.clip(dis_ary, 0.0, 255.0).astype(np.uint8)


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height

        # Both img_sfc and bump_sfc should have a palette.
        name = self.main.settings.subsettings['bumpmap']['image']
        sfc = pg.image.load(main.GetDataPath(name))
        if self.w == -1:
            self.w = sfc.get_width()
        if self.h == -1:
            self.h = sfc.get_height()
        self.img_sfc = pg.transform.scale(sfc, (self.w, self.h))
        name = self.main.settings.subsettings['bumpmap']['bumpmap']
        sfc = pg.image.load(main.GetDataPath(name))
        self.bump_sfc = pg.transform.scale(sfc, (self.w, self.h))

        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        self.sfc = pg.Surface((self.w, self.h), 0, 32)
        self.sfc.fill(black)

        # Turn bumpmap surface information into an array.
        bump_ary = pg.surfarray.array2d(self.bump_sfc).astype(np.int)
        # Insert redundant information to make sure differential arrays
        # are of consistent size.
        bump_ary_x = np.insert(bump_ary, 0, bump_ary[0, ...], axis=0)
        bump_ary_y = np.insert(bump_ary, 0, bump_ary[..., 0], axis=1)
        x_ary, y_ary = np.indices((self.w, self.h))
        # Get the differential in horizontal and vertical directions.
        self.diff_x = -np.diff(bump_ary_x, axis=0) + x_ary
        self.diff_y = -np.diff(bump_ary_y, axis=1) + y_ary

        self.table = ComputeTable(self.img_sfc)

        size = eval(self.main.settings.subsettings['bumpmap']['light_size'])
        if size == 0:
            self.lt_size = np.max(bump_ary) - np.min(bump_ary)
        else:
            self.lt_size = size
        self.light = ComputeLight(self.lt_size)

        self.img_ary = pg.surfarray.array2d(self.img_sfc)

        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        self.lmb_pressed = False

        self.start = self.displace_start = time()


    def BumpMap(self, dst_sfc, src_ary, x, y):
        """ Creates bumpmap effect on given surface.
            src_ary is image array to draw from.
            x and y are light coords. """

        # 32-bit surface
        dst_ary = pg.surfarray.pixels2d(dst_sfc)

        # Make sure differential arrays are adjusted by x and y, and are
        # within light bounds.
        diff_x = np.clip(self.diff_x - x, 0, self.lt_size - 1)
        diff_y = np.clip(self.diff_y - y, 0, self.lt_size - 1)
        # Obtain light level.
        factor = self.light[diff_x, diff_y]

        # Get 32-bit pixel from table depending on source image and
        # light level, and store in destination array.
        dst_ary[...] = self.table[src_ary, factor]

        # Discard array to make sure pixel information is saved into
        # original surface.
        del dst_ary


    def DrawFrame(self):
        if not self.lmb_pressed:
            # Move x and y by trigonometric functions.
            hf_w, hf_h = self.w / 2, self.h / 2
            x = int(hf_w * np.cos(time() * 3.13)) + hf_w - self.lt_size / 2
            y = int(hf_h * np.sin(time() * 2.71)) + hf_h - self.lt_size / 2
        else:
            # Set x and y to mouse position.
            x, y = pg.mouse.get_pos()
            x = x - self.update_rec.x - self.lt_size / 2
            y = y - self.update_rec.y - self.lt_size / 2

        self.BumpMap(self.sfc, self.img_ary, x, y)

        self.frames += 1

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

            if pg.mouse.get_pressed()[0]:
                self.lmb_pressed = True
            else:
                self.lmb_pressed = False
            pg.mouse.set_visible(not self.lmb_pressed)

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


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
