#!/usr/bin/env python3

import serial
import RPi.GPIO as GPIO
import time
import struct
import threading
from configparser import ConfigParser
from datetime import datetime
from receivemonitor import ReceiveMonitor

ACKMSG = 'Received'

class ES920LR():
    def __init__(self, config):
        self.config = config
    
        self.resetpin = int(self.config['LoRa']['resetpin'])
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.resetpin, GPIO.OUT)
        GPIO.output(self.resetpin, 1)

        dev = self.config['LoRa']['device']
        self.serial = serial.Serial(dev, 115200)
        self.lock = threading.Lock()

        now = datetime.now()
        logfile = now.strftime('log-%Y%m%d%H%M%S.log')
        self.logfile = open(logfile, 'w')

        self.rssi = False
        self.rcvid = False
        self.binary = False

        self.reset()
        time.sleep(2.5)
        self.setParameters()
        
    def reset(self):
        GPIO.output(self.resetpin, 0)
        time.sleep(0.1)
        GPIO.output(self.resetpin, 1)

    def waitmsg(self, msg):
        # バイト列で比較
        line = self.readline()
        while not msg.encode('ascii') in line:
            line = self.readline()
    
    def setParameters(self):
        self.waitmsg("Select Mode")
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
        if self.config['LoRa']['rcvid'] == '1':
            self.rcvid = True
        self.sendcmd("p %s" % self.config['LoRa']['rssi'])
        if self.config['LoRa']['rssi'] == '1':
            self.rssi = True
        self.sendcmd("u %s" % self.config['LoRa']['power'])
        self.sendcmd("A %s" % self.config['LoRa']['format'])
        if self.config['LoRa']['format'] == '2':
            self.binary = True 
        self.sendcmd("z")

        self.readline(timeout=1)

    def sendcmd(self, command):
        line = command + '\r\n'
        self.serial.write(line.encode('ascii'))
        self.waitmsg('OK')

    def sendmsg(self, message):
        now = datetime.now()

        line = message + '\r\n'
        self.serial.write(line.encode('ascii'))

        log = now.strftime('%Y%m%d%H%M%S,') + message + '\n'
        self.logfile.write(log)
        self.logfile.flush()

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

    def readbinary(self):
        length = int.from_bytes(self.serial.read(1), byteorder='big')
        line = self.serial.read(length)
        return line
    
    def sendbinary(self, binmsg):
        now = datetime.now()

        line = len(binmsg).to_bytes(1, byteorder='big') + binmsg.encode()
        self.serial.write(line)

        log = now.strftime('%Y%m%d%H%M%S,') + binmsg + '\n'
        self.logfile.write(log)
        self.logfile.flush()

    def parse(self, line):
        if self.binary:
            fmt = '4s4s4s' + str(len(line) - 12) + 's'
        else:
            fmt = '4s4s4s' + str(len(line) - 14) + 'sxx'
        data = struct.unpack(fmt, line)
        hex2i = lambda x: int(x, 16) if int(x, 16) <= 0x7fff else ~ (0xffff - int(x, 16)) + 1
        rssi = hex2i(data[0])
        panid = hex2i(data[1])
        srcid = hex2i(data[2])
        msg = data[3].decode('ascii')
        return (rssi, panid, srcid, msg)

def main():
    lora = ES920LR("/dev/ttyUSB1") # 要修正
    while True:
        lora.sendmsg("test")
        time.sleep(10)

if __name__ == "__main__":
    main()
