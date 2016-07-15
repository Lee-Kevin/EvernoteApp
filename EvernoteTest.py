#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from evernote.api.client import EvernoteClient
from HTMLParser import HTMLParser
logging.basicConfig(level='INFO')

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

client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()          # here will throw an error
print user.username
noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
    print n.name

content = noteStore.getNoteContent(noteGuid)
print(content)

parser = MyHTMLParser()
parser.feed(content)

for result in parser.ToDo:
    logging.info("The result is: %s",result)
if __name__ == "__main__":
    logging.info("你好")