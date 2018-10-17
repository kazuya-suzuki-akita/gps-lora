#!/usr/bin/env python3
# 更新間隔設定(単位 ms)
# $PMTK220,1000
# GPRMC 及び GPGGA のみ受信
# $PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

from sys import argv
from adafruitgps import AdafruitGPS

def main():
    if len(argv) != 2:
        print('Usage: %s cmd' % argv[0])
        quit()
    cmd = argv[1]
    gps = AdafruitGPS("/dev/ttyS0")
    gps.device.write(gps.add_cksum(cmd) + '\r\n')

if __name__ == "__main__":
    main()
