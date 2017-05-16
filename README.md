# Kenobi
Kenobi robot is developed in Python on a Raspberry Pi 3.

**photo robot**

## Functions
1. Google Assistant, using the [Googla Assistant SDK for raspberry Pi](https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/)

2. Driven mode via an Andoïd device (Bluetooth connection), program created with [App Inventor](http://ai2.appinventor.mit.edu/?locale=en#4644884558643200)

**photo appli android**

3. Autonomous mode
- Move randomly
- Avoid obstacles using an ultrasonic sensor
- Display a beating heart
- Play droïd sounds

## Future functions
- Face recognition
- Targeting of a tennis ball

## Functional diagram:
![photo Kenobi](Kenobi.jpg)

## Auto start-up

```
crontab -u pi -e
  @reboot python /home/pi/Kenobi/kenobi.py```
