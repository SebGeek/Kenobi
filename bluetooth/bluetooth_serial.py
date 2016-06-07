#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import serial
import subprocess
import multiprocessing
import psutil
from Queue import Empty

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

        self.connection()

        super(ThreadBluetooth, self).__init__()

    def connection(self):
        for proc in psutil.process_iter():
            if ('python' in proc.cmdline()) and ('rpc_server_linux.py' in proc.cmdline()):
                #proc.kill()
                #self.debug(True, "Previous execution of rpc_server_linux.py was killed")
                break

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
                    print "device not connected"
                else:
                    print "serial open"
                    time.sleep(0.2)
                    try:
                        self.serial_link.flushInput()
                        time.sleep(0.1)
                        self.serial_link.flushInput()
                    except: #serial.SerialException, IOError:
                        print "flush error"
                        self.serial_link.close()

                        cmd = "sudo killall rfcomm >/dev/null &"
                        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        time.sleep(0.5)
                        cmd = "sudo rfcomm listen hci0 >/dev/null &"
                        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        time.sleep(0.5)

                    else:
                        self.com_queue_TX.put(("BLUETOOTH_device_connected", None), block=False)
                        self.serial_link.write("Kenobi is ready !\r\n")
                        break
                    
                time.sleep(1)
                
    def run(self):
        while self.RqTermination == False:
            try:
                cmd_recv = self.serial_link.readline()
            except serial.SerialException:
                print "device unconnected"
                self.serial_link.close()
                self.connection()
                
            except serial.SerialTimeoutException:
                print "timeout: nothing received"
            else:
                #print cmd_recv,
                if "ORIENTATION" in cmd_recv:
                    cmd_recv_split = cmd_recv.split(" ")
                    (roll, magnitude, angle) = int(cmd_recv_split[1]), int(cmd_recv_split[2]), int(cmd_recv_split[3])
                    self.com_queue_TX.put(("BLUETOOTH_analog_sensor", (roll, magnitude, angle)), block=False)
                elif "QUIT" in cmd_recv:
                    self.com_queue_TX.put(("BLUETOOTH_QUIT", None), block=False)
                elif "SHUTDOWN" in cmd_recv:
                    self.com_queue_TX.put(("BLUETOOTH_SHUTDOWN", None), block=False)
                elif "AUTO" in cmd_recv:
                    self.com_queue_TX.put(("BLUETOOTH_AUTO", None), block=False)
                elif "MANUAL" in cmd_recv:
                    self.com_queue_TX.put(("BLUETOOTH_MANUAL", None), block=False)

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
                    print "unknown msg"

        self.serial_link.close()  # close port
        print "BLUETOOTH end of thread"

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

        cmd_recv = ""
        while "QUIT" not in cmd_recv:
            try:
                cmd_recv = ser.readline()
            except serial.SerialException:
                print "error in serial read"
                break
            else:
                print cmd_recv,
                #ser.write("Pi received:" + cmd_recv)  # write a string

        ser.close()  # close port
