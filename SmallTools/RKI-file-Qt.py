#!/usr/bin/env/python
# -*- coding: utf-8 -*-
# reads .csv with corona incident data from Robert Koch Institute
# and selects data for local area
# demonstrates the use of PyQt5 GUI
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from TextInput_ui import Ui_Dialog
import csv
import urllib.request


class MyTextDialog(QDialog):
    cr = []  # Liste der Inzidenzen für die Landkreise

    # -------------------------------------------------------------------
    # Prozeduren zum Handeln der GUI Events. Die Namen sind frei wählbar.
    # Jede Prozedur muss in __init__ mit dem Event verbunden werden.
    # -------------------------------------------------------------------

    def pushButton_click(self):
        Kreis = self.ui.plainTextEdit.toPlainText()
        self.win_settext("")
        for row in self.cr:
            if row['GEN'].find(Kreis) != -1:
                self.win_addtext(row['GEN'] + ':')
                self.win_addtext('Daten vom ' + row['last_update'])
                self.win_addtext('Einwohner: ' + row['EWZ'])
                self.win_addtext('Fälle gesamt: ' + row['cases'])
                cases = row['cases7_per_100k']
                self.win_addtext('7T-Inz: ' + cases[: cases.find(".") + 2])

    # -----------------------------------------------
    # Ende der Prozeduren zum Handeln der GUI Events.
    # -----------------------------------------------

    def win_settext(self, mytext):
        # Achtung, newline wird automatisch angehängt.
        self.ui.textBrowser.setText(mytext)

    def win_addtext(self, mytext):
        # Achtung, newline wird automatisch angehängt.
        self.ui.textBrowser.append(mytext)

    def __init__(self):
        # Initialisierung der Klasse und damit des Dialogs
        super().__init__()

        # Erzeugen des Dialogfensters
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.plainTextEdit.insertPlainText("Rheingau")

        # -----------------------------------------------------------
        # Die GUI Events werden mit der jeweiligen Prozedur verbunden
        # -----------------------------------------------------------
        self.ui.pushButton.clicked.connect(self.pushButton_click)
        # -----------------------------------------------------------

        # Initialisierung der Inzidenz-Daten des Robert Koch Instituts
        # Download der CSV Datei mit den Daten für alle Landkreise
        url = r"https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        self.cr = list(csv.DictReader(lines))

        # Dann aktualisieren wir das Fenster vor der ersten Anzeige...
        self.pushButton_click()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = MyTextDialog()
    app_window.show()
    sys.exit(app.exec_())

    mainloop()
