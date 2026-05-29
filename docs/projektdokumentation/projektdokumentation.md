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

Um die Gesamtenergie der Kolonie konstant zu halten und einen fairen Vergleich zu ermöglichen, gilt n×E = 3000 für alle Simulationen in Experiment 1:

| Simulation | Ameisen | Energie | n×E |
|---|---|---|---|
| sim_5ants  | 5  | 600 | 3000 |
| sim_10ants | 10 | 300 | 3000 |
| sim_20ants | 20 | 150 | 3000 |

---

## 3. Experiment 1: Nahrungsversorgung

### Motivation

Experiment 1 untersucht direkt die Forschungsfrage: Wie verändert sich die Ausbeutungseffizienz, wenn bei konstanter Kolonie-Gesamtenergie (n×E = 3000) die Anzahl der Ameisen variiert wird? Das Szenario startet kalt ohne vorplatzierte Pheromonspuren. Zwei Nahrungsquellen in entgegengesetzten Ecken erzeugen eine nicht-triviale Herausforderung.

### Versuchsaufbau

- **Grid:** 15×15, Nest bei (7,7)
- **Nahrungsquellen:** (2,2) und (12,12), je 30 Einheiten (gesamt 60), je 10 Schritte Manhattan-Distanz vom Nest
- **Hindernisse:** (4,5), (5,5), (6,5) sowie (8,9), (9,9), (10,9) — zwei kurze Mauern
- **Populationen:** 5 (E=600), 10 (E=300), 20 (E=150) — jeweils n×E=3000
- **Parameter:** Wahrnehmung=4, Pheromon-Abgabe=20.0, Verdunstungsrate=0.015, max_ticks=1000, seed=2004

### Simulationsverlauf

#### Simulation 1: 5 Ameisen (E=600)

Die erste Nahrungsquelle wird bei T=16 gefunden. Die erste Lieferung ans Nest erfolgt erst bei T=223 — 207 Ticks nach dem Fund. Bei T=100 und T=200 sind noch 0% der Nahrung geliefert; der erste Eintrag erscheint erst bei T=300 mit 1.7% (1 Einheit). Bis T=500 steigt die Effizienz auf 8.3% (5 Einheiten) und stagniert dort bis zum Ende der Simulation. 3 Tiere sterben; 2 überleben bis T=1000.

#### Simulation 2: 10 Ameisen (E=300)

Die erste Nahrung wird bei T=22 gefunden, die erste Lieferung erfolgt bei T=51 — deutlich früher als bei 5 Ameisen. Bei T=100 sind bereits 6.7% (4 Einheiten) geliefert. Die Effizienz steigt gleichmäßig: 15.0% bei T=300, 18.3% bei T=500, 25.0% bei T=1000 (15 Einheiten). 7 Tiere sterben; 3 überleben.

#### Simulation 3: 20 Ameisen (E=150)

Die erste Nahrung wird bei T=20 gefunden, die erste Lieferung bei T=47. Der Anstieg ist der schnellste aller drei Simulationen: 6.7% bei T=100, 20.0% bei T=200, 28.3% bei T=300. Ab T=500 verlangsamt sich die Ausbeutung (40.0%) — die meisten Tiere sind zu diesem Zeitpunkt gestorben. Die Simulation endet bei T=1000 mit 43.3% (26 Einheiten). 19 Tiere sterben; 1 überlebt.

### Ergebnisse

| Simulation | Ameisen | Energie | Erste Lieferung | Effizienz (T=1000) | Tode | Überlebende |
|---|---|---|---|---|---|---|
| sim_5ants  | 5  | 600 | T=223 | 8.3%  (5/60)  | 3  | 2/5  |
| sim_10ants | 10 | 300 | T=51  | 25.0% (15/60) | 7  | 3/10 |
| sim_20ants | 20 | 150 | T=47  | 43.3% (26/60) | 19 | 1/20 |

Effizienz-Verlauf:

| Tick   | 5 Ameisen | 10 Ameisen | 20 Ameisen |
|---|---|---|---|
| T=100  | 0.0%  | 6.7%  | 6.7%  |
| T=200  | 0.0%  | 8.3%  | 20.0% |
| T=300  | 1.7%  | 15.0% | 28.3% |
| T=500  | 8.3%  | 18.3% | 40.0% |
| T=750  | 8.3%  | 21.7% | 41.7% |
| T=1000 | 8.3%  | 25.0% | 43.3% |

### Interpretation

Die Ergebnisse zeigen eine klare monotone Korrelation zwischen Populationsgröße und Ausbeutungseffizienz: 5 Ameisen liefern 8.3%, 10 Ameisen 25.0%, 20 Ameisen 43.3% — bei identischer Kolonie-Gesamtenergie. Die Forschungsfrage ist damit zugunsten größerer Populationen zu beantworten.

Der entscheidende Unterschied liegt in der Geschwindigkeit der Spurenbildung. Mit 5 Ameisen dauert es bis T=223, bis die erste Einheit ans Nest gelangt — die Gradienten sind zu schwach für eine zuverlässige Rückkehr. Mit 20 Ameisen gelingt die erste Lieferung bereits bei T=47: Mehr Ameisen legen mehr Pheromon pro Zeiteinheit, wodurch Gradienten früher stark genug werden, um Träger zuverlässig zurück zum Nest zu leiten. Die hohe Sterblichkeit bei 20 Ameisen (19/20) zeigt, dass E=150 bei 10 Schritten Weglänge knapp bemessen ist — die Kolonie liefert den Großteil ihrer Beute in einem frühen Schub, bevor die Population kollabiert.

---

## 4. Experiment 2: Pheromonspur-Unterbrechung

### Motivation

Experiment 2 untersucht die Robustheit des Algorithmus gegenüber Unterbrechungen bestehender Pheromonspuren. Durch vorplatzierte Spuren (Warmstart) wird die anfängliche Erkundungsphase übersprungen und der Effekt der Lücke isoliert messbar. Das Experiment zeigt, ob und wie schnell das System eine beschädigte Route selbst repariert.

### Versuchsaufbau

- **Grid:** 12×12, Nest bei (6,6)
- **Nahrungsquelle:** (0,6), 30 Einheiten, 6 Schritte Manhattan vom Nest
- **Vorplatzierte Spuren:** Entlang y=6 von x=0 bis x=5 sind je 10.0 Einheiten Nahrung- und Nest-Pheromon platziert
- **Lücke (Sim 2):** Bei x=3 und x=4 sind keine Pheromone vorhanden
- **Hindernisse:** (3,9), (4,9), (8,3), (8,4)
- **Parameter:** 10 Ameisen, E=200, Wahrnehmung=4, Pheromon-Abgabe=20.0, Verdunstungsrate=0.015, max_ticks=600, seed=2004

### Simulationsverlauf

#### Simulation 1: Vollständige Pheromonspur (Baseline)

Die erste Nahrung wird bei T=10 gefunden, die erste Lieferung erfolgt bei T=19. Die Ausbeutung steigt rasch: 60.0% bei T=100, 100% bei T=200. Alle 30 Einheiten sind spätestens bei T=200 geliefert. Ab diesem Punkt sterben die Tiere durch Energiemangel; bei T=600 sind alle 10 Ameisen tot.

#### Simulation 2: Unterbrochene Pheromonspur (Lücke bei x=3,4)

Die erste Nahrung wird bei T=33 gefunden — 23 Ticks später als in Sim 1. Die erste Lieferung folgt bei T=64 (+45 Ticks Verzögerung). Der Unterschied ist bei T=100 am deutlichsten: nur 13.3% (4 Einheiten) gegenüber 60.0% in Sim 1. Die Kolonie überbrückt die Lücke durch Erkundung und baut neue Pheromonpfade auf: 53.3% bei T=200, 96.7% bei T=300, 100% bei T=500. Die vollständige Ausbeutung aller 30 Einheiten wird damit um ca. 300 Ticks verzögert, aber letztlich erreicht. 9 Tiere sterben; 1 überlebt.

### Ergebnisse

| Simulation | Erste Lieferung | T=100 | T=200 | T=300 | T=600 | Erschöpfung |
|---|---|---|---|---|---|---|
| sim_complete | T=19 | 60.0% | 100.0% | 100.0% | 100.0% | T≈200 |
| sim_gap      | T=64 | 13.3% | 53.3%  | 96.7%  | 100.0% | T≈500 |

### Interpretation

Beide Simulationen erreichen letztlich 100% Ausbeutung — der Algorithmus zeigt vollständige Selbstheilungsfähigkeit bei gegebener Laufzeit. Der Kontrast liegt in der Geschwindigkeit: Die Lücke verschiebt den Zeitpunkt der ersten Lieferung um 45 Ticks und verzögert die vollständige Erschöpfung um rund 300 Ticks. Am prägnantesten ist der Unterschied bei T=100, wo die Lücken-Simulation mit 13.3% knapp ein Viertel der Baseline-Effizienz (60.0%) erreicht.

Der Algorithmus überbrückt die Lücke durch probabilistische Erkundung: Ameisen, die die Spur bis x=5 verfolgen und dort die Lücke antreffen, erkunden benachbarte Felder und legen bei Erfolg neue Pheromonpfade durch den leeren Bereich. Dieser Prozess braucht Zeit, gelingt aber zuverlässig. Im Kontext der Forschungsfrage zeigt das Experiment, dass Spurrobustheit von der Koloniegröße abhängt: Mehr Ameisen würden die Lücke schneller überbrücken, da mehr Erkundungspfade parallel getestet werden.

---

## 5. Experiment 3: Skalierbarkeit

### Motivation

Experiment 3 untersucht, wie sich die Effizienz der Kolonie mit steigender Populationsgröße auf einem deutlich größeren Grid entwickelt. Vier Nahrungsquellen in den Ecken des 25×25-Grids (je ~22 Schritte vom Nest) stellen hohe Anforderungen an Erkundung und Transportkapazität. Das Experiment zeigt, ab wann Skaleneffekte abnehmen und welche Mindestkoloniegröße für effektive Ausbeutung auf großen Grids erforderlich ist.

### Versuchsaufbau

- **Grid:** 25×25, Nest bei (12,12)
- **Nahrungsquellen:** (1,1), (23,1), (1,23), (23,23), je 50 Einheiten (gesamt 200)
- **Hindernismauern:** (8,10–13), (16,11–14), (11–13,8), (12–14,16) — vier kurze Barrieren um das Nest
- **Populationen:** 10, 20, 30, 39 Ameisen
- **Parameter:** E=500, Wahrnehmung=4, Pheromon-Abgabe=45.0, Verdunstungsrate=0.005, max_ticks=1500, seed=2004

Die Pheromon-Parameter weichen bewusst von Experiment 1 ab: Die minimale Manhattan-Distanz zu den Eckenquellen beträgt ~22 Schritte — mehr als doppelt so weit wie in Experiment 1. Bei gleicher Verdunstungsrate würden Pheromone entlang langer Pfade so stark abbauen, dass Träger die Steigung zum Nest nicht mehr zuverlässig erkennen können. Die Verdunstungsrate wurde daher von 0.015 auf 0.005 reduziert und die Abgabemenge von 20.0 auf 45.0 erhöht, um ausreichend starke Gradienten über die längeren Distanzen sicherzustellen.

### Simulationsverlauf

#### Simulation 1: 10 Ameisen

Die erste Nahrung wird erst bei T=150 gefunden — die geringe Populationsdichte auf dem 25×25-Grid führt zu einer langen Erkundungsphase. Die erste Lieferung erfolgt bei T=233. Der Anstieg bleibt moderat: 2.5% bei T=500, 5.0% bei T=1000, 5.5% bei T=1500 (11 Einheiten). 7 Tiere sterben; 3 überleben.

#### Simulation 2: 20 Ameisen

Die erste Nahrung wird bei T=44 gefunden, die erste Lieferung erfolgt bei T=259 — trotz früherer Entdeckung mit 215 Ticks deutlich verzögert, da die Gradienten zunächst zu schwach für zuverlässige Rückkehr sind. Ab T=500 beschleunigt sich die Ausbeutung: 5.5% bei T=500, 8.0% bei T=750 (16 Einheiten), danach Stagnation. 19 Tiere sterben; 1 überlebt.

#### Simulation 3: 30 Ameisen

Die erste Nahrung wird bei T=44 gefunden, die erste Lieferung folgt deutlich früher als bei 20 Ameisen: T=101. Der Anstieg ist gleichmäßiger und stärker: 5.0% bei T=300, 8.5% bei T=500, 12.5% bei T=1000, 14.0% bei T=1500 (28 Einheiten). 26 Tiere sterben; 4 überleben.

#### Simulation 4: 39 Ameisen

Die erste Nahrung wird bei T=46 gefunden, die erste Lieferung bei T=119. Der Anstieg ist der stärkste aller vier Simulationen: 8.5% bei T=300, 15.5% bei T=500, 20.0% bei T=750, 30.5% bei T=1500 (61 Einheiten). 24 Tiere sterben; 15 überleben — die höchste Überlebensrate relativ zur Startgröße nach 30 Ameisen.

### Ergebnisse

| Simulation | Erste Nahrung | Erste Lieferung | Effizienz (T=1500) | Tode | Überlebende |
|---|---|---|---|---|---|
| sim_10ants | T=150 | T=233 | 5.5%  (11/200) | 7  | 3/10  |
| sim_20ants | T=44  | T=259 | 8.0%  (16/200) | 19 | 1/20  |
| sim_30ants | T=44  | T=101 | 14.0% (28/200) | 26 | 4/30  |
| sim_39ants | T=46  | T=119 | 30.5% (61/200) | 24 | 15/39 |

Effizienz-Verlauf:

| Tick   | 10 Ameisen | 20 Ameisen | 30 Ameisen | 39 Ameisen |
|---|---|---|---|---|
| T=300  | 0.5%  | 1.0%  | 5.0%  | 8.5%  |
| T=500  | 2.5%  | 5.5%  | 8.5%  | 15.5% |
| T=750  | 4.0%  | 8.0%  | 11.5% | 20.0% |
| T=1000 | 5.0%  | 8.0%  | 12.5% | 25.5% |
| T=1500 | 5.5%  | 8.0%  | 14.0% | 30.5% |

### Interpretation

Die Effizienz steigt monoton mit der Populationsgröße: 5.5% → 8.0% → 14.0% → 30.5%. Der Zuwachs ist jedoch nicht linear — der Sprung von 30 auf 39 Ameisen (+16.5 Prozentpunkte) ist deutlich größer als der von 10 auf 20 (+2.5) oder 20 auf 30 (+6.0). Das legt eine kritische Schwelle nahe: Erst ab ~35–39 Ameisen baut die Kolonie auf dem 25×25-Grid schnell genug Gradienten auf, um eine selbstverstärkende Transportroutine zu etablieren. Kleinere Kolonien finden zwar Nahrung (Erstfund bei T=44–150), können aber ohne ausreichend starke Pheromonspuren keine effiziente Rückkehrroute stabilisieren.

Der Vergleich zwischen 20 und 30 Ameisen ist aufschlussreich: Beide finden Nahrung erstmals bei T=44, aber die erste Lieferung erfolgt bei 20 Ameisen erst T=259, bei 30 Ameisen schon T=101. Mehr parallele Sucher legen schneller genug Pheromon ab, um den Gradienten über die 22-Schritte-Distanz navigierbar zu machen.

Bezogen auf die Forschungsfrage bestätigt Experiment 3 die Tendenz aus Experiment 1: Mehr Ameisen liefern auf größeren Grids mehr Nahrung. Die nichtlineare Skalierung zeigt zudem, dass auf großen Grids eine Mindest-Populationsgröße erforderlich ist, unterhalb derer keine stabile Ausbeutung entsteht.

---

## 6. Zusammenfassung und Ausblick

Alle drei Experimente zeigen konsistent, dass größere Ameisenkolonien — bei gleicher oder pro-Kopf geringerer Energie — mehr Nahrung liefern als kleinere. In Experiment 1 steigt die Effizienz von 8.3% (5 Ameisen) über 25.0% (10 Ameisen) auf 43.3% (20 Ameisen) bei konstantem n×E=3000. In Experiment 2 überbrücken die Ameisen eine vollständige Spurunterbrechung durch Erkundung und erreichen trotz einer Verzögerung von ~300 Ticks am Ende ebenfalls 100% Ausbeutung. In Experiment 3 zeigt sich auf dem großen 25×25-Grid eine nichtlineare Skalierung (5.5% → 8% → 14% → 30.5%), die auf eine kritische Mindest-Populationsgröße für stabile Gradientenbildung über lange Distanzen hinweist. Die Forschungsfrage ist damit klar zu beantworten: *Mehr Ameisen mit geringerer individueller Energie sind effizienter*, solange die Gradienten ausreichend stark für zuverlässige Rücknavigation sind.

Als sinnvolle Anschlussuntersuchungen bieten sich an: dynamische Hindernisse oder sich verändernde Nahrungsquellen zur Beobachtung von Adaption; mehrere Nester mit geteilter Pheromon-Infrastruktur; alternative Verdunstungsstrategien (z.B. distanzabhängige Raten); sowie eine quantitative Auswertung der Brokering-Variante im Direktvergleich mit der Basis-Implementierung auf denselben Experimentkonfigurationen.

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
