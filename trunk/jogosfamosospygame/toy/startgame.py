# Nice data/lib separation code
# Idea from: Pixelman (http://pymike.aftermatheffect.com/games

import sys
import os

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)

import lib
lib.main.main()
