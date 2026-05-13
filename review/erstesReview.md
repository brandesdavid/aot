# Review für Gruppe 19

Wir bewerten die Projektskizze unter der Annahme, dass wir noch nicht viel über die Aufgabe wissen. Das entstehende Feedback könnte eurer Gruppe helfen,  mögliche blinde Flecke in Erklärungen oder Darstellungen für die Dokumentation aufzuzeigen.

Wir beschreiben zunächst eine Inkonsistenz, die uns bezüglich der Pheromonmodelierung aufgefallen ist und gehen dann konkreter auf einzelne Abschnitte eurer Projektskizze ein.


## Inkonsistent in der Pheromonmodelierung
Im Klassendiagramm und der JSON-Erklärung wird die Anzahl eines Itemtyps auf einer Cell als int modelliert, Verdunstung als Subtraktion eines festen Wertes (evaporation_amount: 1). In den Experimenten steht jedoch Evaporation: 0.02 (ein Dezimalwert), der eine bruchteilige oder multiplikative Prozentverdunstung impliziert. In beiden Fällen würde das durch den Typunterschied zu ungewolltem verhalten führen.
Es sollte eine Entscheidung getroffen werden, und überall vereinheitlicht werden.


## 1. Kurzbeschreibung der Simulation

Um diesen Abschnitt sinnvoller und hilfreicher für das Verständnis des Projekts zu gestalten könntet ihr darauf achten, dass die in diesem Abschnitt aufkommenden Fragen im weiteren Verlauf des Dokuments wieder aufgegriffen werden.
Beispielsweise könnte der Satz "treffen Entscheidungen auf Basis lokaler Informationen", später genauer geklärt werden. Ihr könntet also dann später die Frage erklären: Was zählt alles zu den lokalen Informationen eines Ant-Agents? Im JSON wurde die "moore" Nachbarschaft angegeben. Wir persönlich würden noch einen Satz dazu hinzufügen.

## 2. Hypothese

Ihr schreibt: "Ursache hierfür sind redundante Wege [...]". Wir denken, dass die "Ursache" im Kontext des Problems außerhalb der zu beweisenden (oder widerlegenden) Hypothese beschrieben werden kann und viel mehr als eine Begründung warum ein interessanter Zusammenhang zwichen der Anzahl Ameisen und der Effizienz der Nahrungsbeschaffung vermutet wird.

Alternative Formulierung der Hypothese: "Wenn die Effizienz der Nahrungsbeschaffung mit zunehmender Anzahl von Ameisen anwächst, dann steigt die Effizienz ab einem Punkt X nicht mehr proportional zur Population"

Ihr könnt an dieser Stelle noch auf eure geplanten Experimente und Simulationen verweisen um zu verdeutlichen, wie ihr vorhabt eure Hypothese zu verifizieren, beziehungsweise zu falsifizieren.

Eure Bewertung der Effizienz ist plausibel und passend.

## 3. und 4. Klassendiagramm und Erklärungen

Die Agenten verändern die Welt nicht direkt, sondern senden Aktionen an den Manager. In diesem Zusammenhang wäre es hilfreich, noch einen Satz hinzuzufügen, der das Verhältnis von Inbox und Queue zueinander erläutert und auf deren Funktionsweise hinweist.

Wir finden es gut, dass ihr die Pheromonverdunstung mit einem Alterseffekt (stepsSinceFood und stepsSinceNest) des Ameisen implementiert, da die Pheromonverdunstung die Pfade aktuell haltet und die Spuren besser durch den entstehenden Gradienten verstärkt werden.

Ihr meintet, dass der Manager die Bewegung und Pheromonablage dann im selben Takt als eine einzige, legale Aktion ausführt. Hier wäre es wichtig noch anzugeben: wird das Pheromon erst abgelegt und dann auf das nächste Feld bewegt, oder wird es erst bewegt und dann auf das neue Feld Pheromone abgelegt?
Wir finden, dass die Manager- und Agentenaufteilung gut aufgeteilt ist. Insbesondere ist die Inbox-Mechanik praktikabel, also dass der Agent eine Aktions-Anfrage an den Manager sendet und dazu eine Bestätigung oder Ablehnung der angefragten Aktion erhält. Das hilft besonders die Aktionskonflikte zentral im Manager zu lösen.

## 5. JSON

Für die Capacity der Felder bezüglich eurer Hypothese wäre es wichtig aufzupassen, dass ihr die Kapazität einer Zelle nicht auf 999 einschränkt, insbesondere beim Nest. Solltet ihr 1200 Ameisen spawnen wollen, stellt sich die Frage ob alle auf das 999 Kapazitätsfeld passen oder nicht.

Wenn ihr die Nachbarschaft in der JSON-Datei angeben könnt, solltet ihr euch auch überlegen, ob ihr Experimente bezüglich der Nachbarschaften durchführen wollt. Das heißt, ob verschiedene Nachbarschaften unterschiedliche Ergebnisse zu eurer Hypothese liefern könnten.

Zu den Feldern haben wir uns die Fragen gestellt: 1. Wieso werden in der JSON die besonderen Felder mit einer Kapazität von 0 dargestellt? Das könnte in der Entwicklung irreführend werden, wenn das Nest oder Food als Blockade verstanden wird. 2. Müssen die besonderen Felder angegeben werden? Wir fragen uns ob es nicht reicht, die Items auf der Zelle zu überprüfen und je nachdem handeln zu lassen?

Aktuell braucht ihr für Experiment 1 mit drei Simulationen (E1-A, E1-B, E1-C) drei separate JSON-Dateien, die sich nur in agents.count unterscheiden. Das führt zu Copy-Paste-Fehlerquellen und macht Vergleiche unübersichtlich.
Ihr könntet in euer JSON-Schema ein neuen `simulations` key einführen, sodass nur die Keys überschrieben werden, die sich zwischen den Simulationen unterscheiden und die generelle Config des Experiments als root keys definieren:

```json
{ 
    "agents": { "count": 15, ... },
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

## Zusammenfassung
Wir finden, dass die Projektskizze gut strukturiert ist und die wichtigsten Komponenten des Projekts adressiert. Wir haben einige Fragen und Anregungen zur Verbesserung der Dokumentation und der Implementierung gegeben und hoffen, dass dieses Feedback euch hilft, die Implementierung und die Forschungsfrage erweitern zu können.

Viele Grüße
