# !/usr/bin/python
import os
import time
import multiprocessing
from Queue import Queue, Empty

class ThreadMoveServo(multiprocessing.Process):
    ''' Create a thread '''
    def __init__(self, com_queue_RX, com_queue_TX, val=8, up=True, speed=0.01):
        self.update(val, up, speed)
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX
    
        self.RqTermination = False

        # servod is compiled from ServoBlaster GITHub
        # https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
        os.system('sudo ./servod')
        
        super(ThreadMoveServo, self).__init__()
    
    def update(self, val=None, up=None, speed=None):
        if val != None:
            self.val = val
        if up != None:
            self.up = up
        if speed != None:
            self.speed = speed
    
    def run(self):
        while self.RqTermination == False:
            if self.val == 92:
                self.up = False
            elif self.val == 8:
                self.up = True
                
            os.system("echo 0=" + str(self.val) + "% > /dev/servoblaster")
            time.sleep(self.speed)
            
            if self.up == True:
                self.val += 1
            else:
                self.val -= 1
            
            #self.com_queue_TX.put(("FRAME_QUEUE_STATE", True), block=False)
            
            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "UPDATE":
                    (val, up, speed) = com_msg[1]
                    self.update(val, up, float(speed))
                else:
                    print "unknown msg"


if __name__=='__main__':
    ThreadMoveServo_com_queue_TX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_TX.cancel_join_thread()
    ThreadMoveServo_com_queue_RX = multiprocessing.Queue()
    ThreadMoveServo_com_queue_RX.cancel_join_thread()

    ThreadMoveServo = ThreadMoveServo(ThreadMoveServo_com_queue_RX, ThreadMoveServo_com_queue_TX)
    ThreadMoveServo.start()
    
    while True:
        #val = raw_input("value ? (8~92)")
        speed = raw_input("speed ? (in sec - 0 to exit)")
        
        if speed == "0":
            print "stop request"
            ThreadMoveServo_com_queue_RX.put(("STOP",))
            ThreadMoveServo.join() # Wait until thread terminates
            break
        
        ThreadMoveServo_com_queue_RX.put(("UPDATE", (None, None, speed)))