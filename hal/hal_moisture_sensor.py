import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def init():
    # set GPIO 4 as pull-up Input.
    GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)


def read_Moisture():
    status = GPIO.input(4)
    return status


