# Review für Gruppe 19

Wir bewerten die Projektskizze unter der Annahme, dass wir noch nicht viel über die Aufgabe wissen. Das entstehende Feedback könnte eurer Gruppe helfen, für die Dokumentationen mögliche blinde Flecke in Erklärungen oder Darstellungen aufzuzeigen.

Wir beschreiben zunächst eine Inkonsistents, die uns bezüglich der Pheromonmodelierung aufgefallen ist und gehen dann konkreter auf einzelne Abschnitte eurer Projektskizze ein.


## Inkonsistent in der Pheromonmodelierung
Im Klassendiagramm und der JSON-Erklärung wird Pheromone als int modelliert, Verdunstung als Subtraktion eines festen Wertes (evaporation_amount: 1). In den Experimenten steht jedoch Evaporation: 0.02 — ein Dezimalwert, der eine multiplikative Prozentverdunstung impliziert. Beide Modelle haben sehr unterschiedliches Verhalten: Bei kleinen Pheromonmengen und fixem Abzug fällt der Wert abrupt auf 0. Bei prozentualer Verdunstung hingegen asymptotisch.
Es sollte eine Entscheidung getroffen werden, und überall vereinheitlicht werden. Integer-Subtraktion ist wohl einfacher und deterministischer umzusetzen.


## 1. Kurzbeschreibung der Simulation

Um diesen Abschnitt sinnvoller und hilfreicher, für das Verständnis von dem Projekt, zu gestalten könntet ihr darauf achten, dass die in diesem Abschnitt aufkommenden Fragen im weiteren Verlauf des Dokuments wieder aufgegriffen werden.
Beispielsweise könnte der Satz "treffen Entscheidungen auf Basis lokaler Informationen", später genauer geklärt werden. Was zählt alles zu den lokalen Informationen eines Ant-Agents?

## 2. Hypothese

Ihr schreibt: "Ursache hierfür sind redundante Wege [...]". Wir denken, dass die "Ursache" im Kontext des Problems außerhalb der zu beweisenden (oder widerlegenden) Hypothese beschrieben werden kann und viel mehr als eine Begründung warum ein interessanter Zusammenhang zwichen der Anzahl Ameisen und der Effizienz der Nahrungsbeschaffung vermutet wird.

Alternative Formulierung der Hypothese: "Wenn die Effizienz der Nahrungsbeschaffung mit zunehmender Anzahl von Ameisen anwächst, dann steigt die Effizienz ab einem Punkt X nicht mehr proportional zur Population"

Ihr könnt an dieser Stelle noch auf eure geplanten Experimente und Simulationen verweisen um zu verdeutlichen, wie ihr vorhabt eure Hyptothese zu verifizieren beziehungsweise zu falsifizieren.

Eure Bewertung der Effizienz ist plausibel und passend.

## 3. und 4. Klassendiagramm und Erklärungen

Die Agenten verändern die Welt nicht direkt, sondern senden Aktionen an den Manager. In diesem Zusammenhang wäre es hilfreich, noch einen Satz hinzuzufügen, der das Verhältnis von Inbox und Queue zueinander erläutert und auf deren Funktionsweise hinweist.

- Eine Frage zur Implementierung vom Pheromon decreasing rate und dem Internen Schrittzähler, vielleicht könnte das der Implementation helfen. Hängt die Pheromonverdunstung als von einer AntAgent Instanz ab (also NUR wenn Schrittzähler um eins inkrementiert wird, dann Pheromon einmal dekrementiert)? Wie ist es eigentlich, wenn ein Ameise mehrere Pheromone abgelegt, und dann wieder zum nest geht? verdunstet dann beim resetten des schrittzählers auf 0, das pheromon nicht? 
  - Ich würde vielleicht eher empfehlen, vielleicht einfach mit dem takt die Pheromon Itemanzahl zu dekrementieren global, denn die stepsSinceFood und stepsSinceNest etwas redundant wirkt
- "Der Manager führt Bewegung und Pheromonablage dann im selben Takt als eine einzige, legale Aktion aus."
  - wichtig vielleicht zu beachten: wird das pheromon erst abgelegt, dann auf das nächste feld gegangen, oder erst bewegung und dann auf das neue pheromone abgelegt?
- die manager und agenten aufteilung mit anfrage von aktion an den manager zurück zur bestätigung oder ablehnung der aktion zum agenten finde ich sehr gut aufgeteilt, das hilft besonders bei aktionskonflikten zentral im manager zu lösen
-

## 5. JSON

Für die Capacity der Felder bezüglich eurer Hypothese wäre es wichtig aufzupassen, dass ihr die Kapazität einer Zelle nicht auf 999 einschränkt, insbesondere beim Nest. Solltet ihr 1200 Ameisen möglicherweise spawnen wollen, stellt sich die Frage ob alle auf das 999 Kapazitätsfeld passen oder nicht.

Wenn ihr die Nachbarschaft in dem JSON File angeben könnt, solltet ihr euch auch überlegen, ob ihr Experimente bezüglich der Nachbarschaften durchführen wollt.

Wieso wird in der JSON die besonderen Felder mit einer Kapazität von 0 dargestellt? Das könnte in der Entwicklung irreführend werden, wenn das Nest oder Food als Blockade verstanden wird. wieso müssen die besonderen Felder angegeben werden? Reicht es nicht zu überprüfen, was für ein Item auf der Zelle ist und je nachdem handeln?

Aktuell braucht ihr für Experiment 1 mit drei Simulationen (E1-A, E1-B, E1-C) drei separate JSON-Dateien, die sich nur in agents.count unterscheiden. Das führt zu Copy-Paste-Fehlerquellen und macht Vergleiche unübersichtlich.
Ihr könntet in euer JSON-Schema ein neuen `simulations` key einführen, sodass nur die Keys überschrieben werden, die sich zwischen den Simulationen unterscheiden und die generelle Config des Experiments als root keys definieren:

```json
{ 
    "agentnts": { "count": 15, ... },
    /* Weitere generelle Experiment config */
    /* ... */
    , "simulations": [
        /* Hier nur die Werte überschreiben, die sich zwischen den Simulationen unterscheiden. */ 
        { "id": "E1-A", "agents": { "count": 5 } },
        { "id": "E1-B" },
        { "id": "E1-C", "agents": { "count": 30 } }
    ] 
} 

```
## 7. Logging

Der von euch definierte Gesamt-Score ergibt Sinn und kann helfen auch ohne GUI einen Überblick über die ausgeführten Simulationen zu bekommen.

