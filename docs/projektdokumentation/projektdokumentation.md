<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 90vh; max-height: 90vh; margin: 0; padding: 0; text-align: center; box-sizing: border-box;">
  <h1 style="margin: 0 0 0.5em 0;">Projektdokumentation</h1>
  <p style="margin: 0 0 1em 0;">TU Berlin – SoSe 2026 – Agententechnologien - Gruppe 18</p>
  <p style="margin: 0;">Moritz Clerc 498074, Carlos Driller 495897, David Brandes 495394</p>
</div>

<h2 style="page-break-before: always;">1. Systemdesign</h2>

noch zu machen, siehe systemdesign.md

---

## 2. Forschungsfrage

*Sind wenige Ameisen mit höherer Maximalenergie effizienter in der Ausbeutung der Nahrungsquellen als eine größere Anzahl an Ameisen mit geringerer Maximalenergie?*

**Effizienz** wird gemessen als Ausbeutungsrate: gelieferte Nahrungseinheiten pro Tick, sowie als Tick der vollständigen Ausbeutung aller Quellen. Damit werden sowohl die Geschwindigkeit (Zeit bis zur vollständigen Ausbeutung) als auch der absolute Ertrag (Gesamtmenge) erfasst.

---

wir haben ja n x E = 3000 konstant (experiment1_coldstart.json) gemacht:

  | Simulation | Ameisen | Energie | n×E   |
  |---|---|---|---|
  | sim_5ants   | 5        | 600      | 3000  |
  | sim_10ants  | 10       | 300      | 3000  |
  | sim_20ants  | 20       | 150      | 3000  |

d.h. Simulation läuft jetzt korrekt (hoffentlich) ergebnisse:

  Exp1 (Forschungsfrage):
  - 5 Ameisen (E=600): 18/60 = 30% -> 4/5 überleben 
  - 10 Ameisen (E=300): 33/60 = 55% -> 5/10 überleben 
  - 20 Ameisen (E=150): 36/60 = 60% -> 1/20 überlebt

  -> Mehr Ameisen = mehr Effizienz, auch mit je weniger Energie. Die Forschungsfrage ist jetzt
  beantwortbar.

  Exp3 (Skalierbarkeit):
  - 10→14%, 20→23.5%, 30→33.5%, 39→42% -> saubere monotone Kurve 

btw: in exp1 sterben die meisten 20-Ameisen-Kolonie bis T=750. das ist mit
  150 energie auf einer 15x15-karte (10 schritte bis zur quelle) an der unteren grenze.

## 3. Experiment 1: Nahrungsversorgung

### Motivation

<!-- Warum dieses Experiment? Was soll gezeigt werden? (2-3 Sätze) -->

### Versuchsaufbau

<!-- Grid-Größe, Nest-Position, Nahrungsquellen (Position, Menge), Hindernisse, Populationsgrößen, Parameter -->

### Simulationsverlauf

#### Simulation 1: 5 Ameisen

<!-- Beschreibung des Verlaufs: Wann wurden Quellen gefunden? Wie entwickelte sich die Ausbeutung? -->

#### Simulation 2: 10 Ameisen

<!-- -->

#### Simulation 3: 20 Ameisen

<!-- -->

### Ergebnisse

<!-- Tabelle oder Grafik mit gesammelter Nahrung pro Tick, Tick der ersten Lieferung, Gesamtausbeute -->

### Interpretation

<!-- Was zeigen die Ergebnisse bezüglich der Forschungsfrage? Stärken/Schwächen des Algorithmus bei verschiedenen Populationsgrößen? -->

---

## 4. Experiment 2: Pheromonspur-Unterbrechung

### Motivation

<!-- Warum dieses Experiment? Welche Eigenschaft des Algorithmus wird untersucht? (2-3 Sätze) -->

### Versuchsaufbau

<!-- Grid, vorplatzierte Pheromonspuren, Lücke im Sim 2, Parameter -->

### Simulationsverlauf

#### Simulation 1: Vollständige Pheromonspur (Baseline)

<!-- -->

#### Simulation 2: Unterbrochene Pheromonspur (Lücke bei x=3,4)

<!-- Wie lange dauert die Wiederherstellung? Wie verhält sich der Schwarm in der Zwischenzeit? -->

### Ergebnisse

<!-- Vergleich: Ticks bis erste Lieferung in Sim 1 vs. Sim 2 -->

### Interpretation

<!-- Zeigt der Algorithmus Selbstheilungsfähigkeit? Wie robust ist er bei Spurunterbrechungen? -->

---

## 5. Experiment 3: Skalierbarkeit

### Motivation

<!-- Warum dieses Experiment? Welche Skalierungsdimension wird untersucht? (2-3 Sätze) -->

### Versuchsaufbau

<!-- Grid 25x25, vier Ecknahrungsquellen, Hindernisse, vier Populationsgrößen (10/20/30/39), Parameter -->

### Simulationsverlauf

#### Simulation 1: 10 Ameisen

<!-- -->

#### Simulation 2: 20 Ameisen

<!-- -->

#### Simulation 3: 30 Ameisen

<!-- -->

#### Simulation 4: 39 Ameisen

<!-- -->

### Ergebnisse

<!-- Gesamtausbeute, Ausbeutungsrate, Anteil Träger/Sucher über Zeit je Populationsgröße -->

### Interpretation

<!-- Ab welcher Populationsgröße sinkt die marginale Effizienz? Engpässe, konkurrierende Spuren, Diminishing Returns? -->

---

## 6. Zusammenfassung und Ausblick

<!-- 1 Absatz: Was wurde gezeigt? Welche Erkenntnisse zur Forschungsfrage? -->
<!-- Ausblick: Welche Anschlussaktivitäten wären sinnvoll? (z.B. dynamische Hindernisse, mehrere Nester, andere Pheromonstrategien) -->

---

## 7. Brokering-Variante

Für eine effizientere Ausbeutung der Nahrungsquellen schlagen wir eine Arbeitsaufteilung vor: Explorer erkunden, Exploiter transportieren Nahrung zum Nest. Nahrungsquellen werden zu Item-Agenten (Diensterbringer), die auf einem Feld liegen und bei Kontakt Nahrung bereitstellen — das Aufsammeln von Nahrung wird dadurch zu einer Agenteninteraktion.

Die Rollen Exploiter und Explorer unterscheiden sich in der Navigation. Exploiter weichen nur mit geringer Wahrscheinlichkeit von Pheromonspuren ab, weil sie nicht erkunden, sondern bekannte Wege zu Nest und Quellen nutzen sollen. Explorer weichen hingegen häufig ab, um neue Futterquellen zu finden.

Explorer transportieren keine Nahrung. Beim Fund einer Quelle speichern sie deren Lage als relativen Vektor (pro Schritt mit der eigenen Bewegung mitgeführt), wie lange der Fund zurückliegt und wie groß die Quelle beim Fund war. Treffen sich Explorer und Exploiter auf demselben Feld, kann der Explorer den Exploiter fragen wo eine Futterquelle ist. Der Explorer gibt dem Exploiter eine Recommendation mit der Richtung zur Futterquelle. Welche Quelle der Explorer empfiehlt, hängt von seiner Erinnerung ab: War beim Fund noch viel Nahrung übrig, wurde die Futterquelle erst vor wenigen Zeittakten gefunden und liegt in der Nähe? So wird diese Quelle sehr wahrscheinlich genannt. Exploiter dürfen Empfehlungen von den Explorern ignorieren und sich ausschließlich an der Pheromonspur orientieren.

### Erwartete Veränderungen im Systemverhalten

In *Experiment 1* sollten Exploiter früher zum Nest liefern, weil sie Informationen über gefundene Futterquellen untereinander propagieren. Vorallem können sich die Explorer auf das Suchen von Nahrung konzentrieren und nicht zwischen Nahrungs- und Nestsuche hin und her wechseln. Besonders bei kleinen Populationen profitiert die Kolonie von Explorern, die Suchwissen bündeln. In *Experiment 2* können Explorer eine Orientierung geben wenn aufgrund fehlender Pheromonspur Orientierung fehlt. Die Ausbeutung sollte schneller wieder anlaufen. In *Experiment 3* werden die Nachteile, dieser dezentralen Brokering Variante offensichtlich: Explorer und Exploiter treffen sich selten auf großen Grids und die Empfehlungen über die Position von Futterquellen sind häufig veraltet.

### Begründung der Wahl

Ein zentraler oder globaler Wissenszustand -- etwa ein Nest-Register aller bekannten Quellen, das jede Ameise abfragen könnte -- wäre potenziell effizienter, weil Information sofort und für alle verfügbar wäre. Trotzdem haben wir uns gegen diesen Weg entschieden.
Entscheidend für die gewählte Brokering-Variante ist, dass sie den Fokus auf lokaler Wahrnehmung behält. Exploiter orientieren sich weiterhin an dem, was sie am aktuellen Feld und in der Nachbarschaft sehen -- Pheromone, Nest, Nahrung -- und erhalten Recommendations nur im direkten Kontakt mit einem Explorer auf demselben Feld. Explorer teilen ebenfalls nur Wissen aus eigener Erfahrung mit; niemand liest einen gemeinsamen Weltzustand aus.

Aufgrund dem Fokus auf die lokale Wahrnehmung sind die Informationsasymmetrien groß: Exploiter wissen nicht warum ein Explorer eine gewisse Futterquelle empfiehlt. Explorer wiederrum wissen nicht, ob Exploiter tatsächlich der Recommendation folgen. Auch wissen alle Ameisen nicht, ob an der empfohlenen Stelle noch Futter liegt.

Wir haben uns für die Recommendation Brokering-Variante entschieden, da sie uns realistisch erscheint und gleichzeitig, wie unter *Erwartete Veränderungen im Systemverhalten aufgeführt*, begründet erwarten dürfen, dass die Effizienz der Futterausbeutung steigt.
