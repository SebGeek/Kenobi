#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from Adafruit_LED_Backpack import Matrix8x8
import multiprocessing
from Queue import Empty

class ThreadMatrixLED(multiprocessing.Process):
    ''' Create a thread '''

    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.RqTermination = False

        self.display = Matrix8x8.Matrix8x8()
        # Initialize the display. Must be called once before using the display.
        self.display.begin()
        self.display.clear()

        super(ThreadMatrixLED, self).__init__()

    def run(self):
        function = None
        while self.RqTermination == False:
            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=False, timeout=None)
            except Empty:
                # No msg received
                if function != None:
                    function()
                else:
                    time.sleep(0.2)
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "MATRIXLED_heart_beat":
                    function = self.heart_beat
                elif com_msg[0] == "MATRIXLED_clear_display":
                    function = self.clear_display
                else:
                    print "unknown msg"

        self.clear_display()
        print "MATRIXLED end of thread"

    def clear_display(self):
        self.display.clear()
        self.display.write_display()
        time.sleep(0.2)

    def heart_beat(self):
        heart1 = [0b00000000, 0b01100110, 0b10011001, 0b10000001, 0b01000010, 0b00100100, 0b00011000, 0b00000000]
        heart2 = [0b00000000, 0b01100110, 0b11111111, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00000000]

        for y in range(0, 8):
            position = 128
            for x in range(0, 8):
                value = position & heart1[y]
                self.display.set_pixel(x, y, value)
                position >>= 1

        self.display.write_display()
        time.sleep(0.2)

        for y in range(0, 8):
            position = 128
            for x in range(0, 8):
                value = position & heart2[y]
                self.display.set_pixel(x, y, value)
                position >>= 1

        self.display.write_display()
        time.sleep(0.8)
