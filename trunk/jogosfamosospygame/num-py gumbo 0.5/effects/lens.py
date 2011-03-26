#!/usr/bin/python

# lens.py : see docstring below for description of program
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
Creates a distorting lens effect.
The mouse moves the lens when left button
is pressed.
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
from patterns import XORPattern


black     = (   0,   0,   0, 255 )
white     = ( 255, 255, 255, 255 )
lens_blue = ( 127, 191, 255, 255 )

lens_range = 128


def ConstructLensArray(x, y):
    # Called from numpy.fromfunction; creates a 2D lookup array that has
    # been distorted to make the effect look as though its center is
    # magnifying the screen.
    w, h = x.shape
    ix, iy = x - w / 2.0 + 0.5, y - h / 2.0 + 0.5
    dstn_ary = (ix ** 2 + iy ** 2) / (w / 2.0) ** 2
    distort_dstn_ary = dstn_ary ** 0.8
    distort_x = distort_dstn_ary * ix + 0.5
    distort_x = distort_x.reshape((w, h, 1)).round()
    distort_y = distort_dstn_ary * iy + 0.5
    distort_y = distort_y.reshape((w, h, 1)).round()
    color_ary = np.zeros((w, h)) + (1.0 - distort_dstn_ary) * (lens_range - 1)
    color_ary += 256 - lens_range
    color_ary = color_ary.reshape((w, h, 1))
    distort_ind_ary = np.dstack((distort_x, distort_y, color_ary))
    ind_x_ary, ind_y_ary = np.indices((w, h)).reshape((2, w, h, 1))
    color_ary = np.ones((w, h, 1))
    ind_ary = np.concatenate((ind_x_ary, ind_y_ary, color_ary), axis=2)
    in_circle = np.less(dstn_ary, 1.0)
    lt, g_eq = np.where(in_circle == True), np.where(in_circle == False)
    res = np.zeros((w, h, 3), dtype=np.int32)
    res[lt] = distort_ind_ary[lt]
    res[g_eq] = ind_ary[g_eq]

    return res


class Lens (object):

    def __init__(self, size, pos):
        (self.w, self.h) = size
        (self.x, self.y) = pos
        self.lens_ary = np.fromfunction(ConstructLensArray, (self.w, self.h))


    def GetRec(self):
        return pg.Rect(self.x, self.y, self.w, self.h)


    def SetPos(self, x, y):
        self.x, self.y = x, y


    def Update(self, x_min, x_max, y_min, y_max, start_pos, start_time):
        x_span = x_max - x_min
        y_span = y_max - y_min
        t = time() - start_time

        # Move lens x and y values directly according to start position
        # and elapsed time, to give the moving lens a consistent speed
        # regardless of framerate.
        x = int((start_pos[0] - x_min + t * 227.0) % (2 * x_span))
        y = int((start_pos[1] - y_min + t * 195.0) % (2 * y_span))

        if x > x_span:
            x = 2 * x_span - x
        self.x = x + x_min
        if self.x <= x_min:
            self.x = x_min
        elif self.x >= x_max:
            self.x = x_max
        if y > y_span:
            y = 2 * y_span - y
        self.y = y + y_min
        if self.y <= y_min:
            self.y = y_min
        elif self.y >= y_max:
            self.y = y_max


    def Display(self, sfc):
        sfc_w, sfc_h = sfc.get_size()
        x_off, y_off = 0, 0
        w, h = self.w, self.h
        if self.x < 0:
            x_off = -self.x
            w = self.w + self.x
        elif self.x >= sfc_w - self.w:
            w = sfc_w - self.x
        if self.y < 0:
            y_off = -self.y
            h = self.h + self.y
        elif self.y >= sfc_h - self.h:
            h = sfc_h - self.y

        sfc_ary = pg.surfarray.pixels2d(sfc)
        off_ary = self.lens_ary + (self.x, self.y, 0)
        off_ary = off_ary[x_off: x_off + w, y_off: y_off + h]
        off_ary = off_ary.reshape((w, h, 3))
        xs, ys, clrs = off_ary[..., 0], off_ary[..., 1], off_ary[..., 2]
        x_span = slice(max(0, self.x), min(self.x + self.w, sfc_ary.shape[0]))
        y_span = slice(max(0, self.y), min(self.y + self.h, sfc_ary.shape[1]))
        w, h = x_span.stop - x_span.start, y_span.stop - y_span.start
        sfc_ary[x_span, y_span] = sfc_ary[xs, ys].reshape(w, h) * clrs
        del sfc_ary


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        dim = min(self.w, self.h)
        size = eval(self.main.settings.subsettings['lens']['lens_size'])
        if preview:
            self.lens_size = dim * 2 / 3
        elif size == 0:
            self.lens_size = dim * 5 / 12
        elif size > min(self.w, self.h):
            self.lens_size = min(self.w, self.h)
        else:
            self.lens_size = size
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

        pattern_ary = XORPattern(self.w, self.h, 2)

        lens_pal = [
                tuple([ int(lens_blue[w] * (q / 256.0)) for w in range(3) ])
                for q in range(256 - lens_range, 256)
                ]
        self.pal = [ black, white ] + [ black ] * (256 - lens_range - 2)
        self.pal += lens_pal

        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        self.sfc.set_palette(self.pal)

        self.bg_sfc = pg.Surface((self.w, self.h), 0, 8)
        self.bg_sfc.set_palette(self.pal)
        bg_ary = pg.surfarray.pixels2d(self.bg_sfc)
        bg_ary[...] = pattern_ary
        del bg_ary

        self.sfc.blit(self.bg_sfc, (0, 0))

        self.half_w, self.half_h = self.lens_size / 2, self.lens_size / 2
        self.start_pos = (self.w / 2 - self.half_w, self.h / 2 - self.half_h)
        self.lens = Lens((self.lens_size, ) * 2, self.start_pos)
        self.rec = self.lens.GetRec()
        self.last_rec = self.rec.copy()

        self.start = self.displace_time = time()


    def DrawFrame(self):
        self.union = self.rec.union(self.last_rec)
        self.sfc.blit(self.bg_sfc, self.union.topleft, self.union)
        self.lens.Display(self.sfc)

        self.lens.Update(
                -self.half_w, self.w - self.half_w,
                -self.half_h, self.h - self.half_h,
                self.start_pos, self.displace_time
                )

        self.last_rec = self.rec
        self.rec = self.lens.GetRec()
        self.frames += 1

        return self.sfc


    def Run(self):
        self.main.screen.blit(self.sfc, self.update_rec)
        pg.display.update()
        while True:
            if pg.mouse.get_pressed()[0]:
                pg.mouse.set_visible(False)
                mx, my = pg.mouse.get_pos()
                mx = max(0, min(mx - self.update_rec.left, self.w))
                my = max(0, min(my - self.update_rec.top, self.h))
                self.lens.SetPos(mx - self.half_w, my - self.half_h)
                self.displace_time = time()
                self.rec = self.lens.GetRec()
                self.start_pos = self.rec.topleft
            else:
                pg.mouse.set_visible(True)

            sfc = self.DrawFrame()
            dst_rec = self.union.move(self.update_rec.topleft)
            self.main.screen.blit(sfc, dst_rec, self.union)
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


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
