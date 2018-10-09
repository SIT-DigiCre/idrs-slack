#!/usr/bin/env python3

import os
import time
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
        res = sc.api_call("chat.postMessage", channel = sendchannel, text = ":unlock: UNlocked" if isunlocked else ":lock: locked")
        keystatus = isunlocked
        if (res["ok"]):
            sendlog.append((res["channel"], res["ts"]))
        if (len(sendlog) > 10):
            mes = sendlog.pop(0)
            sc.api_call("chat.delete", channel = mes[0], ts = mes[1])
    time.sleep(1)
