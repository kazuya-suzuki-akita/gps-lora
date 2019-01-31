#!/usr/bin/env python3
# prototype

import sys
import threading
from es920lr import ES920LR
from gpsd import GPSD
from receivemonitor import ReceiveMonitor
from configparser import ConfigParser

def send_loop(lora, gps):
    while True:
    with gps.lock:
        valid_str = 'T' if gps.valid == True else 'F'
        now = datetime.now()
	msg = '{},{:.5f},{:.5f},{},{},{}'.format(
            now.strftime('%y%m%d%H%M%S'),
            gps.latitude, gps.longitude, gps.altitude, gps.separation,
            valid_str)
        lora.sendmsg(msg)
        time.sleep(10)

def receive_loop(lora, monitor):
    while True:
        try:
            line = str(lora.readline(), encoding='utf-8')
            if ACKMSG in line:
                monitor.update()
        except:
            pass

def main():
    config = ConfigParser()
    config.read(sys.argv[1])
    
    monitor = ReceiveMonitor(config)
    thread_monitor = threading.Thread(target=monitor.loop)
    thread_monitor.start()

    gpsd = GPSD()
    thread_gps = threading.Thread(target=gpsd.loop)
    thread_gps.start()

    lora = ES920LR(config)
    thread_sender = threading.Thread(target=send_loop, args=(lora,gpsd,))
    thread_receiver = threading.Thread(target=receive_loop, args=(lora,monitor,))
    thread_sender.start()
    thread_receiver.start()

if __name__ == "__main__":
    main()
