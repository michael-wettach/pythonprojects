# Example assumes Pico is mounted on the Adafruit RGB Keypad
# Also assumes that Pico has the Adafruit circuit python firmware
# and that keyboard libraries are installed as indicated in
# https://github.com/pimoroni/pmk-circuitpython
# Put this file as code.py on the CIRCUITPY file system for autostart
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
from pmk import PMK

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode
from time import sleep 

pmk = PMK(Hardware())
keys = pmk.keys

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayout(keyboard)

global shutdown
shutdown = False

def sendkeys(text):
    # Inspired by Visual Basic SendKeys(), however keys Shift/Ctrl/Alt/Win will be toggled
    # For practical reasons using key names from keycode_win_de.py. 
    specials = ['SHIFT', 'CONTROL', 'ALT', 'WINDOWS', 'LEFT_SHIFT', 'LEFT_CONTROL', 'LEFT_ALT',
                'RIGHT_SHIFT', 'RIGHT_CONTROL', 'RIGHT_ALT', 'ALTGR']
    pressed = []
    modus = 'normal'
    puffer = ''
    for char in text:
        if modus == 'escape':  
            if char == '}':    # ending escape mode
                modus = 'normal'
                key = getattr(Keycode, puffer, 0x00)
                if puffer in specials:
                    if puffer in pressed:
                        keyboard.release(key)
                        pressed.remove(puffer)
                    else:
                        keyboard.press(key)
                        pressed.append(puffer)
                elif puffer[:6] == 'SLEEP ':
                    try:
                        amount = float(puffer[6:])
                    except:
                        amount = 0
                    sleep(amount)
                elif key != 0x00:
                    keyboard.send(key)
                else:
                    pass
                # no error handling implemented
                puffer = ''
            else:               # remaining in escape mode 
                puffer += char
        else: # modus == 'normal'
            if char == "{":
                modus = 'escape'
            else:    
                layout.write(char)
                
    for keyname in specials:    # just in case we forgot to release...
        keyboard.release(getattr(Keycode, keyname, 0x00))


# Here we can put our keyboard macros as strings.
# Each string is assigned to the corresponding button in the order shown below.
# Special character names from keycode_win_de.py must be used.
# For special keys ALT/CTRL/WIN combinations to work you need to use lower case letters.
# Also for these combinations you must send the special key a second time to release.
keymap_text = ['',                            # 0: key 0 is used for termination of process
   '{ALT}{TAB}{ALT}',                         # 1: switch active window.  
   '{CONTROL}{ALT}d{ALT}{CONTROL}',           # 2: show desktop / minimize all windows (Linux)
   '{WINDOWS}d{WINDOWS}',                     # 3: show desktop / minimize all windows (Windows)
   '{CONTROL}{ALT}l{ALT}{CONTROL}',           # 4: lock the current session (Linux)
   '{WINDOWS}l{WINDOWS}',                     # 5: lock the current session (Windows)
   '{ALT}e{ALT}{CONTROL}c{CONTROL}{ESCAPE}',  # 6: copy file path in Windows File Explorer
   '{F2}{SLEEP 0.1}{CONTROL}a{CONTROL}{SLEEP 0.1}' +
   '{CONTROL}x{CONTROL}{SLEEP 0.1}{ESCAPE}',  # 7: copy file name in Windows File Explorer
   '8',                                       # 8:
   '9',                                       # 9:
   'A',                                       # A:
   'B',                                       # B:
   'C',                                       # C:
   'D',                                       # D: 
   'E',                                       # E:
   'F']                                       # F:

for key in keys[1:]:
    @pmk.on_press(key)
    def press_handler(key):
        key.rgb = (255, 255, 0)
        key.led_on()
        text = keymap_text[key.number]
        sendkeys(text)
        sleep(0.1)
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
    pmk.update()
