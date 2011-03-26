#!/usr/bin/python

# spiral.py : see docstring below for description of program
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
Creates Archimedean spiral rendered through
changing vector lines or polygons.
Keyboard controls --
 Up/Down : Adjust rotation rate.
 Left/Right : Adjust rotation stagger.
 PageUp/PageDown : Adjust ripple rate.
 Home/End : Adjust color delta.
 Space : Toggle polygon/line mode.
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


per_len = 32.0
dis_m = 32.0
color_amp = 96.0
color_anchor = 256.0 - color_amp


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        self.pal = [ (q, q, q) for q in range(256) ]
        self.sfc.set_palette(self.pal)

        num_rotations = max(self.w, self.h) * 0.75 / dis_m
        self.d_ary = np.linspace(0.0, num_rotations, per_len * num_rotations)
        self.ary_size = self.d_ary.size
        self.x_ary = self.d_ary * dis_m * np.cos(self.d_ary * 2.0 * np.pi)
        self.y_ary = self.d_ary * dis_m * np.sin(self.d_ary * 2.0 * np.pi)
        self.dis_ary = np.hypot(
                self.x_ary - np.roll(self.x_ary, -1),
                self.y_ary - np.roll(self.y_ary, -1)
                )

        self.angle = 0.0
        self.a_delta = 0.01
        self.stagger = 0.0
        self.color_ripple_rate = 0.5
        self.color_off = 0.0
        self.color_delta = 0.5

        # Arrays holding previous values for polygon-plotting.
        self.xo_ary = self.x_ary.astype(np.int) + self.w / 2
        self.yo_ary = self.y_ary.astype(np.int) + self.h / 2

        self.press_dct = {
                pg.K_UP: 'up_pressed',        pg.K_DOWN: 'dn_pressed',
                pg.K_LEFT: 'lt_pressed',      pg.K_RIGHT: 'rt_pressed',
                pg.K_PAGEUP: 'pgup_pressed',  pg.K_PAGEDOWN: 'pgdn_pressed',
                pg.K_HOME: 'home_pressed',    pg.K_END: 'end_pressed'
                }
        for state in self.press_dct.values():
            setattr(self, state, False)

        name = os.path.splitext(os.path.basename(__file__))[0]
        op = 'draw_mode'
        if self.main.settings.subsettings[name][op].lower() == 'lines':
            self.poly_fill = False
        else:
            self.poly_fill = True

        self.start = self.displace_time = time()


    def DrawFrame(self):
        # This function is where most of the computation takes place.

        # First clear main surface (or don't, for an additionally
        #  strange effect).
        if not self.poly_fill:
            self.sfc.fill(black)

        # stag_ary becomes an array from 0 to stagger size with
        # ary_size elements.
        stag_ary = np.linspace(0.0, self.stagger, self.ary_size)
        a = self.angle / 2.0 + stag_ary
        # len holds the length of the vector, which is the result of
        # combining a few arrays in such a way as to get the 'right'
        # effect.
        len = self.d_ary * dis_m * np.cos(a) + self.dis_ary * np.sin(a)

        ang_ary = np.linspace(0.0, 1.0, self.ary_size, False)
        ang_ary = ang_ary * self.color_ripple_rate + self.color_off
        # Compute color array.
        c_ary = color_amp * np.sin(ang_ary * 2.0 * np.pi) + color_anchor

        # Compute first and second coordinate arrays of the vectors.
        xs_ary = self.x_ary.astype(np.int) + self.w / 2
        ys_ary = self.y_ary.astype(np.int) + self.h / 2
        xe_ary = xs_ary + len * np.cos(self.angle + self.d_ary * 2.0 * np.pi)
        ye_ary = ys_ary + len * np.sin(self.angle + self.d_ary * 2.0 * np.pi)

        for i in range(self.ary_size - 1):
            # The reason for doing all of the computation beforehand was
            # to simplify the line/polygon-drawing code, which helps
            # substantially in terms of speed.
            c = int(c_ary[i])
            x_start, y_start = xs_ary[i], ys_ary[i]
            x_old, y_old = self.xo_ary[i], self.yo_ary[i]
            x_end, y_end = xe_ary[i], ye_ary[i]
            if self.poly_fill:
                pts = ( (x_start, y_start), (x_old, y_old), (x_end, y_end) )
                pg.draw.polygon(self.sfc, c, pts)
            else:
                pg.draw.line(self.sfc, c, (x_start, y_start), (x_end, y_end))

        self.xo_ary[...] = xe_ary
        self.yo_ary[...] = ye_ary

        t = time()
        self.time_diff = t - self.displace_time
        self.displace_time = t
        d = self.a_delta * self.time_diff * 256.0
        self.angle = (self.angle + d) % (4.0 * np.pi)
        self.color_off += self.color_delta * self.time_diff

        self.frames += 1

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

            if self.up_pressed:
                self.a_delta += 0.002 * self.time_diff
            if self.dn_pressed:
                self.a_delta -= 0.002 * self.time_diff

            if self.lt_pressed:
                self.stagger += 1.2 * self.time_diff
            if self.rt_pressed:
                self.stagger -= 1.2 * self.time_diff

            if self.pgup_pressed:
                self.color_ripple_rate += 0.2 * self.time_diff
            if self.pgdn_pressed:
                self.color_ripple_rate -= 0.2 * self.time_diff

            if self.home_pressed:
                self.color_delta -= 0.2 * self.time_diff
            if self.end_pressed:
                self.color_delta += 0.2 * self.time_diff

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
                        self.poly_fill = not self.poly_fill
                    else:
                        for key in self.press_dct:
                            if evt.key == key:
                                setattr(self, self.press_dct[key], True)
                                break
                elif evt.type == pg.KEYUP:
                    for key in self.press_dct:
                            if evt.key == key:
                                setattr(self, self.press_dct[key], False)
                                break


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
