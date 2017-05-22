#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
import threading
import os
import sys
import time
import signal

sys.path.append("/home/pi/Kenobi/bluetooth")
from bluetooth_serial import ThreadBluetooth

sys.path.append("/home/pi/Kenobi/motor")
from motor import ThreadMotor

sys.path.append("/home/pi/Kenobi/LED")
from matrixLED import ThreadMatrixLED

sys.path.append("/home/pi/Kenobi/sound")
from sound import ThreadSound

sys.path.append("/home/pi/Kenobi/servo")
from servo import ThreadMoveServo

import RPi.GPIO as GPIO

GPIO_BLUE_BUTTON = 20
GPIO_RED_BUTTON = 21
GPIO_LED = 26

def close_threads():
    if ObjThreadModeAuto != None:
        ObjThreadModeAuto.stop()
    ThreadMotor_com_queue_RX.put(("STOP", None))
    ThreadBluetooth_com_queue_RX.put(("STOP", None))
    ThreadMatrixLED_com_queue_RX.put(("STOP", None))
    ThreadSound_com_queue_RX.put(("STOP", None))
    ThreadMoveServo_com_queue_RX.put(("STOP", None))

class ThreadModeAuto(threading.Thread):
    def __init__(self):
        self.RqTermination = False
        threading.Thread.__init__(self)

    def run(self):
        while self.RqTermination == False:
            ThreadMotor_com_queue_RX.put(("MOTOR_Request_Distance", None))
            # Wait for MOTOR_Distance message
            com_msg_distance = ThreadMotor_com_queue_TX.get(block=True, timeout=None)
            #print "Kenobi: distance is", com_msg_distance[1]
            if com_msg_distance[1] > 20:
                ThreadMotor_com_queue_RX.put(("MOTOR_FORWARD", 0.5))  # speed
            else:
                ThreadSound_com_queue_RX.put(("SOUND_shock", None))
                ThreadMotor_com_queue_RX.put(("MOTOR_RIGHT", 0.5))
                time.sleep(1) # pour dégagement de l'obstacle
            time.sleep(0.1)

        print "ThreadModeAuto: end of thread"

    def stop(self):
        self.RqTermination = True

def handler(signum, frame):
    print 'Signal handler called with signal' + str(signum) + " " + str(frame)
    close_threads()
    sys.exit(0)

def init_button_led():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Blue connected between GND and GPIO#20
    GPIO.setup(GPIO_RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button Red connected between GND and GPIO#21
    GPIO.setup(GPIO_LED, GPIO.OUT)                                  # LED connected between GND and GPIO#26 through a 440 ohm resistor
    GPIO.output(GPIO_LED, False)

    GPIO.add_event_detect(GPIO_RED_BUTTON, GPIO.FALLING, callback=red_button, bouncetime=200)

def red_button(_):
    os.system("/usr/bin/sudo /sbin/shutdown -h now")

START_WITH_BLUETOOTH_CONNECTION = True
START_IN_AUTO_MODE = False

if __name__ == '__main__':
    init_button_led()

    ThreadMatrixLED_com_queue_TX = multiprocessing.Queue()
    ThreadMatrixLED_com_queue_TX.cancel_join_thread()
    ThreadMatrixLED_com_queue_RX = multiprocessing.Queue()
    ThreadMatrixLED_com_queue_RX.cancel_join_thread()
    ObjThreadMatrixLED = ThreadMatrixLED(ThreadMatrixLED_com_queue_RX, ThreadMatrixLED_com_queue_TX)
    ObjThreadMatrixLED.start()

    ThreadSound_com_queue_TX = multiprocessing.Queue()
    ThreadSound_com_queue_TX.cancel_join_thread()
    ThreadSound_com_queue_RX = multiprocessing.Queue()
    ThreadSound_com_queue_RX.cancel_join_thread()
    ObjThreadSound = ThreadSound(ThreadSound_com_queue_RX, ThreadSound_com_queue_TX)
    ObjThreadSound.start()

    ThreadBluetooth_com_queue_TX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_TX.cancel_join_thread()
    ThreadBluetooth_com_queue_RX = multiprocessing.Queue()
    ThreadBluetooth_com_queue_RX.cancel_join_thread()

    ThreadMatrixLED_com_queue_RX.put(("MATRIXLED_heart_beat", None))

    if START_WITH_BLUETOOTH_CONNECTION == True:
        ObjThreadBluetooth = ThreadBluetooth(ThreadBluetooth_com_queue_RX, ThreadBluetooth_com_queue_TX)
        # Block until a connection is established from Android application
        ObjThreadBluetooth.start()

    ThreadSound_com_queue_RX.put(("SOUND_welcome", None))
    
    ThreadMotor_com_queue_TX = multiprocessing.Queue()
    ThreadMotor_com_queue_TX.cancel_join_thread()
    ThreadMotor_com_queue_RX = multiprocessing.Queue()
    ThreadMotor_com_queue_RX.cancel_join_thread()
    ObjThreadMotor = ThreadMotor(ThreadMotor_com_queue_RX, ThreadMotor_com_queue_TX)
    ObjThreadMotor.start()

    ThreadMoveServo_com_queue_TX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_TX.cancel_join_thread()
    ThreadMoveServo_com_queue_RX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_RX.cancel_join_thread()
    ObjThreadMoveServo = ThreadMoveServo(ThreadMoveServo_com_queue_RX, ThreadMoveServo_com_queue_TX)
    ObjThreadMoveServo.start()

    ObjThreadModeAuto = None
    mode = "NO_MOTOR"

    # Set the signal handler to catch Ctrl-C exception
    signal.signal(signal.SIGINT, handler)

    if START_IN_AUTO_MODE == True:
        ThreadBluetooth_com_queue_TX.put(("BLUETOOTH_AUTO", None), block=False)

    OC_on = False
    pan_angle = 0.0
    tilt_angle = 0.0

    while True:
        ''' Wait for Bluetooth msg received from Android application'''
        com_msg = ThreadBluetooth_com_queue_TX.get(block=True, timeout=None)

        if com_msg[0] == "BLUETOOTH_device_connected":
            print "Kenobi: device connected"
            ThreadBluetooth_com_queue_RX.put(("SEND", "Kenobi is ready !"))

        elif com_msg[0] == "BLUETOOTH_AUTO":
            print "Kenobi: AUTO"
            mode = "AUTO"
            # Stop servo power to avoid camera shaking (PWM is shared between RaspiRobot board and servoblaster)
            ThreadMotor_com_queue_RX.put(("MOTOR_OC", False))
            if ObjThreadModeAuto == None:
                ObjThreadModeAuto = ThreadModeAuto()
                ObjThreadModeAuto.start()

        elif com_msg[0] == "BLUETOOTH_MANUAL":
            if mode == "MANUAL":
                print "Kenobi: NO_MOTOR"
                mode = "NO_MOTOR"
            else:
                print "Kenobi: MANUAL"
                mode = "MANUAL"
            if ObjThreadModeAuto != None:
                ObjThreadModeAuto.stop()
                ObjThreadModeAuto = None

        elif com_msg[0] == "BLUETOOTH_analog_sensor":
            # User has to stop servos power before being able to move the robot
            # to avoid camera shaking: PWM is shared between RaspiRobot board and servoblaster
            if mode == "MANUAL" and OC_on == False:
                ThreadMotor_com_queue_RX.put(("MOTOR_ROLL_MAGNITUDE", com_msg[1]))

        elif com_msg[0] == "BLUETOOTH_ON_OFF":
            OC_on = not OC_on
            ThreadMotor_com_queue_RX.put(("MOTOR_OC", OC_on))
            pan_angle = 0.0
            tilt_angle = 0.0
            ThreadMoveServo_com_queue_RX.put(("SERVO_TILT", (tilt_angle, 2.0)))
            ThreadMoveServo_com_queue_RX.put(("SERVO_PAN", (pan_angle, 2.0)))
        elif com_msg[0] == "BLUETOOTH_UP":
            tilt_angle += 10.0
            if tilt_angle > 60.0:
                tilt_angle = 60.0
            ThreadMoveServo_com_queue_RX.put(("SERVO_TILT", (tilt_angle, 0.2)))
        elif com_msg[0] == "BLUETOOTH_DOWN":
            tilt_angle -= 10.0
            if tilt_angle < -60.0:
                tilt_angle = -60.0
            ThreadMoveServo_com_queue_RX.put(("SERVO_TILT", (tilt_angle, 0.2)))
        elif com_msg[0] == "BLUETOOTH_LEFT":
            pan_angle -= 10.0
            if pan_angle < -60.0:
                pan_angle = -60.0
            ThreadMoveServo_com_queue_RX.put(("SERVO_PAN", (pan_angle, 0.2)))
        elif com_msg[0] == "BLUETOOTH_RIGHT":
            pan_angle += 10.0
            if pan_angle > 60.0:
                pan_angle = 60.0
            ThreadMoveServo_com_queue_RX.put(("SERVO_PAN", (pan_angle, 0.2)))

        elif com_msg[0] == "BLUETOOTH_QUIT":
            print "Kenobi: QUIT !!"
            ThreadBluetooth_com_queue_RX.put(("SEND", "QUIT !!"))
            close_threads()
            break

        elif com_msg[0] == "BLUETOOTH_SHUTDOWN":
            print "Kenobi: SHUTDOWN !!"
            ThreadBluetooth_com_queue_RX.put(("SEND", "SHUTDOWN !!"))
            close_threads()
            os.system("/usr/bin/sudo /sbin/shutdown -h now")
            break

        else:
            print "Kenobi: unknown msg"
