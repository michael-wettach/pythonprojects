# Assumes connections to 1 LED as "on" indicator and 4 buttons.
# Buttons are used to select songs and to end program execution.
# Also one passive piezo buzzer to play the songs.
from machine import Pin, PWM
from utime import sleep_ms
import _thread
import re

button1 = Pin(11, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
button4 = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT) # Port GP15 is at Pin #20
buzzer = PWM(Pin(16))  # Port GP16 is at Pin #21

global button1_pressed
global button2_pressed
global button3_pressed
global button4_pressed

def button_reader_thread():
    global button1_pressed
    global button2_pressed
    global button3_pressed
    global button4_pressed
    while True:
        if button1.value() == 1:
            button1_pressed = True
        if button2.value() == 1:
            button2_pressed = True
        if button3.value() == 1:
            button3_pressed = True
        if button4.value() == 1:
            button4_pressed = True
        sleep_ms(10)    


# The frequencies were derived from Wikipedia (well-tempered tuning)
# Sometimes they do not sound ideal but you can experiment youself...
frequencies = { 'C': 523, 'C#': 554, 'Db': 554, 'D': 587, 'D#': 622, 'Eb': 622, 'E': 659, 'F': 698, 'F#': 740, 
                'Gb': 740, 'G': 784, 'G#': 831, 'Ab': 831, 'A': 880, 'A#': 932, 'Bb': 932, 'B': 988, '_': 0 }
oct_multiplier = [0, 0, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]

def play_note(key, octave, duration):
    frequency = round(frequencies[key] * oct_multiplier[octave])
    if frequency > 100 and frequency < 12000:
        buzzer.freq(frequency)
        buzzer.duty_u16(1000)   # maximum loudness
    sleep_ms(duration-9)        # duration needs to be > 9ms
    buzzer.duty_u16(0)          # shut off sound
    sleep_ms(9)                 # to have a distinct signal on/off 
        
def play_song(song):
    # command syntax: Mnnn=metronome bpm, Nnnn=#notes per quarter, nXn=length/note/octave
    metronome  = re.compile(r'^M(\d\d?\d?)$')
    numnotes   = re.compile(r'^N(\d\d?\d?)$')
    singlenote = re.compile(r'^(\d?\d?\d?)(C|C#|Db|D|D#|Eb|E|F|F#|Gb|G|G#|Ab|A|A#|Bb|B|_)(\d?)$')
    # defaults are 100 beats per minute, 2 notes per quarter (1/8), length 2/8 and octave 4 
    bpm, npq, def_len, def_oct = 100, 2, 2, 4
    for event in song.split(','):
        if singlenote.match(event):
            xlen, key, xoct = singlenote.search(event).groups()
            xlen = def_len if xlen == '' else xlen
            xoct = def_oct if xoct == '' else xoct
            duration = round((int(xlen)/npq)*(60000/bpm))
            play_note(key, int(xoct), duration)
        elif metronome.match(event):
            bpm = int(metronome.search(event).groups()[0])
        elif numnotes.match(event):
            npq = int(numnotes.search(event).groups()[0])
            def_len = npq
               
songs = { 'fanfare': 'M140,C5,1G,1G,Ab,G,_,1B,1_,2C5', 'birthday': 'M120,1C,1C,D,C,F,4E,1C,1C,D,C,G,4F,1C,1C,C5,A,F,E,D,1Bb,1Bb,A,F,G,2F',
          'harry': 'M66,N4,2B,3E5,1G5,2F#5,E5,2B5,6A5,6F#5,3E5,1G5,2F#5,D#5,2F5,10B,2B,3E5,1G5,2F#5,E5,2B5,D6,2Db6,C6,2Ab5,3C6,1B5,2A#5,A#,2G5,6E5' }

_thread.start_new_thread(button_reader_thread, ())
led.value(1)

button1_pressed = False
button2_pressed = False
button3_pressed = False
button4_pressed = False

while not button1_pressed:
    if button2_pressed == True:
        play_song(songs['fanfare'])
        button2_pressed = False
    if button3_pressed == True:
        play_song(songs['birthday'])
        button3_pressed = False
    if button4_pressed == True:
        play_song(songs['harry'])
        button4_pressed = False
    sleep_ms(10)    

led.value(0)
button1_pressed = False
