#!/bin/bash
FILE=/home/pi/"$1"_status_on
if [ -f "$FILE" ]; then
    exit 0
else
    exit 1
fi    
