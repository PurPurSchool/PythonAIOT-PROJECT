import RPi.GPIO as GPIO
from time import sleep
import sys
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)

def init():
    reader = SimpleMFRC522()



