import time
import os
import syslog
import datetime

import tellopy # /usr/local/lib/python3.5/dist-packages/tellopy/_internal


'''
Force interface wlan1 with static IP: 192.168.10.2

Tello IP: 192.168.10.1

Tello LEDs:
- flashing blue          charging
- solid blue             charged
- flashing purple        booting up
- flashing yellow fast   wifi network set up, waiting for connection
- flashing yellow        User connected
'''

glob_data = None

def handler(event, sender, data, **args):
    global glob_data
    
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        glob_data = data

def display(string):
    print(str(datetime.datetime.now()) + " " + str(string))
    #syslog.syslog(str(string))

def drone_action(drone, action, value=None):
    display("drone." + action + "(" + str(value) + ")")
    
    if value == None:
        status = getattr(drone, action)()
    else:
        status = getattr(drone, action)(value)
    if status == False:
        raise("error when calling " + action)
        
    #display(glob_data.ground_speed)
    #time.sleep(1) # time for command to be taken into account
    
    #display(glob_data.ground_speed)
    #while glob_data.ground_speed != 0:
    #    time.sleep(0.1)
    #    display(glob_data.ground_speed)
    
    time.sleep(4) # time for command to be taken into account


def test():    
    os.system("sudo route add default gw 192.168.10.2 wlan1")
    
    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        display("connect")
        drone.connect()
        display("wait_for_connection")
        drone.wait_for_connection(5.0)
        time.sleep(2) # necessary after connection

        display("Battery remaining is " + str(glob_data.battery_percentage) + " %")        
        if glob_data.battery_percentage < 20:
            display("LOW BATTERY !!")
        if (glob_data.height != 0) or (glob_data.ground_speed != 0):
            display("Height/Speed not 0 !!")
        
        fly = True
        if fly == True:
            drone_action(drone, "takeoff")

            #drone_action(drone, "flip_forward")
            #drone_action(drone, "flip_back")
            #drone_action(drone, "flip_right")
            #drone_action(drone, "flip_left")
            
            drone_action(drone, "clockwise", 100)
            drone_action(drone, "clockwise", 0)
            drone_action(drone, "counter_clockwise", 100)
            drone_action(drone, "counter_clockwise", 0)
            
           
            display("Wait 5s to be sure previous commands are finished (so land command is taken into account)")
            time.sleep(5)
            
            display("drone.land()")
            status = drone.land()
            if status == False:
                raise("land")
                
            display("Wait 5s before exit to let land finishing")
            time.sleep(5)

    except Exception as ex:
        display(ex)
        display("PROBLEM TO CONNECT TO TELLO !!")
    finally:
        drone.quit()
        os.system("sudo route del default gw 192.168.10.2 wlan1")

if __name__ == '__main__':
    test()
