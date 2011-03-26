#!/usr/bin/python

# stars.py : see docstring below for description of program
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
Creates an interactive starfield effect.
Makes use of anti-aliased pixels routines.

Controls -- Left Mouse Btn: Accelerate
            Right Mouse Btn: Decelerate
            Space Key: Toggle pixels/lines
Move mouse to change viewer angle.
"""


import sys
import os
import pygame as pg
import numpy as np
from numpy.random import rand, randint
from time import time

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if os.path.pardir not in sys.path:
    sys.path.append(os.path.pardir)
import main


black = (   0,   0,   0, 255 )
white = ( 255, 255, 255, 255 )


def BelowFraction(x):
    """ Calculate fractional part of scalar or array of floats. """

    return np.modf(x)[0]


def AboveFraction(x):
    """ Calculate inverse of fractional part of scalar or array of
        floats. """

    return 1.0 - np.modf(x)[0]


def DrawPixels(dst_sfc, x_ary, y_ary, levels):
    """ Draws basic pixel information to given pygame surface.
        dst_sfc: Surface to draw onto.
        x_ary, y_ary: Two numpy.ndarrays that give the x and y coordinates
            of each pixel to render. Coords can be floating-points.
        levels: A numpy array of values from 0.0 to 1.0, giving the
            brightness level of each pixel. """

    # Get brightness values from levels, between 0 and 255.
    bright_ary = np.maximum(0.0, np.minimum(levels, 1.0)) * 255.0
    bright_ary = bright_ary.astype(np.uint8)
    # Get integer values for coordinates.
    x_int = x_ary.astype(int)
    y_int = y_ary.astype(int)
    # srt_ord set to hold indices of brightness array in sorted order.
    srt_ord = np.argsort(bright_ary)

    # Get 2-dimensional array of surface pixel information.
    dst_ary = pg.surfarray.pixels2d(dst_sfc)
    # Set surface pixels sorted from darkest to brightest values.
    dst_ary[x_int[srt_ord], y_int[srt_ord]] = bright_ary[srt_ord]
    # Delete temporary array to finish changes to surface.
    del dst_ary


def DrawPixelQuads(dst_sfc, x_ary, y_ary, levels):
    """ Draws anti-aliased pixel quads to given pygame surface.
        dst_sfc: Surface to draw onto.
        x_ary, y_ary: Two numpy.ndarrays that give the x and y coordinates
            of each pixel quad to render. Coords can be floating-points.
        levels: A numpy array of values from 0.0 to 1.0, giving the
            brightness level of each pixel. One value per quad needed. """

    bright_ary = np.maximum(0.0, np.minimum(levels, 1.0)) * 255.0
    bright_ary = bright_ary.astype(np.uint8)

    # Hold an x/y coord array for each corner of every pixel quad.
    fx, cx = np.floor(x_ary), np.ceil(x_ary)
    fy, cy = np.floor(y_ary), np.ceil(y_ary)
    # Join x/y arrays, to be rendered in one go.
    x_all = np.concatenate((fx, fx, cx, cx)).astype(int)
    y_all = np.concatenate((fy, cy, fy, cy)).astype(int)
    # Each of the four inner arrays in c_ary holds a corner fraction of
    # each of the pixel quads to draw.
    c_ary = np.array( [
        (AboveFraction(x_ary) + AboveFraction(y_ary)) / 2.0,
        (AboveFraction(x_ary) + BelowFraction(y_ary)) / 2.0,
        (BelowFraction(x_ary) + AboveFraction(y_ary)) / 2.0,
        (BelowFraction(x_ary) + BelowFraction(y_ary)) / 2.0,
        ] )
    # Multiply each fraction by the corresponding brightness level and
    # concatenate values, clipping to 8-bit integers.
    c_ary = np.concatenate((c_ary * bright_ary).astype(np.uint8))
    srt_ord = np.argsort(c_ary)

    dst_ary = pg.surfarray.pixels2d(dst_sfc)
    dst_ary[x_all[srt_ord], y_all[srt_ord]] = c_ary[srt_ord]
    del dst_ary


class Starfield (object):
    """ Sets values for arrays of star information based on given
        constraints. """

    def __init__(self, width, height, min_z, max_z, min_st_z, n_stars):
        """ Initialize constraints and arrays. """

        # Set star-field constraints as given through function arguments.
        self.w, self.h, self.d = width, height, max_z - min_z
        self.n_stars = n_stars
        self.min_x, self.max_x = -float(self.w / 2), float(self.w / 2)
        self.min_y, self.max_y = -float(self.h / 2), float(self.h / 2)
        self.min_z, self.max_z = float(min_z), float(max_z)
        self.min_st_z = float(min_st_z)

        # Initialize four velocity/position arrays to correct size,
        # filled with zeros (floating points).
        for ary_name in ('vel_ary', 'x_ary', 'y_ary', 'z_ary'):
            setattr(self, ary_name, np.zeros(n_stars, dtype=float))

        # Make sure all elements of z_ary are beyond sight so that the
        # whole array is initialized to random values in the call to
        # ResetPastStars().
        #self.z_ary += min_z - 1.0
        self.ResetPastStars(True)


    def ResetPastStars(self, reset_all=False):
        """ All stars past beyond sight are reset to random values. """

        if reset_all == True:
            # Initial reset, all star-field arrays will be randomized.
            size = self.z_ary.size
            indices = np.arange(size)
        else:
            # Get array indices of all cases where z_ary < min_z.
            indices = np.nonzero(self.z_ary < self.min_z)
            size = indices[0].size
        # Set x, y, and z arrays as well as star velocities to
        # constrained random values.
        self.vel_ary[indices] = (0.1 + 9.9 * rand(size)) ** -1.5
        if size > 0:
            # Update velocity square-root values if needed.
            self.vel_sqrt_ary = np.sqrt(self.vel_ary)
        self.x_ary[indices] = self.min_x + rand(size) * self.w
        self.y_ary[indices] = self.min_y + rand(size) * self.h
        if reset_all == True:
            # Star z-values are sort of evenly distributed ahead and
            # behind camera.
            self.z_ary[indices] = self.min_z + rand(size) * self.d
        else:
            # Place new stars ahead.
            self.z_ary[indices] = rand(size) * (self.max_z - self.min_st_z)
            self.z_ary[indices] += self.min_st_z

        # Indices of reset stars might be useful in the future,
        # so return here.
        return indices


    def RotateX(self, x_amt):
        """ Calculate and set roll rotation.
            x_amt is angle in radians to rotate stars. """

        # numpy's universal functions are helpful in making these
        # calculations go smoothly.
        tan2_ary = np.arctan2(self.y_ary, self.x_ary)
        dist_ary = np.hypot(self.x_ary, self.y_ary)
        angle_inc = x_amt / 256.0
        self.x_ary = dist_ary * np.cos(tan2_ary + angle_inc)
        self.y_ary = dist_ary * np.sin(tan2_ary + angle_inc)


class Effect (main.Effect):

    def __init__(self, main, width, height, preview=False):
        self.main = main
        self.w, self.h = width, height
        self.frames = 0
        self.update_rec = pg.Rect(0, 0, self.w, self.h)
        self.update_rec.center = self.main.rec.center

        self.cx, self.cy = self.w / 2, self.h / 2
        self.draw_method = DrawPixelQuads
        name = os.path.splitext(os.path.basename(__file__))[0]
        op = 'draw_mode'
        if self.main.settings.subsettings[name][op].lower() == 'lines':
            self.show_star_lines = True
        else:
            self.show_star_lines = False
        if preview:
            self.n_stars = 512
        else:
            self.n_stars = eval(self.main.settings.subsettings[name]['stars'])
            # The next five calls make sure the star-field is facing in
            # the right direction to start with.
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
            pg.mouse.set_pos((0, 0))
            pg.event.pump()
            pg.mouse.get_rel()
        self.sfc = pg.Surface((self.w, self.h), 0, 8)
        # Set the display palette to a basic black-grey-white scheme.
        self.pal = [ (q, q, q) for q in range(256) ]
        self.sfc.set_palette(self.pal)

        z = 4.0 * self.h
        self.s = Starfield(self.w, self.w, -z, z, z * 3 / 4, self.n_stars)
        # Old x/y arrays of values for drawing star-lines.
        # Set to infinite amounts at first to draw stars and not lines
        # until one frame has passed.
        self.old_x = np.zeros(self.n_stars, dtype=float) + np.inf
        self.old_y = np.zeros(self.n_stars, dtype=float) + np.inf
        self.zoom = self.cx * 1.5
        speed = eval(self.main.settings.subsettings[name]['speed'])
        self.cam_speed = max(1.0, min(float(speed), 32768.0))
        self.max_star_len = self.w / 10
        self.mxr = 0
        self.myr = 0
        self.pitch_ang = 0.0

        self.start = self.displace_start = time()


    def ExtendLines(self, x, y, ox, oy, b):
        """ Calculate and return pixels of extended lines based on given
            arrays.
            x, y: New arrays of screen x/y coordinates.
            ox, oy: Old arrays. Lines will be attempted from x/y to ox/oy.
            b: Brightness level of each coord. """

        # Get absolute difference between old and new arrays.
        abs_dx = abs(ox - x).astype(int) + 1
        abs_dy = abs(oy - y).astype(int) + 1
        # Get maximum of previous two arrays at each element.
        abs_max_d = np.maximum(abs_dx, abs_dy)
        # Cap maximums to a safe value, to conserve computer time and
        # memory, and not be overly sluggish; this limits the length of
        # each star line, though.
        sizes = np.minimum(self.max_star_len, abs_max_d)
        # Initialize return arrays to correct size totals.
        ret_x, ret_y, ret_b = (np.zeros(np.sum(sizes)) for q in range(3))

        # Compute interpolated x- and y-coords and store line
        # information in return arrays.
        # Brightness level of each line is uniform.
        i = 0
        for q in range(sizes.size):
            cap = sizes[q]
            s = slice(i, i + cap)
            ret_x[s] = np.linspace(x[q], ox[q], abs_max_d[q], True)[: cap]
            ret_y[s] = np.linspace(y[q], oy[q], abs_max_d[q], True)[: cap]
            ret_b[s] = np.zeros(cap) + b[q]
            i += cap

        return ret_x, ret_y, ret_b


    def DrawFrame(self):
        # Start with a blank screen each frame.
        self.sfc.fill(black)

        # t is the time taken since the last frame, and won't go
        # above approximately 40 milliseconds.
        self.t = min(0.04, time() - self.displace_start)
        copy_z = np.copy(self.s.z_ary)
        # Change the distance of each star from camera based on
        # speed, time past, and the relative velocity of each star.
        self.s.z_ary -= self.cam_speed * self.t * self.s.vel_ary
        self.displace_start = time()

        # Reset all stars that have "disappeared". If star-lines are
        # being drawn, the old x/y values at these indices are
        # reset, to keep lines from being drawn for one frame
        # (prevents a major slowdown).
        indices = self.s.ResetPastStars()
        if self.show_star_lines:
            self.old_x[indices] = self.old_y[indices] = np.inf

        # Calculate rotated coord arrays based on camera pitch angle.
        cos_ang, sin_ang = np.cos(self.pitch_ang), np.sin(self.pitch_ang)
        rx_ary = self.s.x_ary
        ry_ary = self.s.y_ary * cos_ang + self.s.z_ary * sin_ang
        rz_ary = self.s.z_ary * cos_ang - self.s.y_ary * sin_ang

        # Draw stars that appear ahead of the camera.
        prep = rz_ary > 0.0
        rx, ry, rz = rx_ary[prep], ry_ary[prep], rz_ary[prep]
        # Get x and y screen coordinates.
        x = self.cx + rx / rz * self.zoom
        y = self.cy + ry / rz * self.zoom
        # Get bright amount for visible stars.
        # Multiply by the square-root of the relative star velocity
        # for a nice depth-effect.
        b = (2.0 - rz / self.w) * self.s.vel_sqrt_ary[prep]

        if self.show_star_lines:
            # Find stars that are crossing front to back.
            diff = np.logical_and(self.s.z_ary <= 0.0, copy_z > 0.0)
            ox, oy = self.old_x[prep], self.old_y[prep]
            # Set old screen coords to current coords here.
            self.old_x[prep] = x
            self.old_y[prep] = y
            if np.pi / 2.0 < self.pitch_ang < np.pi * 7.0 / 6.0:
                # A fix for a weird effect that makes the lines draw
                # incorrectly if the camera angle is pointed
                # backward a certain amount.
                x[diff[prep]] = -x[diff[prep]]
                y[diff[prep]] = -y[diff[prep]]
                ox[diff[prep]] = -ox[diff[prep]]
                oy[diff[prep]] = -oy[diff[prep]]
            # Make sure old x/y screen coords are within screen.
            x_in = np.logical_and(ox > 1, ox < self.w - 1)
            y_in = np.logical_and(oy > 1, oy < self.h - 1)
            inside = np.logical_and(x_in, y_in)
            # Test if x or y coords are different enough to justify
            # drawing a line.
            test = np.logical_or(abs(x - ox) > 2.0, abs(y - oy) > 2.0)
            a = np.nonzero(np.logical_and(inside, test))
            # Get the line pixels and add them to the arrays of star
            # pixels to draw.
            lines = self.ExtendLines(x[a], y[a], ox[a], oy[a], b[a])
            ax = np.concatenate((x[inside], lines[0]))
            ay = np.concatenate((y[inside], lines[1]))
            ab = np.concatenate((b[inside], lines[2]))
        else:
            ax = x
            ay = y
            ab = b

        x_in = np.logical_and(ax > 1, ax < self.w - 2)
        y_in = np.logical_and(ay > 1, ay < self.h - 2)
        draw = np.nonzero(np.logical_and(x_in, y_in))

        # Call appropriate draw method on screen with given arrays.
        self.draw_method(self.sfc, ax[draw], ay[draw], ab[draw])

        self.frames += 1

        return self.sfc


    def Run(self):
        while True:
            sfc = self.DrawFrame()
            self.main.screen.blit(sfc, self.update_rec)
            pg.display.update(self.update_rec)

            self.mxr, self.myr = pg.mouse.get_rel()
            if self.show_star_lines and self.mxr != 0 or self.myr != 0:
                # If rotating camera, stop drawing lines for a frame.
                self.old_x[...] = self.old_y[...] = np.inf
            if self.mxr != 0:
                self.s.RotateX(-self.mxr)
            self.pitch_ang -= self.myr * 0.01
            # Keep pitch angle between 0 and 2 * pi radians
            self.pitch_ang %= 2.0 * np.pi

            # Left and right mouse buttons speed up and slow down camera
            # speed.
            self.mb = pg.mouse.get_pressed()
            if self.mb[0]:
                # Cap to max and min speeds, and accelerate according to
                # time past.
                self.cam_speed = min(32768.0, self.cam_speed * (1.0 + self.t))
            if self.mb[2]:
                self.cam_speed = max(1.0, self.cam_speed / (1.0 + self.t))

            # Event handling loop.
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
                        self.show_star_lines = not self.show_star_lines
                        if not self.show_star_lines:
                            self.old_x[...] = self.old_y[...] = np.inf


if __name__ == '__main__':
    main.Init(512, 512, False)
    name = os.path.splitext(os.path.basename(__file__))[0]
    w = main.settings.subsettings[name]['width']
    h = main.settings.subsettings[name]['height']
    program = Effect(main, w, h)
    program.Run()
    print program.GetAverageFPS()
