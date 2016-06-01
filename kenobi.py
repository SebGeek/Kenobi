#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
import time
from Queue import Queue, Empty
import sys

#sys.path.append("./ultrasonic")
#from ultrasonic import ThreadMeasureDistance

#sys.path.append("./servo")
#from servo import ThreadMoveServo

sys.path.append("/home/pi/Kenobi/bluetooth")
from bluetooth_serial import ThreadBluetooth

sys.path.append("/home/pi/Kenobi/motor")
from motor import ThreadMotor

sys.path.append("/home/pi/Kenobi/LED")
import matrix8x8_heartbeat


if __name__ == '__main__':
    # ThreadMeasureDistance_com_queue_TX = multiprocessing.Queue()
    # ThreadMeasureDistance_com_queue_TX.cancel_join_thread()
    # ThreadMeasureDistance_com_queue_RX = multiprocessing.Queue()
    # ThreadMeasureDistance_com_queue_RX.cancel_join_thread()
    # ThreadMeasureDistance = ThreadMeasureDistance(ThreadMeasureDistance_com_queue_RX, ThreadMeasureDistance_com_queue_TX)
    # ThreadMeasureDistance.start()

    # ThreadMoveServo_com_queue_TX = multiprocessing.Queue()
    # ThreadMoveServo_com_queue_TX.cancel_join_thread()
    # ThreadMoveServo_com_queue_RX = multiprocessing.Queue()
    # ThreadMoveServo_com_queue_RX.cancel_join_thread()
    # ThreadMoveServo = ThreadMoveServo(ThreadMoveServo_com_queue_RX, ThreadMoveServo_com_queue_TX)
    # ThreadMoveServo.start()

    ThreadBluetooth_com_queue_TX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_TX.cancel_join_thread()
    ThreadBluetooth_com_queue_RX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_RX.cancel_join_thread()
    ThreadBluetooth = ThreadBluetooth(ThreadBluetooth_com_queue_RX, ThreadBluetooth_com_queue_TX)
    ThreadBluetooth.start()  # Start the thread by calling run() method

    ThreadMotor_com_queue_TX = multiprocessing.Queue()
    ThreadMotor_com_queue_TX.cancel_join_thread()
    ThreadMotor_com_queue_RX = multiprocessing.Queue()
    ThreadMotor_com_queue_RX.cancel_join_thread()
    ThreadMotor = ThreadMotor(ThreadMotor_com_queue_RX, ThreadMotor_com_queue_TX)
    ThreadMotor.start()  # Start the thread by calling run() method

    while True:
        ''' Bluetooth '''
        com_msg = ThreadBluetooth_com_queue_TX.get(block=True, timeout=None)

        if com_msg[0] == "BLUETOOTH_analog_sensor":
            ThreadMotor_com_queue_RX.put(("MOTOR_ROLL_MAGNITUDE", com_msg[1]))
        elif com_msg[0] == "BLUETOOTH_end":
            print "QUIT !!"
            ThreadMotor_com_queue_RX.put(("STOP", None))
            ThreadBluetooth_com_queue_RX.put(("STOP", None))
            break
        else:
            print "unknown msg"

        # ''' Measure distance '''
        # try:
        #     com_msg = ThreadMeasureDistance_com_queue_TX.get(block=False, timeout=None)
        # except Empty:
        #     # No msg received
        #     pass
        # else:
        #     if com_msg[0] == "DISTANCE":
        #         print "Distance:", com_msg[1], "cm"
        #     else:
        #         print "unknown msg"

        # ''' Servo '''
        # speed = raw_input("speed ? (in sec - 0 to exit)")
        # if speed == "0":
        #     break
        # ThreadMoveServo_com_queue_RX.put(("UPDATE", (None, None, speed)))

# ThreadMeasureDistance_com_queue_RX.put(("STOP",))
# ThreadMeasureDistance.join()  # Wait until thread terminates

# ThreadMoveServo_com_queue_RX.put(("STOP",))
# ThreadMoveServo.join()  # Wait until thread terminates