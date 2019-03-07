#!/usr/bin/env python3

import sys
import time
from smbus2 import SMBusWrapper

while True:
    try:
        with SMBusWrapper(1) as bus:
            print(bus.read_byte_data(sys.argv[1], sys.argv[2]))
    except Exception as e:
        print(e)
    time.sleep(1)
