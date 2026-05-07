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

