#!/usr/bin/env python3

import sys
import threading
from time import sleep
from datetime import datetime
from configparser import ConfigParser
from es920lr import ES920LR
from queue import Queue

# default parameters
maxretry = 3
CONFIGFILE_OUT = "repeater-out.ini"
CONFIGFILE_IN = "repeater-in.ini"

def send_loop(lora, sendqueue):
    while True:
        msg = sendqueue.get()
        for i in range(maxretry):
            lora.sendmsg(msg)
            line = str(lora.readline(), encoding='utf-8')
            if 'OK' in line:
                break
            sleep(2)

def main():
    if len(sys.argv) >= 3:
        configfile_out = sys.argv[2]
    else:
        configfile_out = CONFIGFILE_OUT
    config_out = ConfigParser()
    config_out.read(configfile_out)
    lora_out = ES920LR(config_out)

    if len(sys.argv) >= 2:
        configfile_in = sys.argv[1]
    else:
        configfile_in = CONFIGFILE_IN
    config_in = ConfigParser()
    config_in.read(configfile_in)
    lora_in = ES920LR(config_in)

    sendqueue = Queue()
    thread_send = threading.Thread(
        target=send_loop,args=(lora_out,sendqueue,))
    thread_send.start()

    now = datetime.now()
    logprefix = "repeater-r" + config_in['LoRa']['resetpin']
    logfile = now.strftime(logprefix + '-%Y%m%d%H%M%S.log')
    f = open(logfile, 'w')

    while True:
        line = lora_in.readline()
        if not line[0:7].isalnum():
            f.write('Received unknown message')
        else:
            rssi, panid, srcid, msg = lora_in.parse(line)
            now = datetime.now()
            now_str = now.strftime('%Y%m%d%H%M%S')
            f.write('{},{},{}\n'.format(now_str, msg, rssi))
            sendqueue.put(msg)
        f.flush()

if __name__ == "__main__":
    main()
