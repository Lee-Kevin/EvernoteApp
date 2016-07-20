#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from evernote.api.client import EvernoteClient
from HTMLParser import HTMLParser
import talkey
from weather import weatherReport
import threading 
import time

logging.basicConfig(level='INFO')
# define a global threading lock 
Global_Lock = threading.Lock()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ToDo = []
        self.Flag = None
    def handle_starttag(self, tag, attrs):
        logging.info("Encountered a start tag: %s, %s", tag,attrs)
        if tag == "en-todo":
            logging.info( "this is to do tag:")
            if len(attrs) == 0:                                             # Here is the things that need to be done
                self.Flag = True
                logging.info("Here is need to be done")
            else:
                if (attrs[0][0] == "checked" and attrs[0][1] == "true"):
                    logging.info("Here is already done")
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.Flag == True:
            logging.info(data)
            self.Flag = False
            self.ToDo.append(data)
        else:
            pass

# 3bee4c0c-2caf-413c-9e49-d51da6fcdc8c
dev_token = "S=s1:U=92b7b:E=15d39d06877:C=155e21f3928:P=1cd:A=en-devtoken:V=2:H=1304173954fbc76d7432cdf262f7b228"
noteGuid  = "1e77d88b-49e6-4410-aaf5-c85c3bb70a0d"

tts = talkey.Talkey()
tts.say("This is a test")

# Sign in the Evernote
client = None
noteStore = None

def SignInEvernote():
    global client,noteStore 
    result = False
    try:
        client = EvernoteClient(token=dev_token)
        userStore = client.get_user_store()
        user = userStore.getUser()          # here will throw an error
        logging.info(user.username)
        noteStore = client.get_note_store()
        result    = True 
    except Exception, e:
        logging.warn(e)
    return result


def GetNoteContent(noteGuid):
    global noteStore
    content = None
    try:
        content = noteStore.getNoteContent(noteGuid)
    except Exception,e:
        logging.warn(e)
    return content

#parser = MyHTMLParser()
#parser.feed(content)

#This is the Time Out var.
TimeOutIndex = 0

weatherSpeach = None

def weatherInformation():
    speach       = None
    city         = "shenzhen"
    weather = weatherReport(city)
    if weather.getWeather() == True:
        speach = ("The weather is %s. Temperature: %.1f. Humidity: %.1f%%. Wind speed: %.1f meters per second" % (weather.weather_desc,weather.temperature,weather.humidity,weather.wind_speed))
        logging.info(speach)
    return speach

def GetWeatherThread():
    global weatherSpeach
    while True:
        try:
            speach = weatherInformation()
            if speach != None:
                Global_Lock.acquire()
                weatherSpeach = speach
                Global_Lock.release()
            else:
                pass
            time.sleep(10)
        except KeyboardInterrupt:

            break
        except Exception,e:
            logging.info(e)

# A Class to manage the thread
class GetWeatherInfoTask():
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self,TimeInterval):
        global Global_Lock
        while self._running:
            speach = weatherInformation()
            if speach != None:
                global Global_Lock
                Global_Lock.acquire()
                weatherSpeach = speach
                Global_Lock.release()
            else:
                pass
            time.sleep(TimeInterval)



if __name__ == "__main__":
#    Task1_weather = threading.Thread(target = GetWeatherThread,name = 'Weather Thread')
#    Task1_weather.start()
    Task1Weather = GetWeatherInfoTask()
    Task1WeatherThread = threading.Thread(target=Task1Weather.run, name="Weather Task", args=(5,))
    Task1WeatherThread.start()


    SignResult = SignInEvernote()
    while SignResult == False:
        TimeOutIndex = TimeOutIndex + 1
        if TimeOutIndex == 10:
            logging.warn("Can't Sign in the Evernote")
            TimeOutIndex = 0
            break
        SignResult = SignInEvernote()
    
    parser = MyHTMLParser()
    content = GetNoteContent(noteGuid)
    if content != None :
        parser.feed(content)
        for result in parser.ToDo:
            logging.info("The result is: %s",result)
            tts.say(result)
    else:
        pass
    logging.info("你好")
    while True:
        try:
            logging.info("This is in loop")
            time.sleep(10)
            Task1Weather.terminate()

        except KeyboardInterrupt:
            exit()
        except Exception, e:
            logging.info(e)
        if Task1WeatherThread.is_alive():
            logging.info("The Thread is still running")

        else:
            logging.info("The Thread isn't running")

            Task1WeatherThread = threading.Thread(target=Task1Weather.run, name="Weather Task", args=(5,))
            Task1WeatherThread.start()
            while True:
                time.sleep(3)
                logging.info("This is in Loop2")
