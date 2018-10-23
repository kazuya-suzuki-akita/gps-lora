#!/usr/bin/env python3

import threading
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

class ReceiveMonitor():
    def __init__(self, config):
        self.ledpin = int(config['LED']['pin'])

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.ledpin, GPIO.OUT)

        self.updated = datetime.now() - datetime.timedelta(seconds=25)

    def update(self):
        self.updated = datetime.now()

    def loop(self):
        while True:
            delta = ( datetime.now() - self.updated ).total_seconds()
            if delta < 20:
                GPIO.output(self.ledpin, 1)
                sleep(0.5)
                GPIO.output(self.ledpin, 0)
                sleep(0.5)
            else:
                sleep(2)

def main():
    monitor = ReceiveMonitor()
    monitor.loop()

if __name__ == "__main__":
    main()
