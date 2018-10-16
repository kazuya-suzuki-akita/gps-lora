#!/usr/bin/env python3
# prototype

import threading
from adafruitgps import AdafruitGPS
from es920lr import ES920LR
from alivemonitor import AliveMonitor

def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    lora = ES920LR("/dev/ttyUSB1")
    monitor = AliveMonitor()

    thread_gps = threading.Thread(target=gps.loop)
    thread_sender = threading.Thread(target=lora.send_loop, args=(gps,))
    thread_reciever = threading.Thread(target=lora.recieve_loop)
    thread_monitor = threading.Thread(target=monitor.loop)

    thread_gps.start()
    thread_sender.start()
    thread_reciever.start()
    thread_monitor.start()

if __name__ == "__main__":
    main()
