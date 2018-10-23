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

        self.reset()
        time.sleep(2.5)
        self.setParameters()
        
    def reset(self):
        GPIO.output(self.resetpin, 0)
        time.sleep(0.1)
        GPIO.output(self.resetpin, 1)

    def waitmsg(self, msg):
        line = str(self.readline(), encoding='utf-8')
        while msg in line:
            line = str(self.readline(), encoding='utf-8')

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
        line = command + '\r\n'
        self.serial.write(line.encode('utf-8'))
        time.sleep(0.1)

    def sendmsg(self, message):
        now = datetime.now()

        line = message + '\r\n'
        self.serial.write(line.encode('utf-8'))

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

    def parse(self, line):
        fmt = '4s4s4s' + str(len(line) - 14) + 'sxx'
        data = struct.unpack(fmt, line)
        hex2i = lambda x: int(x, 16) if int(x, 16) <= 0x7fff else ~ (0xffff - int(x, 16)) + 1
        rssi = hex2i(data[0])
        panid = hex2i(data[1])
        srcid = hex2i(data[2])
        msg = data[3].decode('utf-8')
        return (rssi, panid, srcid, msg)

    def terminal_send_loop(self, gps):
        while True:
            with gps.lock:
                valid_str = 'T' if gps.valid == True else 'F'
                now = datetime.now()
                msg = '{},{:.5f},{:.5f},{},{},{}'.format(
                    now.strftime('%y%m%d%H%M%S'),
                    gps.latitude, gps.longitude, gps.altitude, gps.separation,
                    valid_str)
            self.sendmsg(msg)
            time.sleep(10)

    def terminal_receive_loop(self, monitor):
        while True:
            try:
                line = str(self.readline(), encoding='utf-8')
                if ACKMSG in line:
                    monitor.update()
                    print('updated')
            except:
                pass

    def base_send_loop(self):
        while True:
            self.sendmsg(ACKMSG)
            time.sleep(10)

def main():
    lora = ES920LR("/dev/ttyUSB1") # 要修正
    while True:
        lora.sendmsg("test")
        time.sleep(10)

if __name__ == "__main__":
    main()
