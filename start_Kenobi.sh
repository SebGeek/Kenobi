#!/usr/bin/env bash

#/home/pi/env/bin/python -m googlesamples.assistant

while [ true ]
do
    python3 /home/pi/Kenobi/recognition/detect_objects.py

    #python3 /home/pi/Kenobi/tello/tello_dance.py

    python3 /home/pi/Kenobi/kenobi.py
done
