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

        super(ThreadMotor, self).__init__()


    def run(self):
        # battery voltage is 7.4V, max voltage for motors is 6.0V
        self.raspirobot = RRB3(7.4, 6)  # Do not call from __init__() else the library doesn't work

        while self.RqTermination == False:
            ''' read com_queue_RX '''
            com_msg = self.com_queue_RX.get(block=True, timeout=None)
            if com_msg[0] == "STOP":
                self.RqTermination = True
            elif com_msg[0] == "MOTOR_ROLL_MAGNITUDE":
                (roll, magnitude, angle) = com_msg[1]
                self.motor_run(roll, magnitude, angle)
            else:
                print "unknown msg"

        self.raspirobot.set_motors(0, 0, 0, 0)

    def motor_run(self, roll, magnitude, angle):
        # SPEED: magnitude is 0 to 1000
        motor_speed = magnitude / 300.
        if motor_speed < 0.1:
            motor_speed = 0.0
        elif motor_speed > 1.0:
            motor_speed = 1.0
        motor_speed_left = motor_speed_right = motor_speed

        # FORWARD/REVERSE: angle is negative in reverse position, else positive
        if angle >= 0:
            direction_left = 0
            direction_right = 0
        else:
            direction_left = 1
            direction_right = 1

        # DIRECTION: roll is -90 at right, +90 at left
        if roll < 0:
            motor_speed_right -= abs(roll / 90.)
        else:
            motor_speed_left  -= abs(roll / 90.)
        if motor_speed_right < 0:
            motor_speed_right = 0
        if motor_speed_left < 0:
            motor_speed_left = 0

        self.raspirobot.set_motors(motor_speed_left, direction_left, motor_speed_right, direction_right)


if __name__ == '__main__':
    rr = RRB3(7.4, 6)  # battery voltage is 7.4V, max voltage for motors is 6.0V

    print rr.get_distance()

    motor_speed = 0.6
    #rr.set_motors(motor_speed, 0, motor_speed, 0)
    #rr.forward(1, motor_speed)
    rr.right(0.5, motor_speed)

    time.sleep(2)
    rr.cleanup()

    # ThreadMotor_com_queue_TX = multiprocessing.Queue()
    # ThreadMotor_com_queue_TX.cancel_join_thread()
    # ThreadMotor_com_queue_RX = multiprocessing.Queue()
    # ThreadMotor_com_queue_RX.cancel_join_thread()
    # ThreadMotor = ThreadMotor(ThreadMotor_com_queue_RX, ThreadMotor_com_queue_TX)
    #
    # ThreadMotor.start()  # Start the thread by calling run() method
    # ThreadMotor_com_queue_RX.put(("MOTOR_ROLL_MAGNITUDE", (0, 200)))
    # time.sleep(1)
    # print "QUIT !!"
    # ThreadMotor_com_queue_RX.put(("STOP", None))
