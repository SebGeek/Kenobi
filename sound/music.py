#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("phenomenal.mp3")
pygame.mixer.music.play()

time.sleep(10)
#while pygame.mixer.music.get_busy() == True:
#    continue