DLRG-Wettkampf
==============

Dieses Python-Script kann dazu genutzt werden, um einen DLRG Wettkampf
auszuwerten. Es werden die Punkte berechnet, eine Platzierung erstellt und
Urkunden, sowie Ergebnislisten mit pdflatex erstellt.

Um das Script sinnvoll einsetzen zu können, muss zuerst der Wettkampf
"erstellt" werden:
1) Mit
   $ ./auswertung.py --erstelle-wettkampfliste-beispiel
   wird eine beispielhafte Wettkampfliste im Ordner in/ erstellt.
   Diese sollte editiert werden und von in/wettkampfliste-beispiel.csv nach
   in/wettkampfliste.csv umbenannt werden.

2) Mit
   $ ./auswertung.py --erstelle-rekorde-beispiel
   wird eine beispielhafte Tabelle für die Referenzrekorde erstellt.
   Auch diese Datei muss dem Wettkampf angepasst werden und von
   in/rekorde-beispiel.csv nach in/rekorde.csv umbenannt werden.
   Derzeit sind nur gemischt ausgetragene Wettkämpfe möglich, eine Aufteilung
   nach männlich/weiblich ist nicht möglich.

3) Mit
   $ ./auswertung.py --erstelle-stammdaten
   wird eine Stammdaten-Template erstellt. In dieser Datei werden die Namen,
   Teamnamen, usw. und Zeiten der Schwimmer eingetragen. Hierfür müssen die
   Dateien in/wettkampfliste.csv und in/rekorde.csv exisitieren!

4) Mit
   $ ./auswertung.py --erstelle-urkunden
   werden die Punkte berechnet und im Ordner out/ gespeichert.
   Zusätzlich wird mit pdflatex Urkunden und Ergebnislisten erstellt. Die
   Templates liegen im Ordner template/
