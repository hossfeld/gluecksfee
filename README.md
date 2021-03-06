# Glücksfee 

Dieses Python-Skript implementiert ein Losverfahren zur fairen Zuweisung von interessierten SeminarteilnehmerInnen zu Seminaren. Beim Losverfahren wird die begrenzte Kapazität (Anzahl Plätze pro Seminar) berücksichtigt. Desweiteren berücksichtigt das Losverfahren, wieviele Seminare ein Teilnehmer bereits zugewiesen bekommen hat. Dazu wird die bisherige maximale Anzahl von zugewiesen Seminaren benutzt: `curMax`. Eine TeilnehmerIn `i` hat bereits `yi` viele Seminare zugewiesen bekommen. Dann wird die (unnormierte) Wahrscheinlichkeit, dass diese TeilnehmerIn einen Seminarplatz für das nächste Seminar zugewiesen bekommt, wie folgt berechnet:

`pi = curMax+1-yi`

Falls einer TeilnehmerIn `i` noch kein Seminar zugewiesen wurde, wird dies gesondert berücksichtigt und die Wahrscheinlichkeit entsprechend erhöht. Dies führt dazu, dass die Anzahl der TeilnehmerInnen mit mind. einem zugewiesenen Seminar maximiert wird.

`pi = pi*100 = (curMax+1)*100`

Die Wahrscheinlichkeiten über alle Teilnehmer werden dann normiert: `p = p/p.sum()`

_Beispiel: Es wurde bereits einige Seminare zugewiesen, als nächstes kommt das Seminar 1 dran:_

    user 19 has 2 seminars assigned: [5 8] and requested [0 1 2 4 5 6 8]; prob. for next seminar 0.07%
    user 22 has 1 seminars assigned: 6 and requested [0 1 3 4 6]; prob. for next seminar 0.13%
    user 23 has 0 seminars assigned: [] and requested [0 3 4]; prob. for next seminar 19.71%

Die Wahrscheinlichkeiten in den Zuweisungsrunden sehen wie folgt aus. `p_0` ist die Wahrscheinlichkeit für TeilnehmerInnen, die bisher noch kein Seminar zugewiesen bekommen hat. `p_i` ist die Wahrscheinlichkeit für TeilnehmerInnen, die bisher `i` Seminare zugewiesen bekommen haben. `p_*=100%` zeigt an, dass weniger Anfragen als Plätze vorhanden sind und alle zugewiesen werden. In Klammern sind die Anzahl der zugewiesenen TeilnehmerInnen angegeben.
	
	Round 0: Seminar "Python für Anfänger A" p_*=100% (8); 
	Round 1: Seminar "Python für Anfänger B" p_*=100% (8); 
	Round 2: Seminar "Tandemfahren" p_*=100% (8); 
	Round 3: Seminar "Hundeerziehung" p_*=100% (9); 
	Round 4: Seminar "Vegan kochen" p_*=100% (11); 
	Round 5: Seminar "Informatik Einführung A" p_0=19.7109% (5); p_1=0.1314% (9); p_2=0.0657% (4); 
	Round 6: Seminar "Informatik Einführung B" p_0=16.4384% (6); p_1=0.1096% (8); p_2=0.0548% (9); 
	Round 7: Seminar "Klimaneutralität A" p_0=31.9234% (3); p_1=0.2394% (9); p_2=0.1596% (12); p_3=0.0798% (2); 
	Round 8: Seminar "Klimaneutralität B" p_0=85.4701% (1); p_1=0.6410% (11); p_2=0.4274% (15); p_3=0.2137% (5); 
	Round 9: Seminar "Klimaneutralität C" p_1=5.8824% (7); p_2=3.9216% (12); p_3=1.9608% (6); 	
		
Bei der Zuweisung werden die Seminare in aufsteigender Reihenfolge ihrer Beliebtheit durchgegangen. Zuerst wird mit dem Seminar mit der geringsten Nachfrage begonnen. 
Falls ein Seminar mehr Plätze als Anfragen hat, werden alle TeilnehmerInnen dem Seminar zugewiesen.

Mit dieser Zuweisungsstrategie wird gewährleistet, dass die zur Verfügung stehenden Seminarplätze möglichst gut ausgenutzt werden und so den SeminarteilnehmerInnen maximal viele Seminarplätze zuzuzweisen. Das Losverfahren berücksichtigt hierbei eine maximal Anzahl von Seminaren, die einem Seminarteilnehmer zugewiesen wird; der Default-Wert sind 999 Seminare. Die erwartete Fairness des Verfahrens ist nah am theoretischen Optimum. Desweiteren wird die Anzahl der TeilnehmerInnen mit mind. einem zugewiesenen Seminar maximiert. 

## Eingabedatei
Die Eingabedaten werden in einer Excel-Datei (siehe ['input.xlsx'](https://github.com/hossfeld/gluecksfee/blob/main/input.xlsx)) angegeben und müssen sich in dem Excel-Sheet "registrierung" befinden. Die Spalten beinhalten die zur Verfügung stehenden Seminare. In der Beispieldatei sind dies die folgenden 10 Seminare:
1. Python für Anfänger A
2. Python für Anfänger B
3. Tandemfahren
4. Hundeerziehung
5. Vegan kochen
6. Informatik Einführung A
7. Informatik Einführung B
8. Klimaneutralität A
9. Klimaneutralität B
10. Klimaneutralität C

Für jede registrierte TeilnehmerIn gibt es eine Zeile. Eine "1" gibt an, dass sich die TeilnehmerIn für das Seminar registriert hat. In der Beispieldatei hat sich Mia für 4 Seminare angemeldet: Python für Anfänger A, Python für Anfänger B, Tandemfahren, Klimaneutralität B. 

Manche Seminare werden zu verschiedenen Zeiten angeboten, wie z.B. "Python für Anfänger A" und "Python für Anfänger B". Um anzugeben, dass Seminar inhaltlich identisch sind, gibt es eine Extrazeile "inhaltlich" mit der inhaltlich identische Seminare angegeben werden. In diesem Fall würde Mia höchstens einer der beiden Python-Seminare zugewiesen werden, aber niemals mehreren inhaltlich identischen Seminaren.

Um die Anzahl der zur Verfügung stehenden Plätze pro Seminar anzugeben, gibt es eine Extrazeile, die "Plaetze" anzugeben ist. Die Anzahl der Plätze pro Seminar kann variabel angegeben werden, wie es in der Beispieldatei angegeben ist. Wird diese Zeile weggelassen, werden pro Seminar standardmäßig 14 Plätze angenommen.

_Beispiel-Datei: input.xlsx:_
Person	| Python für Anfänger | Yoga | Tandemfahren | Hundeerziehung | Vegan kochen | Reggae tanzen | Informatik Einführung | Klimaneutralität | Herbstlaubbastelarbeit | Moderation von Seminaren
Person 	| Python für Anfänger A	|  Python für Anfänger B	|  Tandemfahren	|  Hundeerziehung	|  Vegan kochen	|  Informatik Einführung A	|  Informatik Einführung B	|  Klimaneutralität A	|  Klimaneutralität B	| Klimaneutralität C
-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----
inhaltlich |  1 | 	1 | 2 | 3 | 4 | 5 | 5 | 6 | 6 | 6
Plaetze | 17 | 15 | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 10
Mia | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0
Emma | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0
Hannah | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0

## Ausführung des Programms
Das Programm wird in einer Konsole aufgerufen. Hierbei können verschiedene Parameter angegeben werden. Wichtig ist hierbei der `SEED`, der den [Zufallszahlengenerator](https://de.wikipedia.org/wiki/Zufallszahlengenerator) für das Losverfahren initialisiert. Bei jedem Start des Losverfahrens mit dem gleichem Startwert (engl. seed) wird die gleiche Zufallszahlenfolge erzeugt, weshalb diese Zufallszahlen reproduziert werden können. Damit ist das Losverfahren auch im Nachhinein noch nachvollziehbar und reproduzierbar. Die erzeugten Zufallszahlen dienen dazu, die Seminarteilnehmer entsprechend der Wahrscheinlichkeiten (s. oben) zuzuweisen.


```
SeKo Gluecksfee zur Seminarteilnehmer Auslosung

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
```

## Ausgabe des Programms
Das Programm speichert das Ergebnis des Losverfahrens in einer Excel-Datei. Der Default-Name ist `output.xlsx`, aber es kann ein beliebiger Dateiname angegeben werden. Es stehen verschiedene Excel-Sheets zur Verfügung, um das Ergebnis des Losverfahrens darzustellen. 

#### Seminar
Für jedes angebotene Seminar gibt es eine Zeile. Die Spalte _Plaetze_ zeigt die zur Verfügung stehenden Seminarplätze für dieses Seminar an, d.h. die Eingabe aus der Inputdatei. Die Spalte _Teilnehmer_ gibt an, wieviele TeilnehmerInnen diesem Seminar zugewiesen wurden. Die Spalte _Anfragen_ zeigt an, wieviele TeilnehmerInnen sich für das Seminar angemeldet haben. Die Spalte _Zugewiesen_ gibt den Prozentsatz an, wieviele zur Verfügung stehende Seminarplätze für dieses Seminar zugewiesen wurden. In den darauffolgenden Spalten stehen die Namen der durch das Losverfahren bestimmten TeilnehmerInnen.

#### Assignment
Das Sheet _Assignment_ ist wie die Eingabedatei aufgebaut. In den Spalten finden sich die Seminare; jede Zeile spiegelt die Zuweisung für eine Person wider. Eine `1` bedeutet, dass die Person in der entsprechenden Zeile als TeilnehmerIn für das Seminar in der entsprechenden Spalte ausgewürfelt wurde.

#### Difference
Das Sheet _Difference_ ist wie die Eingabedatei aufgebaut. In den Spalten finden sich die Seminare; jede Zeile spiegelt die Zuweisung für eine Person wider. Eine `1` bedeutet, dass die Person in der entsprechenden Zeile als TeilnehmerIn für das Seminar in der entsprechenden Spalte ausgewürfelt wurde.  Eine `-1` bedeutet, dass die Person in der entsprechenden Zeile sich als TeilnehmerIn für das Seminar angemeldet hatte, allerdings wurde der TeilnehmerIn kein Platz ausgewürfelt (aufgrund der Beschränkung der Anzahl Plätze pro Seminar bzw. der maximalen Anzahl von Seminaren pro Teilnehmer).

#### Stats_Person
Das Sheet _Stats_Person_ gibt eine Statistik der TeilnehmerInnen an. Die Spalte _requested_ zeigt an, für wieviele Seminare sich die TeilnehmerIn angemeldet hat. Die Spalte _assigned_ gibt an, wieviele Seminar für diese Person ausgewürfelt wurden durch das Losverfahren. Die Spalte _ratio_ gibt die Prozentzahl an, wieviele Seminare relativ zu den registrierten ausgewürfelt wurden. 

#### Parameters
Die Eingabeparameter werden in diesem Sheet festgehalten. Insbesondere wird hier der "Seed" für den Zufallszahlengenerator gespeichert, um die Reproduzierbarkeit zu gewährleisten. 
