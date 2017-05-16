# Kenobi
Robot Kenobi developed in Python on a Raspberry Pi 3.

## Functions
- Google Assistant, using the [Googla Assistant SDK for raspberry Pi](https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/)
- Autonomous mode and driven mode via an Andoïd device, program created with [App Inventor](http://ai2.appinventor.mit.edu/?locale=en#4644884558643200)
- Affiche un visage qui bouge lorsqu’il parle
- Dirigeable par bluetooth depuis un smartphone
- Reconnaissance vocale
- Reconnaissance faciale pour saluer
- Depuis internet (si connexion Wifi disponible), indique si des mails ou messages Facebook sont disponibles
- Synthèse vocale
- Emet des sons de droïde
- Poursuite d’une balle rouge
- Détection des obstacles par ultrason

## Picture
**TBD**

## Functional diagram:
![photo Kenobi](Kenobi.jpg)

## Auto start-up
crontab -u pi -e
@reboot python /home/pi/Kenobi/kenobi.py
