#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
1. https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/config-dev-project-and-account

2. https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/configure-audio
Verify that recording and playback work:

# Play a test sound (this will be a person speaking). Press Ctrl+C when done.
# If you don't hear anything when you run this, check your speaker connection.
speaker-test -t wav

# Record a short audio clip.
arecord --format=S16_LE --duration=5 --rate=16k --file-type=raw out.raw
# Check the recording by replaying it.
aplay --format=S16_LE --rate=16k out.raw

# Adjust the playback and recording volume.
alsamixer
If recording and playback are working, then you are done configuring audio. If not (or if you receive an error), continue to the next step below.
Find your recording and playback devices.

# Note the card number and device number for recording.
arecord -l
# Note the card number and device number for playback.
aplay -l
Create a new file named .asoundrc in the home directory (/home/pi). Make sure it has the right slave definitions for microphone and speaker:

pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:<card number>,<device number>"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:<card number>,<device number>"
  }
}


3.
sudo apt-get update
sudo apt-get install python3-dev python3-venv
python3 -m venv env
env/bin/python -m pip install pip setuptools --upgrade
source env/bin/activate

python -m googlesamples.assistant.auth_helpers --client-secrets /home/pi/client_secret_xxx.googleusercontent.com.json

python -m googlesamples.assistant

https://console.developers.google.com/apis/api/embeddedassistant.googleapis.com/overview?project=api-assistant

pip install RPi.GPIO

** Start assistant:
source /home/pi/env/bin/activate
python -m googlesamples.assistant
OR:
/home/pi/env/bin/python -m googlesamples.assistant

** Source modified:
/home/pi/env/lib/python3.4/site-packages/googlesamples/assistant/__main__.py

* AUTOMATIC start-up
crontab -u pi -e
@reboot /home/pi/env/bin/python -m googlesamples.assistant

'''
