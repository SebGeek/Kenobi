import time
import os
import sys
import syslog
import datetime
import pygame
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

def drone_action(drone, action, value=None, sound=None):
    display("drone." + action + "(" + str(value) + ")")
    
    if value == None:
        status = getattr(drone, action)()
    else:
        status = getattr(drone, action)(value)
    if status == False:
        raise("error when calling " + action)
    
    start_time = time.time()
    if sound != None:
        pygame.mixer.music.load("/home/pi/Kenobi/sound/sons_laser/" + sound)
        pygame.mixer.music.play()
        while (pygame.mixer.music.get_busy() == True) or (time.time() - start_time < 4):
            # Play until end of music file or 4 s are elapsed
            pygame.time.Clock().tick(10)
        
    while time.time() - start_time < 4: # time for command to be taken into account
        time.sleep(0.1)


def clean_up(drone):
    drone.quit()
    os.system("sudo route del default gw 192.168.10.2 wlan1")
    sys.exit()


if __name__ == '__main__':
    os.system("sudo route add default gw 192.168.10.2 wlan1")

    pygame.mixer.init()

    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        display("connect")
        drone.connect()
        display("wait_for_connection")
        drone.wait_for_connection(5.0)       
        time.sleep(2) # necessary after connection
        
    except Exception as ex:
        display("PROBLEM TO CONNECT TO TELLO !! error message: " + str(ex))
        clean_up(drone)
        
    try:
        display("Battery remaining is " + str(glob_data.battery_percentage) + " %")        
        if glob_data.battery_percentage < 20:
            display("LOW BATTERY !!")
            clean_up(drone)
        if (glob_data.height != 0) or (glob_data.ground_speed != 0):
            display("Height/Speed are not 0 !!")
            clean_up(drone)
        
        drone_action(drone, "takeoff", sound="Spaceship_Takeoff.mp3")

        drone_action(drone, "flip_forward", sound="3536.mp3")
        drone_action(drone, "flip_back", sound="3537.mp3")
        drone_action(drone, "flip_right", sound="12664.mp3")
        drone_action(drone, "flip_left", sound="11039.mp3")
        
        drone_action(drone, "clockwise", value=100, sound="9741.mp3")
        drone_action(drone, "counter_clockwise", value=100, sound="9741.mp3")
        drone_action(drone, "counter_clockwise", value=0, sound="9741.mp3")
       
        #display("Wait 5s to be sure previous commands are finished (so land command is taken into account)")
        #time.sleep(5)
        
        drone_action(drone, "land", sound="Strange_Static.mp3")
        
        #display("drone.land()")
        #status = drone.land()
        #if status == False:
        #    raise("land")
            
        display("Wait 5s before exit to let land finishing")
        time.sleep(5)

    except Exception as ex:
        display("PROBLEM !! error message: " + str(ex))
    finally:
        clean_up(drone)
