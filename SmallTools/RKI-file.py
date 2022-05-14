#!/usr/bin/env/python
# -*- coding: utf-8 -*-
# reads .csv with corona incident data from Robert Koch Institute
# and selects data for local area
# demonstrates the use of Tkinter GUI
from tkinter import *
import csv
import urllib.request

Kreis = "Rheingau"
url = r"https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"

def win_settext(Win, mytext):
    Win.config(state=NORMAL)
    Win.delete(1.0, END)
    Win.insert(END, mytext)
    Win.config(state=DISABLED)

def win_addtext(Win, mytext):
    # Achtung, newline muss explizit im Parameter mitgegeben werden.
    Win.config(state=NORMAL)
    Win.insert(END, mytext)
    Win.config(state=DISABLED)

def win_getdata(event=None):
    global Kreis 
    Kreis = Entry1.get()
    win_settext(T2, "Suche RKI nach Daten für " + Kreis + "...")
    root.update()
    win_settext(T2, "")
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.DictReader(lines)
    for row in cr:
    	if row['GEN'].find(Kreis) != -1:
            win_addtext(T2, row['GEN'] + ':\n')
            win_addtext(T2, 'Daten vom ' + row['last_update'] + '\n')
            win_addtext(T2, 'Einwohner: ' + row['EWZ'] + '\n')
            win_addtext(T2, 'Fälle gesamt: ' + row['cases'] + '\n')
            win_addtext(T2, 'Fälle 7T: ' + row['cases7_lk'] + '\n')
            cases = row['cases7_per_100k']
            win_addtext(T2, '7T-Inz: ' + cases[: cases.find(".") + 2] + '\n')


def win_ende():
# Beispielaktion für den Button 
    root.destroy()


if __name__ == "__main__":

    # --------------------------------------------------------------
    # Aufbau des Windows
    # --------------------------------------------------------------
    root = Tk()
    root.title('Tkinter GUI')
    root.bind('<Return>', win_getdata)

    Label(root, text='Covid 19 Werte für  ').grid(row=1, column=0, padx=5, pady=5)
    Entry1 = Entry(root)
    Entry1.grid(row=1, column=1, sticky=E, padx=2, pady=5)
    Entry1.insert(0, Kreis)
    # Textfeld für Ausgabe
    T2 = Text(root, height=10, width=42, padx=2, pady=5)
    T2.grid(row=2, column=0, columnspan=2)
    S2 = Scrollbar(root)
    S2.grid(row=2, column=2, sticky='ns')
    S2.config(command=T2.yview)
    T2.config(yscrollcommand=S2.set)
    T2.config(state=DISABLED) # prevents text input
    # Button, lets do something
    Button(root, text='Werte holen', command=win_getdata).grid(row=3, column=1, sticky=W, pady=4)
    Button(root, text='Ende', command=win_ende).grid(row=3, column=1, sticky=E, pady=4)
    root.border = Frame(relief='flat', borderwidth=6)
    # --------------------------------------------------------------
    # Ende Window-Aufbau
    # --------------------------------------------------------------

    # Population des Window-Inhalts
   
    win_getdata()
                   
    mainloop(  )
