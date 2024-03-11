import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
def flatten_number(num):
    while num > 9:
        num = sum(int(digit) for digit in str(num))
    return num
def convertBrightnessToFloat(b):
    analogBrightness = (b / 6) * (0.3 - 0.001) + 0.001
    return analogBrightness

def leading_significant_figure(number):
    # Convert the number to a string
    num_str = str(number)

    # Get the first character of the string (leading significant figure)
    leading_figure = int(num_str[0])

    return leading_figure

channel = AnalogIn(mcp, MCP.P0)

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for the switch and enable pull-up resistor

# 17 == white button
# 16 == red redButtonStateIsPressed
# 12 == black button

SWITCH_PINS = [24, 23,12]
for switch_pin in SWITCH_PINS:
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# SWITCH_PINS.append(12)

try:
    while True:
        # Read the state of the switch
        switch_state = {}

        for switch_pin in SWITCH_PINS:
            switch_state[switch_pin] = GPIO.input(switch_pin)

        print(switch_state)
        print('rawvalue: ',channel.value,'flattened: ', flatten_number(channel.value),"sigfig", leading_significant_figure(channel.value), "brightness", convertBrightnessToFloat(flatten_number(channel.value)))

        # Delay to avoid continuous polling
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # Clean up GPIO
    GPIO.cleanup()
