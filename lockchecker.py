#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
from slackclient import SlackClient

sendchannel = "#bushitsu-locklog"
#sendchannel = "idrs-develop"
keyStatusIn = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(keyStatusIn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
keystatus = False

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
sc.api_call("chat.postMessage", channel = sendchannel, text = "Hello. I woke up!")

sendlog = []
while True:
    ksbf = GPIO.input(keyStatusIn)
    if (ksbf != keystatus):
        if (ksbf):
            res = sc.api_call("chat.postMessage", channel = sendchannel, text = ":unlock: UNlocked")
        else:
            res = sc.api_call("chat.postMessage", channel = sendchannel, text = ":lock: locked")
        keystatus = ksbf
        if (res["ok"]):
            sendlog.append((res["channel"], res["ts"]))
        if (len(sendlog) > 10):
            mes = sendlog.pop(0)
            sc.api_call("chat.delete", channel = mes[0], text = mes[1])
    time.sleep(1)
