#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Read one teleinfo frame and output the frame in CSV format on stdout
"""

import RPi.GPIO as GPIO
import time
import threading

class ThreadPowerLED(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.IsTerminated = False

    def stop(self):
        self.IsTerminated = True

    def run(self):
        while (self.IsTerminated != True):
            GPIO.output(PIN, ON)
            time.sleep(0.00001)
            GPIO.output(PIN, OFF)
            time.sleep(0.00001 * ratio)


PIN = 3

GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
GPIO.setup(PIN, GPIO.OUT)

ON = True
OFF = False

ratio = 0.5

ObjThreadPowerLED = ThreadPowerLED()
ObjThreadPowerLED.start()

while(ratio != -1):
    ratio_string = raw_input("valeur du ratio ? (-1 pour sortir)")
    ratio = float(ratio_string)

ObjThreadPowerLED.stop()
GPIO.cleanup()
