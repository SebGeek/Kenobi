#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import serial
import subprocess
import multiprocessing
import psutil
from Queue import Empty
import signal
import sys

'''
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo rpi-update

Pour appairer le téléphone
sudo bluetoothctl -a
power on
discoverable yes
pairable on
scan on
(wait to see Nexus 4)
scan off
agent on
default-agent
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX => il est normal que la connection se fasse puis se deconnecte (2 secondes après)
                             car le téléphone ne trouve pas de Serial Protocol SP sur le Raspberry Pi
exit

sudo nano /etc/systemd/system/bluetooth.target.wants/bluetooth.service
    ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap --compat
    ExecStartPost=/usr/bin/sdptool add SP
sudo rfcomm listen hci0&
=> à ce moment là, on peut se connecter avec le telephone
sudo minicom rfcomm0

'''

class ThreadBluetooth(multiprocessing.Process):
    ''' Create a thread '''

    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.RqTermination = False

        signal.signal(signal.SIGINT, self.handler)

        self.connection()

        super(ThreadBluetooth, self).__init__()

    def handler(self, signum, frame):
        print 'ThreadBluetooth: Signal handler called with signal', signum
        sys.exit()

    def connection(self):
        cmd = "sudo killall rfcomm >/dev/null &"
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(0.5)
        cmd = "sudo rfcomm listen hci0 >/dev/null &"
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(0.5)
            
        while True:
                try:
                    self.serial_link = serial.Serial('/dev/rfcomm0', baudrate = 115200) #, timeout = 1)
                except serial.SerialException:
                    print "ThreadBluetooth: device not connected"
                else:
                    time.sleep(0.2)
                    try:
                        self.serial_link.flushInput()
                        time.sleep(0.1)
                        self.serial_link.flushInput()
                    except: #serial.SerialException, IOError:
                        print "ThreadBluetooth: flush error"
                        self.serial_link.close()

                        cmd = "sudo killall rfcomm >/dev/null &"
                        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        time.sleep(0.5)
                        cmd = "sudo rfcomm listen hci0 >/dev/null &"
                        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        time.sleep(0.5)

                    else:
                        self.com_queue_TX.put(("BLUETOOTH_device_connected", None), block=False)
                        break
                    
                time.sleep(1)
                
    def run(self):
        while self.RqTermination == False:
            try:
                cmd_recv = self.serial_link.readline()
            except serial.SerialException:
                print "ThreadBluetooth: device unconnected"
                self.serial_link.close()
                self.connection()
                
            except serial.SerialTimeoutException:
                print "ThreadBluetooth: timeout: nothing received"
            else:
                #print "ThreadBluetooth: Received", cmd_recv
                if "ORIENTATION" in cmd_recv:
                    cmd_recv_split = cmd_recv.split(" ")
                    (roll, magnitude, angle) = int(cmd_recv_split[1]), int(cmd_recv_split[2]), int(cmd_recv_split[3])
                    self.com_queue_TX.put(("BLUETOOTH_analog_sensor", (roll, magnitude, angle)), block=False)

                elif cmd_recv == "QUIT\n":
                    self.com_queue_TX.put(("BLUETOOTH_QUIT", None), block=False)
                elif cmd_recv == "SHUTDOWN\n":
                    self.com_queue_TX.put(("BLUETOOTH_SHUTDOWN", None), block=False)

                elif cmd_recv == "AUTO\n":
                    self.com_queue_TX.put(("BLUETOOTH_AUTO", None), block=False)
                elif cmd_recv == "MANUAL\n":
                    self.com_queue_TX.put(("BLUETOOTH_MANUAL", None), block=False)

                elif cmd_recv == "ON_OFF\n":
                    print "BLUETOOTH_ON_OFF"
                    self.com_queue_TX.put(("BLUETOOTH_ON_OFF", None), block=False)
                elif cmd_recv == "UP\n":
                    self.com_queue_TX.put(("BLUETOOTH_UP", None), block=False)
                elif cmd_recv == "DOWN\n":
                    self.com_queue_TX.put(("BLUETOOTH_DOWN", None), block=False)
                elif cmd_recv == "LEFT\n":
                    self.com_queue_TX.put(("BLUETOOTH_LEFT", None), block=False)
                elif cmd_recv == "RIGHT\n":
                    self.com_queue_TX.put(("BLUETOOTH_RIGHT", None), block=False)
                else:
                    print "ThreadBluetooth: unknown msg in com_queue_TX"

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "SEND":
                    self.serial_link.write(com_msg[1] + "\r\n")
                else:
                    print "ThreadBluetooth: unknown msg in com_queue_RX"

        self.serial_link.close()  # close port
        print "ThreadBluetooth: end of thread"

if __name__ == '__main__':

    command = "sudo rfcomm listen hci0 >/dev/null &"
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(0.5)

    try:
        ser = serial.Serial('/dev/rfcomm0', 115200)  # open first serial port
    except serial.SerialException:
        print "no device connected"
    else:
        print "device connected"
        ser.write("hello from Pi\r\n")  # write a string

        cmd_received = ""
        while "QUIT" not in cmd_received:
            try:
                cmd_received = ser.readline()
            except serial.SerialException:
                print "error in serial read"
                break
            else:
                print cmd_received,
                #ser.write("Pi received:" + cmd_recv)  # write a string

        ser.close()  # close port
