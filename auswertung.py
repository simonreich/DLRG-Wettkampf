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

######################################################

# Dateiname der zu lesenden Stammdaten
fileInputStammdaten="stammdaten.csv"

# Dateiname der zu lesenden Meldeliste
fileInputMeldeliste="in/meldeliste.csv"

# Dateiname der zu zu speichernden Laufliste
fileOutputLaufliste="out/laufliste.csv"

# Dateinamen der zu speichernden Liste fuer Laufkarten
fileOutputLaufkarte="out/laufkarte.csv"

# Dateiname der zu lesenden Rekorde
fileInputRekorde="in/rekorde.csv"

# Dateiname der zu lesenden Rekorde
fileInputWettkampfliste="in/wettkampfliste.csv"

# Dateinamen der zu speichernden Ergebnislisten, alphabetisch sortiert
fileOutputAlpha="out/namelist_alpha.csv"

# Dateinamen der zu speichernden Ergebnislisten, nach Gesamtplatz sortiert
fileOutputGesamtplatz="out/namelist_gesamt.csv"

# Dateinamen der zu speichernden Ergebnislisten, nach Altersklassenplatz
# sortiert
fileOutputAlstersklasseplatz="out/namelist_altersklasse.csv"

# Dateinamen der zu speichernden Beispiel-Wettkampflisten
fileOutputWettkampflisteBeispiel="in/wettkampfliste-beispiel.csv"

#Dateinamen der zu speichernden Beispiel-Rekorden
fileOutputRekordeBeispiel="in/rekorde-beispiel.csv"


######################################################
# Latex Templates

# Dateiname des zu lesenden Meldelisten-Templates
fileTemplateMeldeliste="template/meldeliste/meldeliste.tex"
fileTemplateOutMeldeliste="out/meldeliste.tex"

# Dateiname des zu lesenden Urkunden-Templates
fileTemplateUrkunde="template/urkunden/urkunde.tex"
fileTemplateOutUrkunde="out/urkunde.tex"

# Dateiname des zu lesenden Ergebnislisten-Templates
fileTemplateErgebnisliste="template/ergebnislisten/ergebnisliste.tex"
fileTemplateOutErgebnisliste="out/ergebnisliste.tex"

# Dateiname des zu lesenden Lauflisten-Templates
fileTemplateLaufliste="template/lauflisten/laufliste.tex"
fileTemplateOutLaufliste="out/laufliste.tex"

# Dateiname des zu lesenden Laufkarten-Templates
fileTemplateLaufkarte="template/laufkarten/laufkarte.tex"
fileTemplateOutLaufkarte="out/laufkarte.tex"


######################################################
## No Configuration after this
######################################################


# system
import sys

# DLRG-Wettkampf
from lib import meldeliste
from lib import lauflisten
from lib import laufkarten
from lib import rekorde
from lib import wettkampfliste
from lib import stammdaten
from lib import ergebnisliste


# globale Variablen
global dataInputStammdatenHeader
dataInputStammdatenHeader = ["Nummer", "Vorname", "Nachname", "Geburtsdatum", \
    "Mail", "Teamname"]
global dataInputAnzahlStammdaten
dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)
global BahnenAnzahl
BahnenAnzahl = 5


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
                "  -em, --erstelle-meldeliste   aus der Rekorde-Liste und der\n"
                "                            Wettkampfliste wird eine Meldeliste erstellt.\n"
                "  -emp, --erstelle-meldeliste-pdf   aus der ausgefüllten Meldeliste wird\n" 
                "                            ein pdf mittels pdflatex erstellt.\n"
                "  -el, --erstelle-laufliste    aus der Meldeliste wird eine\n"
                "                            Laufliste erzeugt.\n"
                "  -ek, --erstelle-laufkarte    aus der Laufliste werden die\n"
                "                            Laufkarten erzeugt.\n"
                "  -es, --erstelle-stammdaten   aus der Meldeliste wird eine\n"
                "                            Stammdatenbank erstellt, in der die\n"
                "                            Schwimmzeiten eingetragen werden.\n"
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

        elif(arg == "--erstelle-rekorde-beispiel" or
                arg == "-er"):
            rv = rekorde.erstelleRekordeBeispiel(
                fileOutputRekordeBeispiel, 
                fileInputRekorde)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-wettkampfliste-beispiel" or
                arg == "-ew"):
            rv = wettkampfliste.erstelleWettkampflisteBeispiel(
                fileOutputWettkampflisteBeispiel, 
                fileInputWettkampfliste)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-meldeliste" or
                arg == "-em"):
            rv = meldeliste.erstelleMeldeliste(
                fileInputWettkampfliste, 
                fileInputMeldeliste,
                dataInputStammdatenHeader)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-meldeliste-pdf" or
                arg == "-emp"):
            rv = meldeliste.erstellePDFMeldeliste(
                fileTemplateMeldeliste, 
                fileTemplateOutMeldeliste, 
                fileInputMeldeliste, 
                fileInputWettkampfliste)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-laufliste" or
                arg == "-el"):
            rv = lauflisten.erstelleLauflisten(
                fileInputMeldeliste, 
                dataInputStammdatenHeader, 
                fileOutputLaufliste, 
                BahnenAnzahl)
            if rv != 0:
                sys.exit(rv)
            rv =  lauflisten.erstellePDFLauflisten(
                fileTemplateLaufliste,
                fileTemplateOutLaufliste, 
                fileOutputLaufliste,
                BahnenAnzahl)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-laufkarte" or
                arg == "-ek"):
            rv = laufkarten.erstelleLaufkarte(
                fileOutputLaufliste, 
                fileOutputLaufkarte,
                dataInputStammdatenHeader)
            if rv != 0:
                sys.exit(rv)
            rv =  laufkarten.erstellePDFLaufkarten(
                fileTemplateLaufkarte, 
                fileTemplateOutLaufkarte, 
                fileOutputLaufkarte)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-stammdaten" or
                arg == "-es"):
            rv = stammdaten.erstelleStammdaten(
                fileInputWettkampfliste, 
                fileInputMeldeliste, 
                fileInputStammdaten,
                dataInputStammdatenHeader)
            if rv != 0:
                sys.exit(rv)

        elif(arg == "--erstelle-urkunden" or
                arg == "-eu"):
            rv = ergebnisliste.erstelleErgebnisliste(
                fileInputStammdaten, 
                fileInputRekorde, 
                fileInputWettkampfliste, 
                fileOutputAlpha, 
                fileOutputAlstersklasseplatz, 
                fileOutputGesamtplatz,
                dataInputStammdatenHeader)
            if rv != 0:
                sys.exit(rv)
            rv = ergebnisliste.erstellePDFUrkunden(
                fileInputWettkampfliste, 
                fileTemplateUrkunde, 
                fileTemplateOutUrkunde, 
                fileOutputAlpha)
            if rv != 0:
                sys.exit(rv)
            rv = ergebnisliste.erstellePDFErgebnisliste(
                fileTemplateErgebnisliste, 
                fileTemplateOutErgebnisliste,
                fileOutputAlstersklasseplatz)
            if rv != 0:
                sys.exit(rv)

        elif(len(sys.argv) == 1):
            rv = printHilfe(sys.argv[0])
            if rv != 0:
                sys.exit(rv)

    # Ende
    sys.exit(0)


if __name__ == "__main__":
    main()
