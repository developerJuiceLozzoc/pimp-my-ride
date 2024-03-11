import sys
import time
from Dependencies import PIXEL_BOARD
from Dependencies import NUMBER_LEDS
from Dependencies import bindTransition
import asyncio




def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped



def colorSet(forArgument):
    if forArgument == "gay":
        gradient = [
            (255, 0, 0),     # Red
            (255, 127, 0),   # Orange
            (255, 255, 0),   # Yellow
            (0, 255, 0),     # Green
            (0, 0, 255),     # Blue
            (148, 0, 211)    # Violet
        ]
        transition = gradient
    elif forArgument == "mainloop":
        gradient = [
        (25, 0, 51),
        (102, 0, 102),
        (34, 0, 34),
        (75, 0, 130),
        (0, 100, 0)
        ]
        transition = [
        (63, 31, 63),
        (102, 51, 153),
        (75, 0, 130),
        (102, 0, 102)
        ]
    elif forArgument == "babyphat":
        gradient = [
        (255, 192, 203),  # Light Pink
            (255, 215, 0),    # Gold
            (255, 192, 203),  # Light Pink (Repeat for a smooth transition)
            (255, 140, 0),    # Dark Orange
            (255, 105, 180)   # Hot Pink
        ]
        transition = gradient
    else:
        print("Usage: python3 myscript.py <argument>, where argument is enumerated in documentation.")
        sys.exit(1)
    return (transition, gradient)


# brightness is a floating point number ranging from 0-1
def setBrightness(brightness):
    PIXEL_BOARD.brightness = brightness
    print("brightness", PIXEL_BOARD.brightness)

@fire_and_forget
def animationFunction(argument, voltage):
    if voltage:
        PIXEL_BOARD.brightness = 0.1
    else:
        PIXEL_BOARD.brightness = 0.05


    transition, gradient = colorSet(argument)
    grunt = bindTransition(transition)
     # first we say helllo
    PIXEL_BOARD.fill((0,0,0))
    grunt()
    PIXEL_BOARD.fill((0,0,0))

    #now we lay out the gradient for full time usage
    chunk = 0
    sectionLength = int(NUMBER_LEDS / len(gradient))
    for color in gradient:
        for i in range(sectionLength):
            try:
                PIXEL_BOARD[chunk + i] = color
                time.sleep(0.1)
            except IndexError:
                print("oops",chunk+1)
                continue
        chunk += sectionLength
