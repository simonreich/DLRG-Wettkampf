# -*- coding: utf-8 -*-
"""
This file is part of DLRG-Wettkampf.

    Foobar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DLRG-Wettkampf.  If not, see <http://www.gnu.org/licenses/>.
"""


# DLRG-Wettkampf
from lib import helper


# Sanity Check
def sanityCheckLaufkarten(fileInputMeldeliste, dataInputStammdatenHeader):
    """ Sanity Check der Input Daten
        fileInputMeldeliste: 
    """
    # Meldeliste
    data = helper.fileOpen(fileInputMeldeliste)
    if data == 1:
        return 1

    dataInput = [[0 for x in range(0)] for x in range(0)]
    dataInputHeader = []

    rownum=0
    for row in data:
        if rownum == 0:
            dataInputHeader = row
        else:
            dataInput.append(row)
        rownum += 1

    if len(dataInputHeader)-len(dataInputStammdatenHeader) <= 0:
        print("Die Datei " + fileInputMeldeliste + " enthält zu wenig"
            "Wettkämpfe.")
        return 1

    if rownum < 1:
        print("Die Datei " + fileInputMeldeliste + " enthält zu wenig"
            "Teilnehmer.")
        return 1

    return 0


# Berechnet die Laufkarten
def erstelleLaufkarte(fileOutputLaufliste, fileOutputLaufkarte, fileInputMeldeliste, dataInputStammdatenHeader):
    """ Berechnet Laufkarte aus Meldeliste
    """

    # Sanity Check der Input Daten
    if sanityCheckLaufkarten(fileInputMeldeliste, dataInputStammdatenHeader) != 0:
        return 1

    ######################################################
    # Oeffne Datei und lade csv
    # Laufliste
    data = helper.fileOpen(fileOutputLaufliste)
    if data == 1:
        return 1
    
    # Lade csv in Array
    dataInput = [[0 for x in range(0)] for x in range(0)]
    dataInputHeader = []
    
    rownum=0
    for row in data:
        if rownum == 0:
            dataInputHeader = row
        else:
            dataInput.append(row)
        rownum += 1
    

    ######################################################
    # Jeweils eine Zeile fuer jeden Schwimmer ersteleln
    dataOutput = [[0 for x in range(0)] for x in range(0)]
    dataOutputHeader = ["Lauf", "WK", "Bahn", "Name"]
    rownum=0
    for row in dataInput:
        cellnum=0
        for cell in row:
            rowNeu = []
            if cellnum >= 2:
                rowNeu.append(dataInput[rownum][0])          # Lauf
                rowNeu.append(dataInput[rownum][1])          # WK
                rowNeu.append(cellnum-1)                     # Bahn
                rowNeu.append(dataInput[rownum][cellnum])    # Name
                dataOutput.append(rowNeu)

            cellnum += 1
        rownum += 1


    ######################################################
    # Daten speichern
    rv = helper.fileWrite(fileOutputLaufkarte, dataOutput, dataOutputHeader)

    return rv


# Berechnet die Laufkarten
def erstellePDFLaufkarten(fileTemplateLaufkarte, fileTemplateOutLaufkarte, fileOutputLaufkarte):
    """ Erstellt PDFs aus der Laufliste
    """

    ######################################################
    # Oeffne Ergebnisliste Template
    data = helper.fileOpenTemplate(fileTemplateLaufkarte)

    rownum = 0
    for row in data:
        if row.find("<template:laufkarte>") != -1:
            del data[rownum]

            row1 = r"\DTLloaddb{names}{" + fileOutputLaufkarte + "}\n"
            data.insert(rownum, row1)
        rownum += 1


    ######################################################
    # Schreibe Lauflisten Template
    rv = helper.fileWriteTemplate(fileTemplateOutLaufkarte, data)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = helper.callPDFlatex(fileTemplateOutLaufkarte)

    return rv


