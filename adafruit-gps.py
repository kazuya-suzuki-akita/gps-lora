#!/usr/bin/env python3

import serial
from datetime import date, time

class AdafruitGPS():
    def __init__(self, dev):
        self.serial = serial.Serial(dev, 9600)
        self.date = date.today()
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.separation = 0.0
        self.valid = False

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
        return time(hour, minute, second)

    def parse_date(self, date_string):
        year = 2000 + int(date_string[4:6])
        month = int(date_string[2:4])
        day = int(date_string[0:2])
        return date(year, month, day)

    def parse_rmc(self, elements):
        self.valid = True if elements[2] == "A" else False
        if self.valid == False:
            return
        self.latitude = self.calc_coordinate(elements[3], elements[4])
        self.longitude = self.calc_coordinate(elements[5], elements[6])
        self.time = self.parse_time(elements[1])
        self.date = self.parse_date(elements[9])

    def parse_gga(self, elements):
        self.valid = True if int(elements[6]) > 0 else False
        if self.valid == False:
            return
        self.valid = True
        self.time = self.parse_time(elements[1])
        self.latitude = self.calc_coordinate(elements[2], elements[3])
        self.longitude = self.calc_coordinate(elements[4], elements[5])
        self.altitude = float(elements[9])
        self.separation = float(elements[11])

def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    while True:
        line = str(gps.readline(), encoding='utf-8')
        if "$GPRMC" in line:
            elements = line.split(",")
            gps.parse_rmc(elements)
        if "$GPGGA" in line:
            elements = line.split(",")
            gps.parse_gga(elements)
        print(gps.latitude, gps.longitude, gps.altitude, gps.valid, sep=',')

if __name__ == "__main__":
    main()
