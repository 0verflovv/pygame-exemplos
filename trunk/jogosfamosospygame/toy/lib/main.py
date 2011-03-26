""" main.py 
    test game engine
"""

import sys
from intro import *
from menumain import *
from game import *

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'main':
            mainMenu = MainMenu()
            mainMenu.start()
        else:
            level = int(sys.argv[1])
            game = Game(level)
            game.start()
    else:
        intro = Intro()
        intro.start()
        
if __name__ == "__main__":
    main()
