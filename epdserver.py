#!/usr/bin/env python3

import os
import http.server
import socketserver
import urllib
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from epdpil import EPD

# Config
PORT = 8081
epd = EPD()

imgpath = ""
txtlist = {}

class UrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global imgpath
        global txtlist
        res = "failed"
        reqquery = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if ("imgpath" in reqquery): imgpath = reqquery["imgpath"][0]
        txtkey = "0" if ("txtkey" not in reqquery) else reqquery["txtkey"][0]
        if ("disptxt" in reqquery):
            if (txtkey not in txtlist): txtlist[txtkey] = { "pos": (0, 0), "size": 36 }
            txtlist[txtkey]["text"] = reqquery["disptxt"][0]
            if (len(txtlist[txtkey]["text"]) == 0): txtlist.pop(txtkey)
        try:
            if ("txtposx" in reqquery and "txtposy" in reqquery): txtlist[txtkey]["pos"] = (int(reqquery["txtposx"][0]), int(reqquery["txtposy"][0]))
        except:
            pass
        try:
            if ("txtsize" in reqquery): txtlist[txtkey]["size"] = int(reqquery["txtsize"][0])
        except:
            pass
        if os.path.isfile("./img/" + imgpath):
            res = imgpath + " found!"
            with Image.open("./img/" + imgpath) as img:
                drw = ImageDraw.Draw(img)
                for drwtxt in txtlist.values():
                    drw.font = ImageFont.truetype("./img/fonts/ipaexg.ttf", drwtxt["size"])
                    drw.text(drwtxt["pos"], drwtxt["text"], (0, 0, 0))
                epd.init()
                epd.display_frame(epd.get_frame_buffer(img))
                epd.sleep()
        else:
            res = imgpath + " not found!"
        print(res)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(res.encode("utf-8"))
        return

with socketserver.TCPServer(("", PORT), UrlHandler) as httpd:
    httpd.serve_forever()
