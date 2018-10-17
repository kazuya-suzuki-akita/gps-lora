#!/usr/bin/env python3
# prototype

import threading
from es920lr import ES920LR

def main():
    lora = ES920LR("/dev/ttyUSB0", "./config-USB0.ini")

    while True:
        line = lora.readline()
        if !line[0:7].isalnum():
            continue
        rssi, panid, srcid, msg = lora.parse(line)
        print('{},{},{},{}'.format(rssi, panid, srcid, msg)

if __name__ == "__main__":
    main()
