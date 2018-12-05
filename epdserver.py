#!/usr/bin/env python3
import os
import socket
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from epdpil import EPD

# Config
PORT = 5001
epd = EPD()

epddata = { "imgpath": "", "txtlist": {} }


def updateEPDData(req):
    global epddata
    if ("imgpath" in req and len(str(req["imgpath"])) > 0):
        if (os.path.isfile("./img/" + str(req["imgpath"]))):
            epddata["imgpath"] = str(req["imgpath"])
        else:
            return { "res": False, "epddata": epddata }
    if ("txtlist" in req):
        for key in req["txtlist"]:
            if (str(key) in epddata["txtlist"] and len(req["txtlist"][key]) == 0):
                epddata["txtlist"].pop(str(key))
                continue
            if (str(key) not in epddata["txtlist"] and ("text" not in req["txtlist"][key] or len(str(req["txtlist"][key]["text"])) == 0)):
                continue
            if ("text" in req["txtlist"][key]): epddata["txtlist"][str(key)]["text"] = req["txtlist"][key]["text"]
            try:
                if ("posx" in req["txtlist"][key] and "posy" in req["txtlist"][key]):
                    epddata["txtlist"][str(key)]["pos"] = (int(req["txtlist"][key]["posx"]), int(req["txtlist"][key]["posy"]))
                elif ("pos" in req["txtlist"][key] and len(req["txtlist"][key]["pos"]) == 2): 
                    epddata["txtlist"][str(key)]["pos"] = (int(req["txtlist"][key]["pos"][0]), int(req["txtlist"][key]["pos"][1]))
                else: epddata["txtlist"][str(key)]["pos"] = (0, 0)
                if ("size" in req["txtlist"][key]): epddata["txtlist"][str(key)]["size"] = int(req["txtlist"][key]["size"])
                else: epddata["txtlist"][str(key)]["size"] = 36
                if ("font" in req["txtlist"][key] and os.path.isfile("./img/fonts/" + str(req["txtlist"][key]["font"]))):
                    epddata["txtlist"][str(key)]["font"] = str(req["txtlist"][key]["font"])
                else: epddata["txtlist"][str(key)]["font"] = "ipaexg.ttf"
            except:
                epddata["txtlist"].pop(str(key))
                return { "res": False, "epddata": epddata }
    return { "res": True, "epddata": epddata }

def updateEPD():
    with Image.open("./img/" + epddata["imgpath"]) as img:
        drw = ImageDraw.Draw(img)
        for drwtxt in epddata["txtlist"].values():
            drw.font = ImageFont.truetype("./img/fonts/" + drwtxt["font"], drwtxt["size"])
            drw.text(drwtxt["pos"], drwtxt["text"], (0, 0, 0))
        epd.init()
        epd.display_frame(epd.get_frame_buffer(img))
        epd.sleep()


#
# main
#
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

while 1:
    try:
        data, addr = sock.recvfrom(3072)
        print(data.decode("utf-8"))
        print("    len:  " + str(len(data)))
        print("    from: " + addr[0] + ":" + str(addr[1]))
        epdupdateres = updateEPDData(json.loads(data.decode("utf-8")))
        sock.sendto(json.dumps(epdupdateres).encode("utf-8"), addr)
        if epdupdateres["res"]:
            updateEPD()
    except:
        sock.sendto(json.dumps({ "res": False, "epddata": epddata }).encode("utf-8"), addr)
