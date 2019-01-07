import time
import os
import syslog

import tellopy


'''
Force interface wlan1 with static IP: 192.168.10.2


sudo route add default gw 192.168.10.2 wlan1



Tello IP: 192.168.10.1

Tello LEDs:
- flashing blue - charging
- solid blue - charged
- flashing purple - booting up
- flashing yellow fast - wifi network set up, waiting for connection
- flashing yellow - User connected
'''



def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        #print(data)
        syslog.syslog(data)


def test():
    
    os.system("sudo route add default gw 192.168.10.2 wlan1")
    time.sleep(1)
    
    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        syslog.syslog("connect")
        drone.connect()
        syslog.syslog("wait_for_connection")
        drone.wait_for_connection(5.0)
        
        # press blue button to continue
        
        syslog.syslog("takeoff")
        drone.takeoff()
        syslog.syslog("wait 5 sec")
        time.sleep(5)
        
        #for i in range(2):
        #    drone.down(50)
        #    time.sleep(1)
        #    drone.up(50)
        #    time.sleep(1)
        
        syslog.syslog("land")
        drone.land()
    except Exception as ex:
        print(ex)
    finally:
        drone.quit()
        os.system("sudo route del default gw 192.168.10.2 wlan1")

if __name__ == '__main__':
    test()
