import RPi.GPIO as GPIO
import time
import asyncio
from ColorPackage import setBrightness
import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
potentiometer = AnalogIn(mcp, MCP.P0)
is_processing = False  # Initialize the processing flag
switch_states = {}
task = {}
SWITCH_PINS = [24, 12, 23]
BRIGHTNESS = 0 # ranges from 0 to 6
GPIO.setmode(GPIO.BCM)
for switch_pin in SWITCH_PINS:
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def leading_significant_figure(number):
    # Convert the number to a string
    num_str = str(number)

    # Get the first character of the string (leading significant figure)
    leading_figure = int(num_str[0])

    return leading_figure



def convertBrightnessToFloat(b):
    analogBrightness = (b / 6) * (0.3 - 0.001) + 0.001
    return analogBrightness


def bindAnimateSelection(animateSelection):
    debounce_pin_state = False
    def stateMachineOn(newSwitchValues):
        global task
        global BRIGHTNESS
        blackButtonStateIsPressed = not newSwitchValues[12] # probably should ignore this troublesome one
        smallWhiteButtonStateIsPressed = newSwitchValues[24]
        redButtonStateIsPressed = newSwitchValues[23]

        if blackButtonStateIsPressed:
            animateSelection("gay", blackButtonStateIsPressed)  # Fire and forget
        elif redButtonStateIsPressed:
            animateSelection("mainloop", blackButtonStateIsPressed)
        elif smallWhiteButtonStateIsPressed:
            animateSelection("babyphat", blackButtonStateIsPressed)
        else:
            return True
    def gpioMainRunLoop():
        global is_processing  # Declare is_processing as global
        global switch_states
        global BRIGHTNESS
        while True:
            for switch_pin in SWITCH_PINS:
                switch_states[switch_pin] = GPIO.input(switch_pin)

            nextBrightness = leading_significant_figure(potentiometer.value)
            if nextBrightness != BRIGHTNESS:
                BRIGHTNESS = nextBrightness
                setBrightness(convertBrightnessToFloat(BRIGHTNESS))

            if not is_processing:
                if not stateMachineOn(switch_states):
                    is_processing = True
                    start_time = time.time()


            # Check if 2 seconds have passed since the last reset
            if is_processing and (time.time() - start_time) >= 10:
                is_processing = False  # Reset processing flag

            # Delay to avoid continuous polling
            time.sleep(0.1)
    gpioMainRunLoop()
