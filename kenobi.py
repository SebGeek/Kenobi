#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
import os
import sys
import time

sys.path.append("/home/pi/Kenobi/bluetooth")
from bluetooth_serial import ThreadBluetooth

sys.path.append("/home/pi/Kenobi/motor")
from motor import ThreadMotor

sys.path.append("/home/pi/Kenobi/LED")
from matrixLED import ThreadMatrixLED

sys.path.append("/home/pi/Kenobi/sound")
from sound import ThreadSound

def close_threads():
    ThreadMotor_com_queue_RX.put(("STOP", None))
    ThreadBluetooth_com_queue_RX.put(("STOP", None))
    ThreadMatrixLED_com_queue_RX.put(("STOP", None))
    ThreadSound_com_queue_RX.put(("STOP", None))

if __name__ == '__main__':
    ThreadMatrixLED_com_queue_TX = multiprocessing.Queue()
    ThreadMatrixLED_com_queue_TX.cancel_join_thread()
    ThreadMatrixLED_com_queue_RX = multiprocessing.Queue()
    ThreadMatrixLED_com_queue_RX.cancel_join_thread()
    ThreadMatrixLED = ThreadMatrixLED(ThreadMatrixLED_com_queue_RX, ThreadMatrixLED_com_queue_TX)
    ThreadMatrixLED.start()

    ThreadSound_com_queue_TX = multiprocessing.Queue()
    ThreadSound_com_queue_TX.cancel_join_thread()
    ThreadSound_com_queue_RX = multiprocessing.Queue()
    ThreadSound_com_queue_RX.cancel_join_thread()
    ThreadSound = ThreadSound(ThreadSound_com_queue_RX, ThreadSound_com_queue_TX)
    ThreadSound.start()

    ThreadBluetooth_com_queue_TX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_TX.cancel_join_thread()
    ThreadBluetooth_com_queue_RX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_RX.cancel_join_thread()
    ThreadBluetooth = ThreadBluetooth(ThreadBluetooth_com_queue_RX, ThreadBluetooth_com_queue_TX)
    # Block until a connection is established from Android application
    ThreadBluetooth.start()
    ThreadMatrixLED_com_queue_RX.put(("MATRIXLED_heart_beat", None))
    ThreadSound_com_queue_RX.put(("SOUND_welcome", None))
    
    ThreadMotor_com_queue_TX = multiprocessing.Queue()
    ThreadMotor_com_queue_TX.cancel_join_thread()
    ThreadMotor_com_queue_RX = multiprocessing.Queue()
    ThreadMotor_com_queue_RX.cancel_join_thread()
    ThreadMotor = ThreadMotor(ThreadMotor_com_queue_RX, ThreadMotor_com_queue_TX)
    ThreadMotor.start()

    mode = ""

    while True:
        ''' Wait for Bluetooth msg received from Android application'''
        com_msg = ThreadBluetooth_com_queue_TX.get(block=True, timeout=None)

        if com_msg[0] == "BLUETOOTH_device_connected":
            print "device connected"
        elif com_msg[0] == "BLUETOOTH_AUTO":
            print "AUTO"
            mode = "AUTO"
            ThreadSound_com_queue_RX.put(("SOUND_shock", None))
        elif com_msg[0] == "BLUETOOTH_MANUAL":
            print "MANUAL"
            mode = "MANUAL"
        elif com_msg[0] == "BLUETOOTH_analog_sensor":
            if mode == "MANUAL":
                ThreadMotor_com_queue_RX.put(("MOTOR_ROLL_MAGNITUDE", com_msg[1]))
        elif com_msg[0] == "BLUETOOTH_QUIT":
            print "QUIT !!"
            ThreadBluetooth_com_queue_RX.put(("SEND", "QUIT !!"))
            close_threads()
            break
        elif com_msg[0] == "BLUETOOTH_SHUTDOWN":
            print "SHUTDOWN !!"
            ThreadBluetooth_com_queue_RX.put(("SEND", "SHUTDOWN !!"))
            close_threads()
            os.system("/usr/bin/sudo /sbin/shutdown -h now")
            break
        else:
            print "unknown msg"
