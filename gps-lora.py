#!/usr/bin/env python3
# prototype

import threading
import adafruitgps
import es920lr

def initialize():
    gps = AdafruitGPS("/dev/ttyUSB0")
    lora = ES920LR("/dev/ttyUSB1")

def main():
    initialize()

    thread_gps = threading.Thread(target=gps.loop)
    thread_sender = threading.Thread(target=lora.send_loop)
    thread_reciever = threading.Thread(target=lora.recieve_loop)

    thread_gps.start()
    thread_sender.start()
    thread_reciever.start()

if __name__ == "__main__":
    main()
