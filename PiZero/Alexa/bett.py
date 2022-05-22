import RPi.GPIO as GPIO
import time
import sys
from pathlib import Path

my_opt = str(sys.argv[1]) if len(sys.argv) > 1 else "stop"
print("bett.py called to do " + my_opt)

if my_opt == "kopf_hoch":
    # print("Kopf hoch!")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, True)
    Path('/home/pi/kh_status_on').touch()

elif my_opt == "kopf_runter":
    # print("Kopf runter!")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)
    GPIO.output(6, True)
    Path('/home/pi/kr_status_on').touch()

elif my_opt == "beine_hoch":
    # print("Beine hoch!")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, True)
    Path('/home/pi/bh_status_on').touch()

elif my_opt == "beine_runter":
    # print("Beine runter!")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, True)
    Path('/home/pi/br_status_on').touch()

else:
    for i in [ 5, 6, 13, 19 ]:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, False)
    for switch in [ 'kh', 'kr', 'bh', 'br' ]: 
        f = Path('/home/pi/' + switch + '_status_on')   
        if f.is_file():
            f.unlink() 

