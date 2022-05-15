#!/usr/bin/python 
# This creates a MIDI connection between my keyboards,
# splits the larger keyboard at key "e2"
# and assigns different voices to the 2 splits

from mididings import * 
 
config( 
    in_ports = [('Yamaha', 'Digital Piano.*')],     # Yamaha P-105 
    out_ports = [('Casio', 'CASIO.*')],             # Casio CT-X3000 
    initial_scene = 1,                              # to ensure that scene 1 will execute at startup
    data_offset = 0 
) 
 
Bass = Output('Casio', 1, (33,33))      # Bass is a now class that will execute the program change
Guitar = Output('Casio', 2, (32,24))    # Guitar is a now class that will execute the program change 

# For demonstration there is only 1 scene here.
# Before calling the output class, you can execute other changes
# such as changing loudness (velocity) or transposing the key to be played
my_scenes = { 
 
   1: Scene("My Key Split", 
             KeySplit('e2', Velocity(multiply=2) >> Bass,  
                 Velocity(multiply=1.2) >> Transpose(-12) >> Guitar) 
      ) 
} 

# The control = Filter(PROGRAM) would execute Scene 1 when the large keyboard sends a program change. 
# Here this is not necessary, as there is only one scene and we set this above with initial_scene. 
# However, you can do this in a more granular way (looking for specific program changes).
run( 
    scenes = my_scenes, 
    pre = ~Filter(PROGRAM), 
    control = Filter(PROGRAM) >> SceneSwitch(1) 
) 
