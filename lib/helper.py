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


# system
from datetime import date
from datetime import datetime
import operator
import subprocess
import os.path
import csv


def fileOpen(fileName):
    """ Liest eine Datei als csv
        fileName: Dateiname als string
    """
    if os.path.exists(fileName) == False:
        print("Die Datei " + fileName + " existiert nicht.")
        return 1

    # Datei oeffnen
    fileInputHandle = open(fileName, 'rt')
    fileInputReader = csv.reader(fileInputHandle)

    data = [[0 for x in range(0)] for x in range(0)]
    for row in fileInputReader:
        data.append(row)
    
    # Datei schliessen
    fileInputHandle.close ()

    return data


def fileWrite(fileName, data, dataHeader=""):
    """ Schreibt eine Datei als csv
        fileName: Dateiname als string
        data: data list to write
        dataHeader: optional first line to write
    """
    if os.path.exists(fileName) == True:
        print("Die Datei " + fileName + " existiert bereits.")
        return 1

    # Daten speichern
    fileOutputHandle = open (fileName, "wt")
    fileOutputWriter = csv.writer (fileOutputHandle, 
        delimiter=',', 
        quotechar='"', 
        quoting=csv.QUOTE_ALL)

    if dataHeader != "":
        fileOutputWriter.writerow(dataHeader)

    for row in data:
        fileOutputWriter.writerow(row)

    # Datei schliessen
    fileOutputHandle.close()

    print ("Die Datei " + fileName + \
        " wurde erfolgreich geschrieben.")

    return 0


def fileOpenTemplate(fileName):
    """ Liest eine Datei
        fileName: Dateiname als string
    """
    if os.path.exists(fileName) == False:
        print("Die Datei " + fileName + " existiert nicht.")
        return 1

    # Datei oeffnen
    fileInputHandle = open(fileName, 'rt')
    fileInputReader = fileInputHandle.readlines()

    data = [[0 for x in range(0)] for x in range(0)]
    for row in fileInputReader:
        data.append(row)
    
    # Datei schliessen
    fileInputHandle.close ()

    return data


def fileWriteTemplate(fileName, data):
    """ Schreibt eine Datei als csv
        fileName: Dateiname als string
        data: data list to write
        dataHeader: optional first line to write
    """
    if os.path.exists(fileName) == True:
        print("Die Datei " + fileName + " existiert bereits. Sie wird "
            "überschrieben")

    # Daten speichern
    fileOutputHandle = open (fileName, "wt")
    
    for row in data:
        fileOutputHandle.write("".join(str(row)))

    # Datei schliessen
    fileOutputHandle.close()

    print ("Die Datei " + fileName + \
        " wurde erfolgreich geschrieben.")

    return 0


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


# Call pdflatex
def callPDFlatex(filename):
    """ Calls pdflatex twice
        filename:
    """
    rv = subprocess.call(['pdflatex', filename],
        shell=False)
    if rv != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            filename)
        return 1
    rv = subprocess.call(['pdflatex', filename],
        shell=False)
    if rv != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            filename)
        return 1

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


