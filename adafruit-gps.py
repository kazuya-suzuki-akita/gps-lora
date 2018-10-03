#!/usr/bin/env python3

import serial
from datetime import datetime

class AdafruitGPS():
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

    def calc_coordinate(data, direction):
        value = float(data) / 100
        degree = int(value)
        minutes = ( value - degree ) / 0.6
        latitude = float(degree) + minutes
        if direction == "S" or direction == "W":
            latitude *= -1
        return latitude

    def parse_rmc(self, elements):
        # calculate status
        if elements[2] == "A":
            valid = True
        else:
            valid = False

        # calculate latidude
        latitude = calc_coordinate(elements[3], elements[4])

        # calculate longitude
        longitude = calc_coordinate(elements[5], elements[6])

        # calculate time
        date_string = elements[9]
        year = 2000 + int(date_string[4:6])
        month = int(date_string[2:4])
        date = int(date_string[0:2])
        time_string = elements[1]
        hour = int(time_string[0:2])
        minute = int(time_string[2:4])
        second = int(time_string[4:6])
        time = datetime(year, month, date, hour, minute, second)

        return latitude, longitude, valid, time

    def parse_gga(self, elements):
        # calculate time
        time_string = elements[1]
        hour = int(time_string[0:2])
        minute = int(time_string[2:4])
        second = int(time_string[4:6])
        time = datetime(0, 0, 0, hour, minute, second)

        # calculate latidude
        latitude = calc_coordinate(elements[2], elements[3])

        # calculate longitude
        longitude = calc_coordinate(elements[4], elements[5])

        # calculate antennna altitude
        altitude = float(elements[9])

        # calculate geoidal separation
        separation = float(elements[11])

        return latidude, longitude, valid, time, altitude, separation

def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    while True:
        line = str(gps.readline(), encoding='utf-8')
        if "$GPRMC" in line:
            elements = line.split(",")
            latitude, longitude, valid, time = gps.parse_rmc(elements)
            print(latitude, longitude, sep=',')
        if "$GPGGA" in line:
            elements ~ line.split(",")
            latidude, longitude, valid, time, altitude, separation = parse_gga(elements)
            print(latitude, longitude, altitude,sep=',')



if __name__ == "__main__":
    main()
