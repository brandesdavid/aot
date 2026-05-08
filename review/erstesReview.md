# Erstes Review für Gruppe 19

Im Klassendiagramm und der JSON-Erklärung wird Pheromone als int modelliert, Verdunstung als Subtraktion eines festen Wertes (evaporation_amount: 1). In den Experimenten steht jedoch Evaporation: 0.02 — ein Dezimalwert, der eine multiplikative Prozentverdunstung impliziert. Beide Modelle haben sehr unterschiedliches Verhalten: Bei kleinen Pheromonmengen und fixem Abzug fällt der Wert abrupt auf 0. Bei prozentualer Verdunstung hingegen asymptotisch.
Es sollte eine Entscheidung getroffen werden, und überall vereinheitlicht werden. Integer-Subtraktion ist wohl einfacher und deterministischer umzusetzen.

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


(david: ich muss noch das verbessern und schöner schreiben)

Ich bewerte die Projektskizze unter der annahme, das ich als leser noch nicht viel über die Aufgabe weißt. Das entstehende Feedback könnte eurer Gruppe helfen, für die Dokumentationen mögliche blinde Flecke in Erklärungen oder Darstellungen aufzuzeigen.

# kurzbeschreibung

- Es wurde eine kurz und präzise beschrieben, passend details weggelassen, die dann im Verlauf erklärt werden könnten.
  - beispielsweise "treffen Entscheidungen auf Basis lokaler Informationen" -> später genauer geklärt werden, wieviele Felder breit eine Ameise dann wahrnehmen kann

# Hypothese

- "Ursache hierfür sind redundante Wege" 
  - Ich würde sagen, dass die "Ursache" im Kontext des Problems außerhalb der Hypothese beschrieben werden kann als Vermutung
  - Die Hypothese kann aber eine Hypothesen-Ursache beschreiben, also in ein Wenn-Dann-Satz wie:
    - "WENN die Effizienz der Nahrungsbeschaffung mit zunehmender Anzahl von Ameisen anwächst, DANN steigt die Effizienz ab einem Punkt X nicht mehr proportional zur Population"
- "Zur Untersuchung ... variierender Ameisenzahl" Hier stelle ich mir die Frage, ob es schon vielleicht Werte für die Ameisenpopulation existieren, und wenn ja, wie wurde sie erschlossen? Oder werden von 1 bis zu einem Maximalwert alle Ameisenpopulationen je eine Simulation durchgeführt? 
- "Zusätzlich werden weitere Einflussfaktoren..", ich vermute es werden verschieden Simulationen ausgeführt für Ameisenpopulation X, wobei die Simulationen sich da unterscheiden, dass bspw. einmal eine Nahrungsquelle entfernt werden, und einmal die verschoben werden oder ähnlich? 
- Die Bewertung der Effizienz finde ich plausibel und gut.

- Insgesamt guter grober Überblick. Da ich leider mir unsicher bin, wie genau die Forschungsfrage aufgestellt hätte werden müssen, würde ich empfehlen öfters die "wie?" Frage versuchen zu erklären.

# Klassendiagramme/ Erklärung

- "Die Agenten verändern die Welt nicht direkt, sondern senden Aktionen an den Manager. " 
  - hier oder in der nähe vielleicht noch ein Satz hinzufügen, wie der Inbox und Queue sich zu einander verhalten, bzw. auf die Inbox und Queue anweisen
- Eine Frage zur Implementierung vom Pheromon decreasing rate und dem Internen Schrittzähler, vielleicht könnte das der Implementation helfen. Hängt die Pheromonverdunstung als von einer AntAgent Instanz ab (also NUR wenn Schrittzähler um eins inkrementiert wird, dann Pheromon einmal dekrementiert)? Wie ist es eigentlich, wenn ein Ameise mehrere Pheromone abgelegt, und dann wieder zum nest geht? verdunstet dann beim resetten des schrittzählers auf 0, das pheromon nicht? 
  - Ich würde vielleicht eher empfehlen, vielleicht einfach mit dem takt die Pheromon Itemanzahl zu dekrementieren global, denn die stepsSinceFood und stepsSinceNest etwas redundant wirkt
- "Der Manager führt Bewegung und Pheromonablage dann im selben Takt als eine einzige, legale Aktion aus."
  - wichtig vielleicht zu beachten: wird das pheromon erst abgelegt, dann auf das nächste feld gegangen, oder erst bewegung und dann auf das neue pheromone abgelegt?
- die manager und agenten aufteilung mit anfrage von aktion an den manager zurück zur bestätigung oder ablehnung der aktion zum agenten finde ich sehr gut aufgeteilt, das hilft besonders bei aktionskonflikten zentral im manager zu lösen
-

# JSON

- Für die Capacity der felder bezüglich eurer Hypothese wäre es wichtig aufzupassen, dass ihr die kapazität einer zelle nicht auf 999 einschränkt, insbesondere beim nest. Solltet ihr 1200 ameisen möglicherweise spawnen wollen, stellt sich dann die frage ob alle auf das 999 kapazitätsfeld passen oder nicht
- sehr gut dass ihr die nachbarschaft eingefügt habt, das erlaubt verschiedene wahrnehmungen zu testen
- wieso wird in der json die besonderen felder mit einer kapazität von 0 dargestellt? das könnte in der entwicklung irreführend werden, wenn das nest/food als blockade verstanden werden könnte. wieso müssten die besonderen felder eigentlich angegeben werden? reicht es nicht einfach zu überprüfen, was für ein item auf der zelle ist und je nachdem handeln?
- nebeninfo: im sequenzdiagramm nutzt der Manager getPerception(agent) auf die gridworld.

# logging

- ich finde es gut, dass ein score noch berechnet wird für die simulation. das hilft einigermaßen sich anstatt mit einem vollumfänglichen GUI, eine orientierung zu erhalten, wie die experimente verlaufen sind 

