#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
import multiprocessing
from Queue import Empty
import glob
import random
import signal

class ThreadSound(multiprocessing.Process):
    ''' Create a thread '''

    def __init__(self, com_queue_RX, com_queue_TX):
        self.com_queue_RX = com_queue_RX
        self.com_queue_TX = com_queue_TX

        self.RqTermination = False

        self.R2D2_sounds_list = glob.glob("/home/pi/Kenobi/sound/R2D2/*.mp3")

        super(ThreadSound, self).__init__()

    def run(self):
        signal.signal(signal.SIGINT, self.handler)
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
                    pygame.mixer.music.load("/home/pi/Kenobi/sound/R2D2/Beeping and whistling.mp3")
                    pygame.mixer.music.play()
                elif com_msg[0] == "SOUND_shock":
                    index_sound = random.randint(0, len(self.R2D2_sounds_list) - 1)
                    pygame.mixer.music.load(self.R2D2_sounds_list[index_sound])
                    pygame.mixer.music.play()
                else:
                    print "ThreadSound: unknown msg"

        print "ThreadSound: end of thread"

    def handler(self, signum, frame):
        print 'ThreadSound: Signal handler called with signal', signum


if __name__ == '__main__':
    pygame.mixer.init()

    file_list = glob.glob("/home/pi/Kenobi/sound/R2D2/*.mp3")
    for filepath in file_list:
        pygame.mixer.music.load(filepath)
        print "playing", filepath
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            # Play until end of music file
            pygame.time.Clock().tick(10)
