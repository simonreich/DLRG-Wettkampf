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
