#!/usr/bin/env python3
# prototype

import sys
import threading
from es920lr import ES920LR
from gpsd import GPSD
from receivemonitor import ReceiveMonitor
from configparser import ConfigParser

def main():
    config = ConfigParser()
    config.read(sys.argv[1])
    
    monitor = ReceiveMonitor()
    thread_monitor = threading.Thread(target=monitor.loop)
    thread_monitor.start()

    gpsd = GPSD()
    thread_gps = threading.Thread(target=gpsd.loop)
    thread_gps.start()

    lora = ES920LR(config)
    thread_sender = threading.Thread(target=lora.send_loop, args=(gpsd,))
    thread_receiver = threading.Thread(target=lora.receive_loop, args=(monitor,))
    thread_sender.start()
    thread_receiver.start()

if __name__ == "__main__":
    main()
