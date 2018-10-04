#!/usr/bin/env python3
# prototype

import threading
from adafruitgps import AdafruitGPS
from es920lr import ES920LR

def main():
    gps = AdafruitGPS("/dev/ttyUSB0")
    lora = ES920LR("/dev/ttyUSB1")

    thread_gps = threading.Thread(target=gps.loop)
    thread_sender = threading.Thread(target=lora.send_loop, args=(gps,))
    thread_reciever = threading.Thread(target=lora.recieve_loop)

    thread_gps.start()
    thread_sender.start()
    thread_reciever.start()

if __name__ == "__main__":
    main()
