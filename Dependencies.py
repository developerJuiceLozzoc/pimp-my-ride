#include all neccessary packages to get LEDs to work with Raspberry Pi
import _rpi_ws281x
import RPi.GPIO as GPIO
import asyncio

import time
import board
import neopixel
import signal
import sys


NUMBER_LEDS = 144
PIXEL_BOARD = neopixel.NeoPixel(board.D18, NUMBER_LEDS, brightness=0.1)

def bindTransition(transition):
    print("binding stuff")
    def animateTransition():
        time.sleep(0.5)
        PIXEL_BOARD.fill((0, 0, 0))
        for color in transition:
            PIXEL_BOARD.fill(color)
            print("filling with", color)
            time.sleep(1)
        PIXEL_BOARD.fill((0, 0, 0))

    # def graceful_exit_handler(signal, frame):
    #     animateTransition()
    #     GPIO.cleanup()
    #     loop = asyncio.get_running_loop()
    #     loop.close()
    #     print("closed asyncio, exiting now")
    #     sys.exit(0)
    # Register the signal handler
    print("registering signals")
    # signal.signal(signal.SIGTERM, graceful_exit_handler)
    # signal.signal(signal.SIGINT, graceful_exit_handler)
    print("returning new animation transition")
    return animateTransition
