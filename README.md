# Glücksfee: 

Dieses Python-Skript implementiert ein Losverfahren zur fairen Zuweisung von interessierten SeminarteilnehmerInnen zu Seminaren. Beim Losverfahren wird die begrenzte Kapazität (Anzahl Plätze pro Seminar) berücksichtigt. Desweiteren berücksichtigt das Losverfahren, wieviele Seminare ein Teilnehmer bereits zugewiesen bekommen hat. Dazu wird die bisherige maximale Anzahl von zugewiesen Seminaren benutzt: `curMax`. Eine TeilnehmerIn `i` hat bereits `yi` viele Seminare zugewiesen bekommen. Dann wird die (unnormierte) Wahrscheinlichkeit, dass diese TeilnehmerIn einen Seminarplatz für das nächste Seminar zugewiesen bekommt, wie folgt berechnet:

`pi = curMax+0.1-yi`

Die Wahrscheinlichkeiten über alle Teilnehmer werden dann normiert: `p = p/p.sum()`

_Beispiel: Es wurde bereits einige Seminare zugewiesen, als nächstes kommt das Seminar 1 dran:_
    user 39 has 3 seminars assigned: [3 5 9] and requested [0 1 2 3 5 9]; prob. for next seminar 0.27%
    user 41 has 2 seminars assigned: [2 4] and requested [0 1 2 3 4]; prob. for next seminar 2.96%
    user 43 has 0 seminars assigned: [] and requested [0 1]; prob. for next seminar 8.33%
    user 44 has 1 seminars assigned: 4 and requested [0 1 4]; prob. for next seminar 5.65%
    
Bei der Zuweisung werden die Seminare in aufsteigender Reihenfolge ihrer Beliebtheit durchgegangen. Zuerst wird mit dem Seminar mit der geringsten Nachfrage begonnen. Bei der Sortierung wird die relative Nachfrage benutzt: relative_Nachfrage = Anzahl_der_Registierungen / Anzahl_Seminarplätze
Mit dieser Strategie wird gewährleistet, dass die zur Verfügung stehenden Seminarplätze möglichst gut ausgenutzt werden und so den SeminarteilnehmerInnen maximal viele Seminarplätze zuzuzweisen. Das Losverfahren berücksichtigt hierbei eine maximal Anzahl von Seminaren, die einem Seminarteilnehmer zugewiesen wird; der Default-Wert sind 999 Seminare.

## Eingabedatei
Die Eingabedaten werden in einer Excel-Datei (siehe 'input.xlsx') angegeben und müssen sich in dem Excel-Sheet "registrierung" befinden. Die Spalten beinhalten die zur Verfügung stehenden Seminare. In der Beispieldatei sind dies die folgenden 10 Seminare:
* Python für Anfänger	
* Yoga	
* Tandemfahren	
* Hundeerziehung	
* Vegan kochen	
* Reggae tanzen	
* Informatik Einführung	
* Klimaneutralität	
* Herbstlaubbastelarbeit	
* Moderation von Seminaren

Für jede registrierte TeilnehmerIn gibt es eine Zeile. Eine "1" gibt an, dass sich die TeilnehmerIn für das Seminar registriert hat. In der Beispieldatei hat sich Mia für 4 Seminare angemeldet: Python für Anfänger, Yoga, Tandemfahren, Herbstlaubbastelarbeit.

Um die Anzahl der zur Verfügung stehenden Plätze pro Seminar anzugeben, gibt es eine Extrazeile, die "Plaetze" anzugeben ist. Die Anzahl der Plätze pro Seminar kann variabel angegeben werden, wie es in der Beispieldatei angegeben ist. Wird diese Zeile weggelassen, werden pro Seminar standardmäßig 14 Plätze angenommen.


## Ausführung des Programms
Das Programm wird in einer Konsole aufgerufen. Hierbei können verschiedene Parameter angegeben werden. Wichtig ist hierbei der `SEED`, der den [Zufallszahlengenerator](https://de.wikipedia.org/wiki/Zufallszahlengenerator) für das Losverfahren initialisiert. Bei jedem Start des Losverfahrens mit dem gleichem Startwert (engl. seed) wird die gleiche Zufallszahlenfolge erzeugt, weshalb diese Zufallszahlen reproduziert werden können. Damit ist das Losverfahren auch im Nachhinein noch nachvollziehbar und reproduzierbar. Die erzeugten Zufallszahlen dienen dazu, die Seminarteilnehmer entsprechend der Wahrscheinlichkeiten (s. oben) zuzuweisen.


`SeKo Gluecksfee zur Seminarteilnehmer Auslosung

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  randomly initialize the random number generator with
                        that seed
  -i INPUT, --input INPUT
                        Name des Excel-Files zur Eingabe
  -o OUTPUT, --output OUTPUT
                        Die Ausgabe wird im angebenen Excel File gespeichert.
                        Default: output.xlsx
  -m MAXIMUM, --maximum MAXIMUM
                        Die maximale Anzahl von Seminaren, die pro Person
                        zugewiesen wird. Default: 999
  -v [VERBOSE], --verbose [VERBOSE]
                        Gibt eine ausführliche Ausgabe auf der Konsole aus
                        (True or False). Default: True
`                        
