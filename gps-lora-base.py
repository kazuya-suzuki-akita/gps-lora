#!/usr/bin/env python3
# prototype

import sys
import threading
from datetime import datetime
from configparser import ConfigParser
from es920lr import ES920LR

def base_send_loop(lora):
    while True:
        lora.sendmsg(ACKMSG)
        time.sleep(10)

def main():
    config = ConfigParser()
    config.read(sys.argv[1])
    
    lora = ES920LR(config)
#    thread_send = threading.Thread(target=base_send_loop,args=(lora,))
#    thread_send.start()

    now = datetime.now()
    logprefix = "lora-r" + config['LoRa']['resetpin']
    logfile = now.strftime(logprefix + '-%Y%m%d%H%M%S.log')
    f = open(logfile, 'w')
    
    while True:
        line = lora.readline()
        if not line[0:7].isalnum():
            continue
        rssi, panid, srcid, msg = lora.parse(line)
        now = datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        f.write('{},{},{}\n'.format(now_str, msg, rssi))
        f.flush()

if __name__ == "__main__":
    main()
