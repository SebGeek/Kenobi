#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
date = time.strftime('%d/%m/%y %H:%M', time.localtime())

print("Bienvenue dans l'utilitaire Espeak couplé à mbrola (non-free")
# texte = raw_input("tapez votre texte: ")
texte = "Bonjour mon nom est Kenobi !"
texte = texte.replace(" ", "/")
time.sleep(3)  # la fonction sleep seule n'éxiste pas l'associer au module time
command = "espeak -v mb-fr1 " + texte + " -s 130"
os.system(command)
