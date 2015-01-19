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

# System
import random


# Sanity Check
def sanityCheckLauflisten(fileInputMeldeliste, dataInputStammdatenHeader):
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


# Berechnet die Lauflisten
def erstelleLauflisten(fileInputMeldeliste, dataInputStammdatenHeader, fileOutputLaufliste, fileInputWettkampfliste):
    """ Berechnet Lauflisten aus der Meldeliste
    """
    # Sanity Check
    rv = sanityCheckLauflisten(fileInputMeldeliste, dataInputStammdatenHeader)
    if rv != 0:
        return rv


    ######################################################
    # Finde hoechste Anzahl an Bahnen
    data = helper.fileOpen(fileInputWettkampfliste)
    if data == 1:
        return 1

    dataInputBahnenAnzahl = []
    global BahnenAnzahlMax
    BahnenAnzahlMax = 0
    rownum=0
    for row in data:
        if rownum > 0:
            dataInputBahnenAnzahl.append(int(row[3]))
            if int(row[3]) > BahnenAnzahlMax:
                BahnenAnzahlMax = int(row[3])
        rownum += 1


    ######################################################
    # Erstelle Header
    dataOutputHeader = ["Lauf", "WK"]
    dataOutput = [[0 for x in range(0)] for x in range(0)]

    for rownum in range(BahnenAnzahlMax):
        dataOutputHeader.append("Bahn" + str(rownum+1))


    ######################################################
    # Oeffne Meldeliste und erstelle Liste
    data = helper.fileOpen(fileInputMeldeliste)
    if data == 1:
        return 1

    dataInputHeader = []
    dataInput = [[0 for x in range(0)] for x in range(0)]

    # Lade csv in Array
    rownum=0
    for row in data:
        if rownum == 0:
            dataInputHeader = row
        else:
            dataInput.append(row)
        rownum += 1

    # Im Array alle Zeichen != "" mit Namen ersetzen
    dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)
    rownum=0
    for row in dataInput:
        rowName = row[2] + ", " + row[1]
        cellnum=0
        for cell in row:
            if (cellnum >= dataInputAnzahlStammdaten and
                str(cell) != ""):
                dataInput[rownum][cellnum] = rowName
            cellnum += 1
        rownum += 1
            

    ######################################################
    # Verteile Schwimmer

    # wknum 0, ..., WKmax-1
    for wknum in range(len(dataInputHeader)-dataInputAnzahlStammdaten):
        dataInputSpalte = dataInputAnzahlStammdaten+wknum
        laufNamen = []
        rownum=0
        for row in dataInput:
            if dataInput[rownum][dataInputSpalte] != "":
                laufNamen.append(dataInput[rownum][dataInputSpalte])
            rownum += 1

        laufNamen.insert(0, wknum+1)
        dataOutput.append(laufNamen)

    # Zeilen mit mehr als dataInputBahnenAnzahl Eintraege in die naechste Zeile 
    # verschieben
    rownum=0
    for row in dataOutput:
        BahnenAnzahl = dataInputBahnenAnzahl[row[0]-1]
        if len(row)-1 > BahnenAnzahl:
            rowNeu = []

            cellnum=0
            for cell in row:
                if cellnum > BahnenAnzahl:
                    rowNeu.append(cell)
                cellnum += 1

            rowNeu.insert(0, dataOutput[rownum][0])
            dataOutput.insert(rownum+1, rowNeu)

        rownum += 1

    # Alle Eintraege > BahnenAnzahl loeschen
    rownum=0
    for row in dataOutput:
        BahnenAnzahl = dataInputBahnenAnzahl[row[0]-1]
        if len(row) > BahnenAnzahl:
            rowNeu = []

            cellnum=0
            for cell in row:
                if cellnum <= BahnenAnzahl:
                    rowNeu.append(cell)
                cellnum += 1

            del dataOutput[rownum]
            dataOutput.insert(rownum, rowNeu)

        rownum += 1

    # Starter, die alleine sind verteilen: n*BahnenAnzahl+1
    for lenRow1 in range(int(BahnenAnzahlMax/2)+1):
        lenRow = lenRow1+1

        rownum=0
        for row in dataOutput:
            BahnenAnzahl = dataInputBahnenAnzahl[row[0]-1]
            if (len(row) == lenRow and
                    row[0] == dataOutput[rownum-1][0] and
                    len(dataOutput[rownum-1])-1 >= len(row)+1):
                dataOutput[rownum].insert(1, dataOutput[rownum-1][-1])
                del dataOutput[rownum-1][-1]
            rownum += 1

    # Reihenfolge der Schwimmer auf Bahnen randomisieren
    #rownum=0
    #for row in dataOutput:
    #    if len(row) > 2:
    #        wknr = row[0]
    #        del row[0]
    #        random.shuffle(row)
    #        row.insert(0, wknr)
    #        dataOutput[rownum] = row
    #    rownum += 1

    # Leerbahnen einfuegen auf Bahn 1
    rownum=0
    for row in dataOutput:
        if len(row)-1 < BahnenAnzahlMax:
            dataOutput[rownum].insert(1, "")
        rownum += 1

    # Leerbahnen einfuegen abschliessend
    rownum=0
    for row in dataOutput:
        if len(row)-1 < BahnenAnzahlMax:
            for cell in range(BahnenAnzahlMax-len(row)+1):
                dataOutput[rownum].append("")
        rownum += 1

    # Laufnummer einfuegen
    rownum=0
    for row in dataOutput:
        dataOutput[rownum].insert(0, rownum+1)
        rownum += 1


    ######################################################
    # Daten speichern
    rv = helper.fileWrite(fileOutputLaufliste, dataOutput, dataOutputHeader)

    return rv


# Berechnet die Lauflisten
def erstellePDFLauflisten(fileTemplateLaufliste, fileTemplateOutLaufliste,  fileOutputLaufliste, BahnenAnzahl):
    """ Berechnet Lauflisten aus der Meldeliste
    """

    ######################################################
    # Oeffne Ergebnisliste Template
    data = helper.fileOpenTemplate(fileTemplateLaufliste)
    if data == 1:
        return 1

    rownum = 0
    for row in data:
        if row.find("<template:laufliste>") != -1:
            del data[rownum]

            # Pruefen, ob die Tabelle auf eine Seite passt.
            # Es passen Stammdaten und 6 WK auf die erste Seite
            if BahnenAnzahlMax <= 6:
                # Header Tabelle
                row1 = r"\begin{longtable}{"
                row1 += r"p{0.5cm} c |"
                for rownum1 in range(BahnenAnzahlMax):
                    row1 += r" | l"
                row1 += "}\n"
                # Ueberschrift
                row1 += "Lauf & WK"
                for rownum1 in range(BahnenAnzahlMax):
                    row1 = row1 + r" & Bahn " + str(rownum1+1)
                row1 += "\\\\ \hline % \n"
                # Tabelle
                row1 += r"\DTLloaddb{names}{" + fileOutputLaufliste + "} %\n"
                row1 += r"\DTLforeach{names}{"
                row1 += r"\dlauf=Lauf, \dwk=WK"
                for rownum1 in range (BahnenAnzahlMax):
                    row1 += r", \dbahn" + helper.zahl2String(rownum1+1) + r"=Bahn" + \
                        str(rownum1+1)
                row1 += "}{\n"
                row1 += r"\dlauf & \dwk"
                for rownum1 in range (BahnenAnzahlMax):
                    row1 += r"& \PrintName{\dbahn" + helper.zahl2String(rownum1+1) + \
                        r"}"
                row1 += "\\\\[6pt]\n}\n"
                # Footer Tabelle
                row1 += "\end{longtable}\n"

                data.insert(rownum, row1)
        rownum += 1


    ######################################################
    # Schreibe Lauflisten Template
    rv = helper.fileWriteTemplate(fileTemplateOutLaufliste, data)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = helper.callPDFlatex(fileTemplateOutLaufliste)

    return rv
