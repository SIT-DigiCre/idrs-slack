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
    ksup = GPIO.input(keyStatusIn)
    if (ksup != keystatus):
        res = sc.api_call("chat.postMessage", channel = sendchannel, text = ":unlock: UNlocked" if ksup else ":lock: locked")
        keystatus = ksup
        if (res["ok"]):
            sendlog.append((res["channel"], res["ts"]))
        if (len(sendlog) > 10):
            mes = sendlog.pop(0)
            sc.api_call("chat.delete", channel = mes[0], text = mes[1])
    time.sleep(1)
