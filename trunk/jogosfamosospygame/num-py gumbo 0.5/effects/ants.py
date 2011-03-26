#!/usr/bin/python

# ants.py : see docstring below for description of program
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
Simple implementation of Langton's Ant.
Currently only models one ant type.
Controls --
 Left/Right Mouse Btn: Inc./dec. number of ants.
 Middle Mouse Up/Down: Inc./dec. board scale.
 Middle Mouse Btn: Change board type.
 Hold shift key to alter change rate.
 Arrow keys also handle board scale and type.
"""


import sys
import os
import pygame as pg
import numpy as np
from time import time

import patterns

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if os.path.pardir not in sys.path:
    sys.path.append(os.path.pardir)
import main


class AntBoard (object):

    def __init__(self, width, height, board_fnc, scale, n_ants, n_colors):
        self.w, self.h = width, height
        self.n_ants = n_ants
        self.board = board_fnc(self.w, self.h, scale)

        # Arrays holding (separately) ant x-coord, y-coord,
        # direction (u-r-d-l), and color.
        self.x_ary = np.random.randint(0, self.w, self.n_ants)
        self.y_ary = np.random.randint(0, self.h, self.n_ants)
        self.d_ary = np.random.randint(0, 4, self.n_ants)
        self.c_ary = np.arange(self.n_ants) % n_colors + 256 - n_colors


    def Update(self):
        # Change position according to direction array.
        self.y_ary[self.d_ary == 0] -= 1
        self.x_ary[self.d_ary == 1] += 1
        self.y_ary[self.d_ary == 2] += 1
        self.x_ary[self.d_ary == 3] -= 1
        # Wrap coords according to board dimensions.
        self.x_ary %= self.w
        self.y_ary %= self.h

        zero = self.board[self.x_ary, self.y_ary] == 0
        # Set 0's on board to color of ant moving onto them.
        self.board[self.x_ary[zero], self.y_ary[zero]] = self.c_ary[zero]
        # Rotate coloring ants one way.
        self.d_ary[zero] = (self.d_ary[zero] - 1) % 4
        nonzero = np.logical_not(zero)
        # Set colors on board to 0's if an ant moves onto them.
        self.board[self.x_ary[nonzero], self.y_ary[nonzero]] = 0
        # Rotate zeroing ants the opposite way.
        self.d_ary[nonzero] = (self.d_ary[nonzero] + 1) % 4


    def Display(self, dst_sfc):
        dst_ary = pg.surfarray.pixels2d(dst_sfc)
        dst_ary[...] = self.board
        del dst_ary


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.updates = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center
        self.pattern_list = [
                patterns.EmptyPattern, patterns.RandomPattern,
                patterns.AlternatingPattern, patterns.XORPattern,
                patterns.FullPattern,
                ]
        self.pat = 0
        self.scale = 3
        if preview:
            self.n_ants = 4
        else:
            name = os.path.splitext(os.path.basename(__file__))[0]
            self.n_ants = eval(self.main.settings.subsettings[name]['ants'])

        pg.mouse.set_visible(True)

        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        self.colors = 254
        ant_pal = []
        for q in range(self.colors):
            color = [ np.random.randint(128, 256) for q in range(3) ]
            ant_pal.append(color)
        self.pal = [ (0, 0, 0), (95, 95, 95) ] + ant_pal
        self.sfc.set_palette(self.pal)
        p = self.pattern_list[self.pat]
        self.ant_board = AntBoard(
                self.w, self.h, p, self.scale, self.n_ants, self.colors
                )
        self.update_time = 0.01

        self.start = self.frame_start = time()


    def ChangeBoard(self, n_ants_change, pattern_change, scale_change):
        old_n = self.n_ants
        self.n_ants = max(1, self.n_ants + n_ants_change)
        old_p = self.pat
        self.pat = (self.pat + pattern_change) % len(self.pattern_list)
        p = self.pattern_list[self.pat]
        old_s = self.scale
        self.scale = np.clip(self.scale + scale_change, 1, 256)
        if old_n != self.n_ants or old_p != self.pat or old_s != self.scale:
            self.ant_board = AntBoard(
                    self.w, self.h, p, self.scale, self.n_ants, self.colors
                    )


    def DrawFrame(self):
        t = time()
        while time() - t < self.update_time:
            self.ant_board.Update()
            self.updates += 1
        self.ant_board.Display(self.sfc)

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

            shift_down = pg.key.get_mods() & pg.KMOD_SHIFT
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
                    elif evt.key == pg.K_UP:
                        if shift_down:
                            self.ChangeBoard(0, 0, +self.scale)
                        else:
                            self.ChangeBoard(0, 0, +1)
                    elif evt.key == pg.K_DOWN:
                        if shift_down:
                            self.ChangeBoard(0, 0, -self.scale / 2)
                        else:
                            self.ChangeBoard(0, 0, -1)
                    elif evt.key == pg.K_LEFT:
                        self.ChangeBoard(0, -1, 0)
                    elif evt.key == pg.K_RIGHT:
                        self.ChangeBoard(0, +1, 0)
                elif evt.type == pg.MOUSEBUTTONDOWN:
                    if evt.button == 1:
                        if shift_down:
                            self.ChangeBoard(+8, 0, 0)
                        else:
                            self.ChangeBoard(+4, 0, 0)
                    elif evt.button == 3:
                        if shift_down:
                            self.ChangeBoard(-8, 0, 0)
                        else:
                            self.ChangeBoard(-4, 0, 0)
                    elif evt.button == 2:
                        if shift_down:
                            self.ChangeBoard(0, -1, 0)
                        else:
                            self.ChangeBoard(0, +1, 0)
                    elif evt.button == 4:
                        if shift_down:
                            self.ChangeBoard(0, 0, +self.scale)
                        else:
                            self.ChangeBoard(0, 0, +1)
                    elif evt.button == 5:
                        if shift_down:
                            self.ChangeBoard(0, 0, -self.scale / 2)
                        else:
                            self.ChangeBoard(0, 0, -1)


    def GetUpdatesPerSec(self):
        elapsed = time() - self.start
        if elapsed > 0.0:
            ups = self.updates / elapsed
            return "Average updates per second: %.2f" % ups
        else:
            return "No time has elapsed."


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetUpdatesPerSec()
