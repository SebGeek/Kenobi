#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from Adafruit_LED_Backpack import Matrix8x8


display = Matrix8x8.Matrix8x8()

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()

heart1=[0b00000000, 0b01100110, 0b10011001, 0b10000001, 0b01000010, 0b00100100, 0b00011000, 0b00000000]
heart2=[0b00000000, 0b01100110, 0b11111111, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00000000]

for times in range(10):
  for y in range(0, 8):
    position = 128
    for x in range(0, 8):
      value = position & heart1[y]
      display.set_pixel(x, y, value)
      position = position >> 1

  display.write_display()
  time.sleep(0.2)

  for y in range(0, 8):
    position = 128
    for x in range(0, 8):
      value = position & heart2[y]
      display.set_pixel(x, y, value)
      position = position >> 1

  display.write_display()
  time.sleep(0.4)

display.clear()
display.write_display()