#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led_state = False

def change_led_state(gpio_number):
    global led_state

    led_state = not led_state
    GPIO.output(26, led_state)

def power_off_led(gpio_number):
    global led_state

    led_state = False
    GPIO.output(26, led_state)

if __name__ == '__main__':
    print "led and button"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Blue connected between GND and GPIO#20
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Red connected between GND and GPIO#21
    GPIO.setup(26, GPIO.OUT)                          # LED connected between GND and GPIO#26 through a 440 ohm resistor

    # Add our function to execute when the button pressed event happens
    GPIO.add_event_detect(20, GPIO.FALLING, callback=change_led_state, bouncetime=200)
    GPIO.add_event_detect(21, GPIO.FALLING, callback=power_off_led, bouncetime=200)

    while True:
        time.sleep(0.5)
