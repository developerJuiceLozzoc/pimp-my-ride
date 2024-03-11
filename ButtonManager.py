import RPi.GPIO as GPIO
import time
import asyncio

is_processing = False  # Initialize the processing flag
switch_states = {}
task = {}
SWITCH_PINS = [24, 12, 16]



GPIO.setmode(GPIO.BCM)
for switch_pin in SWITCH_PINS:
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def bindAnimateSelection(animateSelection):
    debounce_pin_state = False
    def stateMachineOn(newSwitchValues):
        global task
        blackButtonStateIsPressed = newSwitchValues[12] # probably should ignore this troublesome one
        smallWhiteButtonStateIsPressed = newSwitchValues[24]
        redButtonStateIsPressed = newSwitchValues[16]
        # if blackButtonStateIsPressed:
        #     animateSelection("gay", blackButtonStateIsPressed)  # Fire and forget
        if redButtonStateIsPressed:
            animateSelection("mainloop", blackButtonStateIsPressed)
        elif smallWhiteButtonStateIsPressed:
            animateSelection("babyphat", blackButtonStateIsPressed)
        else:
            return True
    def gpioMainRunLoop():
        global is_processing  # Declare is_processing as global
        global switch_states
        global dumb_dpdt_states
        global debounce_pin_state

        while True:
            for switch_pin in SWITCH_PINS:
                switch_states[switch_pin] = GPIO.input(switch_pin) == GPIO.LOW
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
