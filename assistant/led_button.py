#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# Button connected between GND and GPIO#18
# LED connected between GND and GPIO#23 through a 440 ohm resistor
led_state = False

# Our function on what to do when the button is pressed
def shutdown(gpio_number):
    global led_state

    # os.system("sudo shutdown -h now")
    led_state = not led_state
    GPIO.output(23, led_state)

if __name__ == '__main__':
    print "led and button"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.OUT)

    # Add our function to execute when the button pressed event happens
    GPIO.add_event_detect(18, GPIO.FALLING, callback=shutdown, bouncetime=200)

    while True:
        input_state = GPIO.input(18)
        if input_state == True:
            print "continue"
        else:
            # BUTTON PRESSED
            print "pass"
        time.sleep(0.5)
