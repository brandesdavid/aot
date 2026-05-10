# Zweites Review (Gruppe 22)

Wir bewerten die Projektskizze unter der Annahme, dass wir noch nicht viel über die Aufgabe wissen. Das entstehende Feedback könnte eurer Gruppe helfen, mögliche blinde Flecke in Erklärungen oder Darstellungen für die Dokumentation aufzuzeigen.

Wir gehen in unserem Review nacheinander auf die einzelnen Abschnitte eurer Projektskizze ein.

## 1.1 Systemdesign
Ihr schreibt:
> "Diese Struktur ist jedoch nicht mittels Feldobjekten modelliert, vielmehr sind die ”Felder“ die Einträge verschiedener Arrays (an den jeweils gleichen Indizes)." (P. 2)

Wie hängen die Felder und die Array Indizes zusammen? Ist es ein zwei-dimensionales Array, oder werden alle Felder z.B. von oben links, nach unten rechts durchnummeriert?
Für eine außenstehende Leserin würde es hier helfen, diese Modelierung zu konkretisieren.

Es bleibt unklar, was genau `pheroDropOff` beschreibt: Handelt es sich um die Rate, mit der Pheromone verdunsten, oder um die Menge, die ein Agent ablegt und die anschließend abnimmt? Laut Skizze verwaltet der Agent die Pheromone, die er abgibt – diese verringern sich mit jedem Tick, mit dem sich der Agent von Nest oder Nahrung entfernt, und zwar exponentiell, ähnlich wie bei der Verdunstung, jedoch mit einem eigenen, a priori und für alle Agenten gleich festgelegten Parameter `pheroDropOff`. Es wäre hilfreich, diesen Mechanismus klarer zu beschreiben und zu begründen, warum die abgegebene Pheromonmenge mit zunehmender Entfernung abnimmt.

Auch die Navigationsbeschreibung wirft Fragen auf. Es heißt, der Agent solle „geradeaus laufen, also dorthin, wo er hergekommen ist" - allerdings wurde zuvor nur erwähnt, dass eine Wahrscheinlichkeitsverteilung für die Navigation genutzt wird. Unklar bleibt dabei, welche Rolle die Pheromone in dieser Navigation konkret spielen. Die Formulierung „mit erhöhter Wahrscheinlichkeit in Richtung Nahrung/Nest" lässt offen, ob der Agent dabei einem internen Kompass folgt oder sich an den abgelegten Pheromonen orientiert. Besonders relevant wird diese Frage in Situationen, in denen keine Pheromone vorhanden sind oder in denen beides gleichzeitig eine Rolle spielt – dieser Fall sollte in der Skizze noch adressiert werden.

## 1.3 Ablauf der Simulation

Nahrung nach Tod vs. aktives Droppen: In (d) wird beim Entfernen toter Ameisen fallengelassene Nahrung platziert. In (e) steht allgemein Drop/Pickup der Nahrung. Für uns ist unklar, ob Ameisen freiwillig Essen ablegen können (wenn ja, wann?) und ob (e) nur Pickup oder auch Drop umfasst. Es wäre gut, das zu klären und die Beschreibung so anzupassen, dass sich (d) und (e) nicht teilweise decken.

Wer schreibt die Karte? Die Gridwelt hat addPheromons(), der Agent hat dropPheromon(). In (f) platziert der Manager neue Pheromonmengen nach Meldung der Agenten. Wir würden empfehlen, einmal explizit den Datenfluss (Agent berechnet Menge -> Manager -> Gridwelt) zu beschreiben und ob diskrete „Items“ oder kontinuierliche Mengen auf den Feldern gemeint sind, damit der Wertebereich im Intervall [0, 1] für pheroDropOff bzw. die abgelegte Menge  mit der Verdunstung e mal P passt (Ist es bspw. möglich 0.5 Pheromonitems zu droppen?)

## 1.5 Forschungsfrage
Bei den vorgeschlagenen Methoden zur Berechnung der Effizienz bleibt unklar, was genau gemessen wird. Insbesondere bei der Korrelation zwischen gefundener Nahrung und der Pheromonmenge stellt sich die Frage, was unter „Pheromonsumme" zu verstehen ist – handelt es sich um die Anzahl der Pheromone pro Feld pro Takt, oder um eine andere Größe? Es wäre hilfreich, den Begriff der Netzwerkeffizienz vorab präziser zu definieren, um die nachfolgenden Berechnungen und Vergleiche nachvollziehbarer zu gestalten.

## 1.6 Experimente
Es kann sinnvoll sein noch weitere Experimente zu eurer Forschungsfrage durchzuführen. Die Experimente, die ihr bisher aufgeführt habt, sind viel mehr Simulationen zu einem einzigen Experiment. Z.B. könntet ihr noch ein weiteres Experiment durchführen, bei dem es mehr AntAgents gibt als bei dem ersten. Bei beiden Experimenten gibt es drei Simulationen zwischen denen ihr wie von euch beschrieben die Verdunstungsrate anpasst.

## Anmerkung Datenverarbeitung Wahrnehmung
Dieser Abschnitt ist für uns überhaupt nicht verständlich. Vor allem wäre es gut, wenn ihr hier die angefügte Grafik etwas mehr erläutern würdet. Aber auch in dem Text gibt es einige Lücken, sodass für uns durch diese Anmerkung zur Wahrnehmung nicht besser verständlich wurde wie ihr die Wahrnehmung der Ameisen implementieren wollt.

## Zusammenfassung

Wir hoffen, dass die Anregungen zur Verbesserung der Dokumentation, der Implementierung und der Forschungsfrage helfen können.

Viele Grüße
Moritz Clerc, Carlos Driller, David Brandes
