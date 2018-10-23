#!/usr/bin/env python3
# prototype

import threading
from adafruitgps import AdafruitGPS
from es920lr import ES920LR
from alivemonitor import AliveMonitor
from configparser import ConfigParser

def main():
    config = ConfigParser()
    config.read(sys.argv[1])
    
    monitor = AliveMonitor()
    thread_monitor = threading.Thread(target=monitor.loop)
    thread_monitor.start()

    gps = AdafruitGPS(config)
    thread_gps = threading.Thread(target=gps.loop)
    thread_gps.start()

    lora = ES920LR(config)
    thread_sender = threading.Thread(target=lora.send_loop, args=(gps,))
    thread_reciever = threading.Thread(target=lora.recieve_loop)
    thread_sender.start()
    thread_reciever.start()

if __name__ == "__main__":
    main()
