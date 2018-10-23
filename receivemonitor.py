#!/usr/bin/env python3

import threading
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

class ReceiveMonitor():
    def __init__(self, config):
        ledpin = int(config['LED']['pin'])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ledpin, GPIO.OUT)

        self.lock = threading.Lock()
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
    monitor = ReceiveMonitor()
    monitor.loop()

if __name__ == "__main__":
    main()
