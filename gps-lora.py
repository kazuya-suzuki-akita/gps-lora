#!/usr/bin/env python3
# prototype

import time
import threading
import adafruitgps
import es920lr

def initialize():
    initialize_gps()
    initialize_lora()

def loop_gps():
    while True:

def loop_lora():
    while True:

if __name__ == "__main__":
    initialize()

    thread_gps = threading.Thread(target=loop_gps)
    thread_lora = threading.Thread(target=loop_lora)

    thread_gps.start()
    thread_lora.start()
