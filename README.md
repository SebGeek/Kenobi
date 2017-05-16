# Kenobi
Kenobi robot is developed in Python on a Raspberry Pi 3.

## Functions
- Google Assistant, using the [Googla Assistant SDK for raspberry Pi](https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/)
- Autonomous mode
- Driven mode via an Andoïd device (Bluetooth connection), program created with [App Inventor](http://ai2.appinventor.mit.edu/?locale=en#4644884558643200)
- Affiche un visage qui bouge lorsqu’il parle
- Emet des sons de droïde
- Reconnaissance vocale
- Détection des obstacles par ultrason

## Future functions
- Face recognition
- Follow of a ball

## Picture
**photo robot**

**photo appli android**

## Functional diagram:
![photo Kenobi](Kenobi.jpg)

## Auto start-up
crontab -u pi -e
```@reboot python /home/pi/Kenobi/kenobi.py```
