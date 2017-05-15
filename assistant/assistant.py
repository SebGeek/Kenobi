#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/config-dev-project-and-account

https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/configure-audio

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
