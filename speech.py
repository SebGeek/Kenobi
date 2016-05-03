# !/usr/bin/python
# -*- coding: UTF8 -*-
import time
import os
date = time.strftime('%d/%m/%y %H:%M', time.localtime())

print("Bienvenue dans l'utilitaire Espeak couplé à mbrola (non-free")
# texte = raw_input("tapez votre texte: ")
texte = "Bonjour beau gosse, comment ça va ?"
texte = texte.replace(" ", "/")
time.sleep(3)  # la fonction sleep seule n'éxiste pas l'associer au module time
command = "espeak -v mb-fr1 " + texte + " -s 130"
os.system(command)
