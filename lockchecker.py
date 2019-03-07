#!/usr/bin/env python3

import os
import time
import urllib.request
import urllib.parse
import json
from smbus2 import SMBusWrapper
from slackclient import SlackClient

sendchannel = "#bushitsu-locklog"
#sendchannel = "idrs-develop"
i2caddr = 8

keystatus = None
isunlocked = False

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
sc.api_call("chat.postMessage", channel = sendchannel, text = "Hello. I woke up!")

sendlog = []
while True:
    try:
        with SMBusWrapper(1) as bus:
            readval = bus.read_byte_data(i2caddr, 0)
            if (160 < readval and readval < 200):
                isunlocked = True
            elif (100 < readval and readval < 140):
                isunlocked = False
    except OSError:
        pass
    if (isunlocked != keystatus):
        try:
            res = sc.api_call("chat.postMessage", channel = sendchannel, text = ":unlock: UNlocked" if isunlocked else ":lock: locked")
        except Exception as e:
            print("Slack chat.postMessage error")
            print(e)
        keystatus = isunlocked
        if (res["ok"]):
            sendlog.append((res["channel"], res["ts"]))
        if (len(sendlog) > 10):
            mes = sendlog.pop(0)
            try:
                sc.api_call("chat.delete", channel = mes[0], ts = mes[1])
            except Exception as e:
                print("Slack chat.delete error")
                print(e)
        # Send e-paper display update request
        try:
            req = urllib.request.Request("http://epdserver:8081/update", urllib.parse.urlencode({ "data": json.dumps({ "imgpath": "disp-" + ("open" if isunlocked else "close") + ".png" }) }).encode("utf-8"))
            with urllib.request.urlopen(req) as res:
                print(res.read())
        except Exception as e:
            print("EPD server communication error")
            print(e)
    time.sleep(1)
