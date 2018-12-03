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
disptxt = ""
txtpos = (0, 0)
txtsize = 36

class UrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global imgpath
        global disptxt
        global txtpos
        global txtsize
        res = "failed"
        reqquery = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if ("imgpath" in reqquery): imgpath = reqquery["imgpath"][0]
        if ("disptxt" in reqquery): disptxt = reqquery["disptxt"][0]
        try:
            if ("txtposx" in reqquery and "txtposy" in reqquery): txtpos = (int(reqquery["txtposx"][0]), int(reqquery["txtposy"][0]))
        except:
            pass
        try:
            if ("txtsize" in reqquery): txtsize = int(reqquery["txtsize"][0])
        except:
            txtsize = 36
        if os.path.isfile("./img/" + imgpath):
            res = imgpath + " found!"
            img = Image.open("./img/" + imgpath)
            if (len(disptxt) > 0):
                drw = ImageDraw.Draw(img)
                drw.font = ImageFont.truetype("./img/IPAexfont00201/ipaexg.ttf", txtsize)
                drw.text(txtpos, disptxt, (0, 0, 0))
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
