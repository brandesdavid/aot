<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 90vh; max-height: 90vh; margin: 0; padding: 0; text-align: center; box-sizing: border-box;">
  <h1 style="margin: 0 0 0.5em 0;">Projektdokumentation</h1>
  <p style="margin: 0 0 1em 0;">TU Berlin – SoSe 2026 – Agententechnologien - Gruppe 18</p>
  <p style="margin: 0;">Moritz Clerc 498074, Carlos Driller 495897, David Brandes 495394</p>
</div>

<h2 style="page-break-before: always;">1. Systemdesign</h2>


## Kernkomponenten

**Parser** liest eine JSON-Modelldatei ein und löst Simulationsvarianten (Override-Mechanismus) auf. Mit dem Flag `--visual` werden Logs in `logs/visual/` statt `logs/` geschrieben, sodass visuelle und reguläre Logs nie überschrieben werden.

Pro Tick führt der **Manager** sequenziell aus: Aktionen anwenden -> Energie auffüllen -> Pheromone verdunsten -> tote Agenten entfernen -> Tick loggen -> Agenten wahrnehmen/entscheiden/handeln lassen.

**Field** speichert Agenten und Items (Nahrung, pheromone_nest, pheromone_food). `capacity = 0` markiert ein Hindernis; `capacity = 999` ist praktisch unbegrenzt (Nest). Pheromone sind reguläre Items mit `evaporation_rate > 0`.

**ItemInstance** verwendet **multiplikative Verdunstung** (`quantity *= 1 − rate`): veraltete Spuren verschwinden exponentiell in ~60 Ticks, aktive Spuren stabilisieren sich auf einem Gleichgewichtswert.

---

## Navigationslogik

Der `AntAgent` setzt den reaktiven Ameisenalgorithmus mit folgenden Designentscheidungen um:

1. **4-Nachbarschaft:** Jedes Feld hat vier Nachbarfelder (oben, unten, links, rechts).
2. **Probabilistische Navigation:** Die Wahrscheinlichkeit, ein Nachbarfeld zu wählen, ergibt sich aus:

`P(f) = score(f) / sum(score(f') für alle f')` (f' sind alle Nachbarfelder von f)

wobei `score(f) = max(0.01, pheromon(f) + 0.05 − penalty(f))`. Die `penalty` bestraft zuletzt besuchte Felder, um Kurzzyklen zu vermeiden (Kurzzeitgedächtnis der letzten 12 Positionen).

3. **Anti-Backtrack:** Die entgegengesetzte Richtung zum letzten Schritt wird durch die Penalty-Logik probabilistisch benachteiligt.
4. **Kapazität -1:** Im Kapazitäts-Array eines Agenten steht `"max": -1` für "keine Obergrenze". Diese Konvention betrifft ausschließlich Pheromon-Items, da Ameisen beliebig viel Pheromon ablegen dürfen.

---

## Logging & Effizienzmetrik

Jedes `tick_summary`-Event enthält die absolut gelieferten Einheiten (`food_at_nest`), die normalisierte Effizienz in Prozent (`food_at_nest / initial_total  x  100`), die Restmenge pro Quelle sowie den Koloniezustand (lebende Ameisen, Träger, Sucher).

`efficiency_pct` ist die primäre Metrik zur Beantwortung der Forschungsfrage, da sie unabhängig von der absoluten Quellgröße ist.

---
## Änderungen gegenüber der Projektskizze

Die Pheromonabgabe ist statt eines konstanten Werts nun abnehmend (`base  x  0.97^steps`), und die Verdunstung wurde von linear (`quantity − rate`) auf multiplikativ (`quantity  x  (1−rate)`) umgestellt. Das in der Skizze vorgesehene explizite `isFacing`-Richtungsfeld entfiel zugunsten einer impliziten Penalty auf zuletzt besuchte Positionen. Das Logging wurde um `food_sources` und `efficiency_pct` pro Tick erweitert, und Log-Pfade werden je nach Modus getrennt in `logs/` bzw. `logs/visual/` geschrieben. Für Reproduzierbarkeit wurde ein fester Seed eingeführt. In Experiment 1 sind die Energiewerte nicht mehr gleich, sondern so gesetzt, dass n x E=3000 konstant bleibt (5 -> 600, 10 -> 300, 20 -> 150).

---

## 2. Forschungsfrage

*Sind wenige Ameisen mit höherer Maximalenergie effizienter in der Ausbeutung der Nahrungsquellen als eine größere Anzahl an Ameisen mit geringerer Maximalenergie?*

**Effizienz** wird gemessen als Ausbeutungsrate: gelieferte Nahrungseinheiten pro Tick, sowie als Tick der vollständigen Ausbeutung aller Quellen. Damit werden sowohl die Geschwindigkeit (Zeit bis zur vollständigen Ausbeutung) als auch der absolute Ertrag (Gesamtmenge) erfasst.

Um die Gesamtenergie der Kolonie konstant zu halten und einen fairen Vergleich zu ermöglichen, gilt n x E = 3000 für alle Simulationen in Experiment 1:

| Simulation | Ameisen | Energie | n x E |
|---|---|---|---|
| sim_5ants  | 5  | 600 | 3000 |
| sim_10ants | 10 | 300 | 3000 |
| sim_20ants | 20 | 150 | 3000 |

---

## 3. Experiment 1: Nahrungsversorgung

### Motivation

Experiment 1 untersucht direkt die Forschungsfrage: Wie verändert sich die Ausbeutungseffizienz, wenn bei konstanter Kolonie-Gesamtenergie (n x E = 3000) die Anzahl der Ameisen variiert wird? Das Szenario startet kalt ohne vorplatzierte Pheromonspuren. Zwei Nahrungsquellen in entgegengesetzten Ecken erzeugen eine nicht-triviale Herausforderung.

### Versuchsaufbau

- **Grid:** 15 x 15, Nest bei (7,7)
- **Nahrungsquellen:** (2,2) und (12,12), je 30 Einheiten (gesamt 60), je 10 Schritte Manhattan-Distanz vom Nest
- **Hindernisse:** (4,5), (5,5), (6,5) sowie (8,9), (9,9), (10,9) (zwei kurze Mauern)
- **Populationen:** 5 (E=600), 10 (E=300), 20 (E=150) (jeweils n x E=3000)
- **Parameter:** Wahrnehmung=4, Pheromon-Abgabe=22.0, Verdunstungsrate Nest=0.013, Verdunstungsrate Nahrung=0.013, max_ticks=1000, seed=2004

### Simulationsverlauf

#### Simulation 1: 5 Ameisen (E=600)

Erste Nahrung gefunden bei T=16. Erste Lieferung ans Nest bei T=135, also 119 Ticks nach dem Fund. Bei T=100 und T=200 sind noch 0% geliefert. Ab T=300 steigt die Effizienz auf 10.0% (6 Einheiten), bis T=500 auf 16.7%. Bei T=750 und T=1000 ist die Simulation bei 18.3% (11 Einheiten) stagniert. 2 Tiere sterben; 3 überleben. Zwischenzeitlich entstehen Routen zwischen den Nahrungsquellen, allerdings ist auffällig, dass Ameisen oft zwar Nahrung finden, aber den Weg zurück zum Nest aufgrund von schwachen Pheromonspuren nicht mehr oder nur sehr langsam bewältigen können.

#### Simulation 2: 10 Ameisen (E=300)

Erste Nahrung bei T=22, erste Lieferung bei T=51, also 84 Ticks früher als die 5-Ameisen-Kolonie. Bei T=100 sind bereits 3.3% (2 Einheiten) geliefert. Die Effizienz steigt kontinuierlich: 6.7% bei T=300, 11.7% bei T=500, 18.3% bei T=750 (11 Einheiten). Ab T=750 keine weiteren Fortschritte. 6 Ameisen sterben; 4 überleben. Hier ist ebenfalls zu beobachten, dass Nahrungsträger das Nest oft nicht mehr finden.

#### Simulation 3: 20 Ameisen (E=150)

Erste Nahrung bei T=20, erste Lieferung bei T=47, was die kürzeste Zeit zwischen Fund und Lieferung aller drei Simulationen darstellt. Die Ausbeutung steigt rasch: 8.3% bei T=100, 31.7% bei T=200, 48.3% bei T=300. Eine Nahrungsquelle wird wiederholt über eine relativ stabile Route immer wieder ausgebeutet, bis sie bei=278 leer ist - zu der anderen Nahrungsquelle existiert keine Route mehr und sie wird nicht mehr erreicht. Ab T=361 ist die Effizienz bei 50.0% (30 Einheiten) eingefroren. Alle 20 Ameisen sind ab T=512 gestorben.

### Ergebnisse

| Simulation | Ameisen | Energie | Erste Nahrung | Erste Lieferung | Effizienz (T=1000) | Tode | Überlebende |
|---|---|---|---|---|---|---|---|
| sim_5ants  | 5  | 600 | T=16 | T=135 | 18.3% (11/60) | 2  | 3/5  |
| sim_10ants | 10 | 300 | T=22 | T=51  | 18.3% (11/60) | 6  | 4/10 |
| sim_20ants | 20 | 150 | T=20 | T=47  | 50.0% (30/60) | 20 | 0/20 |

Effizienz-Verlauf:

| Tick   | 5 Ameisen | 10 Ameisen | 20 Ameisen |
|---|---|---|---|
| T=100  | 0.0%  | 3.3%  | 8.3%  |
| T=200  | 3.3%  | 3.3%  | 31.7% |
| T=300  | 10.0% | 6.7%  | 48.3% |
| T=500  | 16.7% | 11.7% | 50.0% |
| T=750  | 18.3% | 18.3% | 50.0% |
| T=1000 | 18.3% | 18.3% | 50.0% |

### Interpretation

Die 20-Ameisen-Kolonie liefert mit 50.0% deutlich mehr als die anderen beiden (je 18.3%), was die Forschungsfrage klar zugunsten größerer Populationen beantwortet. Der entscheidende Unterschied liegt nicht in der Erkundungsgeschwindigkeit (alle drei Kolonien finden Nahrung zwischen T=16 und T=22), sondern in der Rückkehrnavigation: 5 Ameisen brauchen 119 Ticks zwischen Fund und erster Lieferung, 10 Ameisen 29 Ticks, 20 Ameisen nur 27 Ticks. Mehr Ameisen legen mehr Pheromon pro Zeiteinheit ab, was stärkere Nest-Gradienten erzeugt und Träger schneller und zuverlässiger zurückführt.

---

## 4. Experiment 2: Pheromonspur-Unterbrechung

### Motivation

Experiment 2 untersucht die Robustheit des Algorithmus gegenüber Unterbrechungen bestehender Pheromonspuren. Durch vorplatzierte Spuren (Warmstart) wird die anfängliche Erkundungsphase übersprungen und der Effekt der Lücke isoliert messbar. Das Experiment zeigt, ob und wie schnell das System eine beschädigte Route selbst repariert.

### Versuchsaufbau

- **Grid:** 12 x 12, Nest bei (6,6)
- **Nahrungsquelle:** (0,6), 30 Einheiten, 6 Schritte Manhattan vom Nest
- **Vorplatzierte Spuren:** Entlang y=6 von x=0 bis x=5 sind je 10.0 Einheiten Nahrung- und Nest-Pheromon platziert
- **Lücke (Sim 2):** Bei x=3 und x=4 sind keine Pheromone vorhanden
- **Hindernisse:** (3,9), (4,9), (8,3), (8,4)
- **Parameter:** 10 Ameisen, E=200, Wahrnehmung=4, Pheromon-Abgabe=22.0, Verdunstungsrate Nest=0.013, Verdunstungsrate Nahrung=0.013, max_ticks=600, seed=2004

### Simulationsverlauf

#### Simulation 1: Vollständige Pheromonspur (Baseline)

Erste Nahrung bei T=10, erste Lieferung bei T=19. Die Ausbeutung steigt schnell: 60.0% bei T=100, 100.0% ab T=162. Ab T=235 sterben die Ameisen durch Energiemangel; bei T=600 sind alle 10 Ameisen tot.

#### Simulation 2: Unterbrochene Pheromonspur (Lücke bei x=3,4)

Erste Nahrung bei T=33, also 23 Ticks später als in Sim 1. Erste Lieferung bei T=58 (+39 Ticks Verzögerung). Bei T=100 sind erst 13.3% (4 Einheiten) geliefert, gegenüber 60.0% in Sim 1. Die Effizienz steigt danach stetig, als die Spur reetabliert wird: 56.7% bei T=200, 96.7% bei T=300, 100.0% ab T=406 (30 Einheiten). Die vollständige Ausbeutung wird um ~270 Ticks verzögert, aber letztlich erreicht. 9 Ameisen sterben; 1 überlebt.

### Ergebnisse

| Simulation | Erste Nahrung | Erste Lieferung | T=100 | T=200 | T=300 | T=600 | Erschöpfung |
|---|---|---|---|---|---|---|---|
| sim_complete | T=10 | T=19 | 60.0% | 100.0% | 100.0% | 100.0% | T≈200 |
| sim_gap      | T=33 | T=58 | 13.3% | 56.7%  | 96.7%  | 100.0% | T≈500 |

### Interpretation

Beide Simulationen erreichen 100% Ausbeutung. Der Algorithmus stellt die Route innerhalb der Laufzeit vollständig wieder her. Der Kontrast liegt in der Geschwindigkeit: Die Lücke verzögert die erste Lieferung um 39 Ticks und die vollständige Erschöpfung um ~270 Ticks. Am deutlichsten ist der Unterschied bei T=100, wo die Lücken-Simulation mit 13.3% weniger als ein Viertel der Baseline-Effizienz (60.0%) erreicht. Ab T=200 holt sie auf; bei T=300 ist der Rückstand auf 3.3 Prozentpunkte gesunken.

Der Algorithmus überbrückt die Lücke durch Erkundung: Ameisen, die die Spur bis x=5 verfolgen und dort keine Pheromonspuren finden, weichen auf Nachbarfelder aus und legen bei Erfolg neue Pfade durch den leeren Bereich. Dieser Prozess dauert an, bis genug Pheromon akkumuliert ist, um stabile Rückrouten zu bilden.

---

## 5. Experiment 3: Skalierbarkeit

### Motivation

Experiment 3 untersucht, wie sich die Effizienz der Kolonie mit steigender Populationsgröße auf einem deutlich größeren Grid entwickelt. Vier Nahrungsquellen in den Ecken des 25 x 25-Grids (je ~22 Schritte vom Nest) stellen hohe Anforderungen an Erkundung und Transportkapazität. Das Experiment zeigt, ab wann Skaleneffekte abnehmen und welche Mindestkoloniegröße für effektive Ausbeutung auf großen Grids erforderlich ist.

### Versuchsaufbau

- **Grid:** 25 x 25, Nest bei (12,12)
- **Nahrungsquellen:** (1,1), (23,1), (1,23), (23,23), je 50 Einheiten (gesamt 200)
- **Hindernismauern:** (8,10-13), (16,11-14), (11-13,8), (12-14,16), vier kurze Barrieren um das Nest
- **Populationen:** 10, 20, 30, 39 Ameisen
- **Parameter:** E=500, Wahrnehmung=4, Pheromon-Abgabe=50.0, Verdunstungsrate Nest=0.004, Verdunstungsrate Nahrung=0.004, max_ticks=1500, seed=2004

Die Pheromon-Parameter weichen bewusst von Experiment 1 ab: Die minimale Manhattan-Distanz zu den Eckenquellen beträgt ~22 Schritte (mehr als doppelt so weit wie in Experiment 1). Mit den Parametern aus Experiment 1 würden die Pheromone entlang so langer Pfade zu stark abbauen, als dass Träger die Steigung zum Nest zuverlässig erkennen könnten. Die Verdunstungsrate wurde daher auf 0.004 reduziert und die Abgabemenge auf 50.0 erhöht, um ausreichend starke Gradienten über die längeren Distanzen sicherzustellen.

### Simulationsverlauf

#### Simulation 1: 10 Ameisen

Erste Nahrung bei T=150, auf dem 25 x 25-Grid dauert die Erkundungsphase mit nur 10 Ameisen länger als in Experiment 1. Erste Lieferung bei T=239. Die Effizienz bleibt durch die gesamte Simulation niedrig: 1.0% bei ca. T=300 bis ca. T=500, 2.0% ab ca. T=750. Alle 10 Ameisen sterben.

#### Simulation 2: 20 Ameisen

Erste Nahrung bei T=44, erste Lieferung bei T=207, trotz früherer Entdeckung als bei 10 Ameisen dauert es 163 Ticks bis zur ersten Lieferung, da die Gradienten für zuverlässige Rückkehr noch zu schwach sind. Ab ca. T=500 steigt die Effizienz auf 4.0%, bis ca. T=750 auf 5.5%, bis ca. T=1000 auf 7.5%, danach keine weiteren Fortschritte. 19 Ameisen sterben, 1 überlebt.

#### Simulation 3: 30 Ameisen

Erste Nahrung bei T=44, erste Lieferung bei T=203. Trotz identischem Erstfund-Zeitpunkt wie bei 20 Ameisen verläuft der Anstieg ähnlich: 1.5% bei T=300, 6.0% bei T=500, 8.5% bei T=750. Bis T=1000 und T=1500 sind 9.0% (18 Einheiten) geliefert. Alle 30 Ameisen sterben.

#### Simulation 4: 39 Ameisen

Erste Nahrung bei T=46, erste Lieferung bei T=149 (hier die früheste erste Lieferung aller vier Simulationen). Ab T=300 steigt die Effizienz deutlich: 7.0% bei T=300, 11.5% bei T=500, 21.5% bei T=750, 25.0% bei T=1000, 28.0% bei T=1500 (56 Einheiten). 31 Ameisen sterben, 8 überleben. Hier ist bemerkenswert, wie in der Nähe der vier Ecknahrungsquellen, ein Pfad zur west-nördlichen Quelle entsteht. Dieser Pfad wird auch von den meisten Ameisen bevorzugt, jedoch sind in den anderen Ecknahrungsquellen zu erkennen, dass einige Ameisen auch weiterhin explorieren, an jeder anderen Ecke.

### Ergebnisse

| Simulation | Erste Nahrung | Erste Lieferung | Effizienz (T=1500) | Tode | Überlebende |
|---|---|---|---|---|---|
| sim_10ants | T=150 | T=239 | 2.0%  (4/200)  | 10 | 0/10  |
| sim_20ants | T=44  | T=207 | 7.5%  (15/200) | 19 | 1/20  |
| sim_30ants | T=44  | T=203 | 9.0%  (18/200) | 30 | 0/30  |
| sim_39ants | T=46  | T=149 | 28.0% (56/200) | 31 | 8/39  |

Effizienz-Verlauf:

| Tick   | 10 Ameisen | 20 Ameisen | 30 Ameisen | 39 Ameisen |
|---|---|---|---|---|
| T=300  | 1.0%  | 1.5%  | 1.5%  | 7.0%  |
| T=500  | 1.0%  | 4.0%  | 6.0%  | 11.5% |
| T=750  | 1.5%  | 5.5%  | 8.5%  | 21.5% |
| T=1000 | 2.0%  | 7.5%  | 9.0%  | 25.0% |
| T=1500 | 2.0%  | 7.5%  | 9.0%  | 28.0% |

### Interpretation

Die Effizienz steigt monoton mit der Populationsgröße: 2.0% -> 7.5% -> 9.0% -> 28.0%. Der Anstieg ist nicht linear, der Sprung von 30 auf 39 Ameisen (+19 Prozentpunkte) ist deutlich größer als von 10 auf 20 (+5.5) oder 20 auf 30 (+1.5). Das deutet auf eine kritische Schwelle hin: Erst ab ~39 Ameisen entstehen auf dem 25 x 25-Grid schnell genug starke Gradienten für eine stabile Transportroute.

Aufschlussreich ist der Vergleich der ersten Lieferung: 10 Ameisen liefern erst bei T=239, 39 Ameisen bei T=149. Obwohl 20 und 30 Ameisen ihre Nahrung zum selben Zeitpunkt finden (T=44), liefern sie erst bei T=207 bzw. T=203. Das ist ein Zeichen dafür, dass bei diesen Populationsgrößen auf dem großen Grid zu wenig Pheromon pro Zeiteinheit abgelegt wird, um zuverlässige Rückrouten früh zu etablieren.

Bezogen auf die Forschungsfrage bestätigt Experiment 3 die Tendenz aus Experiment 1: Mehr Ameisen liefern mehr Nahrung. Die nichtlineare Skalierung zeigt zusätzlich, dass auf großen Grids eine Mindest-Populationsgröße erforderlich ist, unterhalb derer keine stabile Ausbeutung entsteht.

Bemerkenswert ist dabei das Verhalten bei 39 Ameisen, was schon oben beschrieben wurde. Während die meisten Ameisen sich auf die west-nördliche Nahrung konzentrieren und dort eine dominante Transportroute aufbauen, erkunden einzelne Ameisen weiterhin die anderen Ecken. Dieses spontane Aufteilen in Ausbeutung und Exploration entsteht alleine durch die Pheromonverstärkung der ersten stabilen Route und könnte dem System zusätzliche Robustheit verleihen. Für kleinere Populationen fehlt diese Redundanz, denn sie reichen nicht aus, um gleichzeitig eine stabile Route zu betreiben und neue Quellen zu erkunden.

---

## 6. Zusammenfassung und Ausblick

Alle drei Experimente zeigen konsistent, dass größere Ameisenkolonien (bei gleicher oder pro-Kopf geringerer Energie) mehr Nahrung liefern als kleinere. In Experiment 1 liefern 5 und 10 Ameisen je 18.3%, während 20 Ameisen 50.0% erreichen; der Unterschied liegt nicht in der Erkundung (erste Nahrung bei T=16-22), sondern in der Rückkehrgeschwindigkeit: 5 Ameisen brauchen 119 Ticks bis zur ersten Lieferung, 20 Ameisen nur 27. In Experiment 2 überbrücken die Ameisen eine vollständige Spurunterbrechung durch Erkundung und erreichen trotz einer Verzögerung von ~300 Ticks am Ende ebenfalls 100% Ausbeutung. In Experiment 3 zeigt sich auf dem 25 x 25-Grid eine nichtlineare Skalierung (2.0% -> 7.5% -> 9.0% -> 28.0%), die auf eine kritische Mindest-Populationsgröße für stabile Gradientenbildung über lange Distanzen hinweist. Die Forschungsfrage ist damit klar zu beantworten: *Mehr Ameisen mit geringerer individueller Energie sind effizienter*, solange die Pheromondichten für zuverlässige Rücknavigation ausreichen.

Als sinnvolle Anschlussuntersuchungen bieten sich an: dynamische Hindernisse oder sich verändernde Nahrungsquellen zur Beobachtung von Adaption, mehrere Nester mit geteilter Pheromon-Infrastruktur, alternative Verdunstungsstrategien (z.B. distanzabhängige Raten), sowie eine quantitative Auswertung der Brokering-Variante im Direktvergleich mit der Basis-Implementierung auf denselben Experimentkonfigurationen.

---

## 7. Brokering-Variante

Für eine effizientere Ausbeutung der Nahrungsquellen schlagen wir eine Arbeitsaufteilung vor: Explorer erkunden, Exploiter transportieren Nahrung zum Nest. Nahrungsquellen werden zu Item-Agenten (Diensterbringer), die auf einem Feld liegen und bei Kontakt Nahrung bereitstellen, das Aufsammeln von Nahrung wird dadurch zu einer Agenteninteraktion.

Die Rollen Exploiter und Explorer unterscheiden sich in der Navigation. Exploiter weichen nur mit geringer Wahrscheinlichkeit von Pheromonspuren ab, weil sie nicht erkunden, sondern bekannte Wege zu Nest und Quellen nutzen sollen. Explorer weichen hingegen häufig ab, um neue Futterquellen zu finden.

Explorer transportieren keine Nahrung. Beim Fund einer Quelle speichern sie deren Lage als relativen Vektor (pro Schritt mit der eigenen Bewegung mitgeführt), wie lange der Fund zurückliegt und wie groß die Quelle beim Fund war. Treffen sich Explorer und Exploiter auf demselben Feld, kann der Explorer den Exploiter fragen wo eine Futterquelle ist. Der Explorer gibt dem Exploiter eine Recommendation mit der Richtung zur Futterquelle. Welche Quelle der Explorer empfiehlt, hängt von seiner Erinnerung ab: War beim Fund noch viel Nahrung übrig, wurde die Futterquelle erst vor wenigen Zeittakten gefunden und liegt in der Nähe? So wird diese Quelle sehr wahrscheinlich genannt. Exploiter dürfen Empfehlungen von den Explorern ignorieren und sich ausschließlich an der Pheromonspur orientieren.

### Erwartete Veränderungen im Systemverhalten

In *Experiment 1* sollten Exploiter früher zum Nest liefern, weil sie Informationen über gefundene Futterquellen untereinander propagieren. Vorallem können sich die Explorer auf das Suchen von Nahrung konzentrieren und nicht zwischen Nahrungs- und Nestsuche hin und her wechseln. Besonders bei kleinen Populationen profitiert die Kolonie von Explorern, die Suchwissen bündeln. In *Experiment 2* können Explorer eine Orientierung geben wenn aufgrund fehlender Pheromonspur Orientierung fehlt. Die Ausbeutung sollte schneller wieder anlaufen. In *Experiment 3* werden die Nachteile, dieser dezentralen Brokering Variante offensichtlich: Explorer und Exploiter treffen sich selten auf großen Grids und die Empfehlungen über die Position von Futterquellen sind häufig veraltet.

### Begründung der Wahl

Ein zentraler oder globaler Wissenszustand, etwa ein Nest-Register aller bekannten Quellen, das jede Ameise abfragen könnte (wäre potenziell effizienter), weil Information sofort und für alle verfügbar wäre. Trotzdem haben wir uns gegen diesen Weg entschieden.
Entscheidend für die gewählte Brokering-Variante ist, dass sie den Fokus auf lokaler Wahrnehmung behält. Exploiter orientieren sich weiterhin an dem, was sie am aktuellen Feld und in der Nachbarschaft sehen, Pheromone, Nest, Nahrung, und erhalten Recommendations nur im direkten Kontakt mit einem Explorer auf demselben Feld. Explorer teilen ebenfalls nur Wissen aus eigener Erfahrung mit; niemand liest einen gemeinsamen Weltzustand aus.

Aufgrund dem Fokus auf die lokale Wahrnehmung sind die Informationsasymmetrien groß: Exploiter wissen nicht warum ein Explorer eine gewisse Futterquelle empfiehlt. Explorer wiederrum wissen nicht, ob Exploiter tatsächlich der Recommendation folgen. Auch wissen alle Ameisen nicht, ob an der empfohlenen Stelle noch Futter liegt.

Wir haben uns für die Recommendation Brokering-Variante entschieden, da sie uns realistisch erscheint und gleichzeitig, wie unter *Erwartete Veränderungen im Systemverhalten aufgeführt*, begründet erwarten dürfen, dass die Effizienz der Futterausbeutung steigt.
