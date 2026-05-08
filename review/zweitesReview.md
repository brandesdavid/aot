# Zweites Review (Gruppe 22)

Ihr schreibt:
> "Diese Struktur ist jedoch nicht mittels Feldobjekten modelliert, vielmehr sind die ”Felder“ die Einträge verschiedener Arrays (an den jeweils gleichen Indizes)." (P. 2)

Wie hängen die Felder und die Array Indizes zusammen? Ist es ein zwei-dimensionales Array, oder werden alle Felder z.B. von oben links, nach unten rechts durchnummeriert?
Für eine außenstehende Leserin würde es hier helfen, diese Modelierung zu konkretisieren.

Es kann sinnvoll sein noch weitere Experimente zu eurer Forschungsfrage durchzuführen. Die Experimente, die ihr bisher aufgeführt habt, sind viel mehr Simulationen zu einem einzigen Experiment. Z.B. könntet ihr noch ein weiteres Experiment durchführen, bei dem es mehr AntAgents gibt als bei dem ersten. Bei beiden Experimenten gibt es drei Simulationen zwischen denen ihr wie von euch beschrieben die Verdunstungsrate anpasst.

(david: muss das hier auch noch schöner schreiben:)

# systemdesign
- hier ist unklar was pheroDropOff macht: ist es die Rate, wie schnell sich die Pheromone verdunsten, oder wie viel ein Agent es ablegt, welches dann abnimmt? Wie bei der Verdunstung wird also die Pheromonzahl, die ein Agent abgibt verringert? Wieso eigentlich?
  - "Außerdem verwaltet der Agent
die Pheromone, die er abgibt, diese verringern sich mit jedem Tick, mit
dem sich der Agent von Nest/Nahrung entfernt, und zwar ebenso ex-
ponentiell wie bei der Verdunstung, jedoch mit einem eigenen (a priori
und für alle gleich festgelegtem) Parameter pheroDropOff"
- "Dabei soll der Agent geradeaus laufen, also dorthin wo er hergekommen ist.." 
  - es wurde nur gesagt, dass eine wahrscheinlichkeitsverteilung genutzt wird für die navigation
    wie spielen sich die pheromone hier zur navigation ein? 
    - "... und mit erhöhter Wahrscheinlichkeit in Richtung Nahrung/Nest" -> etwas unklar, ob Agent einfach gerade aus läuft und einen Kompass nutzt zum Nest/Nahrung, oder dabei die Pheromone als Navigation nimmt. Was ist wenn 

# ablauf der simulation

- " Manager sortiert tote Ameisen aus... platziert Nahrung auf Feld" 
  - ich könnte mir vorstellen, dass diese nahrung den kürzesten weg  schaden würde.
  - ant colony optimization hat standardmäßig kein reuse für essen. die platzierte nahrung impliziert eine biologischere simulation einer ameisenkolonie.

- "(e)Manager verwaltet Nahrung, führt drop bzw pickup funktionen aus", kann eine ameise auch einfach food droppen, oder nur wenn eine ameise stirbt? wird das nicht schon in schritt (d) ausgeführt?
- "(f) Manager platzier neue Pheromone, entsprechend der Position der Agenten und der Menge die ihm die dropPheromon Funktion mitteilt" -> verwaltet nicht der Agent die pheromone? kommt die menge aus pheroDropoff an? Es wurde gesagt, dass der Wert zwischen 0 bis 1 ist. ist es möglich 0.5 pheromonitems zu droppen?
- hier ist fragwürdig, wieso die menge an pheromonen die eine ameise abgibt sich weiter abnimmt. kann eine ameise essen finden irgendwann keine nestpheromone mehr ablegen?

# forschungsfrage:

- hier ist unsicher bei den möglichen wegen zu berechnung der effizienz zu sagen, was genau berechnet wird.
- wie wird die korrelation mit der gefundenen nahrung und der pheromonsumme berechnet? was ist die pheromonsumme? pro takt wieviele pheromone auf dem feld sind? 
- ich würde hier empfehlen, vielleicht genauer zu definieren, was die effizienz eines netzwerks ist.
- beim abschnitt der experimente wird die verdunstungsrate erhöht. ich würde für die hypothese wenigstens noch die anzahl der ameisen miteinbringen