from lib import helper


# Sanity Check
def sanityCheckLaufkarten(fileInputMeldeliste, dataInputStammdatenHeader):
    """ Sanity Check der Input Daten
        fileInputMeldeliste: 
    """
    # Meldeliste
    data = helper.fileOpen(fileInputMeldeliste)
    if data == 1:
        return 1

    dataInput = [[0 for x in range(0)] for x in range(0)]
    dataInputHeader = []

    rownum=0
    for row in data:
        if rownum == 0:
            dataInputHeader = row
        else:
            dataInput.append(row)
        rownum += 1

    if len(dataInputHeader)-len(dataInputStammdatenHeader) <= 0:
        print("Die Datei " + fileInputMeldeliste + " enthält zu wenig"
            "Wettkämpfe.")
        return 1

    if rownum < 1:
        print("Die Datei " + fileInputMeldeliste + " enthält zu wenig"
            "Teilnehmer.")
        return 1

    return 0


# Berechnet die Laufkarten
def erstelleLaufkarte(fileOutputLaufliste, fileOutputLaufkarte, dataInputStammdatenHeader):
    """ Berechnet Laufkarte aus Meldeliste
    """

    # Sanity Check der Input Daten
    #if sanityCheckLaufkarten(fileInputMeldeliste, dataInputStammdatenHeader) != 0:
    #    return 1

    ######################################################
    # Oeffne Datei und lade csv
    # Laufliste
    data = helper.fileOpen(fileOutputLaufliste)
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
            dataInput.append(row)
        rownum += 1
    

    ######################################################
    # Zeilen mit mehr als 1 Eintrag in die naechste Zeile 
    # verschieben
    dataOutput = [[0 for x in range(0)] for x in range(0)]
    dataOutputHeader = ["Lauf", "WK", "Bahn", "Name"]
    rownum=0
    for row in dataInput:
        cellnum=0
        for cell in row:
            rowNeu = []
            if cellnum >= 2:
                rowNeu.append(dataInput[rownum][0])          # Lauf
                rowNeu.append(dataInput[rownum][1])          # WK
                rowNeu.append(len(row)-cellnum)              # Bahn
                rowNeu.append(dataInput[rownum][cellnum])    # Name
                dataOutput.append(rowNeu)

            cellnum += 1
        rownum += 1


    ######################################################
    # Daten speichern
    rv = helper.fileWrite(fileOutputLaufkarte, dataOutput, dataOutputHeader)

    return rv


# Berechnet die Laufkarten
def erstellePDFLaufkarten(fileTemplateLaufkarte, fileTemplateOutLaufkarte, fileOutputLaufkarte):
    """ Erstellt PDFs aus der Laufliste
    """

    ######################################################
    # Oeffne Ergebnisliste Template
    data = helper.fileOpenTemplate(fileTemplateLaufkarte)

    rownum = 0
    for row in data:
        if row.find("<template:laufkarte>") != -1:
            del data[rownum]

            row1 = r"\DTLloaddb{names}{" + fileOutputLaufkarte + "}\n"
            data.insert(rownum, row1)
        rownum += 1


    ######################################################
    # Schreibe Lauflisten Template
    rv = helper.fileWriteTemplate(fileTemplateOutLaufkarte, data)
    if rv != 0:
        return rv


    ######################################################
    # pdflatex aufrufen
    rv = subprocess.call(['pdflatex', fileTemplateOutLaufkarte], 
        shell=False)
    if rv != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            fileTemplateOutLaufkarte)
        return 1
    rv = subprocess.call(['pdflatex', fileTemplateOutLaufkarte], 
        shell=False)
    if rv != 0:
        print("pdflatex konnte nicht aufgerufen werden. Der folgende Befehl "
            "konnte nicht ausgeführt werden:\npdflatex " + \
            fileTemplateOutLaufkarte)
        return 1

    return 0


