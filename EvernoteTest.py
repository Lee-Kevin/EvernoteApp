#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from evernote.api.client import EvernoteClient
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag, attrs

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data


# 3bee4c0c-2caf-413c-9e49-d51da6fcdc8c
dev_token = "S=s1:U=92b7b:E=15d39d06877:C=155e21f3928:P=1cd:A=en-devtoken:V=2:H=1304173954fbc76d7432cdf262f7b228"
noteGuid  = "1e77d88b-49e6-4410-aaf5-c85c3bb70a0d"

client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username
noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
    print n.name

content = noteStore.getNoteContent(noteGuid)
print(content)

parser = MyHTMLParser()
parser.feed(content)


if __name__ == "__main__":
    print("你好")