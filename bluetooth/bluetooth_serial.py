#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import serial
import subprocess

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
                ser.write("Pi received:" + cmd_recv)  # write a string

        ser.close()  # close port
