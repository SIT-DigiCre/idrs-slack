#!/usr/bin/env python3

import os
import http.server
import socketserver
import urllib
from epdpil import EPD

# Config
PORT = 8081
epd = EPD()

class UrlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        res = "failed"
        imgpath = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if ("imgpath" in imgpath):
            imgpath = imgpath["imgpath"][0]
            if os.path.isfile("./img/" + imgpath):
                res = imgpath + " found!"
                epd.init()
                epd.display_frame(epd.get_frame_buffer("./img/" + imgpath))
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
