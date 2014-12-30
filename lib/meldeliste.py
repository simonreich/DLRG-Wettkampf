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


def erstellePDFMeldeliste(fileTemplateMeldeliste, fileTemplateOutMeldeliste, fileInputMeldeliste, fileInputWettkampfliste):
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
        dataInputWettkampfliste.append(row)
        rownum += 1
    dataInputAnzahlWK = rownum-1


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
            row1 += r"p{0.5cm} l l l |"
            for rownum1 in range(dataInputAnzahlWK):
                row1 += r" c"
            row1 = row1 + "}\n"
            # Ueberschrift
            row1 += ("Nr & Name & Vorname & Team "
                "Pkt")
            for rownum1 in range(dataInputAnzahlWK):
                row1 = row1 + r" & WK " + str(rownum1+1)
            row1 += "\\\\ \hline\n"
            # Tabelle
            row1 += r"\DTLloaddb{names}{" + fileInputMeldeliste + \
                "}\n"
            row1 += r"\DTLforeach{names}{"
            row1 += (r"\dnummer=Nummer, \dvorname=Vorname, "
                "\dnachname=Nachname, \dgeburtsdatum=Geburtsdatum, "
                "\dmail=Mail, \dteamname=Teamname")
            for rownum1 in range (dataInputAnzahlWK):
                row1 += r", \dwk" + helper.zahl2String(rownum1+1) + r"=WK" + \
                    str(rownum1+1)
            row1 += "}{\n"
            row1 += r"\dnummer & \dnachname & \dvorname & \dteamname "
            for rownum1 in range (dataInputAnzahlWK):
                row1 += r"& \PrintX{\dwk" + helper.zahl2String(rownum1+1) + \
                        r"}"
            row1 += "\\\\\\hline\n}\n"
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
