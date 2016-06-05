#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Kenobi/sound/R2D2/Beeping and whistling.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy() == True:
    continue