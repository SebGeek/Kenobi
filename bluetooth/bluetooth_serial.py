#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import bluetooth

'''
B8:27:EB:83:9E:E9       raspberrypi3
00:1D:DF:FE:B0:A9       n/a Sculpt Touche Mouse ?
C0:D9:62:04:84:DF       PC-SEB
98:D6:F7:71:8C:53       Nexus 4

sudo bluetoothctl
power on
agent on
default-agent
scan on
pair 98:D6:F7:71:8C:53

I am using bluetooth to connect to serial on python so I simply run sudo rfcomm bind 0 xx:xx:xx:xx:xx:xx via subprocess.call to created a serial port.
Make sure to run sudo rfcomm release 0 at the end of the script to release the serial port
sudo rfcomm bind 0 98:D6:F7:71:8C:53
sudo rfcomm release 0


'''

if __name__ == '__main__':


    if len(sys.argv) < 2:
            print "usage: sdp-browser <addr>"
            print "   addr can be a bluetooth address, \"localhost\" or \"all\""
            sys.exit(2)

    target = sys.argv[1]
    if target == "all" : target = None

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
            print "found %d services on %s" % (len(services), sys.argv[1])
            print
    else:
            print "no services found"

    for svc in services:
            print "Service Name: %s" % svc["name"]
            print "  Host: %s" % svc["host"]
            print "  Description: %s" % svc["description"]
            print "  Provided By: %s" % svc["provider"]
            print "  Protocol: %s" % svc["protocol"]
            print "  channel/PSM: %s" % svc["port"]
            print "  svc classes: %s" % svc["service-classes"]
            print "  profiles: %s" % svc["profiles"]
            print "  service id: %s" % svc["service-id"]