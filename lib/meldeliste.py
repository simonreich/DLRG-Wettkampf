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


def erstelleMeldelisteSanitycheck(fileInputWettkampfliste):
    """ Sanity Check der Input Daten
        fileInputWettkampfliste:
    """
    # Wettkampfliste
    data = helper.fileOpen(fileInputWettkampfliste)
    if data == 1:
        return 1

    dataInputWettkampfliste = [[0 for x in range(0)] for x in range(0)]
    dataInputWettlampflisteHeader = []

    rownum=0
    for row in data:
        if rownum == 0:
            dataInputWettkampflisteHeader = row
        else:
            dataInputWettkampfliste.append(row)
        rownum += 1

    dataInputWettkampflisteAnzahlWK = rownum-1

    if dataInputWettkampflisteAnzahlWK <= 0:
        print("Die Datei " + fileInputWettkampfliste + " enthält zu wenig "
            "Wettkämpfe.")
        return 1

    return 0


# Erstelle Meldelisten template
def erstelleMeldeliste(fileInputWettkampfliste, fileInputMeldeliste, dataInputStammdatenHeader):
    """ Erstellt eine Datei, die eine leere Meldeliste beinhaltet.
        fileInputWettkampfliste:
        fileInputMeldeliste:
    """

    # Sanity Check der Input Daten
    if erstelleMeldelisteSanitycheck(fileInputWettkampfliste) != 0:
        return 1

    dataOutput = dataInputStammdatenHeader

    # Oeffne Wettkampfliste und erstelle Liste
    data = helper.fileOpen(fileInputWettkampfliste)
    if data == 1:
        return 1

    # Lade csv in Array
    rownum=0
    for row in data:
        rownum += 1
    rownumTotal = rownum-1

    for rownum in range(rownumTotal):
        dataOutput.append("WK" + str(rownum+1))

    # Daten speichern
    rv = helper.fileWrite(fileInputMeldeliste, dataOutput)

    return rv


def erstellePDFMeldeliste(fileTemplateMeldeliste, fileTemplateOutMeldeliste, fileInputMeldeliste, fileInputWettkampfliste, dataInputAnzahlStammdaten):
    """ Erstellt PDFs aus der Meldeliste
    """

    ######################################################
    # Lade Wettkampfliste

    # Oeffne Wettkampfliste und erstelle Liste
    data = helper.fileOpen(fileInputWettkampfliste)
    if data == 1:
        return 1

    # Lade csv in Array
    dataInputWettkampfliste = [[0 for x in range(0)] for x in range(0)]
    rownum=0
    for row in data:
        if rownum >= 0:
            dataInputWettkampfliste.append(row)
        rownum += 1
    dataInputAnzahlWK = rownum-1


    ######################################################
    # Lade Meldeliste

    # Oeffne Meldeliste und erstelle Liste
    data = helper.fileOpen(fileInputMeldeliste)
    if data == 1:
        return 1

    # Lade csv in Array
    dataInputMeldeliste = [[0 for x in range(0)] for x in range(0)]
    rownum=0
    for row in data:
        if rownum > 0:
            dataInputMeldeliste.append(row)
        rownum += 1

    # Alphabetisch sortieren
    dataInputMeldeliste = helper.sort_table_low(dataInputMeldeliste, [2, 1])


    ######################################################
    # Oeffne Meldeliste Template
    data = helper.fileOpenTemplate(fileTemplateMeldeliste)
    if data == 1:
        return 1

    rownum = 0
    for row in data:
        if row.find("<template:meldeliste>") != -1:
            del data[rownum]

            # Header Tabelle
            row1 = r"\begin{longtable}{"
            row1 += r"l l c ||"
            for rownum1 in range(dataInputAnzahlWK):
                row1 += r" c"
            row1 = row1 + "}\n"
            # Ueberschrift
            row1 += ("Name & Vorname & AK")
            for rownum1 in range(dataInputAnzahlWK):
                row1 = row1 + r" & WK " + str(rownum1+1)
            row1 += "\\\\ \hline \hline\n"
            # Tabelle
            rownum2 = 0
            for row2 in dataInputMeldeliste:
                cellnum2 = 0
                for cell2 in row2:
                    if cellnum2 == 0:
                        row1 += str(row2[2]) + \
                            r" & " + str(row2[1]) + \
                            r" & " + str(helper.berechneAltersklasse(row2[3]))
                    elif cellnum2 >= dataInputAnzahlStammdaten:
                        row1 += r" & " + str(cell2)
                    cellnum2 += 1
                row1 += "\\\\ \\hline\n"
                rownum2 += 1
            # Footer Tabelle
            row1 += "\end{longtable}\n"

            data.insert(rownum, row1)
            print(rownum, row1)

        rownum += 1
    
    for row in data:
        print(row)        
        
    ######################################################
    # Schreibe Meldeliste Template
    rv = helper.fileWriteTemplate(fileTemplateOutMeldeliste, data)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = helper.callPDFlatex(fileTemplateOutMeldeliste)

    return rv
