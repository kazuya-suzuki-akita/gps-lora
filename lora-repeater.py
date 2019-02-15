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
configfile_out = "repeater_out.ini"
configfile_in = "repeater_in.ini"

def repeater_send_loop(lora, sendqueue):
    msg = sendqueue.get()
    for i in range(maxretry):
        lora.sendmsg(msg)
        line = str(lora.readline(), encoding='utf-8')
        if 'OK' in line:
            break
        sleep(1)

def main():
    if len(sys.argv) >= 3:
        configfile_out = sys.argv[2]
    config_out = ConfigParser()
    config_out.read(configfile_out)
    lora_out = ES920LR(config_out)

    if len(sys.argv) >= 2:
        configfile_out = sys.argv[1]
    config_in = ConfigParser()
    config_in.read(configfile_in)
    lora_in = ES920LR(config_in)

    sendqueue = Queue()
    thread_send = threading.Thread(
        target=repeater_send_loop,args=(lora_out,sendqueue,))
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
            rssi, panid, srcid, msg = lora.parse(line)
            now = datetime.now()
            now_str = now.strftime('%Y%m%d%H%M%S')
            f.write('{},{},{}\n'.format(now_str, msg, rssi))
            sendqueue.put(line)
        f.flush()

if __name__ == "__main__":
    main()
