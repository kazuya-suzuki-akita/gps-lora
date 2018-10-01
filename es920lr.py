#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO
import time
import struct
from configparser import ConfigParser

ResetPin = 12

class ES920LR():
    def __init__(self, dev, filename="./config.ini"):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ResetPin, GPIO.OUT)
        GPIO.output(ResetPin, 1)

        self.dev = dev
        self.serial = serial.Serial(dev, 115200)

        self.readConfig(filename)
        self.setParameter()

    def readConfig(self, filename):
        self.config = ConfigParser()
        self.config.read(filename)

    def setParameters(self):
        self.sendcmd("2")
        self.sendcmd("x")
        self.sendcmd("a 2")
        self.sendcmd("b %s" % self.config['LoRa']['bw'])
        self.sendcmd("c %s" % self.config['LoRa']['sf'])
        self.sendcmd("d %s" % self.config['LoRa']['channel'])
        self.sendcmd("e %s" % self.config['LoRa']['panid'])
        self.sendcmd("f %s" % self.config['LoRa']['ownid'])
        self.sendcmd("g %s" % self.config['LoRa']['dstid'])
        self.sendcmd("l %s" % self.config['LoRa']['ack'])
        self.sendcmd("o %s" % self.config['LoRa']['rcvid'])
        self.sendcmd("p %s" % self.config['LoRa']['rssi'])
        self.sendcmd("u %s" % self.config['LoRa']['power'])
        self.sendcmd("z")

    def sendcmd(self, command):
        self.sendmsg(command)
        sleep(0.1)

    def sendmsg(self, message):
        line = "{0}\r\n".format(message).encode('utf-8')
        self.serial.write(line)

    def readline(self, timeout = None):
        if timeout != None:
            self.serial.close()
            self.serial.timeout = timeout
            self.serial.open()
        line = self.serial.readline()
        if timeout != None:
            self.serial.close()
            self.serial.timeout = None
            self.serial.open()
        return line

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
    while True:
        self.serial.sendmsg("test")
        sleep(10)

if __name__ == "__main__":
    main()
