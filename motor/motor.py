#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from rrb3 import *


if __name__ == '__main__':
    rr = RRB3(9, 6)
    rr.set_led1(1)
    time.sleep(2)
    rr.set_led1(0)
    time.sleep(2)
    rr.set_led2(1)
    time.sleep(2)
    rr.set_led2(0)
    time.sleep(2)
    print rr.sw1_closed()