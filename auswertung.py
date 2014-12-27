"""
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
    der GNU General Public License, wie von der Free Software Foundation,
    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
    veröffentlichten Version, weiterverbreiten und/oder modifizieren.

    Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber
    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
    Siehe die GNU General Public License für weitere Details.

    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
"""

# Dateiname der zu lesenden Stammdaten
fileInputStammdaten="stammdaten.csv"

# Dateiname der zu lesenden Rekorde
fileInputRekorde="in/rekorde.csv"

# Dateiname der zu lesenden Rekorde
fileInputWettkampfliste="in/wettkampfliste.csv"

# Dateiname des zu lesenden Urkunden-Templates
fileInputUrkunde="template/urkunden/urkunde.tex"

# Dateiname des zu lesenden Ergebnislisten-Templates
fileInputErgebnisliste="template/ergebnislisten/ergebnisliste.tex"

# Dateinamen der zu speichernden Ergebnislisten, alphabetisch sortiert
fileOutputAlpha="out/namelist_alpha.csv"

# Dateinamen der zu speichernden Ergebnislisten, nach Gesamtplatz sortiert
fileOutputGesamtplatz="out/namelist_gesamt.csv"

# Dateinamen der zu speichernden Ergebnislisten, nach Altersklassenplatz
# sortiert
fileOutputAlstersklasseplatz="out/namelist_altersklasse.csv"

# Ordner fuer Outputdateien
fileOutputFolder="out"

# Dateinamen der zu speichernden Beispiel-Wettkampflisten
fileOutputWettkampflisteBeispiel="in/wettkampfliste-beispiel.csv"

#Dateinamen der zu speichernden Beispiel-Rekorden
fileOutputRekordeBeispiel="in/rekorde-beispiel.csv"


######################################################
## No Configuration after this
######################################################


import csv
import sys
from datetime import date
from datetime import datetime
import operator
import os.path
import subprocess


# Stammdaten
global dataInputStammdatenHeader
global dataInputAnzahlStammdaten
dataInputStammdatenHeader = ["Nummer", "Vorname", "Nachname", "Geburtsdatum", \
    "Mail", "Teamname"]
dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)


def sanityCheckInputfiles(typeOfTest):
    """ Prueft, ob die Inputdaten korrekt formatiert sind
        typeOfTest: prueft wieviel getestet werden soll
                    erlaubt sind
                    1 fuer Test von fileInputRekorde und
                      fileInputWettkampfliste
                    2 fuer Test von 1 und
                      fileInputStammdaten
                    3 fuer Test von 1, 2 und
                      fileInputUrkunde und fileInputErgebnisliste
    """
    if os.path.exists(fileInputRekorde) == False:
        print("Die Datei " + fileInputRekorde + " existiert nicht.")
        return 1
    if os.path.exists(fileInputWettkampfliste) == False:
        print("Die Datei " + fileInputWettkampfliste + " existiert nicht.")
        return 1

    # Rekorde
    fileInputHandle = open(fileInputRekorde, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    dataInputRekorde = [[0 for x in range(0)] for x in range(0)]
    dataInputRekordeHeader = []
    
    rownum=0
    for row in fileInputReader:
        if rownum == 0:
            dataInputRekordeHeader = row
        else:
            dataInputRekorde.append(row)
        rownum += 1

    dataInputRekordeAnzahlWK = len(dataInputRekordeHeader)-1

    if dataInputRekordeAnzahlWK <= 0:
        print("Die Datei " + fileInputRekorde + " enthält zu wenig Wettkämpfe.")
        return 1
    if len(dataInputRekorde) <= 0:
        print("Die Datei " + fileInputRekorde + " enthält zu wenig "
            "Altersklassen.")
        return 1

    # Wettkampfliste
    fileInputHandle = open(fileInputWettkampfliste, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    dataInputWettkampfliste = [[0 for x in range(0)] for x in range(0)]
    dataInputWettlampflisteHeader = []
    
    rownum=0
    for row in fileInputReader:
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


    # Ende von Test 1
    if typeOfTest == 1:
        return 0


    if os.path.exists(fileInputStammdaten) == False:
        print("Die Datei " + fileInputStammdaten+ " existiert nicht.")
        return 1

    # Stammdaten
    fileInputHandle = open(fileInputStammdaten, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    dataInputStammdaten = [[0 for x in range(0)] for x in range(0)]
    dataInputStammdatenHeader = []
    
    rownum=0
    for row in fileInputReader:
        if rownum == 0:
            dataInputStammdatenHeader = row
        else:
            dataInputStammdaten.append(row)

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

    if os.path.isdir(fileOutputFolder) == False:
        print("Der Ordner " + fileOutputFolder + " existiert nicht.")
        return 1


    # Ende von Test 2
    if typeOfTest == 2:
        return 0


    if os.path.exists(fileInputUrkunde) == False:
        print("Die Datei " + fileInputUrkunde + " existiert nicht.")
        return 1
    if os.path.exists(fileInputErgebnisliste) == False:
        print("Die Datei " + fileInputErgebnisliste + " existiert nicht.")
        return 1


    # Ende von Test 3
    return 0


def sort_table_high(table, cols):
    """ sort a table by multiple columns, first element is highest
        table: a list of lists (or tuple of tuples) where each inner list 
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    table.reverse()
    return table


def sort_table_low(table, cols):
    """ sort a table by multiple columns, first element is lowest
        table: a list of lists (or tuple of tuples) where each inner list 
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        table = sorted(table, key=operator.itemgetter(col))
    return table


# Berechne die Altersklasse
def berechneAltersklasse (born):
    """ Berechnet die Altersklassen nach eingabe des Datums
        born: ein Datum nach dd.mm.YYYY
    """
    date_object = datetime.strptime(born, '%d.%m.%Y')
    today = date.today()
    age_year = today.year - date_object.year - \
        ((today.month, today.day) < (date_object.month, date_object.day))
    if age_year > 18:
        return "offen"
    else:
        if age_year%2 == 0:
            return str(age_year-1)+ "/" + str(age_year)
        else:
            return str(age_year)+ "/" + str(age_year+1)

    return "offen"


# Berechne die Punkte nach der DLRG Formel von 2011
def berechnePunkte (zeit, rekord):
    """ Berechnet die Punkte nach der DLRG Punkte Fromel aus dem 
        Regelwerk von 2011.
        zeit:   die erreichte Schwimmzeit in Sekunden
        rekord: Referenzrekord, also der aktuelle Weltrekord in 
                Sekunden
    """
    punkte = 0.0

    # a string is passed
    if zeit == "" or rekord == "":
        return 0

    # convert string to float
    zeit = float(zeit)
    rekord = float(rekord)

    # berechne Punkte
    if zeit <= 0 or rekord <= 0:
        return 0

    if zeit < 2*rekord:
        punkte = 467*(zeit/rekord)*(zeit/rekord) - 2001*(zeit/rekord) + 2534
    else:
        punkte = 2000/3 - 400/3*(zeit/rekord)

    # auf zwei Nachkommastellen runden
    punkte = float("{0:.2f}".format(punkte))

    return punkte


# Erstellt ein Text aus der Nummer
def zahl2String (nummer):
    """ Gibt eine Zahl zwischen 0 ... 20 als Tring zurueck
        nummer: ein int zwischen 0 ... 20   
    """
    if nummer == 0:
        return "null"
    elif nummer == 1:
        return "eins"
    elif nummer == 2:
        return "zwei"
    elif nummer == 3:
        return "drei"
    elif nummer == 4:
        return "vier"
    elif nummer == 5:
        return "fuenf"
    elif nummer == 6:
        return "sechs"
    elif nummer == 7:
        return "sieben"
    elif nummer == 8:
        return "acht"
    elif nummer == 9:
        return "neun"
    elif nummer == 10:
        return "zehn"
    elif nummer == 11:
        return "elf"
    elif nummer == 12:
        return "zwoelf"
    elif nummer == 13:
        return "dreizehn"
    elif nummer == 14:
        return "vierzehn"
    elif nummer == 15:
        return "fuenfzehn"
    elif nummer == 16:
        return "sechzehn"
    elif nummer == 17:
        return "siebzehn"
    elif nummer == 18:
        return "achtzehn"
    elif nummer == 19:
        return "neunzehn"
    elif nummer == 20:
        return "zwanzig"

    return ""


# Schreibe Hilfetext
def printHilfe (programname):
    """ Gibt einen Hilfetext auf den Bildschirm aus.
    """
    hilfeText = "Aufruf: " + programname + (" [OPTION]\n"
                "Berechnet Punkte und Platzierung für DLRG Schwimmwettkämpfe.\n"
                "Ergebnisse werden als csv-Tabelle gespeichert und mit pdflatex\n"
                "zu Urkunden und Ergebnislisten formatiert.\n\n"
                "[OPTION] kann eine der folgenden Aufrufe sein:\n\n"
                "  -er, --erstelle-rekorde-beispiel  im Ordner in/ wird eine Beispieldatei\n"
                "                            für die Referenzrekorde erzeugt.\n"
                "                            Diese Datei enthält muss für jeden Wettkampf\n"
                "                            den aktuellen Weltrekord für jede Altersklasse\n"
                "                            beinhalten\n"
                "  -ew, --erstelle-wettkampfliste-beispiel  im Ordner in/ wird eine\n"
                "                            Beispieldatei für die Wettkampfliste erzeugt.\n"
                "                            Diese Datei enthält muss für jeden Wettkampf\n"
                "                            eine Distanz, die Einheit der Distanz\n"
                "                            und einen Text, der auf den Urkunden benutzt\n"
                "                            wird.\n"
                "  -es, --erstelle-stammdaten   es wird die Rekordliste und Wettkampfliste\n"
                "                            benutzt, um eine Stammdatenbank-Template zu\n"
                "                            erstellen. In diesem Template können dann alle\n"
                "                            Wettkampfzeiten eingetragen werden.\n"
                "  -eu, --erstelle-urkunden  Es werden alle Puntke und Platzierungen\n"
                "                            berechnet.\n"
                "                            Diese werden verschieden sortiert im Ordner\n"
                "                            out/ gespeichert.\n"
                "                            Weiterhin werden mit pdflatex Urkunden und\n"
                "                            Ergebnislisten erstellt. Dafür werden die\n"
                "                            Templates im Ordner template/ benutzt.\n"
                "  -h, --hilfe, --help       Dieser Hilfetext.")

    print(hilfeText)

    return 0


# Erstelle Beispieldatei fuer Wettkampfliste
def erstelleWettkampflisteBeispiel():
    """ Erstellt eine Datei, die Beispieldaten fuer eine Wettkampfliste
        beinhaltet.
    """
    print("Es wird eine Beispieldatei nach " + \
        fileOutputWettkampflisteBeispiel + " geschrieben.")
    print("Dort befinden sich Beispiele für die Datei " + \
        fileInputWettkampfliste + ".")
    dataOutput = [["Distanz", "Einheit", "Schwimmstil"], 
        [50, "m", "Delphin"], 
        [50, "m", "Rücken"], 
        [50, "m", "Brust"], 
        [50, "m", "Freistil"], 
        [100, "m", "Lagen"]]
    fileOutputHandle = open (fileOutputWettkampflisteBeispiel, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)

    for row in dataOutput:
        fileOutputWriter.writerow(row)

    fileOutputHandle.close()

    return 0


# Erstelle Beispieldatei fuer Rekorde
def erstelleRekordeBeispiel():
    """ Erstellt eine Datei, die Beispieldaten fuer eine Rekordliste
        beinhaltet.
    """
    print("Es wird eine Beispieldatei nach " + fileOutputRekordeBeispiel + \
        " geschrieben.")
    print("Dort befinden sich Beispiele für die Datei " + fileInputRekorde + ".")
    dataOutput = [["Altersklasse", "WK1", "WK2", "WK3", "WK4", "WK5"], 
        ["5/6",10,11,12,13,14], 
        ["7/8",8.9,7.6,4.5,11.5,30.4], 
        ["9/10",8.9,7.6,4.5,11.5,30.4], 
        ["11/12",12.4,45.5,14.5,17.6,12.4], 
        ["13/14",12.4,45.5,14.5,17.6,12.4], 
        ["15/16",10.4,12.3,14.4,15.6,17.5], 
        ["17/18",12.3,14.5,15.6,16.7,18.9], 
        ["offen",20,20,20,20,40]]
    fileOutputHandle = open (fileOutputRekordeBeispiel, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)

    for row in dataOutput:
        fileOutputWriter.writerow(row)

    fileOutputHandle.close()

    return 0


# Erstelle Stammdaten template
def erstelleStammdaten():
    """ Erstellt eine Datei, die eine leere Stammdatenbank beinhaltet.
    """

    # Sanity Check der Input Daten
    if sanityCheckInputfiles(1) != 0:
        return 1

    if os.path.exists(fileInputWettkampfliste) == False:
        print("Die Datei " + fileInputWettkampfliste + " existiert nicht.")
        return 1

    if os.path.exists(fileInputStammdaten) == True:
        print("Die Datei " + fileInputStammdaten + " existiert bereits.")
        return 1

    dataOutput = dataInputStammdatenHeader

    # Oeffne Wettkampfliste und erstelle Liste
    fileInputHandle = open(fileInputWettkampfliste, 'rt')
    fileInputReader = csv.reader (fileInputHandle)

    # Lade csv in Array
    rownum=0
    for row in fileInputReader:
        rownum += 1
    rownumTotal = rownum-1

    # Datei schliessen
    fileInputHandle.close ()

    for rownum in range(rownumTotal):
        dataOutput.append("WK" + str(rownum+1))

    # Daten speichern
    fileOutputHandle = open (fileInputStammdaten, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)

    fileOutputWriter.writerow(dataOutput)

    fileOutputHandle.close()

    print ("Die Datei" + fileInputStammdaten + \
        " wurde ergolgreich geschrieben.")

    return 0


# Erstelle Stammdaten template
def berechneUrkunden():
    """ Berechnet Punkte und Ranking und benutzt anschliessend
        pdflatex, um Urkunden zu erstellen
    """

    # Sanity Check der Input Daten
    if sanityCheckInputfiles(2) != 0:
        return 1

    ######################################################
    # Oeffne Datei und lade csv
    if os.path.exists(fileInputStammdaten) == False:
        print("Die Datei " + fileInputStammdaten + " existiert nicht.")
        return 1

    print ("Lade Datei", fileInputStammdaten)
    
    # Stammdaten
    fileInputHandle = open(fileInputStammdaten, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    # Lade csv in Array
    dataInput = [[0 for x in range(0)] for x in range(0)]
    dataInputHeader = []
    
    rownum=0
    for row in fileInputReader:
        if rownum == 0:
            dataInputHeader = row
        else:
            dataInput.append (row)
    
        rownum += 1
    
    # Datei schliessen
    fileInputHandle.close ()
    
    # Daten in das Output Array kopieren
    dataOutput = dataInput
    dataOutputHeader = dataInputHeader
    
    
    # Rekorde
    if os.path.exists(fileInputRekorde) == False:
        print("Die Datei " + fileInputRekorde + " existiert nicht.")
        return 1

    fileInputHandle = open(fileInputRekorde, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    # Lade csv in Array
    dataRekorde = [[0 for x in range(0)] for x in range(0)]
    dataRekordetHeader = []
    
    rownum=0
    for row in fileInputReader:
        if rownum == 0:
            dataRekordeHeader = row
        else:
            dataRekorde.append (row)
    
        rownum += 1
    
    # Datei schliessen
    fileInputHandle.close ()
    
    
    ######################################################
    # Anzahl der Wettkaempfe
    global dataInputAnzahlWK
    dataInputAnzahlWK = 0
    
    # Lese Anzahl der Wettkaempfe
    for row in dataInput:
        dataInputAnzahlWK = len(row)-dataInputAnzahlStammdaten

    if os.path.exists(fileInputWettkampfliste) == False:
        print("Die Datei " + fileInputWettkampfliste + " existiert nicht.")
        return 1

    fileInputHandle = open(fileInputWettkampfliste, 'rt')
    fileInputReader = csv.reader (fileInputHandle)
    
    rownum=0
    for row in fileInputReader:
        rownum += 1
    
    # Datei schliessen
    fileInputHandle.close ()

    dataInputAnzahlWK = rownum-1
    
    
    ######################################################
    # Altersklasse berechnen
    print ("Berechne Altersklasse")
    
    dataOutputAltersklasseHeader = "Altersklasse"
    dataOutputAltersklasse = []
    
    for row in dataInput:
        dataOutputAltersklasse.append (berechneAltersklasse (row[3]))
    
    
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
                berechnePunkte(
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
    for row in sort_table_high(dataOutput, (dataInputAnzahlStammdaten+1, 2)):
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
    for row in sort_table_high(dataOutput, (dataInputAnzahlStammdaten, 
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
    fileOutputHandle = open (fileOutputAlpha, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)
    
    fileOutputWriter.writerow (dataOutputHeader)
    for row in sort_table_low(dataOutput, (2, 1)):
        fileOutputWriter.writerow(row)
    
    fileOutputHandle.close()
    
    # Gesamtplatz
    fileOutputHandle = open (fileOutputGesamtplatz, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)
    
    fileOutputWriter.writerow (dataOutputHeader)
    for row in sort_table_low(dataOutput, (dataInputAnzahlStammdaten+2, 2)):
        fileOutputWriter.writerow(row)
    
    fileOutputHandle.close()
    
    # Altersklassenplatz
    fileOutputHandle = open (fileOutputAlstersklasseplatz, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)
    
    fileOutputWriter.writerow (dataOutputHeader)
    for row in sort_table_low(dataOutput, (dataInputAnzahlStammdaten, 
            dataInputAnzahlStammdaten+3)):
        fileOutputWriter.writerow(row)
    
    fileOutputHandle.close()

    return 0
    

# Erstelle Stammdaten template
def erstellePDFs():
    """ Erstellt PDFs mittels pfdlatex.
        Die templates liegen im Ordner template/
    """

    # Sanity Check der Input Daten
    if sanityCheckInputfiles(3) != 0:
        return 1

    ######################################################
    # Lade Wettkampfliste
    if os.path.exists(fileInputWettkampfliste) == False:
        print("Die Datei " + fileInputWettkampfliste + " existiert nicht.")
        return 1

    # Oeffne Wettkampfliste und erstelle Liste
    fileInputHandle = open(fileInputWettkampfliste, 'rt')
    fileInputReader = csv.reader (fileInputHandle)

    # Lade csv in Array
    rownum=0
    dataInputWettkamplfliste = [[0 for x in range(0)] for x in range(0)]
    for row in fileInputReader:
        if rownum > 0:
            dataInputWettkamplfliste.append(row)
        rownum += 1
    rownumTotal = rownum-1

    # Datei schliessen
    fileInputHandle.close ()

    dataOutput = ["Nummer", "Vorname", "Nachname", "Geburtsdatum", "Mail", \
        "Teamname"]

    for rownum in range(rownumTotal):
        dataOutput.append("WK" + str(rownum+1))

    # Daten speichern
    fileOutputHandle = open (fileInputStammdaten, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)

    fileOutputWriter.writerow(dataOutput)

    fileOutputHandle.close()


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
            format(dataInputWettkamplfliste[rownumTemp1][0]) + \
            format(r"]{") + \
            format(dataInputWettkamplfliste[rownumTemp1][1]) + \
            format(r"} ") + \
            format(dataInputWettkamplfliste[rownumTemp1][2]) + \
            format(r" & \PrintTime{\dwk") + \
            format(zahl2String(rownumTemp1+1)) + \
            format(r"} & WK ") + \
            format(rownumTemp2+1) + \
            format(r": \unit[") + \
            format(dataInputWettkamplfliste[rownumTemp2][0]) + \
            format(r"]{") + \
            format(dataInputWettkamplfliste[rownumTemp2][1]) + \
            format(r"} ") + \
            format(dataInputWettkamplfliste[rownumTemp2][2]) + \
            format(" & \PrintTime{\dwk") + \
            format(zahl2String(rownumTemp2+1)) + \
            format("} \\\\\n"))
    if dataInputAnzahlWK%2 == 1:
        dataOutput.append("WK " + \
            format(dataInputAnzahlWK2+1) + \
            format(r": \unit[") + \
            format(dataInputWettkamplfliste[dataInputAnzahlWK2][0]) + \
            format(r"]{") + \
            format(dataInputWettkamplfliste[dataInputAnzahlWK2][1]) + \
            format(r"} ") + \
            format(dataInputWettkamplfliste[dataInputAnzahlWK2][2]) + \
            format(" & \PrintTime{\dwk") + \
            format(zahl2String(dataInputAnzahlWK2+1)) + \
            format("} & & \\\\\n"))
    dataOutput.append(format("\end{tabular}\n"))


    ######################################################
    # Oeffne Urkunde Template
    if os.path.exists(fileInputUrkunde) == False:
        print("Die Datei " + fileInputUrkunde + " existiert nicht.")
        return 1

    # Urkunden Template
    fileInputHandle = open(fileInputUrkunde, 'rt')
    dataInputTemplate = fileInputHandle.readlines()
    fileInputHandle.close()

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
                row1 = row1 + r", \dwk" + zahl2String(rownum1+1) + r"=WK" + \
                    str(rownum1+1)
                row1 = row1 + r", \dwk" + zahl2String(rownum1+1) + \
                    r"punkte=WK" + str(rownum1+1) + r"_Punkte"
            row1 = row1 + "}{\n"
            dataInputTemplate.insert(rownum, row1)

        rownum += 1


    ######################################################
    # Schreibe Urkunden Template
    fileOutputUrkunde = fileInputUrkunde + ".temp"
    fileOutputHandle = open (fileOutputUrkunde, "wt")
    for row in dataInputTemplate:
        fileOutputHandle.write("".join(str(row)))

    fileOutputHandle.close()


    ######################################################
    # pdflatex aufrufen
    return_value = subprocess.call(['pdflatex', fileOutputUrkunde], shell=False)
    if return_value != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + fileOutputUrkunde)
        return 1
    return_value = subprocess.call(['pdflatex', fileOutputUrkunde], shell=False)
    if return_value != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + fileOutputUrkunde)
        return 1
        
        


    ######################################################
    # Oeffne Ergebnisliste Template
    if os.path.exists(fileInputErgebnisliste) == False:
        print("Die Datei " + fileInputErgebnisliste + " existiert nicht.")
        return 1

    # Urkunden Template
    fileInputHandle = open(fileInputErgebnisliste, 'rt')
    dataInputTemplate = fileInputHandle.readlines()
    fileInputHandle.close()

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
                    row1 += r", \dwk" + zahl2String(rownum1+1) + r"=WK" + \
                        str(rownum1+1)
                    row1 += r", \dwk" + zahl2String(rownum1+1) + \
                        r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                row1 += "}{\n"
                row1 += (r"\dnummer & \dvorname & \dnachname & \dteamname & "
                    "\daltersklasse & \daltersklasseplatz & \dgesamtplatz & "
                    "\dgesamtpunkte")
                for rownum1 in range (dataInputAnzahlWK):
                    row1 += r"& \PrintTime{\dwk" + zahl2String(rownum1+1) + \
                        r"} & \dwk" + zahl2String(rownum1+1) + r"punkte"
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
                    row1 += r", \dwk" + zahl2String(rownum1+1) + r"=WK" + \
                        str(rownum1+1)
                    row1 += r", \dwk" + zahl2String(rownum1+1) + \
                        r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                row1 += "}{\n"
                row1 += (r"\dnummer & \dvorname & \dnachname & \dteamname & "
                    "\daltersklasse & \daltersklasseplatz & \dgesamtplatz & "
                    "\dgesamtpunkte")
                for rownum1 in range (dataInputAnzahlWKSeite1):
                    row1 += r"& \PrintTime{\dwk" + zahl2String(rownum1+1) + \
                        r"} & \dwk" + zahl2String(rownum1+1) + r"punkte"
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
                        row1 += r", \dwk" + zahl2String(rownum1+1) + r"=WK" + \
                            str(rownum1+1)
                        row1 += r", \dwk" + zahl2String(rownum1+1) + \
                            r"punkte=WK" + str(rownum1+1) + r"_Punkte"
                    row1 += "}{\n"
                    for rownum1 in range (dataInputAnzahlWKSeite2Print):
                        if rownum1 == 0:
                            row1 += r"\PrintTime{\dwk" + \
                                zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"} & \dwk" + \
                                zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"punkte"
                        else: 
                            row1 += r" & \PrintTime{\dwk" + \
                                zahl2String(\
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"} & \dwk" + \
                                zahl2String(
                                    rownum1+dataInputAnzahlWKSeite2Offset+1) + \
                                r"punkte"
                    row1 += "\\\\\n}\n"
                    # Footer Tabelle
                    row1 += "\end{longtable}\n"
                dataInputTemplate.insert(rownum, row1)
                

        rownum += 1
                
            
    ######################################################
    # Schreibe Urkunden Template
    fileOutputErgebnisliste = fileInputErgebnisliste + ".temp"
    fileOutputHandle = open (fileOutputErgebnisliste, "wt")
    for row in dataInputTemplate:
        fileOutputHandle.write("".join(str(row)))

    fileOutputHandle.close()


    ######################################################
    # pdflatex aufrufen
    return_value = subprocess.call(['pdflatex', fileOutputErgebnisliste], 
        shell=False)
    if return_value != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            fileOutputErgebnisliste)
        return 1
    return_value = subprocess.call(['pdflatex', fileOutputErgebnisliste], 
        shell=False)
    if return_value != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            fileOutputErgebnisliste)
        return 1


# main function
def main(argv=None):
    """ main function
        argv: possible arguments, will be replaced by sys.argv if none are 
              given.
    """
    if argv is None:
        argv = sys.argv

    for arg in argv:
        if (arg == "-h" or
                arg == "-help" or
                arg == "--help" or
                arg == "--hilfe" or
                arg == "-?" or
                arg == "?"):
            printHilfe(sys.argv[0])

        elif (arg == "--erstelle-stammdaten" or
                arg == "-es"):
            return_value = erstelleStammdaten()
            if return_value != 0:
                sys.exit(return_value)

        elif (arg == "--erstelle-rekorde-beispiel" or
                arg == "-er"):
            return_value = erstelleRekordeBeispiel()
            if return_value != 0:
                sys.exit(return_value)

        elif (arg == "--erstelle-wettkampfliste-beispiel" or
                arg == "-ew"):
            return_value = erstelleWettkampflisteBeispiel()
            if return_value != 0:
                sys.exit(return_value)

        elif (arg == "--erstelle-urkunden" or
                arg == "-eu"):
            return_value = berechneUrkunden()
            if return_value != 0:
                sys.exit(return_value)
            return_value = erstellePDFs()
            if return_value != 0:
                sys.exit(return_value)

        elif (len(sys.argv) == 1):
            return_value = printHilfe(sys.argv[0])
            if return_value != 0:
                sys.exit(return_value)

    # Ende
    sys.exit(0)


if __name__ == "__main__":
    main()
