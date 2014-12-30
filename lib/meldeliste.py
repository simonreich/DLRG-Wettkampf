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
