#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    print "led and button"

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.OUT)

    while True:
        input_state = GPIO.input(18)
        if input_state == True:
            GPIO.output(23, False)
            print "continue"
        else:
            GPIO.output(23, True)
            print "pass"
        time.sleep(0.5)
