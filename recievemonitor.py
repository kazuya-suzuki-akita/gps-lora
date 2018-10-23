#!/usr/bin/env python3

import threading
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

LEDPin = 36

class RecieveMonitor():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(LEDPin, GPIO.OUT)

        self.lock = threading.lock()
        self.updated = datetime.now()

    def update(self):
        with self.lock():
            self.updated = datetime.now()

    def loop(self):
        while True:
            with self.lock():
                delta = ( datetime.now() - self.updated ).total_seconds()
            if delta < 20:
                GPIO.output(LEDPin, 1)
                sleep(0.5)
                GPIO.output(LEDPin, 0)
                sleep(0.5)
            else:
                sleep(2)

def main():
    monitor = RecieveMonitor()
    monitor.loop()

if __name__ == "__main__":
    main()
