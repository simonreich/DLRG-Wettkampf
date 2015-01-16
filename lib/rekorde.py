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


# Erstelle Beispieldatei fuer Rekorde
def erstelleRekordeBeispiel(fileOutputRekordeBeispiel, fileInputRekorde):
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

    # Daten speichern
    rv = helper.fileWrite(fileOutputRekordeBeispiel, dataOutput)

    return 0
