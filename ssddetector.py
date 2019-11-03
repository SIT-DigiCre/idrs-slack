#!/usr/bin/env python3

import collections
import os
import time
import json
from picamera import PiCamera
from slackclient import SlackClient
from ssdlib import SSDLib

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
ssdlib = SSDLib('weights_SSD300.hdf5')

while True:
    try:
        time.sleep(60)
        jsondata = {}
        with open('tmpdata.json') as f:
            jsondata = json.load(f)
        if not jsondata["unlocked"]:
            continue
        estList = []
        pcam = PiCamera()
        for i in range(10):
            pcam.capture('/tmp/image.jpg')
            res = ssdlib.predict(['/tmp/image.jpg'])
            estList.append(len(ssdlib.getObjects(res[0], 'Person')))
        modeval = collections.Counter(estList).most_common()[0][0]
        colorCode = "#00ef00"
        if 3 < modeval:
            colorCode = "#efef00"
        if 7 < modeval:
            colorCode = "#ef0000"
        nowtime = time.localtime()
        timestr = ('0' + str(nowtime.tm_hour))[-2:] + ':' + ('0' + str(nowtime.tm_min))[-2:]
        msg = jsondata["msg"] + "\n" + colorCode + " estimated " + str(modeval) + " person(s), " + timestr
        sc.api_call("chat.update", channel = jsondata["channel"], ts = jsondata["ts"], text = msg)
    except Exception as e:
        print(e)
