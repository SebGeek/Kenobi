#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import serial
import subprocess
import multiprocessing
from Queue import Empty

'''
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo rpi-update

B8:27:EB:83:9E:E9       raspberrypi3
00:1D:DF:FE:B0:A9       PHILIPS HTL4110B barre de son
C0:D9:62:04:84:DF       PC-SEB
98:D6:F7:71:8C:53       Nexus 4

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
pair 98:D6:F7:71:8C:53
trust 98:D6:F7:71:8C:53
connect 98:D6:F7:71:8C:53 => il est normal que la connection se fasse puis se deconnecte (2 secondes après) car le téléphone ne trouve pas de Serial Protocol SP sur le Raspberry Pi
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

        cmd = "sudo rfcomm listen hci0 >/dev/null &"
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(0.5)

        while True:
            try:
                self.serial_link = serial.Serial('/dev/rfcomm0', 115200)  # open first serial port
            except:
                print "no device connected"
                time.sleep(1)
            else:
                print "device connected"
                self.serial_link.flushInput()
                time.sleep(0.1)
                self.serial_link.flushInput()

                self.serial_link.write("hello from Pi\r\n")  # write a string

                self.cmd_recv = ""

                super(ThreadBluetooth, self).__init__()
                break

    def run(self):
        while self.RqTermination == False:
            try:
                self.cmd_recv = self.serial_link.readline()
            except:
                print "error in serial read"
                #break
                pass
            else:
                #print self.cmd_recv,
                if " " in self.cmd_recv:
                    (roll, magnitude) = int(self.cmd_recv.split(" ")[0]), int(self.cmd_recv.split(" ")[1])
                    self.com_queue_TX.put(("BLUETOOTH_analog_sensor", (roll, magnitude)), block=False)
                elif "END" in self.cmd_recv:
                    self.com_queue_TX.put(("BLUETOOTH_end", None), block=False)

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                else:
                    print "unknown msg"

        self.serial_link.close()  # close port

if __name__ == '__main__':

    command = "sudo rfcomm listen hci0 >/dev/null &"
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(0.5)

    try:
        ser = serial.Serial('/dev/rfcomm0', 115200)  # open first serial port
    except:
        print "no device connected"
    else:
        print "device connected"
        ser.write("hello from Pi\r\n")  # write a string

        cmd_recv = ""
        while "END" not in cmd_recv:
            try:
                cmd_recv = ser.readline()
            except:
                print "error in serial read"
                break
            else:
                print cmd_recv,
                #ser.write("Pi received:" + cmd_recv)  # write a string

        ser.close()  # close port
