from lib import helper


# Erstelle Stammdaten template
def erstelleStammdaten(fileInputWettkampfliste, fileInputMeldeliste, fileInputStammdaten, dataInputStammdatenHeader):
    """ Erstellt eine Datei, die eine leere Stammdatenbank beinhaltet.
    """

    dataOutputHeader = dataInputStammdatenHeader
    dataOutput = [[0 for x in range(0)] for x in range(0)]
    dataInputAnzahlStammdaten = len(dataInputStammdatenHeader)

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
        dataOutputHeader.append("WK" + str(rownum+1))

    # Oeffne Meldeliste und kopiere Stammdaten
    data = helper.fileOpen(fileInputMeldeliste)
    if data == 1:
        return 1

    # Lade csv in Array
    rownum=0
    for row in data:
        if rownum > 0:
            dataOutput.append(row)
        rownum += 1

    rownum=0
    for row in dataOutput:
        cellnum=0
        for cell in row:
            if (rownum >= dataInputAnzahlStammdaten):
                dataOutput[rownum][cellnum] = ""
            cellnum += 1
        rownum += 1

    # Daten speichern
    rv = helper.fileWrite(fileInputStammdaten, dataOutput, dataOutputHeader)

    return 0
