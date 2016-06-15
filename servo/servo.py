#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import multiprocessing
from Queue import Queue, Empty

class ThreadMoveServo(multiprocessing.Process):
    ''' Create a thread '''
    def __init__(self, com_queue_RX, com_queue_TX, val=8, up=False, speed=0.01):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX
        self.RqTermination = False

        self.update(val, up, speed)

        # servod is compiled from ServoBlaster GITHub
        # https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
        # servos must be connected on pins 35 (GPIO19) and 36 (GPIO16)
        os.system('sudo /home/pi/Kenobi/servo/servod --p1pins="35,36" > /dev/null')
        
        super(ThreadMoveServo, self).__init__()
    
    def update(self, val=None, up=None, speed=None):
        if val != None:
            self.val = val
        if up != None:
            self.up = up
        if speed != None:
            self.speed = speed
    
    def run(self):
        while self.RqTermination == False:
            # 0=vertical   / 73=down / mid=35 / 1=up
            # 1=horizontal / 3=right / mid=40 / 80=left
            os.system("echo 0=" + str(self.val) + "% > /dev/servoblaster")
            time.sleep(0.2)

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=True, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "UPDATE":
                    (val, up, speed) = com_msg[1]
                    self.update(val, up, speed)
                else:
                    print "unknown msg"

def change_angle(pwm, angle):
    dutycycle = ((angle / 180.0) + 1.0) * 5.0
    pwm.ChangeDutyCycle(dutycycle)

if __name__ == '__main__':
    '''
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    # PWM on port GPIO_pin at 50 Hertz (20ms)
    pwm_vertical = GPIO.PWM(19, 50)
    pwm_horizontal = GPIO.PWM(16, 50)
    dutycycle = ((90 / 180.0) + 1.0) * 5.0
    pwm_vertical.start(dutycycle)
    pwm_horizontal.start(dutycycle)

    while True:
        angle = raw_input("pwm_vertical: angle ?")
        change_angle(pwm_vertical, int(angle))
        time.sleep(1)

    pwm_vertical.stop()
    pwm_horizontal.stop()
    GPIO.cleanup()
    '''

    ThreadMoveServo_com_queue_TX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_TX.cancel_join_thread()
    ThreadMoveServo_com_queue_RX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_RX.cancel_join_thread()

    ThreadMoveServo = ThreadMoveServo(ThreadMoveServo_com_queue_RX, ThreadMoveServo_com_queue_TX)
    ThreadMoveServo.start()
    
    while True:
        value = raw_input("val ? (in sec - 0 to exit)")
        
        if value == "0":
            print "stop request"
            ThreadMoveServo_com_queue_RX.put(("STOP",))
            ThreadMoveServo.join() # Wait until thread terminates
            break
        
        ThreadMoveServo_com_queue_RX.put(("UPDATE", (int(value), None, None)))
