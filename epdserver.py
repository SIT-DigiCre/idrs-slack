#!/usr/bin/env python3
import os
import socket
import json
from flask import Flask, request, jsonify
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from epdpil import EPD

# Config
PORT = 8081
epd = EPD()

epddata = { "imgpath": "", "txtlist": {} }
app = Flask(__name__)


def updateEPDData(req):
    global epddata
    if (len(req) == 0):
        return { "status": False, "data": epddata }
    if ("imgpath" in req and len(str(req["imgpath"])) > 0):
        if (os.path.isfile("./img/" + str(req["imgpath"]))):
            epddata["imgpath"] = str(req["imgpath"])
        else:
            return { "status": False, "data": epddata }
    if ("txtlist" in req):
        for key in req["txtlist"]:
            if (str(key) in epddata["txtlist"] and len(req["txtlist"][key]) == 0):
                epddata["txtlist"].pop(str(key))
                continue
            if (str(key) not in epddata["txtlist"] and ("text" not in req["txtlist"][key] or len(str(req["txtlist"][key]["text"])) == 0)):
                continue
            if ("text" in req["txtlist"][key]):
                if (str(key) in epddata["txtlist"]): epddata["txtlist"][str(key)]["text"] = req["txtlist"][key]["text"]
                else: epddata["txtlist"][str(key)] = { "text": req["txtlist"][key]["text"], "pos": (0, 0), "size": 36, "font": "ipaexg.ttf" }
            try:
                if ("posx" in req["txtlist"][key] and "posy" in req["txtlist"][key]):
                    epddata["txtlist"][str(key)]["pos"] = (int(req["txtlist"][key]["posx"]), int(req["txtlist"][key]["posy"]))
                elif ("pos" in req["txtlist"][key] and len(req["txtlist"][key]["pos"]) == 2): 
                    epddata["txtlist"][str(key)]["pos"] = (int(req["txtlist"][key]["pos"][0]), int(req["txtlist"][key]["pos"][1]))
                if ("size" in req["txtlist"][key]): epddata["txtlist"][str(key)]["size"] = int(req["txtlist"][key]["size"])
                if ("font" in req["txtlist"][key] and os.path.isfile("./img/fonts/" + str(req["txtlist"][key]["font"]))):
                    epddata["txtlist"][str(key)]["font"] = str(req["txtlist"][key]["font"])
            except:
                epddata["txtlist"].pop(str(key))
                return { "status": False, "data": epddata }
    return { "status": True, "data": epddata }

def updateEPD():
    with Image.open("./img/" + epddata["imgpath"]) as img:
        drw = ImageDraw.Draw(img)
        for drwtxt in epddata["txtlist"].values():
            drw.font = ImageFont.truetype("./img/fonts/" + drwtxt["font"], drwtxt["size"])
            drw.text(drwtxt["pos"], drwtxt["text"], (0, 0, 0))
        epd.init()
        epd.display_frame(epd.get_frame_buffer(img))
        epd.sleep()


# Exception define
class UserRequestError(Exception):
    pass

#
# Server
#
@app.route("/update", methods = ["post", "put"])
def updatepost():
    try:
        if (request.headers.get("Content-Type") == "application/json"):
            req = request.json
        else:
            if (not "data" in request.form): raise UserRequestError("data parameter isn't set!")
            req = json.loads(request.form["data"])
        epdupdateres = updateEPDData(req)
        response = jsonify(epdupdateres)
        response.status_code = 200 if epdupdateres["status"] else 400
        if epdupdateres["status"]:
            updateEPD()
    except UserRequestError as e:
        response = jsonify({ "status": False, "data": epddata, "message": "Bad request!\n" + str(e) })
        response.status_code = 400
    except json.JSONDecodeError as e:
        response = jsonify({ "status": False, "data": epddata, "message": "JSON decode error!\n" + str(e) })
        response.status_code = 400
    except Exception as e:
        response = jsonify({ "status": False, "data": epddata, "message": str(e) })
        response.status_code = 500
    response.mimetype = "application/json"
    return response

@app.route("/status", methods = ["get"])
def getstatus():
    response = jsonify({ "status": True, "data": epddata })
    response.status_code = 200
    response.mimetype = "application/json"
    return response

#
# main
#
app.run(host = "0.0.0.0", port = PORT, threaded = False)
