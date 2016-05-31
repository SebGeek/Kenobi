#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from rrb3 import RRB3
import multiprocessing
from Queue import Empty

'''
https://github.com/simonmonk/raspirobotboard3
'''

class ThreadMotor(multiprocessing.Process):
    ''' Create a thread '''

    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.RqTermination = False

        self.raspirobot = RRB3(7.4, 6)  # battery voltage is 7.4V, max voltage for motors is 6.0V
        print "first", self.raspirobot
        self.raspirobot.forward(1, 0.2)

        super(ThreadMotor, self).__init__()
        self.start()  # Start the thread by calling run() method

    def run(self):
        while self.RqTermination == False:
            time.sleep(0.25)

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "MOTOR_ROLL_MAGNITUDE":
                    (roll, magnitude) = com_msg[1]
                    print (roll, magnitude)
                    self.motor_run(roll, magnitude)
                else:
                    print "unknown msg"

    def motor_run(self, roll, magnitude):
        # set both motors going forward at magnitude speed
        motor_speed = magnitude / 1000
        #self.raspirobot.set_motors(motor_speed, 0, motor_speed, 0)

        self.raspirobot.forward(1, 0.6)
        print self.raspirobot

if __name__ == '__main__':
    rr = RRB3(7.4, 6)  # battery voltage is 7.4V, max voltage for motors is 6.0V

    print rr.get_distance()

    motor_speed = 0.6
    rr.set_motors(motor_speed, 0, motor_speed, 0)
    time.sleep(2)
    #rr.forward(1, motor_speed)
    #rr.right(0.5, motor_speed)
