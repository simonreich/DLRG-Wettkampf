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


# Erstelle Beispieldatei fuer Wettkampfliste
def erstelleWettkampflisteBeispiel(fileOutputWettkampflisteBeispiel, fileInputWettkampfliste):
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

    # Daten speichern
    rv = helper.fileWrite(fileOutputWettkampflisteBeispiel, dataOutput)

    return rv
