#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led_state = False

def change_led_state(gpio_number):
    global led_state

    led_state = not led_state
    GPIO.output(23, led_state)

def power_off_led(gpio_number):
    global led_state

    led_state = False
    GPIO.output(23, led_state)

if __name__ == '__main__':
    print "led and button"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Blue connected between GND and GPIO#18
    GPIO.setup(23, GPIO.OUT)                          # LED connected between GND and GPIO#23 through a 440 ohm resistor
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Red connected between GND and GPIO#24

    # Add our function to execute when the button pressed event happens
    GPIO.add_event_detect(18, GPIO.FALLING, callback=change_led_state, bouncetime=200)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=power_off_led, bouncetime=200)

    while True:
        time.sleep(0.5)
