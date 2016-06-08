#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
import multiprocessing
from Queue import Empty


class ThreadSound(multiprocessing.Process):
    ''' Create a thread '''

    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.RqTermination = False

        super(ThreadSound, self).__init__()

    def run(self):
        pygame.mixer.init()  # Do not call from __init__() else the library doesn't work

        while self.RqTermination == False:
            ''' read com_queue_RX '''
            try:
                com_msg = self.com_queue_RX.get(block=True, timeout=None)
            except Empty:
                # No msg received
                pass
            else:
                if com_msg[0] == "STOP":
                    self.RqTermination = True
                elif com_msg[0] == "SOUND_welcome":
                    print "welcome"
                    pygame.mixer.music.load("/home/pi/Kenobi/sound/R2D2/Beeping and whistling.mp3")
                    pygame.mixer.music.play()
                elif com_msg[0] == "SOUND_shock":
                    pygame.mixer.music.load("/home/pi/Kenobi/sound/R2D2/Snappy R2D2.mp3")
                    pygame.mixer.music.play()
                else:
                    print "unknown msg"

        print "ThreadSound: end of thread"

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Kenobi/sound/R2D2/Beeping and whistling.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue
