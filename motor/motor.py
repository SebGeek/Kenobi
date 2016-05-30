#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from rrb3 import *

'''
https://github.com/simonmonk/raspirobotboard3
'''

if __name__ == '__main__':
    rr = RRB3(7.4, 6) # battery voltage is 7.4V, max voltage for motors is 6.0V

    print rr.get_distance()

    motor_speed = 0.6
    rr.forward(1, motor_speed)
    rr.right(0.5, motor_speed)
    rr.forward(1, motor_speed)
    rr.left(0.5, motor_speed)
    rr.forward(2, motor_speed)
    rr.right(0.5, motor_speed)
    rr.forward(2, motor_speed)
    rr.left(0.5, motor_speed)