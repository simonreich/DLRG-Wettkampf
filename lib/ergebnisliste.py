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
def sanityCheckErgebnisliste(fileInputRekorde, fileInputWettkampfliste, fileInputStammdaten, dataInputStammdatenHeader):
    """ Sanity Check der Input Daten
        fileInputMeldeliste: 
    """

    dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)

    # Rekorde
    data = helper.fileOpen(fileInputRekorde)
    if data == 1:
        return 1

    dataInputRekorde = [[0 for x in range(0)] for x in range(0)]
    dataInputRekordeHeader = []

    rownum=0
    for row in data:
        if rownum == 0:
            dataInputRekordeHeader = row
        else:
            dataInputRekorde.append(row)
        rownum += 1

    dataInputRekordeAnzahlWK = len(dataInputRekordeHeader)-1

    if dataInputRekordeAnzahlWK <= 0:
        print("Die Datei " + fileInputRekorde + " enthält zu wenig "
            "Wettkämpfe.")
        return 1
    if len(dataInputRekorde) <= 0:
        print("Die Datei " + fileInputRekorde + " enthält zu wenig "
            "Altersklassen.")
        return 1

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

    if dataInputRekordeAnzahlWK != dataInputWettkampflisteAnzahlWK:
        print("In den Dateien \n" + fileInputWettkampfliste + "\n" + \
            fileInputRekorde + "\nist eine unterschiedliche Anzahl an "
            "Wettkämpfen eingetragen.")
        return 1

    # Stammdaten
    data = helper.fileOpen(fileInputStammdaten)
    if data == 1:
        return 1

    dataInputStammdaten = [[0 for x in range(0)] for x in range(0)]
    dataInputStammdatenHeader = []

    rownum=0
    for row in data:
        if rownum == 0:
            dataInputStammdatenHeader = row
        else:
            dataInputStammdaten.append(row)
        rownum += 1

    dataInputStammdatenAnzahlWK = \
        len(dataInputStammdatenHeader)-dataInputAnzahlStammdaten

    if dataInputStammdatenAnzahlWK <= 0:
        print("Die Datei " + fileInputStammdaten + " enthält zu wenig"
            "Wettkämpfe.")
        return 1
    if dataInputRekordeAnzahlWK != dataInputStammdatenAnzahlWK:
        print("In den Dateien \n" + \
            fileInputWettkampfliste + "\n" + \
            fileInputRekorde + "\n" + \
            fileInputStammdaten + "\n" + \
            "ist eine unterschiedliche Anzahl an Wettkämpfen eingetragen.")
        return 1

    return 0


# Erstelle Ergebnisliste
def erstelleErgebnisliste(fileInputStammdaten, fileInputRekorde, fileInputWettkampfliste, fileOutputAlpha, fileOutputAlstersklasseplatz, fileOutputGesamtplatz, dataInputStammdatenHeader):
    """ Berechnet Punkte und Ranking
    """
    # Sanity Check der Input Daten
    if sanityCheckErgebnisliste(fileInputRekorde, fileInputWettkampfliste, fileInputStammdaten, dataInputStammdatenHeader) != 0:
        return 1

    ######################################################
    # Oeffne Datei und lade csv
    print ("Lade Datei", fileInputStammdaten)
    
    # Stammdaten
    data = helper.fileOpen(fileInputStammdaten)
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
            dataInput.append (row)
    
        rownum += 1
    
    # Daten in das Output Array kopieren
    dataOutput = dataInput
    dataOutputHeader = dataInputHeader
    
    
    # Rekorde
    data = helper.fileOpen(fileInputRekorde)
    if data == 1:
        return 1

    dataRekorde = [[0 for x in range(0)] for x in range(0)]
    dataRekordetHeader = []
    
    rownum=0
    for row in data:
        if rownum == 0:
            dataRekordeHeader = row
        else:
            dataRekorde.append (row)
    
        rownum += 1
    
    
    ######################################################
    # Anzahl der Wettkaempfe
    global dataInputAnzahlWK
    dataInputAnzahlWK = 0
    
    dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)
    
    # Lese Anzahl der Wettkaempfe
    for row in dataInput:
        dataInputAnzahlWK = len(row)-dataInputAnzahlStammdaten

    data = helper.fileOpen(fileInputWettkampfliste)
    if data == 1:
        return 1
    
    rownum=0
    for row in data:
        rownum += 1

    dataInputAnzahlWK = rownum-1
    
    
    ######################################################
    # Altersklasse berechnen
    print ("Berechne Altersklasse")
    
    dataOutputAltersklasseHeader = "Altersklasse"
    dataOutputAltersklasse = []
    
    for row in dataInput:
        dataOutputAltersklasse.append (helper.berechneAltersklasse (row[3]))
    
    
    ######################################################
    # Punkte berechnen
    print ("Berechne Punkte")
    
    dataOutputPunkteHeader = []
    dataOutputPunkte = [[0 for x in range(0)] for x in range(0)]
    
    # Erstelle Header
    for colnum in range(dataInputAnzahlWK):
        dataOutputPunkteHeader.append ("WK" + str(colnum+1) + "_Punkte")
    
    # Berechne Punkte
    rownum=0
    for row in dataInput:
        # Zuerst Referenzrekorde aus Tabelle laden
        for rowRekorde in dataRekorde:
            if rowRekorde[0] == dataOutputAltersklasse[rownum]:
                dataRekordeRow = rowRekorde
    
        dataOutputPunkteRow = []
        for colnum in range(dataInputAnzahlWK):
            dataOutputPunkteRow.append(
                helper.berechnePunkte(
                    row[colnum+dataInputAnzahlStammdaten], 
                    dataRekordeRow[colnum+1])
                )
        
        dataOutputPunkte.append(dataOutputPunkteRow)
    
        rownum += 1
    
    dataOutputPunkteTotal = []
    dataOutputPunkteTotalHeader = "Gesamtpunkte"
    
    for row in dataOutputPunkte:
        counter = 0
        if(sorted(row)[-1] != 0):
            punkte = sorted(row)[-1] 
            counter += 1
        if(sorted(row)[-2] != 0):
            punkte += sorted(row)[-2] 
            counter += 1
        if(sorted(row)[-3] != 0):
            punkte += sorted(row)[-3] 
            counter += 1
        
        if (counter != 0):
            punkte /= counter
        else:
            punkte = 0

        # auf zwei Nachkommastellen runden
        punkte = float("{0:.2f}".format(punkte))

        dataOutputPunkteTotal.append(punkte)
    
    
    ######################################################
    # Platzierung berechnen
    print ("Berechne Platzierung")
    
    dataOuput = dataInput
    dataOuputHeader = dataInputHeader

    # Altersklasse hinzufuegen
    dataOuputHeader.insert (dataInputAnzahlStammdaten, "Altersklasse")
    rownum = 0
    for row in dataOutput:
        dataOutput[rownum].insert(dataInputAnzahlStammdaten, 
            dataOutputAltersklasse[rownum])
        rownum += 1
    
    # Gesamtpunkte hinzufuegen
    dataOuputHeader.insert (dataInputAnzahlStammdaten+1, "Gesamtpunkte")
    rownum = 0
    for row in dataOutput:
        dataOutput[rownum].insert (dataInputAnzahlStammdaten+1, 
            dataOutputPunkteTotal[rownum])
        rownum += 1
    
    # Einzelpunkte hinzufuegen
    for colnum in range(dataInputAnzahlWK):
        dataOutputHeader.insert(dataInputAnzahlStammdaten+3+(2*colnum), 
            dataOutputPunkteHeader[colnum])
    
    rownum = 0
    for row in dataOutput:
        for colnum in range(dataInputAnzahlWK):
            dataOutput[rownum].insert(dataInputAnzahlStammdaten+3+(2*colnum), 
                dataOutputPunkte[rownum][colnum])
        rownum += 1
        
    # Nach Gesamtpunkten sortieren, zuerst ohne Altersklassen
    dataOuputHeader.insert (dataInputAnzahlStammdaten+2, "Gesamtplatz")
    
    dataOutputGesamtplatz = [[0 for x in range(0)] for x in range(0)]
    rownum = 0
    for row in helper.sort_table_high(dataOutput, (dataInputAnzahlStammdaten+1, 2)):
        dataOutputGesamtplatz.append(row)
        dataOutputGesamtplatz[rownum].insert(dataInputAnzahlStammdaten+2, 
            rownum+1)
        rownum += 1
    
    dataOutput = dataOutputGesamtplatz
    
    # Nach Gesamtpunkten sortieren, diesmal nach Altersklasse
    dataOuputHeader.insert (dataInputAnzahlStammdaten+3, "Altersklasseplatz")
    
    dataOutputGesamtplatz = [[0 for x in range(0)] for x in range(0)]
    rownum = 0
    platz = 1
    altersklasseAlt = ""
    for row in helper.sort_table_high(dataOutput, (dataInputAnzahlStammdaten, 
            dataInputAnzahlStammdaten+1)):
        dataOutputGesamtplatz.append(row)
    
        if(altersklasseAlt != row[dataInputAnzahlStammdaten]):
            platz = 1
            altersklasseAlt = row[dataInputAnzahlStammdaten]
        else:
            platz += 1
    
        dataOutputGesamtplatz[rownum].insert(dataInputAnzahlStammdaten+3, platz)
    
        rownum += 1
    
    dataOutput = dataOutputGesamtplatz
    
    
    ######################################################
    # Daten speichern
    print ("Speichere berechnete Daten")
    
    # Alphabetisch
    data = [[0 for x in range(0)] for x in range(0)]
    for row in helper.sort_table_low(dataOutput, (2, 1)):
        data.append(row)
    rv = helper.fileWrite(fileOutputAlpha, data, dataOutputHeader)
    if rv != 0:
        return rv
    
    # Gesamtplatz
    data = [[0 for x in range(0)] for x in range(0)]
    for row in helper.sort_table_low(dataOutput, (dataInputAnzahlStammdaten+2, 2)):
        data.append(row)
    rv = helper.fileWrite(fileOutputGesamtplatz, data, dataOutputHeader)
    if rv != 0:
        return rv

    
    # Altersklassenplatz
    data = [[0 for x in range(0)] for x in range(0)]
    for row in helper.sort_table_low(dataOutput, (
            dataInputAnzahlStammdaten, 
            dataInputAnzahlStammdaten+3)):
        data.append(row)
    rv = helper.fileWrite(fileOutputAlstersklasseplatz, data, dataOutputHeader)
    if rv != 0:
        return rv

    return 0


# Erstelle PDF Urkunde
def erstellePDFUrkunden(fileInputWettkampfliste, fileTemplateUrkunde, fileTemplateOutUrkunde, fileOutputAlpha):
    """ Erstellt PDFs mittels pfdlatex.
        Die templates liegen im Ordner template/
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
        if rownum > 0:
            dataInputWettkampfliste.append(row)
        rownum += 1
    dataInputAnzahlWK = rownum-1


    ######################################################
    # Erstelle Ergebnisliste für Tabelle
    dataInputAnzahlWK2 = int(dataInputAnzahlWK/2)

    dataOutput = []
    dataOutput.append("\\begin{tabular}{ l r | l r }\n")
    for rownum in range(dataInputAnzahlWK2):
        rownumTemp1 = rownum
        rownumTemp2 = dataInputAnzahlWK2 + dataInputAnzahlWK%2 + rownum
        dataOutput.append(r"WK " + \
            format(rownumTemp1+1) + \
            format(r": \unit[") + \
            format(dataInputWettkampfliste[rownumTemp1][0]) + \
            format(r"]{") + \
            format(dataInputWettkampfliste[rownumTemp1][1]) + \
            format(r"} ") + \
            format(dataInputWettkampfliste[rownumTemp1][2]) + \
            format(r" & \PrintTime{\dwk") + \
            format(helper.zahl2String(rownumTemp1+1)) + \
            format(r"} & WK ") + \
            format(rownumTemp2+1) + \
            format(r": \unit[") + \
            format(dataInputWettkampfliste[rownumTemp2][0]) + \
            format(r"]{") + \
            format(dataInputWettkampfliste[rownumTemp2][1]) + \
            format(r"} ") + \
            format(dataInputWettkampfliste[rownumTemp2][2]) + \
            format(" & \PrintTime{\dwk") + \
            format(helper.zahl2String(rownumTemp2+1)) + \
            format("} \\\\\n"))
    if dataInputAnzahlWK%2 == 1:
        dataOutput.append("WK " + \
            format(dataInputAnzahlWK2+1) + \
            format(r": \unit[") + \
            format(dataInputWettkampfliste[dataInputAnzahlWK2][0]) + \
            format(r"]{") + \
            format(dataInputWettkampfliste[dataInputAnzahlWK2][1]) + \
            format(r"} ") + \
            format(dataInputWettkampfliste[dataInputAnzahlWK2][2]) + \
            format(" & \PrintTime{\dwk") + \
            format(helper.zahl2String(dataInputAnzahlWK2+1)) + \
            format("} & & \\\\\n"))
    dataOutput.append(format("\end{tabular}\n"))


    ######################################################
    # Oeffne Urkunde Template
    data = helper.fileOpenTemplate(fileTemplateUrkunde)
    if data == 1:
        return 1
    dataInputTemplate = data

    rownum = 0
    for row in dataInputTemplate:
        if row.find("<template:wettkampfliste>") != -1:
            del dataInputTemplate[rownum]
            rownum1 = 0
            for row1 in dataOutput:
                dataInputTemplate.insert(rownum+rownum1, row1)
                rownum1 += 1
        elif row.find("<template:dateistammdaten>") != -1:
            del dataInputTemplate[rownum]
            dataInputTemplate.insert(rownum, fileOutputAlpha)
        elif row.find("<template:stammdaten>") != -1:
            del dataInputTemplate[rownum]
            row1 =(r"{\dnummer=Nummer, \dvorname=Vorname, \dnachname=Nachname, "
                "\dgeburtsdatum=Geburtsdatum, \dmail=Mail, "
                "\dteamname=Teamname, \daltersklasse=Altersklasse, "
                "\daltersklasseplatz=Altersklasseplatz, "
                "\dgesamtplatz=Gesamtplatz, \dgesamtpunkte=Gesamtpunkte")
            for rownum1 in range (dataInputAnzahlWK):
                row1 = row1 + r", \dwk" + helper.zahl2String(rownum1+1) + r"=WK" + \
                    str(rownum1+1)
                row1 = row1 + r", \dwk" + helper.zahl2String(rownum1+1) + \
                    r"punkte=WK" + str(rownum1+1) + r"_Punkte"
            row1 = row1 + "}{\n"
            dataInputTemplate.insert(rownum, row1)

        rownum += 1


    ######################################################
    # Schreibe Urkunden Template
    rv = helper.fileWriteTemplate(fileTemplateOutUrkunde, dataInputTemplate)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = helper.callPDFlatex(fileTemplateOutUrkunde)

    return rv


def erstellePDFErgebnisliste(fileTemplateErgebnisliste, fileTemplateOutErgebnisliste, fileOutputAlstersklasseplatz):
    """ Erstellt ein PDF aus der Ergebnisliste
    """
    # Oeffne Ergebnisliste Template
    data = helper.fileOpenTemplate(fileTemplateErgebnisliste)
    if data == 1:
        return 1
    dataInputTemplate = data

    rownum = 0
    for row in dataInputTemplate:
        if row.find("<template:ergebnisliste>") != -1:
            del dataInputTemplate[rownum]

            # Pruefen, ob die Tabelle auf eine Seite passt.
            # Es passen Stammdaten und 6 WK auf die erste Seite
            if dataInputAnzahlWK <= 6:
                # Header Tabelle
                row1 = r"\begin{longtable}{"
                row1 += r"p{0.5cm} l l l l c c | r"
                for rownum1 in range(dataInputAnzahlWK):
                    row1 += r" | r r"
                row1 = row1 + "}\n"
                # Ueberschrift
                row1 += ("Nr & Vorname & Nachname & Team & AK & AK-P & Ges-P & "
                    "Pkt")
                for rownum1 in range(dataInputAnzahlWK):
                    row1 = row1 + r" & \multicolumn{2}{|c}{WK " + \
                        str(rownum1+1) + r"}"
                row1 += "\\\\ \hline\n"
                # Tabelle
                row1 += r"\DTLloaddb{names}{" + fileOutputAlstersklasseplatz + \
                    "}\n"
                row1 += r"\DTLforeach{names}{"
                row1 += (r"\dnummer=Nummer, \dvorname=Vorname, "
                    "\dnachname=Nachname, \dgeburtsdatum=Geburtsdatum, "
                    "\dmail=Mail, \dteamname=Teamname, "
                    "\daltersklasse=Altersklasse, "
                    "\daltersklasseplatz=Altersklasseplatz, "
                    "\dgesamtplatz=Gesamtplatz, \dgesamtpunkte=Gesamtpunkte")
                for rownum1 in range (dataInputAnzahlWK):
                    row1 += r", \dwk" + helper.zahl2String(rownum1+1) + r"=WK" + \
                        str(rownum1+1)
                    row1 += r", \dwk" + helper.zahl2String(rownum1+1) + \
                        r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                row1 += "}{\n"
                row1 += (r"\dnummer & \dvorname & \dnachname & \dteamname & "
                    "\daltersklasse & \daltersklasseplatz & \dgesamtplatz & "
                    "\dgesamtpunkte")
                for rownum1 in range (dataInputAnzahlWK):
                    row1 += r"& \PrintTime{\dwk" + helper.zahl2String(rownum1+1) + \
                        r"} & \dwk" + helper.zahl2String(rownum1+1) + r"punkte"
                row1 += "\\\\\n}\n"
                # Footer Tabelle
                row1 += "\end{longtable}\n"

                dataInputTemplate.insert(rownum, row1)
            else:
                # Erste Seite
                # 0, ..., 5 Es passen 6 WK auf die erste Seite
                dataInputAnzahlWKSeite1 = 6 
                # Header Tabelle
                row1 = r"\begin{longtable}{"
                row1 += r"p{0.5cm} l l l l c c | r"
                for rownum1 in range(dataInputAnzahlWKSeite1):
                    row1 += r" | r r"
                row1 = row1 + "}\n"
                # Ueberschrift
                row1 += ("Nr & Vorname & Nachname & Team & AK & AK-P & Ges-P & "
                    "Pkt")
                for rownum1 in range(dataInputAnzahlWKSeite1):
                    row1 = row1 + r" & \multicolumn{2}{|c}{WK " + \
                        str(rownum1+1) + r"}"
                row1 += "\\\\ \hline\n"
                # Tabelle
                row1 += r"\DTLloaddb{names}{" + fileOutputAlstersklasseplatz + \
                    "}\n"
                row1 += r"\DTLforeach{names}{"
                row1 += (r"\dnummer=Nummer, \dvorname=Vorname, "
                    "\dnachname=Nachname, \dgeburtsdatum=Geburtsdatum, "
                    "\dmail=Mail, \dteamname=Teamname, "
                    "\daltersklasse=Altersklasse, "
                    "\daltersklasseplatz=Altersklasseplatz, "
                    "\dgesamtplatz=Gesamtplatz, \dgesamtpunkte=Gesamtpunkte")
                for rownum1 in range (dataInputAnzahlWK):
                    row1 += r", \dwk" + helper.zahl2String(rownum1+1) + r"=WK" + \
                        str(rownum1+1)
                    row1 += r", \dwk" + helper.zahl2String(rownum1+1) + \
                        r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                row1 += "}{\n"
                row1 += (r"\dnummer & \dvorname & \dnachname & \dteamname & "
                    "\daltersklasse & \daltersklasseplatz & \dgesamtplatz & "
                    "\dgesamtpunkte")
                for rownum1 in range (dataInputAnzahlWKSeite1):
                    row1 += r"& \PrintTime{\dwk" + helper.zahl2String(rownum1+1) + \
                        r"} & \dwk" + helper.zahl2String(rownum1+1) + r"punkte"
                row1 += "\\\\\n}\n"
                # Footer Tabelle
                row1 += "\end{longtable}\n"

                # Alle weiteren Seiten
                # Es passen 11 WK auf jede weitere Seite
                # 11 WK auf jede kommende Seite
                dataInputAnzahlWKSeite2 = 11
    
                temp = (dataInputAnzahlWK-dataInputAnzahlWKSeite1)/ \
                    dataInputAnzahlWKSeite2 + 1
                for tablenr in range(int(temp)):
                    # Variablen

                    # Erster Wettkampf jeder Tabelle
                    dataInputAnzahlWKSeite2Offset = dataInputAnzahlWKSeite1 + \
                        tablenr*dataInputAnzahlWKSeite2

                    # Anzahl der Wettkaempfe pro Seite
                    if dataInputAnzahlWK-dataInputAnzahlWKSeite2Offset > \
                            dataInputAnzahlWKSeite2:
                        dataInputAnzahlWKSeite2Print = dataInputAnzahlWKSeite2
                    else:
                        dataInputAnzahlWKSeite2Print = \
                            dataInputAnzahlWK - dataInputAnzahlWKSeite2Offset

                    # page break
                    row1 += "\n\n\\newpage\n\n\n"

                    # Header Tabelle
                    row1 += r"\begin{longtable}{"
                    for rownum1 in range(dataInputAnzahlWKSeite2Print):
                        if rownum1 == 0:
                            row1 += r" r r"
                        else:
                            row1 += r" | r r"
                    row1 = row1 + "}\n"
                    # Ueberschrift
                    for rownum1 in range(dataInputAnzahlWKSeite2Print):
                        if rownum1 == 0:
                            row1 = row1 + r"\multicolumn{2}{c}{WK " + \
                                str(rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"}"
                        else:
                            row1 = row1 + r" & \multicolumn{2}{|c}{WK " + \
                                str(rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"}"
                    row1 += "\\\\ \hline\n"
                    # Tabelle
                    row1 += r"\DTLforeach{names}{"
                    row1 += (r"\dnummer=Nummer, \dvorname=Vorname, "
                        "\dnachname=Nachname, \dgeburtsdatum=Geburtsdatum, "
                        "\dmail=Mail, \dteamname=Teamname, "
                        "\daltersklasse=Altersklasse, "
                        "\daltersklasseplatz=Altersklasseplatz, "
                        "\dgesamtplatz=Gesamtplatz, "
                        "\dgesamtpunkte=Gesamtpunkte")
                    for rownum1 in range (dataInputAnzahlWK):
                        row1 += r", \dwk" + helper.zahl2String(rownum1+1) + r"=WK" + \
                            str(rownum1+1)
                        row1 += r", \dwk" + helper.zahl2String(rownum1+1) + \
                            r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                    row1 += "}{\n"
                    for rownum1 in range (dataInputAnzahlWKSeite2Print):
                        if rownum1 == 0:
                            row1 += r"\PrintTime{\dwk" + \
                                helper.zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"} & \dwk" + \
                                helper.zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"punkte"
                        else: 
                            row1 += r" & \PrintTime{\dwk" + \
                                helper.zahl2String(\
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"} & \dwk" + \
                                helper.zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"punkte"
                    row1 += "\\\\\n}\n"
                    # Footer Tabelle
                    row1 += "\end{longtable}\n"
                dataInputTemplate.insert(rownum, row1)
                

        rownum += 1
                
            
    ######################################################
    # Schreibe Ergebnisliste Template
    rv = helper.fileWriteTemplate(fileTemplateOutErgebnisliste, dataInputTemplate)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = helper.callPDFlatex(fileTemplateOutErgebnisliste)

    return rv
