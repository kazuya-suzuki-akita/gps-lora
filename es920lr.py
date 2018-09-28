#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO
import time
import struct

ResetPin = 12

class ES920LR():
    def __init__(self, dev):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ResetPin, GPIO.OUT)
        GPIO.output(ResetPin, 1)

        self.dev = dev
        self.s = serial.Serial(dev, 115200)

    def readline(self, timeout = None):
        if timeout != None:
            self.s.close()
            self.s.timeout = timeout
            self.s.open()
        line = self.s.readline()
        if timeout != None:
            self.s.close()
            self.s.timeout = None
            self.s.open()
        return line

    def write(self, msg):
        self.s.write(msg.encode('utf-8'))

    def parse(self, line):
        fmt = '4s4s4s' + str(len(line) - 14) + 'sxx'
        data = struct.unpack(fmt, line)
        hex2i = lambda x: int(x, 16) if int(x, 16) <= 0x7fff else ~ (0xffff - int(x, 16)) + 1
        rssi = hex2i(data[0])
        panid = hex2i(data[1])
        srcid = hex2i(data[2])
        msg = data[3].decode('utf-8')
        return (rssi, panid, srcid, msg)

def main():
    lora = ES920LR("/dev/ttyUSB1")
    while
    print("ES920LR module")

if __name__ == "__main__":
    main()
