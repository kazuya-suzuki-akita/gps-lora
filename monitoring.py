#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

LEDPin = 36

class AliveMonitor():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(LEDPin, GPIO.OUT)

    def loop(self):
        while True:
            GPIO.output(LEDPin, 1)
            sleep(0.2)
            GPIO.output(LEDPin, 0)
            sleep(0.2)
