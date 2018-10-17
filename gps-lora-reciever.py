#!/usr/bin/env python3
# prototype

import threading
from es920lr import ES920LR

def main():
    lora = ES920LR("/dev/ttyUSB0", "./config-USB0.ini")

    while True:
        line = self.readline()
        print(line)    

if __name__ == "__main__":
    main()
