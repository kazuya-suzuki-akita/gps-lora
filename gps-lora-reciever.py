#!/usr/bin/env python3
# prototype

import sys
import threading
from datetime import datetime
from es920lr import ES920LR

logprefix = 'lora-sf7-'

def main():
    lora = ES920LR("/dev/ttyUSB0", "./config-USB0.ini")

    now = datetime.now()
    logfile = now.strftime(logprefix + '%Y%m%d%H%M%S.log')
    f = open(logfile, 'w')
    
    while True:
        line = lora.readline()
        if not line[0:7].isalnum():
            continue
        rssi, panid, srcid, msg = lora.parse(line)
        now = datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        print('{},{},{}'.format(now_str, msg, rssi))
        f.write('{},{},{}\n'.format(now_str, msg, rssi))
        f.flush()

if __name__ == "__main__":
    main()
