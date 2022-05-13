# Example assumes a connected piezo buzzer
# Here we output morse signals with the function send_text
from machine import Pin, PWM
from utime import sleep_ms

dit = 150     # milliseconds for short signal
duration_ms = {0: dit, 1: dit, 2: dit + dit + dit}   # 0: pause, 1: dit/short, 2: dah/long

alphabet = { 'a': [1,2], 'b': [2,1,1,1], 'c': [2,1,2,1], 'd': [2,1,1], 'e': [1], 'f': [1,1,2,1], 'g': [2,2,1], 'h': [1,1,1,1],
             'i': [1,1], 'j': [1,2,2,2], 'k': [2,1,2], 'l': [1,2,1,1], 'm': [2,2], 'n': [2,1], 'o': [2,2,2], 'p': [1,2,2,1],
             'q': [2,2,1,2], 'r': [1,2,1], 's': [1,1,1], 't': [2], 'u': [1,1,2], 'v': [1,1,1,2], 'w': [1,2,2], 'x': [2,1,1,2],
             'y': [2,1,2,2], 'z': [2,2,1,1], 'ä': [1,2,0,0,1], 'ö': [2,2,2,0,0,1], 'ü': [1,1,2,0,0,1], 'ß': [1,1,1,0,0,1,1,1],
             '0': [2,2,2,2,2], '1': [1,2,2,2,2], '2': [1,1,2,2,2], '3': [1,1,1,2,2], '4': [1,1,1,1,2], '5': [1,1,1,1,1], 
             '6': [2,1,1,1,1], '7': [2,2,1,1,1], '8': [2,2,2,1,1], '9': [2,2,2,2,1], ' ': [0,0,0,0,0,0], '.': [1,2,1,2,1,2]
           }
led = Pin(15, Pin.OUT) # Port GP15 is at Pin #20
buzzer = PWM(Pin(20))  # Port GP20 is at Pin #26
buzzer.freq(880)       # simulate morse beep

def send(signal_list):
    for signal in signal_list:
        if signal > 0:                     # only turn on when there is something to see
            buzzer.duty_u16(1000)          # turn buzzer to maximum loudness
            led.value(1)                   # turn on led for long or short signal
            sleep_ms(duration_ms[signal])  # leave led on for duration of signal
        buzzer.duty_u16(0)                 # shut off buzzer sound
        led.value(0)                       # turn off led after signal; cannot hurt at pause
        sleep_ms(duration_ms[0])           # pause 1 dit at signal end
                    
def send_text(text):
    for char in text:
        send(alphabet[char.lower()])       # already has 1 dit pause
        send([0,0])                        # pause at char end = 3 dits
    send([0,0,0,0])                        # pause at word end = 7 dits

for i in range(3):
    send_text('SOS')
