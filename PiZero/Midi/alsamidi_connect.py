#!/usr/bin/python 
# this aims to find yout the ALSA device ids for my keyboards
# and connect them via ALSA, rather that doing that manually.
import subprocess 
import re 
clients = {} 
result = subprocess.check_output(['aconnect', '-i', '-o']) 
for line in result.split("\n"): 
    if line[:7] == 'client ': 
        (nr, name) = re.search(r"client (\d+): \'([^\']+)", line).groups() 
        clients[name] = nr 
CS = 'CASIO USB-MIDI'    # Casio CT-X3000 
C = clients.get(CS) 
YS = 'Digital Piano'     # Yamaha P-105 
Y = clients.get(YS) 
for (client, value) in [(CS, C), (YS, Y)]: 
    if value is None: 
        print client + ' not found' 
        exit(0) 
subprocess.call(['aconnect', Y + ':0', C + ':0']) 
subprocess.call(['sendmidi', 'dev', CS, 'cc', '0', '32', 'pc', '24']) 
result = subprocess.check_output(['aconnect', '-lo']) 
print result 
