#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ouvrir un terminal et executer la commande ci dessous
# python3 detect_objects.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# importer tout les packages requis
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import ntpath
import pygame
import os

import RPi.GPIO as GPIO
import sys
import syslog

GPIO_BLUE_BUTTON = 20
GPIO_RED_BUTTON = 21
GPIO_LED = 26


def blue_button(_):
    GPIO.output(GPIO_LED, False)
    sys.exit()
        
def red_button(_):
    GPIO.output(GPIO_LED, False)
    os.system("/usr/bin/sudo /sbin/shutdown -h now")

def init_button_led():
    print("configure button and led gpios")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Blue connected between GND and GPIO#20
    GPIO.setup(GPIO_RED_BUTTON,  GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button Red  connected between GND and GPIO#21
    GPIO.setup(GPIO_LED, GPIO.OUT)                                  #         LED connected between GND and GPIO#26 through a 440 ohm resistor

    # Add our function to execute when the button pressed event happens
    GPIO.add_event_detect(GPIO_BLUE_BUTTON, GPIO.FALLING, callback=blue_button, bouncetime=200)
    GPIO.add_event_detect(GPIO_RED_BUTTON,  GPIO.FALLING, callback=red_button,  bouncetime=200)
    
    # Light on the led
    GPIO.output(GPIO_LED, True)
    
    
def main():
    # construction des arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=False, default="/home/pi/Kenobi/recognition/MobileNetSSD_deploy.prototxt.txt",
        help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=False, default="/home/pi/Kenobi/recognition/MobileNetSSD_deploy.caffemodel",
        help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.6,
        help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # initialiser la liste des objets entrainés par MobileNet SSD 
    # création du contour de détection avec une couleur attribuée au hasard pour chaque objet
    CLASSES = ["arriere-plan", "avion", "velo", "oiseau", "bateau",
        "bouteille", "autobus", "voiture", "chat", "chaise", "vache", "table",
        "chien", "cheval", "moto", "personne", "plante", "mouton",
        "sofa", "train", "moniteur"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    pygame.mixer.init()

    # chargement des fichiers depuis le répertoire de stockage 
    print(" ...chargement du modèle...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # initialiser la caméra du pi, attendre 2s pour la mise au point ,
    # initialiser le compteur FPS
    print("...démarrage de la Picamera...")
    vs = VideoStream(usePiCamera=True, resolution=(1600, 1200)).start()
    time.sleep(2.0)
    #fps = FPS().start()

    # boucle principale du flux vidéo
    while True:
        # récupération du flux vidéo, redimension 
        # afin d'afficher au maximum 800 pixels 
        frame = vs.read()
        frame = imutils.resize(frame, width=800)

        # récupération des dimensions et transformation en collection d'images
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # determiner la détection et la prédiction 
        net.setInput(blob)
        detections = net.forward()

        # boucle de détection
        list_objects = []
        for i in np.arange(0, detections.shape[2]):
            # calcul de la probabilité de l'objet détecté en fonction de la prédiction
            confidence = detections[0, 0, i, 2]
            
            # supprimer les détections faibles inférieures à la probabilité minimale
            if confidence > args["confidence"]:
                # extraire l'index du type d'objet détecté
                # calcul des coordonnées de la fenêtre de détection 
                idx = int(detections[0, 0, i, 1])
                #box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                #(startX, startY, endX, endY) = box.astype("int")

                # creation du contour autour de l'objet détecté
                # insertion de la prédiction de l'objet détecté 
                #label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                #cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                #y = startY - 15 if startY - 15 > 15 else startY + 15
                #cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                
                # enregistrement de l'image détectée 
                #cv2.imwrite("detection.png", frame)
                obj = CLASSES[idx]
                if obj not in list_objects:
                    list_objects.append(CLASSES[idx])
        
        # affichage du flux vidéo dans une fenètre 
        #cv2.imshow("Frame", frame)
        #key = cv2.waitKey(1) & 0xFF  # ligne necessaire pour l'affichage dans la frame

        # Pronounce the objects seen
        print(list_objects)
        for anobject in list_objects:
            path_to_sound = "/home/pi/Kenobi/recognition/vocabulary/" + anobject + ".ogg"
            if os.path.isfile(path_to_sound):
                pygame.mixer.music.load(path_to_sound)
                pygame.mixer.music.play()
                # Play until end of music file
                while pygame.mixer.music.get_busy() == True:
                    pygame.time.Clock().tick(10)

        # la touche q permet d'interrompre la boucle principale
        #if key == ord("q"):
        #   break

        # mise à jour du FPS 
        #fps.update()

    # arret du compteur et affichage des informations dans la console
    #fps.stop()
    #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    syslog.syslog('Starting')
    init_button_led()
    main()
    
