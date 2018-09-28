#!/usr/bin/env python3

import serial
from datetime import datetime

class AdafruitGPS():
    def __init__(self, dev):
        self.s = serial.Serial(dev, 9600)

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

    def parse_gprmc(self, elements):
        # calculate latidude
        value = float(elements[2]) / 100
        degree = int(value)
        minutes = ( value - degree ) / 0.6
        latitude = float(degree) + minutes
        if elements[3] == "S":
            latitude *= -1

        # calculate longitude
        value = float(elements[4]) / 100
        degree = int(value)
        minutes = ( value - degree ) / 0.6
        longitude = float(degree) + minutes
        if elements[5] == "W":
            longitude *= -1

        # calculate status
        if elements[1] == "A":
            valid = True
        else:
            valid = False

        # calculate time
        date_string = elements[8]
        year = 2000 + int(date_string[4:6])
        month = int(date_string[2:4])
        date = int(date_string[0:2])
        time_string = elements[0]
        hour = int(time_string[0:2])
        minute = int(time_string[2:4])
        second = int(time_string[4:6])
        time = datetime(year, month, date, hour, minute, second)

        return latitude, longitude, valid, time


def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    while True:
        line = str(gps.readline(), encoding='utf-8')
        if "$GPRMC" in line:
            elements = line.split(",")
            elements.pop(0)
            latitude, longitude, valid, time = gps.parse_gprmc(elements)
            print(latitude, longitude, sep=',')

if __name__ == "__main__":
    main()
