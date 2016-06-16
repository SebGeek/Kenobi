#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import multiprocessing
from Queue import Queue, Empty

class ThreadMoveServo(multiprocessing.Process):
    ''' Create a thread '''
    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX
        self.RqTermination = False

        # servod is compiled from ServoBlaster GITHub
        # https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
        # servos must be connected on pins 35 (GPIO19) and 36 (GPIO16)
        os.system('sudo /home/pi/Kenobi/servo/servod --p1pins="35,36" > /dev/null')
        
        super(ThreadMoveServo, self).__init__()

    def run(self):
        # Go to angle=0°
        self.pan_angle_current = 0.0
        self.pan_angle_target = 0.0
        self.pan_angle_increment = 0.0
        self.tilt_angle_current = 0.0
        self.tilt_angle_target = 0.0
        self.tilt_angle_increment = 0.0

        self.period_s = 0.05

        while self.RqTermination == False:
            # Tilt
            # 0=vertical (tilt)  / 73=down (-90°) / mid=35 (0°) / 1=up (90°)
            if self.tilt_angle_current >= 0:
                tilt_dutycycle = 35.0 + ( (self.tilt_angle_current / 90.0) * (1.0 - 35.0) )
            else:
                tilt_dutycycle = 35.0 + ( (self.tilt_angle_current / 90.0) * (35.0 - 73.0) )
            os.system("echo 0=" + str(int(tilt_dutycycle)) + "% > /dev/servoblaster")

            tilt_angle_delta = self.tilt_angle_target - self.tilt_angle_current
            if abs(tilt_angle_delta) > 2:
                self.tilt_angle_current += self.tilt_angle_increment

            # Pan
            # 1=horizontal (pan) / 80=left (-90°) / mid=40 (0°) / 3=right (90°)
            if self.pan_angle_current >= 0:
                pan_dutycycle = 40.0 + ( (self.pan_angle_current / 90.0) * (3.0 - 40.0) )
            else:
                pan_dutycycle = 40.0 + ( (self.pan_angle_current / 90.0) * (40.0 - 80.0) )
            #print "pan_angle_current", self.pan_angle_current, "pan_angle_increment=", self.pan_angle_increment, "pan_angle_target=", self.pan_angle_target
            os.system("echo 1=" + str(int(pan_dutycycle)) + "% > /dev/servoblaster")

            pan_angle_delta = self.pan_angle_target - self.pan_angle_current
            if abs(pan_angle_delta) > 2:
                self.pan_angle_current += self.pan_angle_increment

            time.sleep(self.period_s)

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "SERVO_PAN":
                    (angle, duration) = com_msg[1]
                    self.pan_update(angle, duration)
                elif com_msg[0] == "SERVO_TILT":
                    (angle, duration) = com_msg[1]
                    self.tilt_update(angle, duration)
                else:
                    print "unknown msg"

        print "ThreadMoveServo: end of thread"

    def pan_update(self, angle, duration_s):
        self.pan_angle_target = float(angle)
        self.pan_angle_increment = (self.pan_angle_target - self.pan_angle_current) * (self.period_s / duration_s)

    def tilt_update(self, angle, duration_s):
        self.tilt_angle_target = float(angle)
        self.tilt_angle_increment = (self.tilt_angle_target - self.tilt_angle_current) * (self.period_s / duration_s)

'''
def change_angle(pwm, angle):
    dutycycle = ((angle / 180.0) + 1.0) * 5.0
    pwm.ChangeDutyCycle(dutycycle)
'''

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
        value = raw_input("val for angle (-90 to 90°) ?  (0 to exit)")
        
        if value == "0":
            print "stop request"
            ThreadMoveServo_com_queue_RX.put(("STOP",))
            ThreadMoveServo.join() # Wait until thread terminates
            break
        
        ThreadMoveServo_com_queue_RX.put(("SERVO_PAN", (int(value), 2.0)))
        ThreadMoveServo_com_queue_RX.put(("SERVO_TILT", (int(value), 2.0)))
