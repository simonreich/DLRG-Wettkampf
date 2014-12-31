DLRG-Wettkampf
==============

Dieses Python-Script kann dazu genutzt werden, um einen DLRG Wettkampf
aeszuwerten. Es werden die Punkte berechnet, eine Platzierung erstellt und
Urkunden, sowie Ergebnislisten mit pdflatex erstellt.

Das Programm erstellt nach jedem Arbeitsschritt entweder eine csv-Tabelle 
(comma separated table) oder eine pdf-Datei.


## Übersicht der Arbeitsschritte

```
+-------------+ +--------------------+
| 1)          | | 1)                 |
| rekorce.csv | | wettkampfliste.csv |
|             | |                    |
+-------------+ +--------------------+
      |                   |
      +-----+-------------+
            |
            V
+------------------------+
| 2)                     |
| erstelle-Meldeliste    |
|                        +-----------------------+-----------------------------------+
| Output: meldeliste.csv |                       |                                   |
|                        |                       |                                   |
+------------------------+                       |                                   |
            |                                    |                                   |
            |                                    |                                   |
            |                                    |                                   |
            V                                    V                                   V
+------------------------+          +--------------------------+         +-----------------------+
| 6)                     |          |  3)                      |         | 4)                    |
| ertelle-Stammdaten     |          |  erstelle-Meldeliste-pdf |         | erstelle-Laufliste    |
|                        |          |                          |         |                       |
| Output: stammdaten.csv |          |  Output: meldeliste.pdf  |         | Output: laufliste.csv |
|                        |          |                          |         |         laufliste.pdf |
+------------------------+          +--------------------------+         |                       |
            |                                                            +-----------------------+
            |                                                                        |
            |                                                                        |
            V                                                                        V
+---------------------------+                                            +-----------------------+
| 7)                        |                                            | 5)                    |
| ertelle-Urkunden          |                                            | erstelle-Laufkarte    |
|                           |                                            |                       |
| Output: ergebnisliste.pdf |                                            | Output: laufkarte.csv |
|         urkunden.pdf      |                                            |         laufkarte.pdf |
|         namelist.csv      |                                            |                       |
|                           |                                            +-----------------------+
+---------------------------+
```


## Detailierte Erklärung

Im Flowchart sind verschiedene Arbeitsschritte eingezeichnet. Diese sind folgen
dem Ablauf eines Wettkampfs und werden im weiteren beschrieben.

Für alle pdfs wird pdflatex verwendet (welches installiert sein muss). Die 
verwendeten Templates ligen im Ordner template/

1. 
   1. Mit
      $ ./auswertung.py --erstelle-wettkampfliste-beispiel
      wird eine beispielhafte Wettkampfliste im Ordner in/ erstellt.
      Diese sollte editiert werden und von in/wettkampfliste-beispiel.csv nach
      in/wettkampfliste.csv umbenannt werden.
   2. Mit
	  $ ./auswertung.py --erstelle-rekorde-beispiel
	  wird eine beispielhafte Tabelle für die Referenzrekorde erstellt.
	  Auch diese Datei muss dem Wettkampf angepasst werden und von
	  in/rekorde-beispiel.csv nach in/rekorde.csv umbenannt werden.
	  Derzeit sind nur gemischt ausgetragene Wettkämpfe möglich, eine Aufteilung
	  nach männlich/weiblich ist nicht möglich.

2. Mit
   $ ./auswertung.py --erstelle-meldeliste
   wird dann eine leere Meldeliste erzeugt. Hier werden Namen, Mailadresse, usw.
   eingetragen. Weiterhin wird ein "x" (oder beliebiges anderes Zeichen) bei den
   Wettkämpfen gesetzt, an denen der Schwimmer teilnimmt.

3. Mit
   $ ./auswertung.py --erstelle-meldeliste-pdf
   wird aus der ausgefüllten tabelle eine pdf-Datei erzeugt, die als Meldeliste
   veröffentlicht werden kann.

4. Mit
   $ ./auswertung.py --erstelle-laufliste
   werden die Schwimmer auf Bahnen verteilt und in Läufe eingeteilt. laufkarte
   im Script auswertung.py im Hauptordner evtl die Variable BahnenAnzahl 
   angepasst werden, wenn nicht genau 5 Bahnen zur Verfügung stehen.

5. Mit
   $ ./auswertung.py --erstelle-laufkarte
   werden dann die Laufkarten erstellt. Hier können Zeitnehmer Zeit und 
   Strafpunkte eintragen.

6. Mit
   $ ./auswertung.py --erstelle-stammdaten
   wird die Meldeliste in die Datei stammdaten.csv kopiert. Hier können nun die 
   tatsächlich geschwommenen Zeiten eingetragen werden.

7. Mit
   $ ./auswertung.py --erstelle-urkunden
   werden die Punkte berechnet und im Ordner out/ gespeichert.
   Zusätzlich wird mit pdflatex Urkunden und Ergebnislisten erstellt. Die
   Templates liegen im Ordner template/
