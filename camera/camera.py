#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import multiprocessing
from Queue import Queue, Empty
import signal

class ThreadCamera(multiprocessing.Process):
    ''' Create a thread '''
    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX
        self.RqTermination = False

        super(ThreadCamera, self).__init__()

    def run(self):
        signal.signal(signal.SIGINT, self.handler)

        while self.RqTermination == False:

            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "SERVO_PAN":
                    (angle, duration) = com_msg[1]
                    self.pan_update(angle, duration)
                elif com_msg[0] == "SERVO_TILT":
                    (angle, duration) = com_msg[1]
                    self.tilt_update(angle, duration)
                else:
                    print "ThreadCamera: unknown msg"

        print "ThreadCamera: end of thread"

    def pan_update(self, angle, duration_s):
        self.pan_angle_target = float(angle)
        self.pan_angle_increment = (self.pan_angle_target - self.pan_angle_current) * (self.period_s / duration_s)

    def tilt_update(self, angle, duration_s):
        self.tilt_angle_target = float(angle)
        self.tilt_angle_increment = (self.tilt_angle_target - self.tilt_angle_current) * (self.period_s / duration_s)

    def handler(self, signum, frame):
        print 'ThreadCamera: Signal handler called with signal', signum


if __name__ == '__main__':

    '''
    This is how to track a white ball example using SimpleCV
    The parameters may need to be adjusted to match the RGB color
    of your object.
    The demo video can be found at:
    http://www.youtube.com/watch?v=jihxqg3kr-g
    '''
    print __doc__

    import SimpleCV

    display = SimpleCV.Display()
    cam = SimpleCV.Camera()
    normaldisplay = True

    while display.isNotDone():

        if display.mouseRight:
            normaldisplay = not (normaldisplay)
            print "Display Mode:", "Normal" if normaldisplay else "Segmented"

        img = cam.getImage().flipHorizontal()
        dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
        segmented = dist.stretch(200, 255)
        blobs = segmented.findBlobs()
        if blobs:

            circles = blobs.filter([b.isCircle(0.2) for b in blobs])
            print circles
            if circles:
                img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(), SimpleCV.Color.BLUE, 3)

        if normaldisplay:
            img.show()
        else:
            segmented.show()
