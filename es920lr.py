#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO
import time
import struct
from configparser import ConfigParser
import threading

ResetPin = 12

class ES920LR():
    def __init__(self, dev, configfile="./config.ini"):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ResetPin, GPIO.OUT)
        GPIO.output(ResetPin, 1)

        self.dev = dev
        self.serial = serial.Serial(dev, 115200)
        self.lock = threading.Lock()

        now = datetime.now()
        logfile = now.strftime('log-%Y%m%d%H%M%S.log', 'w')
        self.logfile = open(logfile)

        self.reset()
        time.sleep(2.5)
        self.readConfig(configfile)
        self.setParameters()

    def reset(self):
        GPIO.output(ResetPin, 0)
        time.sleep(0.1)
        GPIO.output(ResetPin, 1)

    def waitmsg(self, msg):
        line = str(self.readline(), encoding='utf-8')
        while msg in line:
            line = str(self.readline(), encoding='utf-8')

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
        time.sleep(0.1)

    def sendmsg(self, message):
        now = datetime.now()

        line = "{0}".format(message).encode('utf-8')
        self.serial.write(line + "\r\n")

        log = now.strftime(now.strftime('%Y%m%d%H%M%S,' + line + '\n'))
        self.logfile.write(log)

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

    def send_loop(self, gps):
        while True:
            with gps.lock:
                valid_str = 'T' if gps.valid == True else 'F'
                msg = '{}{},{:.5f},{:.5f},{},{},{}'.format(
                    gps.date.strftime('%y%m%d'), gps.time.strftime('%H%M%S'),
                    gps.latitude, gps.longitude, gps.altitude, gps.separation,
                    valid_str)
            self.sendmsg(msg)
            time.sleep(10)

    def recieve_loop(self):
        while True:
            self.readline() # 読み捨て
def main():
    lora = ES920LR("/dev/ttyUSB1")
    while True:
        lora.sendmsg("test")
        time.sleep(10)

if __name__ == "__main__":
    main()
