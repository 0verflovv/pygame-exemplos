#!/usr/bin/python

# main.py : starts full demo suite
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
from numpy.random import randint, rand
from time import time

import __main__


black = (   0,   0,   0, 255 )
white = ( 255, 255, 255, 255 )


preview_w, preview_h = 96, 96
from_intro = False


main_path = os.path.dirname(os.path.realpath(__file__))


def GetDataPath(filename):
    return os.path.join(main_path, 'data', filename)


def GetSnapPath(filename):
    return os.path.join(main_path, 'snaps', filename)


def TakeSnapshot(sfc, filename):
    """ Put a png image snapshot of the given surface in the 'snaps'
        directory. """

    name = os.path.splitext(os.path.basename(filename))[0]
    pg.image.save(sfc, GetSnapPath('%s.png' % name))


def Init(width, height, mixer):
    """ This function is called once by the main effect module that is
        running. """

    global settings, rec, mono_font, screen

    settings = Settings(os.path.join(main_path, 'settings.cfg'), mixer)
    rec = pg.Rect(0, 0, width, height)
    mono_font = GetDataPath('LiberationMono-Regular.ttf')

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.display.init()
    pg.font.init()
    if settings.mixer:
        pg.mixer.init(22050, -16, 2, 2048)
        pg.mixer.music.load(os.path.join(main_path, settings.music))

    icon = pg.image.load(GetDataPath('icon.png'))
    pg.display.set_icon(icon)
    pg.display.set_caption('demo suite')
    screen = pg.display.set_mode((width, height), 0, 32)
    screen.fill(black)
    pg.display.update()

    pg.mouse.set_visible(False)


class Settings (object):
    """ Store settings from a .cfg file for later access. """

    def __init__(self, filename, mixer):
        from ConfigParser import RawConfigParser
        config = RawConfigParser()
        config.read(filename)

        self.play_intro = config.getboolean('Main', 'play_intro')
        if mixer:
            self.mixer = config.getboolean('Main', 'mixer')
        else:
            self.mixer = False
        self.music = GetDataPath(config.get('Main', 'music'))
        self.music = os.path.expanduser(self.music)

        width = config.getint('Defaults', 'width')
        height = config.getint('Defaults', 'height')

        self.subsettings = {}
        sections = config.sections()
        for defaults in ('Main', 'Defaults'):
            sections.remove(defaults)
        for sec in sections:
            op_dict = {}
            for op in config.options(sec):
                op_dict[op] = config.get(sec, op)
                if op in ('width', 'height'):
                    op_dict[op] = eval(op_dict[op])
            for op in ('width', 'height'):
                if op not in op_dict or op_dict[op] == 0:
                    op_dict[op] = locals()[op]
            self.subsettings[sec] = op_dict


class Effect (object):
    """ Effects are derived from this class so GetAverageFPS won't have
        to be redefined repeatedly. """

    def GetAverageFPS(self):
        elapsed = time() - self.start
        if elapsed > 0.0:
            return "Average FPS: %.2f" % (self.frames / elapsed)
        else:
            return "No time has elapsed."


class Intro (Effect):
    """ Contains data for intro sequence. """

    def __init__(self, width, height):
        """ Initialize data for intro. """

        self.screen = screen
        self.w, self.h = width, height
        self.frames = 0

        self.smp_buf = 512
        self.smp_amp = 1 << 10
        if settings.mixer:
            self.chn = pg.mixer.Channel(0)
        self.volume = 0.0
        self.hi_volume = 0.0
        self.noise_len = self.smp_buf * 4

        self.font = pg.font.Font(mono_font, 24)
        self.lsz = self.font.get_linesize() * 1.5
        self.author_sfc = pg.Surface((self.w, self.h), 0, 8)
        self.author_sfc.set_palette([ black, white ])
        self.author_sfc.fill(0)
        self.author_sfc.set_colorkey(1)
        texts = ('Sean McKean', 'of', 'Gamechild Software', 'proudly presents')
        y = self.h / 2 - 2 * self.lsz
        self.author_rect = pg.Rect(0, y, self.w, 0)
        for t in texts:
            sfc = self.font.render(t, False, white)
            rect = sfc.get_rect()
            rect.centerx = self.w / 2
            rect.top = y
            y += self.lsz
            self.author_sfc.blit(sfc, rect)
        self.author_rect.h = y - self.author_rect.y

        self.grey_scale = [ (q, q, q) for q in range(256) ]
        self.trans_sfc = pg.Surface((self.w, self.h), 0, 8)
        self.trans_sfc.set_palette(self.grey_scale)
        self.trans_sfc.fill(0)
        self.trans_pos = 0.0
        self.prev_pos = 0
        self.phase = 'start'

        # static_sfc is filled with 256 shades of random noise.
        self.static_sfc = pg.Surface((self.w * 2, self.h * 2), 0, 8)
        self.static_sfc.set_palette(self.grey_scale)
        static_ary = pg.surfarray.pixels2d(self.static_sfc)
        static_ary[...] = np.random.randint(0, 256, static_ary.shape)
        del static_ary

        # alpha_sfc is utilized for screen-fading transitions.
        self.alpha_sfc = pg.Surface((self.w, self.h), 0, 32)
        self.alpha_sfc.fill(black)
        self.alpha = 0.0
        self.alpha_sfc.set_alpha(int(self.alpha))

        self.temp_sfc = self.screen.copy()
        self.temp_sfc.set_colorkey(black)
        self.temp_sfc.fill(black)

        self.start = self.displace_start = time()


    def InitTitle(self):
        """ Prepare title screen effect. """
        self.title = titlescreen.Effect(__main__, 512, 512)


    def MakeNoise(self):
        """ Create an audio sample filled with 16-bit noise and return.
            The quality of the sample is controlled by hi_volume to
            create a smooth transition. """

        amp = int(self.smp_amp * self.volume)
        rand_ary = randint(-amp, amp + 1, (self.noise_len, 2))
        rand_ary = rand_ary.astype(np.int16)
        lo_ary = rand_ary[: : 8].repeat(8, axis=0)
        fin_ary = rand_ary * self.hi_volume + lo_ary * (1.0 - self.hi_volume)
        return pg.sndarray.make_sound(fin_ary.astype(np.int16))


    def UpdateGliders(self, displace):
        """ displace is time displacement for controlling speed of the
            gliders. """

        prev, pos = self.prev_pos, int(self.trans_pos)
        h = self.author_rect.y + self.author_rect.h
        trans_ary = pg.surfarray.pixels2d(self.trans_sfc)
        x_inds = range(trans_ary.shape[0])
        pos = int(self.trans_pos)
        if self.phase != 'start':
            del x_inds[self.w - pos: pos]
        trans_ary[x_inds, : ] /= 1.0 + displace * 2.0
        trans_ary[prev: pos, self.author_rect.y: h ] = 255
        x = self.w - 1
        trans_ary[x - pos: x - prev, self.author_rect.y: h] = 255
        del trans_ary

        self.prev_pos = int(self.trans_pos)
        self.trans_pos += displace * 128.0
        if self.phase == 'start':
            if self.trans_pos >= self.w / 2:
                self.phase = 'glide fill'
        elif self.trans_pos >= self.w:
            self.trans_pos = self.author_rect.y
            self.prev_pos = self.author_rect.y
            self.trans_sfc.set_palette_at(0, white)
            self.trans_sfc.fill(0)
            self.trans_sfc.set_colorkey(1)
            self.phase = 'random fill'


    def UpdateRandomFill(self, displace):
        self.volume = min(self.volume + displace / 2.0, 1.0)
        prev, pos = self.prev_pos, int(self.trans_pos)
        trans_ary = pg.surfarray.pixels2d(self.trans_sfc)
        for y in range(max(0, min(pos - 128, prev)), min(pos, self.h)):
            factor = float(pos - y) / 128
            trans_ary[..., y] = rand(self.w) < factor
        del trans_ary

        self.prev_pos = int(self.trans_pos)
        self.trans_pos += displace * 96.0
        if self.trans_pos >= self.h + 128:
            self.phase = 'random fadein'


    def UpdateRandomFadeIn(self, displace):
        self.alpha += displace * 64.0
        if self.alpha >= 255:
            self.alpha = 255.0
        self.alpha_sfc.set_alpha(int(self.alpha))
        self.hi_volume += displace / 2.0
        if self.hi_volume >= 1.0:
            self.hi_volume = 1.0
            if self.alpha >= 255:
                self.alpha = 255
                self.phase = 'random fadeout'
                self.InitTitle()


    def UpdateRandomFadeOut(self, displace):
        self.alpha -= displace * 64.0
        if self.alpha <= 0:
            self.alpha = 0.0
        self.alpha_sfc.set_alpha(int(self.alpha))
        self.volume -= displace / 2.0
        if self.volume <= 0.0:
            self.volume = 0.0
            if self.alpha <= 0:
                self.phase = 'end'


    def Run(self):
        while True:
            self.screen.fill(black)
            # Control the output based on the phase state.
            if self.phase in ('start', 'glide fill'):
                # Segment 1: display initial text.
                self.screen.blit(self.trans_sfc, (0, 0))
                self.screen.blit(self.author_sfc, (0, 0))
            elif self.phase == 'random fill':
                # Segment 2: fill text with random static noise.
                x, y = randint(-self.w, 1), randint(-self.h, 1)
                self.screen.blit(self.static_sfc, (x, y))
                self.screen.blit(self.trans_sfc, (0, 0))
                self.screen.blit(self.author_sfc, (0, 0))
            elif self.phase == 'random fadein':
                # Segment 3: fade into filling screen with noise.
                x, y = randint(-self.w, 1), randint(-self.h, 1)
                self.alpha_sfc.blit(self.static_sfc, (x, y))
                self.screen.blit(self.alpha_sfc, (0, 0))
                self.temp_sfc.blit(self.static_sfc, (x, y))
                self.temp_sfc.blit(self.author_sfc, (0, 0))
                self.screen.blit(self.temp_sfc, (0, 0))
            elif self.phase == 'random fadeout':
                # Segment 4: fade into title screen.
                sfc = self.title.DrawFrame()
                self.screen.blit(sfc, (0, 0))
                x, y = randint(-self.w, 1), randint(-self.h, 1)
                self.alpha_sfc.blit(self.static_sfc, (x, y))
                self.screen.blit(self.alpha_sfc, (0, 0))
            elif self.phase == 'end':
                # Final segment: run title.
                if settings.mixer:
                    self.chn.stop()
                    pg.mixer.music.play(-1)
                return self.title.Run()
            pg.display.update()
            self.frames += 1

            t = time()
            span = (t - self.displace_start) * 1

            # Update data based on phase.
            if self.phase in ('start', 'glide fill'):
                self.UpdateGliders(span)
            elif self.phase == 'random fill':
                self.UpdateRandomFill(span)
            elif self.phase == 'random fadein':
                self.UpdateRandomFadeIn(span)
            elif self.phase == 'random fadeout':
                self.UpdateRandomFadeOut(span)

            self.displace_start = t

            if settings.mixer:
                self.noise = self.MakeNoise()
                self.chn.play(self.noise, -1)

            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    return False
                elif evt.type == pg.KEYDOWN:
                    if evt.key == pg.K_ESCAPE:
                        return False
                    elif evt.key == pg.K_F12:
                        if evt.mod & pg.KMOD_CTRL:
                            TakeSnapshot(self.screen, __file__)
                    elif evt.key == pg.K_RETURN:
                        self.InitTitle()
                        self.phase = 'end'
                elif evt.type == pg.MOUSEBUTTONDOWN:
                    self.InitTitle()
                    self.phase = 'end'


if __name__ == '__main__':
    mixer = '-q' not in sys.argv
    Init(512, 512, mixer)

    from effects import titlescreen

    if '-t' not in sys.argv and settings.play_intro:
        from_intro = True
        effect = Intro(512, 512).Run()
    else:
        effect = titlescreen.Effect(__main__, 512, 512)
    while effect:
        effect = effect.Run()
