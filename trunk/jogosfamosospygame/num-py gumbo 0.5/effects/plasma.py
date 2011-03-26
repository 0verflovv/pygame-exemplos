#!/usr/bin/python

# plasma.py : see docstring below for description of program
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
Plasma demo.
See README.txt file for original source credits.
Press 1-4 keys to toggle the displaying
of the four plasma arrays, or 'a'
to turn them all on.
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


def SineHypotAry(w, h, span, zoom):
    """ Creates a concentric-patterned array. """
    x_ary, y_ary = np.indices((w, h)) / zoom
    ary = (span / 2 - 1) * np.sin(np.hypot(w / 2 - x_ary, h / 2 - y_ary) / 16)

    return ary.astype(np.uint8) + span / 2


def SineCosineAry(w, h, span, zoom):
    """ Creates an array patterned by trig functions. """
    x_ary, y_ary = np.indices((w, h)) / zoom
    sin = np.sin(x_ary / (37 + 15 * np.cos(y_ary / 74)))
    cos = np.cos(y_ary / (31 + 11 * np.cos(x_ary / 57)))
    ary = (span / 2 - 1) * sin * cos

    return ary.astype(np.uint8) + span / 2


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.preview = preview
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        self.pal_ary = np.zeros((256, 3), dtype=np.float)
        self.sfc.set_palette(self.pal_ary.astype(np.uint8))
        self.sfc.fill(0)
        self.pal_ind = np.arange(256)

        self.sum_ary = np.zeros((self.w, self.h), dtype=np.uint8)

        self.plasma_a_ary = SineHypotAry(self.w * 2, self.h * 2, 128, 1.2)
        self.plasma_b_ary = SineCosineAry(self.w * 2, self.h * 2, 128, 1.2)
        self.plasma_c_ary = SineHypotAry(self.w * 2, self.h * 2, 128, 1.6)
        self.plasma_d_ary = SineCosineAry(self.w * 2, self.h * 2, 128, 1.6)
        self.disp_a = True
        self.disp_b = True
        self.disp_c = True
        self.disp_d = True

        self.start = self.displace_start = time()


    def DrawFrame(self):
        # Capture time to be used in this frame's calculations.
        tm = (time() - self.start) * 64.0

        # Alter palette with sine and cosine, and make sure it is
        # continuous from end to end.
        self.pal_ary[..., 0] = +np.cos(self.pal_ind * np.pi / 128 + tm / 74)
        self.pal_ary[..., 1] = +np.sin(self.pal_ind * np.pi / 128 + tm / 63)
        self.pal_ary[..., 2] = -np.cos(self.pal_ind * np.pi / 128 + tm / 81)
        self.pal_ary = 128 + 127 * self.pal_ary
        self.sfc.set_palette(self.pal_ary.astype(np.uint8))

        # Set offset coords of each plasma map.
        x1 = self.w / 2 + (self.w / 2 - 1) * np.cos(tm / 97)
        y1 = self.h / 2 + (self.h / 2 - 1) * np.sin(tm / 123)
        x2 = self.w / 2 + (self.w / 2 - 1) * np.sin(-tm / 114)
        y2 = self.h / 2 + (self.h / 2 - 1) * np.cos(-tm / 75)
        x3 = self.w - 1 - x1
        y3 = self.h - 1 - y1
        x4 = self.w - 1 - x2
        y4 = self.h - 1 - y2

        self.sum_ary.fill(0)

        w, h = self.w, self.h
        # Sum selected arrays into 8-bit array.
        if self.disp_a:
            self.sum_ary += self.plasma_a_ary[x1: x1 + w, y1: y1 + h]
        if self.disp_b:
            self.sum_ary += self.plasma_b_ary[x2: x2 + w, y2: y2 + h]
        if self.disp_c:
            self.sum_ary += self.plasma_c_ary[x3: x3 + w, y3: y3 + h]
        if self.disp_d:
            self.sum_ary += self.plasma_d_ary[x4: x4 + w, y4: y4 + h]

        dst_ary = pg.surfarray.pixels2d(self.sfc)
        dst_ary[...] = self.sum_ary
        del dst_ary

        self.frames += 1

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

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
                    elif evt.key == pg.K_1:
                        self.disp_a = not self.disp_a
                    elif evt.key == pg.K_2:
                        self.disp_b = not self.disp_b
                    elif evt.key == pg.K_3:
                        self.disp_c = not self.disp_c
                    elif evt.key == pg.K_4:
                        self.disp_d = not self.disp_d
                    elif evt.key == pg.K_a:
                        self.disp_a = True
                        self.disp_b = True
                        self.disp_c = True
                        self.disp_d = True


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
