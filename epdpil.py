#!/usr/bin/env python3

# Waveshare 7.5inch e-Ink display
# Refer to Waveshare Wiki: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT

 #  Copyright (C) Waveshare     July 10 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.

import spidev
import RPi.GPIO as GPIO
import io
import time
import numpy as np
from PIL import Image

# Config
CS_PIN    = 8
THRESHOLD = 210


# EPD7IN5 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
IMAGE_PROCESS                               = 0x13
LUT_FOR_VCOM                                = 0x20
LUT_BLUE                                    = 0x21
LUT_WHITE                                   = 0x22
LUT_GRAY_1                                  = 0x23
LUT_GRAY_2                                  = 0x24
LUT_RED_0                                   = 0x25
LUT_RED_1                                   = 0x26
LUT_RED_2                                   = 0x27
LUT_RED_3                                   = 0x28
LUT_XON                                     = 0x29
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_CALIBRATION                     = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
TCON_RESOLUTION                             = 0x61
SPI_FLASH_CONTROL                           = 0x65
REVISION                                    = 0x70
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
READ_VCOM_VALUE                             = 0x81
VCM_DC_SETTING                              = 0x82


class EPD:
    def __init__(self, width = 640, height = 384, reset_pin = 17, dc_pin = 25, cs_pin = 8, busy_pin = 24):
        self.width     = width
        self.height    = height
        self.reset_pin = reset_pin
        self.dc_pin    = dc_pin
        self.cs_pin    = cs_pin
        self.busy_pin  = busy_pin
        self.SPI = spidev.SpiDev(0, 0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.reset_pin, GPIO.OUT)
        GPIO.setup(self.dc_pin, GPIO.OUT)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.busy_pin, GPIO.IN)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b00

    def __del__(self):
        GPIO.cleanup(self.reset_pin)
        GPIO.cleanup(self.dc_pin)
        GPIO.cleanup(self.cs_pin)
        GPIO.cleanup(self.busy_pin)

    def digital_write(self, pin, val):
        GPIO.output(pin, val)

    def digital_read(self, pin):
        return GPIO.input(pin)

    def send_command(self, cmd):
        self.digital_write(self.dc_pin, GPIO.LOW)
        self.SPI.writebytes([cmd])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        self.SPI.writebytes([data])

    def wait_until_idle(self):
        while (self.digital_read(self.busy_pin) == 0):
            time.sleep(0.1)

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)
        time.sleep(0.2)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        time.sleep(0.2)

    def sleep(self):
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)
        self.send_data(0xa5)

    def init(self):
        self.reset()

        self.send_command(POWER_SETTING)
        self.send_data(0x37)
        self.send_data(0x00)

        self.send_command(PANEL_SETTING)
        self.send_data(0xCF)
        self.send_data(0x08)

        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0xc7)
        self.send_data(0xcc)
        self.send_data(0x28)

        self.send_command(POWER_ON)
        self.wait_until_idle()

        self.send_command(PLL_CONTROL)
        self.send_data(0x3c)

        self.send_command(TEMPERATURE_CALIBRATION)
        self.send_data(0x00)

        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x77)

        self.send_command(TCON_SETTING)
        self.send_data(0x22)

        self.send_command(TCON_RESOLUTION)
        self.send_data(0x02)     #source 640
        self.send_data(0x80)
        self.send_data(0x01)     #gate 384
        self.send_data(0x80)

        self.send_command(VCM_DC_SETTING)
        self.send_data(0x1E)      #decide by LUT file

        self.send_command(0xe5)           #FLASH MODE
        self.send_data(0x03)

    def get_frame_buffer(self, image, trh = THRESHOLD):
        buf = [0x00] * (self.width * self.height // 8)
        if (isinstance(image, str)): image = Image.open(image)
        if (image.size[0] != self.width or image.size[1] != self.height):
            raise ValueError("Image size error!")
        image = np.array(image.convert("L"))
        for y in range(self.height):
            for x in range(self.width):
                if (image[y, x] > trh):
                    buf[(x + y * self.width) // 8] |= 0x80 >> (x % 8)
        return buf

    def display_frame(self, fbuf):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, self.width * self.height // 8):
            temp1 = fbuf[i]
            for j in range(4):
                pixdata = 0x00
                if (temp1 & 0x80):
                    pixdata |= 0x30
                if (temp1 & 0x40):
                    pixdata |= 0x03
                temp1 = (temp1 << 2) & 0xff
                self.send_data(pixdata)
        self.send_command(DISPLAY_REFRESH)
        time.sleep(0.1)
        self.wait_until_idle()
