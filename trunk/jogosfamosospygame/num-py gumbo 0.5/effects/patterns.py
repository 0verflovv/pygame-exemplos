# patterns.py : defines functions that return patterned arrays
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


import numpy as np


def ScaleArray(ary, w, h, scale):

    def ApplyFunc(ary, axis):
        return np.repeat(ary, scale, axis=axis)

    # Scale board in each dimension.
    ary = np.apply_over_axes(ApplyFunc, ary, (0, 1))

    # Clip to given width / height and return.
    return ary[: w, : h]


# These functions each create a 2D array consisting of 1's and 0's that
# represent the namesake's pattern.

def EmptyPattern(w, h, scale):
    return np.zeros((w, h), dtype=np.uint8)


def FullPattern(w, h, scale):
    return np.ones((w, h), dtype=np.uint8)


def RandomPattern(w, h, scale):
    min_w = w / scale + 1
    min_h = h / scale + 1
    ary = np.random.randint(0, 2, (min_w, min_h)).astype(np.uint8)

    return ScaleArray(ary, w, h, scale)


def AlternatingPattern(w, h, scale):
    min_w = w / scale + 1
    min_h = h / scale + 1
    ary = np.zeros((min_w, min_h), dtype=np.uint8)
    ary[: : 2, : : 2] = ary[1: : 2, 1: : 2] = 1

    return ScaleArray(ary, w, h, scale)


def XORPattern(w, h, scale):
    min_w = w / scale + 1
    min_h = h / scale + 1

    # The algorithm breaks down as so:
    #  xi and yi hold indices of the x- and y- coordinates along a grid
    #  starting from zero...
    xi, yi = np.indices((min_w, min_h))
    #  xor the index arrays together
    xor_ary = np.bitwise_xor(xi, yi)
    #  count the maximum number of bits to be totaled
    n_bits = int(np.ceil(np.log2(max(min_w, min_h))))
    #  define the resulting array, initially filled with zeros
    ary = np.zeros((min_w, min_h), dtype=np.uint8)
    for q in range(n_bits):
        #  sum the 'on' bits at each pattern location (works because
        #  res and ary are both ndarrays of equal dimensions)
        ary += (xor_ary >> q) & 1
    #  each location is 0 or 1 depending on an even or odd total.
    ary %= 2

    return ScaleArray(ary, w, h, scale)
