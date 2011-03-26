#!/usr/bin/python

# titlescreen.py : provides interface for selecting which demo to run
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

instruct_clr = (   0, 255, 255, 255 )
select_clr   = (   0,  63,  63, 255 )

title_str = 'Num-Py Gumbo v0.5'


class TitleText (object):
    """ Handles text that masks a scrolling background texture. """

    def __init__(self, main, string, font_size, center_pt):
        self.string = string
        self.font_size = font_size
        self.center_pt = center_pt
        self.font = pg.font.Font(main.mono_font, self.font_size)
        self.text_sfc = self.font.render(self.string, True, black)
        self.rec = self.text_sfc.get_rect()
        self.rec.center = self.center_pt
        self.w, self.h = self.rec.size
        self.alpha_ary = 255 - pg.surfarray.array_alpha(self.text_sfc)
        tmp_ary = pg.surfarray.pixels_alpha(self.text_sfc)
        tmp_ary[...] = self.alpha_ary
        del tmp_ary
        self.back_sz = 256
        half = self.back_sz / 2
        quarter_ary = np.zeros((half, half), dtype=np.uint32)
        x_ary, y_ary = np.indices((half, half)) + 256 - half
        quarter_ary += y_ary * 0x000100 + x_ary
        self.back_sfc = pg.Surface((self.back_sz, self.back_sz), 0, 32)
        back_ary = pg.surfarray.pixels2d(self.back_sfc)
        back_ary[: half, : half] = quarter_ary[: : 1, : : 1]
        back_ary[half: , : half] = quarter_ary[: :-1, : : 1]
        back_ary[: half, half: ] = quarter_ary[: : 1, : :-1]
        back_ary[half: , half: ] = quarter_ary[: :-1, : :-1]
        del back_ary
        self.final_sfc = pg.Surface((self.rec.size), 0, 32)
        self.final_sfc.set_colorkey(black)

        self.angle = np.random.rand() * 2.0 * np.pi
        self.angle_speed = 16.0
        self.x, self.y = 0.0, 0.0


    def Update(self, displace):
        mult_a = np.random.rand() * 2.0 * self.angle_speed - self.angle_speed
        self.angle = (self.angle + displace * mult_a) % (2.0 * np.pi)
        mult_x = 511.0 * np.cos(self.angle)
        mult_y = 93.0 * np.sin(self.angle)
        self.x = (self.x + displace * mult_x) % self.back_sz
        self.y = (self.y + displace * mult_y) % self.back_sz


    def Display(self, dst_sfc):
        for mult_y in range(-int(self.y), self.h, self.back_sz):
            for mult_x in range(-int(self.x), self.w, self.back_sz):
                self.final_sfc.blit(self.back_sfc, (mult_x, mult_y))
        self.final_sfc.blit(self.text_sfc, (0, 0))
        dst_sfc.blit(self.final_sfc, self.rec)


class Menu (object):
    """ A basic menu with selection methods. """

    def __init__(self, main, items, font_size, x, y, width, height):
        self.items = items
        self.font_size = font_size
        self.x, self.y = x, y
        self.w, self.h = width, height
        self.out_rec = pg.Rect(self.x, self.y, self.w, self.h)

        self.font = pg.font.Font(main.mono_font, self.font_size)
        self.line_size = self.font.get_linesize()
        self.full_h = self.line_size * len(self.items)
        self.src_rec = pg.Rect(0, 0, self.w, self.h)
        self.sel_rec = pg.Rect(0, 0, self.w, self.line_size)
        self.sel_pos = self.x, self.y

        self.def_sfc = pg.Surface((self.w, self.full_h), 0, 32)
        self.def_sfc.fill(black)
        y = 0
        for item in self.items:
            text_sfc = self.font.render(item[0], True, white, black)
            rec = text_sfc.get_rect()
            rec.midtop = (self.w / 2, y)
            self.def_sfc.blit(text_sfc, rec)
            y += self.line_size

        self.sel_sfc = pg.Surface((self.w, self.full_h), 0, 32)
        self.sel_sfc.fill(select_clr)
        y = 0
        for item in self.items:
            text_sfc = self.font.render(item[0], True, white, select_clr)
            rec = text_sfc.get_rect()
            rec.midtop = (self.w / 2, y)
            self.sel_sfc.blit(text_sfc, rec)
            y += self.line_size


    def GetSelection(self):
        return self.select


    def CollidesWith(self, p):
        return self.out_rec.collidepoint(p)


    def SelectByPoint(self, y):
        which = self.select + (y - self.sel_pos[1]) / self.line_size
        if which == -1:
            which = 0
        elif which == -2:
            which = len(self.items) - 1
        elif which == len(self.items):
            which = len(self.items) - 1
        elif which == len(self.items) + 1:
            which = 0
        else:
            which = np.clip(which, 0, len(self.items) - 1)
        return self.Select(which)


    def Select(self, select):
        self.select = select % len(self.items)
        line = self.select * self.line_size
        self.sel_pos = (self.x, self.y + self.h / 2 - self.line_size / 2)
        self.sel_rec.y = line
        self.src_rec.y = line + self.line_size / 2 - self.h / 2

        return self.items[self.select][1]


    def Display(self, dst_sfc):
        dst_sfc.fill(black, self.out_rec)
        dst_sfc.blit(self.def_sfc, self.out_rec, self.src_rec)
        dst_sfc.blit(self.sel_sfc, self.sel_pos, self.sel_rec)
        pg.draw.rect(dst_sfc, white, self.out_rec, 1)


class Emitter (object):
    """ Creates a rising steam effect. """

    def __init__(self, start, width, height, steam_width, speed, amp, alpha):
        self.start_pt = start
        self.w, self.h = width, height
        self.sw = steam_width
        self.speed = speed
        self.amp = amp
        self.alpha = alpha
        self.blend = 24
        self.angle = np.random.rand() * 2.0 * np.pi
        fill_ary = abs(((np.arange(256) + 128) % 256) - 128).astype(np.uint32)
        self.fr, self.to = self.w / 2 - self.sw / 2, self.w / 2 + self.sw / 2
        ind_ary = np.linspace(0, 256, self.sw, False).astype(np.int)
        self.layer = fill_ary[ind_ary] / self.blend * 0x010101

        self.steam_sfc = pg.Surface((self.w, self.h), 0, 32)
        self.rec = self.steam_sfc.get_rect()
        self.rec.midbottom = self.start_pt

        self.add_sfc = pg.Surface((self.w, self.h), 0, 32)
        self.add_sfc.fill(black)

        self.top_taper_sfc = pg.Surface((self.w, self.sw * 2)).convert_alpha()
        self.top_taper_sfc.fill(black)
        alpha_ary = pg.surfarray.pixels_alpha(self.top_taper_sfc)
        tmp_ary = np.indices((self.w, self.sw * 2))[1] * 255 / self.sw / 2
        alpha_ary[...] = 255 - tmp_ary
        del alpha_ary

        self.final_sfc = pg.Surface((self.w, self.h), 0, 32)
        self.final_sfc.set_alpha(self.alpha)

        self.add = 0.01 * self.speed
        self.span = 0.0


    def Update(self, displace):
        self.span += displace * 128.0
        int_span = min(int(self.span), self.h)
        self.span %= 1.0

        self.steam_sfc.blit(self.steam_sfc, (0, -int_span))

        steam_ary = pg.surfarray.pixels2d(self.steam_sfc)
        for level in range(-int_span, 0):
            steam_ary[..., level] = 0
            for b in range(-self.blend / 2, self.blend / 2 + 1):
                adjust = int(self.amp * np.sin(self.angle + b * self.add))
                slc = slice(self.fr + adjust, self.to + adjust)
                steam_ary[slc, level] += self.layer
            self.angle = (self.angle + self.add) % (2.0 * np.pi)
        del steam_ary


    def Display(self, dst_sfc):
        self.final_sfc.blit(self.steam_sfc, (0, 0))
        self.final_sfc.blit(self.top_taper_sfc, (0, 0))

        dst_sfc.blit(self.final_sfc, self.rec)


class Effect (main.Effect):
    """ Main title screen class. """

    def __init__(self, main, width, height):
        self.main = main
        self.screen = self.main.screen
        self.w, self.h = width, height
        self.mixer = self.main.settings.mixer
        self.frames = 0

        pg.key.set_repeat(160, 80)
        pg.mouse.set_visible(True)

        self.effects = [
                ("Langton's Ant",   'ants'   ),
                ("Starfield",       'stars'  ),
                ("Spiral",          'spiral' ),
                ("Distorting Lens", 'lens'   ),
                ("Plasma",          'plasma' ),
                ("Fire",            'fire'   ),
                ("Flubber",         'flubber'),
                ("Bumpmap",         'bumpmap'),
                ]
        self.effect_firsts = [ q[0][0].lower() for q in self.effects ]

        self.sfc = pg.Surface((self.w, self.h), 0, self.screen)
        self.sfc.fill(black)

        self.title = TitleText(self.main, title_str, 32, (self.w / 2, 16))

        mx, my = self.w / 2 + 24, self.h * 5 / 16
        mw, mh = self.w / 2 - 32, self.h * 9 / 32
        self.menu = Menu(self.main, self.effects, 24, mx, my, mw, mh)

        width, height = self.w / 4, self.h * 3 / 8
        start_pt = self.w / 4 + 16, height

        path = self.main.GetDataPath('bowl.png')
        self.bowl_sfc = pg.image.load(path)
        self.bowl_rec = self.bowl_sfc.get_rect()
        self.bowl_rec.midtop = start_pt
        self.preview_rec = pg.Rect(0, 0, main.preview_w, main.preview_h)
        self.preview_rec.center = self.bowl_rec.center
        self.preview_rec.move_ip(0, -8)
        self.pre_sur_rec = self.preview_rec.inflate(2, 2)

        self.emitters = [
                Emitter(start_pt, width, height, 32, 1.31, 16.0, 8),
                Emitter(start_pt, width, height, 32, 1.47, 24.0, 8),
                Emitter(start_pt, width, height, 32, 1.03, 32.0, 8),
                ]

        self.desc_sfc = pg.Surface((self.w, self.h * 11 / 32), 0, 32)
        self.desc_rec = self.desc_sfc.get_rect()
        self.desc_rec.bottom = self.h
        self.small_font = pg.font.Font(self.main.mono_font, 16)
        self.small_font_ht = self.small_font.get_linesize()

        instruct_sfcs = []
        lines = (
                'Select demo with', 'keyboard or mouse.',
                'Run selected demo by', 'pressing Enter key or',
                'clicking on picture.',
                )
        for line in lines:
            sfc = self.small_font.render(line, False, instruct_clr, black)
            instruct_sfcs.append(sfc)
        w, h = mw, self.small_font_ht * len(lines)
        self.instruct_sfc = pg.Surface((w, h), 0, 32)
        self.instruct_sfc.fill(black)
        self.instruct_rec = self.instruct_sfc.get_rect()
        self.instruct_rec.bottomleft = (mx, my - self.small_font_ht / 2)
        y = 0
        for sfc in instruct_sfcs:
            rec = sfc.get_rect()
            rec.midtop = (mw / 2, y)
            self.instruct_sfc.blit(sfc, rec)
            y += self.small_font_ht

        self.effect_name = self.menu.Select(0)
        self.old_effect = None
        self.PreviewSelected()
        self.preview_time = None
        self.preview_span = 0.25

        if self.main.settings.mixer and not self.main.from_intro:
            pg.mixer.music.play(-1)

        self.start = self.displace_start = time()


    def MakeDescriptionSfc(self, lines):
        self.desc_sfc.fill(black)
        text_sfc = self.small_font.render('Description:', False, white)
        self.desc_sfc.blit(text_sfc, (8, 0))
        y = self.small_font_ht
        for line in lines:
            text_sfc = self.small_font.render(line, False, white)
            self.desc_sfc.blit(text_sfc, (16, y))
            y += self.small_font_ht


    def PreviewSelected(self):
        if self.effect_name != self.old_effect:
            exec('import %s as effect' % self.effect_name)
            self.MakeDescriptionSfc(effect.__doc__.strip().split('\n'))
            w, h = self.main.preview_w, self.main.preview_h
            self.preview = effect.Effect(self.main, w, h, preview=True)
            self.old_effect = self.effect_name


    def RunSelected(self):
        pg.key.set_repeat()
        name = self.effect_name
        exec('import %s as effect' % name)
        w = self.main.settings.subsettings[name]['width']
        h = self.main.settings.subsettings[name]['height']
        self.effect = effect.Effect(self.main, w, h)
        self.screen.fill(black)
        pg.display.update()
        if self.effect.Run():
            # On my version of Linux/pygame, an effect that grabs input
            # will leave the mouse in an 'unclaimed' state once
            # finished, where a mouse button will need to be pressed
            # once before further clicks will be processed :(
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            pg.key.set_repeat(160, 80)
            self.displace_start = time()
            return self
        else:
            return False


    def DrawFrame(self):
        mx, my = pg.mouse.get_pos()
        for emitter in self.emitters:
            emitter.Display(self.sfc)
        self.sfc.blit(self.bowl_sfc, self.bowl_rec)
        frame = self.preview.DrawFrame()
        self.sfc.blit(frame, self.preview_rec)
        if self.preview_rec.collidepoint(mx, my):
            pg.draw.rect(self.sfc, white, self.pre_sur_rec, 1)
        self.title.Display(self.sfc)
        self.menu.Display(self.sfc)
        self.sfc.blit(self.instruct_sfc, self.instruct_rec)
        self.sfc.blit(self.desc_sfc, self.desc_rec)
        self.frames += 1

        t = time()
        span = t - self.displace_start
        for emitter in self.emitters:
            emitter.Update(span)
        self.title.Update(span)
        self.displace_start = t

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.screen.blit(sfc, (0, 0))
            pg.display.update()

            if self.preview_time is not None:
                if time() - self.preview_time > self.preview_span:
                    self.PreviewSelected()
                    self.preview_time = None

            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    return False
                elif evt.type == pg.MOUSEBUTTONDOWN:
                    if evt.button == 1:
                        if self.preview_rec.collidepoint(evt.pos):
                            return self.RunSelected()
                        elif self.menu.CollidesWith(evt.pos):
                            y = evt.pos[1]
                            self.effect_name = self.menu.SelectByPoint(y)
                            self.PreviewSelected()
                    elif evt.button == 4:
                        s = self.menu.GetSelection()
                        self.effect_name = self.menu.Select(s - 1)
                        self.preview_time = time()
                    elif evt.button == 5:
                        s = self.menu.GetSelection()
                        self.effect_name = self.menu.Select(s + 1)
                        self.preview_time = time()
                elif evt.type == pg.KEYDOWN:
                    if evt.key == pg.K_ESCAPE:
                        return False
                    elif evt.key == pg.K_F12:
                        if evt.mod & pg.KMOD_CTRL:
                            main.TakeSnapshot(sfc, __file__)
                    elif evt.key == pg.K_UP:
                        s = self.menu.GetSelection()
                        self.effect_name = self.menu.Select(s - 1)
                        self.preview_time = time()
                    elif evt.key == pg.K_DOWN:
                        s = self.menu.GetSelection()
                        self.effect_name = self.menu.Select(s + 1)
                        self.preview_time = time()
                    elif evt.key == pg.K_RETURN:
                        return self.RunSelected()
                    elif evt.unicode != '' and 32 < ord(evt.unicode) < 127:
                        s = self.menu.GetSelection()
                        first = evt.unicode.lower()
                        if first in self.effect_firsts:
                            t = (s + 1) % len(self.effects)
                            while t != s and first != self.effect_firsts[t]:
                                t = (t + 1) % len(self.effects)
                            self.effect_name = self.menu.Select(t)
                            self.preview_time = time()


if __name__ == '__main__':
    main.Init(512, 512, True)
    program = Effect(main, 512, 512)
    while program.Run():
        pass
