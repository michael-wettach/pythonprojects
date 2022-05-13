# Example assumes Pico is mounted on the Adafruit RGB Keypad
# Also assumes that Pico has the Adafruit circuit python firmware
# and that midi controller libraries are installed as indicated in
# https://github.com/pimoroni/pmk-circuitpython
# Put this file as code.py on the CIRCUITPY file system for autostart
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  
from time import sleep 

import usb_midi
import adafruit_midi

# Only importing what is used will save a little bit of memory
# from adafruit_midi.pitch_bend import PitchBend
# from adafruit_midi.channel_pressure import ChannelPressure
# from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.control_change import ControlChange
from adafruit_midi.system_exclusive import SystemExclusive

# Set up pmk
pmk = PMK(Hardware())
keys = pmk.keys

global shutdown
shutdown = False

# Set USB MIDI up on channel 0.
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=15)

# The colour to set the keys when pressed.
rgb = (255, 255, 0)

# Initial values for MIDI note and velocity.
start_note = 36
velocity = 127

# # Examples
#   midi.send(NoteOn(44, 120))  # G sharp 2nd octave
#   time.sleep(0.25)
# # note how a list of messages can be used
#   midi.send([NoteOff("G#2", 120), ControlChange(3, 44)])

# Loop through keys and attach decorators.
for key in keys[1:]:
    # If pressed, send a MIDI note on command and light key.
    @pmk.on_press(key)
    def press_handler(key):
        note = start_note + key.number
        key.rgb = rgb
        key.led_on()
        sleep(0.1)
        midi.send(NoteOn(note, velocity))

    # If released, send a MIDI note off command and turn off LED.
    @pmk.on_release(key)
    def release_handler(key):
        note = start_note + key.number
        key.rgb = (0, 0, 0)
        midi.send(NoteOff(note, 0))
        key.led_off()

key = keys[0]  # I want one key to get out of the endless loop
@pmk.on_press(key)
def press_handler(key):
    global shutdown
    pmk.set_all(255, 0, 0)
    sleep(0.5)
    pmk.set_all(0, 0, 0)
    shutdown = True

while not shutdown:
    # Always remember to call pmk.update()!
    pmk.update()
