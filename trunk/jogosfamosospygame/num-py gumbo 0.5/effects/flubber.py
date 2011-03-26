#!/usr/bin/python

# flubber.py : see docstring below for description of program
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
Flubber demo.
See README.txt file for original source and
image credits.
Press space key to alter flubber shape.
Press 't' key to toggle texture-mapping.
Click left mouse button and drag to change
flubber angle and curve.
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


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.preview = preview
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        name = os.path.splitext(os.path.basename(__file__))[0]
        if preview:
            self.spans = 4
        else:
            # Make sure mouse input is grabbed by pygame.
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)
            self.spans = eval(self.main.settings.subsettings[name]['spans'])
        draw_mode = self.main.settings.subsettings[name]['draw_mode']
        self.draw_texture = draw_mode.lower() == 'texture'
        self.img_name = self.main.settings.subsettings[name]['image']

        self.sfc = pg.Surface((self.w, self.h), 0, 32)
        self.sfc.fill(black)

        self.img_sfc = pg.image.load(self.main.GetDataPath(self.img_name))
        # Set up one-dimensional palette map, from 8-bit color to 32-bit.
        pal = self.img_sfc.get_palette()
        pal = [ self.sfc.map_rgb(q) for q in pal ]
        self.pal_map = np.array(pal, dtype=np.uint32)
        self.img_ary = pg.surfarray.array2d(self.img_sfc)
        (self.img_w, self.img_h) = self.img_ary.shape

        # Add a couple of shapes to the x and z points lists,
        # for variety.
        self.x_pt_list = []
        self.z_pt_list = []
        angle = np.arange(self.spans).astype(np.float).reshape((self.spans, 1))
        angle *= np.pi * 2.0 / self.spans
        cos, sin = np.cos(angle), np.sin(angle)
        x_ary, y_ary = np.indices((self.spans, self.h))
        w = self.w
        sin_a = np.sin((x_ary + 47 * np.cos(y_ary * 0.123)) * 0.019)
        cos_a = np.cos((y_ary + 39 * np.sin(x_ary * 0.137)) * 0.023)
        sin_b = np.sin((y_ary + 43 * np.cos(x_ary * 0.111)) * 0.014)
        cos_b = np.cos((x_ary + 31 * np.sin(y_ary * 0.147)) * 0.027)
        radx = w / 6 + w / 10 * sin_a * cos_a
        rady = w / 6 + w / 10 * sin_b * cos_b
        self.x_pt_list.append((self.w / 9.0) * cos)
        self.z_pt_list.append((self.w / 3.0) * sin)
        self.x_pt_list.append(radx * cos)
        self.z_pt_list.append(rady * sin)
        self.choice = 0

        y_ary = np.arange(self.h).reshape((1, self.h))
        self.angle_slices = np.cos(-y_ary / 193.0 * 200.0 / self.h)
        self.offset_slices = np.sin(y_ary / 59.0 * 200.0 / self.h)

        self.lmb_pressed = False
        self.mx, self.my = 0, 0

        self.start = self.displace_start = time()


    def DrawFlubber(self, dst_sfc, x_coords, y_offset):
        dst_ary = pg.surfarray.pixels2d(dst_sfc)

        x1, x2 = x_coords, np.roll(x_coords, -1, axis=0)

        if self.draw_texture:
            # Texture the flubber with the given image.
            w = float(self.img_w)
            # Loop over each y-slice...
            for y in range(self.h):
                xs = []
                # ... and loop over each span of x.
                for x in range(self.spans):
                    xa = x1[x, y]
                    xb = x2[x, y]
                    # Make sure span is facing camera and within screen.
                    if xa < xb and xa < self.w and xb >= 0:
                        fr = (x) * w / self.spans
                        to = (x + 1) * w / self.spans
                        fill = np.linspace(fr, to, xb - xa, False)
                        l = max(0, xa)
                        r = min(xb, self.w)
                        fill_l = l - xa
                        fill_r = fill.size + r - xb
                        # Get image coords.
                        img_x_ary = fill.astype(np.int32)[fill_l: fill_r]
                        img_y = (y + y_offset) % self.img_h
                        # texels holds an array of 8-bit texture pixels.
                        texels = self.img_ary[img_x_ary, img_y]
                        # Fill destination array with map colors.
                        dst_ary[l: r, y] = self.pal_map[texels]
        else:
            # Fill with gradients of green.
            for y in range(self.h):
                for x in range(self.spans):
                    xa = x1[x, y]
                    xb = x2[x, y]
                    if xa < xb and xa < self.w and xb >= 0:
                        # Gradient alternates direction between odd and
                        # even spans.
                        if x % 2 == 0:
                            fill = np.linspace(255, 64, xb - xa, False)
                        else:
                            fill = np.linspace(64, 255, xb - xa, False)
                        l = max(0, xa)
                        r = min(xb, self.w)
                        fill_l = l - xa
                        fill_r = fill.size + r - xb
                        # Give the fill gradient a green hue.
                        fill = fill.astype(np.uint32) * 0x000100
                        # Set destination span to fill.
                        dst_ary[l: r, y] = fill[fill_l: fill_r]

        del dst_ary


    def DrawFrame(self):
        if self.lmb_pressed:
            # Alter inputs with the mouse.
            rel_x, rel_y = pg.mouse.get_rel()
            self.mx += rel_x
            self.my += rel_y
            tm = self.my * 65536.0
            angle = self.mx / 64.0
        else:
            # Adjust inputs by time from start.
            tm = (time() - self.start) * 1048576.0
            cosines = np.cos(tm / 3179640.0) * self.angle_slices
            angle = 2.0 * np.pi * (cosines * np.sin(tm / 2714147.0) + 1)
            angle += tm / 1948613.0

        cos, sin = np.cos(angle), np.sin(angle)
        temp = np.cos(tm / 2945174.0)
        x_off = self.w / 2 + (self.w / 8.0) * temp * self.offset_slices

        # Set x screen coords with the help of trig functions.
        x_coords = x_off + ( self.x_pt_list[self.choice] *  cos +
                             self.z_pt_list[self.choice] * -sin )
        x_coords = x_coords.astype(np.int)

        # Scroll the texture, if any.
        y_offset = int(tm / 31456.0)

        self.sfc.fill(black)
        self.DrawFlubber(self.sfc, x_coords, y_offset)

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
                    elif evt.key == pg.K_t:
                        self.draw_texture = not self.draw_texture
                    elif evt.key == pg.K_SPACE:
                        self.choice = (self.choice + 1) % len(self.x_pt_list)
                elif evt.type == pg.MOUSEBUTTONDOWN:
                    if evt.button == 1:
                        self.lmb_pressed = True
                        self.mx, self.my = 0, 0
                        pg.mouse.get_rel()
                elif evt.type == pg.MOUSEBUTTONUP:
                    if evt.button == 1:
                        self.lmb_pressed = False


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
