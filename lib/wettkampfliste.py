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
