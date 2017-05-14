#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import multiprocessing
from Queue import Queue, Empty

# This library is not used by Kenobi (use the RasPiRobot board, See motor.py)

TRIG = 23 # GPIO number
ECHO = 24 # GPIO number

class ThreadMeasureDistance(multiprocessing.Process):
    ''' Create a thread '''
    def __init__(self, com_queue_RX, com_queue_TX, period = 2):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.period = period
        self.RqTermination = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)

        super(ThreadMeasureDistance, self).__init__()

    def run(self):
        while self.RqTermination == False:
            send_trig = time.time()

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
                if pulse_start - send_trig > 1:
                    break

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150 # en cm

                if distance > 50:
                    break

            self.com_queue_TX.put(("DISTANCE", distance), block=False)

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    #print "ThreadMeasureDistance: receive stop request"
                    self.RqTermination = True
                    break
                elif com_msg[0] == "UPDATE":
                    (self.period) = com_msg[1]
                else:
                    print "unknown msg"

            time.sleep(self.period)

        # End of thread
        GPIO.cleanup()


if __name__=='__main__':
    ThreadMeasureDistance_com_queue_TX = multiprocessing.Queue()
    ThreadMeasureDistance_com_queue_TX.cancel_join_thread()
    ThreadMeasureDistance_com_queue_RX = multiprocessing.Queue()
    ThreadMeasureDistance_com_queue_RX.cancel_join_thread()

    ThreadMeasureDistance = ThreadMeasureDistance(ThreadMeasureDistance_com_queue_RX, ThreadMeasureDistance_com_queue_TX)
    ThreadMeasureDistance.start()

    while True:
        speed = raw_input("read distance - 0 to exit")

        if speed == "0":
            break

        ''' read com_queue_TX '''
        try:
            com_msg = ThreadMeasureDistance_com_queue_TX.get(block=True, timeout=None)
        except Empty:
            # No msg received
            pass
        else:
            if com_msg[0] == "DISTANCE":
                print "Distance:", com_msg[1], "cm"
            else:
                print "unknown msg"

    ThreadMeasureDistance_com_queue_RX.put(("STOP",))
    #print "Wait until thread terminates"
    ThreadMeasureDistance.join()
