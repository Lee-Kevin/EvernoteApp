# Evernote
-----
## Intrudction
This is an APP that can read the weather info form the openweathermap as well as the Evernote note and then speak it out

## Install Espeak
* Open your favourite terminate and excute the following commands
```
sudo apt-get install python-dev
```
```
sudo agt-get install espeak
sudo apt-get install python-espeak
```
* Test it
```
espeak "hello world"
```
## Install Talkey
[Talkey](http://talkey.readthedocs.org/) is a simple Text-To-Speech (TTS) interface library with multi-language and multi-engine support.
* Install from talkey
```
pip install talkey
```
* Test it in python 
```
import talkey
tts = talkey.Talkey()
tts.say('Old McDonald had a farm')
```
