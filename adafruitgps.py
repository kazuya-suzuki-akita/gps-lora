#!/usr/bin/env python3

import serial
import threading
from datetime import date, time, timezone, timedelta

JST = timezone(timedelta(hours=+9), 'JST')

class AdafruitGPSDevice():
    def __init__(self, dev):
        self.serial = serial.Serial(dev, 9600)

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

    def write(self, msg):
        self.serial.write(msg.encode('utf-8'))

class AdafruitGPS():
    def __init__(self, dev):
        self.date = date.today()
        self.time = time(0, 0, 0)
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.separation = 0.0
        self.valid = False
        self.lock = threading.Lock()

        self.device = AdafruitGPSDevice(dev)
        self.device.write(self.add_cksum("$PMTK220,1000") + '\r\n')

    def add_cksum(self, msg):
        sum = 0
        char_list = list(msg)
        char_list.pop(0)
        for ch in char_list:
            sum ^= ord(ch)
        sum_str = format(sum, '02x')
        return msg + "*" + sum_str

    def calc_coordinate(self, data, direction):
        value = float(data) / 100
        degree = int(value)
        minutes = ( value - degree ) / 0.6
        latitude = float(degree) + minutes
        if direction == "S" or direction == "W":
            latitude *= -1
        return latitude

    def parse_time(self, time_string):
        hour = int(time_string[0:2])
        minute = int(time_string[2:4])
        second = int(time_string[4:6])
        microsecond = int(time_string[7:10]) * 1000
        return time(hour, minute, second, microsecond)

    def parse_date(self, date_string):
        year = 2000 + int(date_string[4:6])
        month = int(date_string[2:4])
        day = int(date_string[0:2])
        return date(year, month, day)

    def parse_rmc(self, elements):
        try:
            valid = True if elements[2] == "A" else False
            if valid == False:
                raise
            latitude = self.calc_coordinate(elements[3], elements[4])
            longitude = self.calc_coordinate(elements[5], elements[6])
            current_time = self.parse_time(elements[1])
            today = self.parse_date(elements[9])
        except:
            with self.lock:
                self.valid = False
        else:
            with self.lock:
                self.valid = valid
                self.latitude = latitude
                self.longitude = longitude
                self.time = current_time
                self.date = today

    def parse_gga(self, elements):
        try:
            valid = True if int(elements[6]) > 0 else False
            if valid == False:
                raise
            current_time = self.parse_time(elements[1])
            latitude = self.calc_coordinate(elements[2], elements[3])
            longitude = self.calc_coordinate(elements[4], elements[5])
            altitude = float(elements[9])
            separation = float(elements[11])
        except:
            with self.lock:
                self.valid = False
        else:
            with self.lock:
                self.valid = valid
                self.latitude = latitude
                self.longitude = longitude
                self.time = current_time
                self.altitude = altitude
                self.separation = separation

    def loop(self):
        while True:
            try:
                line = str(self.device.readline(), encoding='utf-8')
            except:
                pass
            else:
                if "$GPRMC" in line:
                    elements = line.split(",")
                    self.parse_rmc(elements)
                if "$GPGGA" in line:
                    elements = line.split(",")
                    self.parse_gga(elements)

def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    while True:
        line = str(gps.device.readline(), encoding='utf-8')
        if "$GPRMC" in line:
            elements = line.split(",")
            gps.parse_rmc(elements)
        if "$GPGGA" in line:
            elements = line.split(",")
            gps.parse_gga(elements)
        print(gps.latitude, gps.longitude, gps.altitude, gps.valid, sep=',')

if __name__ == "__main__":
    main()
