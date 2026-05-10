# Zweites Review (Gruppe 22)

Wir gehen in unserem Review nacheinander auf die einzelnen Abschnitte eurer Projektskizze ein.

## 1.1 Systemdesign
Ihr schreibt:
> "Diese Struktur ist jedoch nicht mittels Feldobjekten modelliert, vielmehr sind die ”Felder“ die Einträge verschiedener Arrays (an den jeweils gleichen Indizes)." (P. 2)

Wie hängen die Felder und die Array Indizes zusammen? Ist es ein zwei-dimensionales Array, oder werden alle Felder z.B. von oben links, nach unten rechts durchnummeriert?
Für eine außenstehende Leserin würde es hier helfen, diese Modelierung zu konkretisieren.

Es bleibt unklar, was genau `pheroDropOff` beschreibt: Handelt es sich um die Rate, mit der Pheromone verdunsten, oder um die Menge, die ein Agent ablegt und die anschließend abnimmt? Laut Skizze verwaltet der Agent die Pheromone, die er abgibt – diese verringern sich mit jedem Tick, mit dem sich der Agent von Nest oder Nahrung entfernt, und zwar exponentiell, ähnlich wie bei der Verdunstung, jedoch mit einem eigenen, a priori und für alle Agenten gleich festgelegten Parameter `pheroDropOff`. Es wäre hilfreich, diesen Mechanismus klarer zu beschreiben und zu begründen, warum die abgegebene Pheromonmenge mit zunehmender Entfernung abnimmt.

Auch die Navigationsbeschreibung wirft Fragen auf. Es heißt, der Agent solle „geradeaus laufen, also dorthin, wo er hergekommen ist" - allerdings wurde zuvor nur erwähnt, dass eine Wahrscheinlichkeitsverteilung für die Navigation genutzt wird. Unklar bleibt dabei, welche Rolle die Pheromone in dieser Navigation konkret spielen. Die Formulierung „mit erhöhter Wahrscheinlichkeit in Richtung Nahrung/Nest" lässt offen, ob der Agent dabei einem internen Kompass folgt oder sich an den abgelegten Pheromonen orientiert. Besonders relevant wird diese Frage in Situationen, in denen keine Pheromone vorhanden sind oder in denen beides gleichzeitig eine Rolle spielt – dieser Fall sollte in der Skizze noch adressiert werden.

## 1.3 Ablauf der simulation

- " Manager sortiert tote Ameisen aus... platziert Nahrung auf Feld" 
  - ich könnte mir vorstellen, dass diese nahrung den kürzesten weg  schaden würde.
  - ant colony optimization hat standardmäßig kein reuse für essen. die platzierte nahrung impliziert eine biologischere simulation einer ameisenkolonie.

Ihr schreibt unter (e) "Manager verwaltet Nahrung, führt drop bzw pickup funktionen aus", kann eine Ameise auch freiwillig food droppen, oder nur wenn eine Ameise stirbt? Wenn nur Essen von gestorbenen Ameisen fallen gelassen wird, wird dieser Schritt nicht schon in Punkt (d) abgedeckt?

- "(f) Manager platzier neue Pheromone, entsprechend der Position der Agenten und der Menge die ihm die dropPheromon Funktion mitteilt" -> verwaltet nicht der Agent die pheromone? kommt die menge aus pheroDropoff an? Es wurde gesagt, dass der Wert zwischen 0 bis 1 ist. ist es möglich 0.5 pheromonitems zu droppen?
- hier ist fragwürdig, wieso die menge an pheromonen die eine ameise abgibt sich weiter abnimmt. kann eine ameise essen finden irgendwann keine nestpheromone mehr ablegen?

## 1.5 Forschungsfrage
Bei den vorgeschlagenen Methoden zur Berechnung der Effizienz bleibt unklar, was genau gemessen wird. Insbesondere bei der Korrelation zwischen gefundener Nahrung und der Pheromonmenge stellt sich die Frage, was unter „Pheromonsumme" zu verstehen ist – handelt es sich um die Anzahl der Pheromone pro Feld pro Takt, oder um eine andere Größe? Es wäre hilfreich, den Begriff der Netzwerkeffizienz vorab präziser zu definieren, um die nachfolgenden Berechnungen und Vergleiche nachvollziehbarer zu gestalten.

## 1.6 Experimente
Es kann sinnvoll sein noch weitere Experimente zu eurer Forschungsfrage durchzuführen. Die Experimente, die ihr bisher aufgeführt habt, sind viel mehr Simulationen zu einem einzigen Experiment. Z.B. könntet ihr noch ein weiteres Experiment durchführen, bei dem es mehr AntAgents gibt als bei dem ersten. Bei beiden Experimenten gibt es drei Simulationen zwischen denen ihr wie von euch beschrieben die Verdunstungsrate anpasst.

## Anmerkung Datenverarbeitung Wahrnehmung
Dieser Abschnitt ist für uns überhaupt nicht verständlich. Vor allem solltet ihr hier die angefügte Grafik erklären. Aber auch in dem Text gibt es einige Lücken, sodass für uns durch diese Anmerkung zur Wahrnehmung nicht besser verständlich wurde wie ihr die Wahrnehmung der Ameisen implementieren wollt.
