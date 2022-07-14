import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def init():
    # set GPIO 17 as pull-up Input.
    GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)


def read_PIR():
    status = GPIO.input(17)
    return status


