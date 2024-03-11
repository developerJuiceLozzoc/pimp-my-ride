# myscript.py
import sys
import time
from ButtonManager import bindAnimateSelection
from ColorPackage import animationFunction
from ColorPackage import colorSet
from Dependencies import PIXEL_BOARD



transition, gradient = colorSet("mainloop")
for color in transition:
    PIXEL_BOARD.fill(color)
    time.sleep(1)
PIXEL_BOARD.fill((0, 0, 0))
# i need the transition to do the startup thing

bindAnimateSelection(animationFunction)
