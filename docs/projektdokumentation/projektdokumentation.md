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
- **Parameter:** Wahrnehmung=4, Pheromon-Abgabe=10.0, Verdunstungsrate=0.05, max_ticks=1000, seed=42

### Simulationsverlauf

#### Simulation 1: 5 Ameisen (E=600)

Die Kolonie findet die erste Nahrungsquelle bei T=42 und liefert erstmals bei T=83 ans Nest. Der Aufbau stabiler Pheromonspuren geht langsam vonstatten: Bei T=100 sind erst 1.7% der Nahrung geliefert. Es festigt sich zu keinem Zeitpunkt eine effiziente Route. Durch die geringe Ameisenanzahl bauen sich die Spuren nur schwach, verpuffen schnell wieder, und Ameisen bewegen sich wenig Zielstrebig zur Nahrung. Zwischen T=500 und T=750 beschleunigt sich die Ausbeutung merklich auf 23.3%, Ein Tier stirbt; Insgesamt werden bis T=1000 insgesamt 18 Einheiten am Nest abgeliefert(30%).

#### Simulation 2: 10 Ameisen (E=300)

Die erste Nahrung wird bei T=24 entdeckt, die erste Lieferung erfolgt bei T=47, also deutlich früher als mit 5 Ameisen. Das Doppelte an Suchern führt zu schnellerem Spuraufbau und gleichmäßigerem Anstieg: 6.7% bei T=100, 16.7% bei T=250, 30% bei T=500, 38.3% bei T=750, 55% bei T=1000. Die Effizienz steigt nahezu linear über den gesamten Simulationszeitraum. 5 Tiere sterben; die überlebenden 5 sind bei T=1000 noch aktiv im Transport (2 Träger).

#### Simulation 3: 20 Ameisen (E=150)

Die erste Nahrung wird bereits bei T=16 gefunden, die erste Lieferung erfolgt bei T=31, was den schnellste Start aller drei Simulationen darstellt. Die hohe Ameisenanzahl ermöglicht einen schnellen Spuraufbau, sodass bei T=100 bereits 23.3% und bei T=250 43.3% der Nahrung erbeutet wurde. Allerdings reicht die Energie von E=150 bei 10 Schritten Weglänge kaum für mehrere vollständige Runden: Zwischen T=250 und T=500 sterben die meisten Tiere (von 13 auf 3 Überlebende). Ab T=500 stagniert die Ausbeutung bei 55–60%, da kaum noch lebende Träger vorhanden sind. Bis T=1000 überlebt nur 1 Tier; insgesamt werden 36 Einheiten (60%) geliefert.

### Ergebnisse

| Simulation | Ameisen | Energie | Erste Lieferung | Effizienz (T=1000) | Tode | Überlebende |
|---|---|---|---|---|---|---|
| sim_5ants  | 5  | 600 | T=83 | 30.0% (18/60) | 1  | 4/5  |
| sim_10ants | 10 | 300 | T=47 | 55.0% (33/60) | 5  | 5/10 |
| sim_20ants | 20 | 150 | T=31 | 60.0% (36/60) | 19 | 1/20 |

Effizienz-Verlauf:

| Tick | 5 Ameisen | 10 Ameisen | 20 Ameisen |
|---|---|---|---|
| T=100  | 1.7%  | 6.7%  | 23.3% |
| T=250  | 8.3%  | 16.7% | 43.3% |
| T=500  | 10.0% | 30.0% | 55.0% |
| T=750  | 23.3% | 38.3% | 60.0% |
| T=1000 | 30.0% | 55.0% | 60.0% |

### Interpretation

Mehr Ameisen führen zu einer höheren Ausbeutungseffizienz, auch wenn jede einzelne Ameise weniger Energie besitzt. Die Forschungsfrage ist damit klar zugunsten größerer Populationen zu beantworten: Größere Kolonien finden Nahrung früher (T=16 vs. T=42) und liefern mehr (60% vs. 30%) — trotz gleicher Gesamtenergie.

Der Algorithmus skaliert gut mit der Ameisenanzahl, solange die individuelle Energie ausreicht, um Hin- und Rückweg zu bewältigen. E=150 liegt bei 10 Schritten Weglänge an der unteren Grenze: Die 20-Ameisen-Kolonie kollabiert nach dem ersten erfolgreichen Ausbeutungsschub fast vollständig. E=300 erlaubt hingegen mehrere Runden und erzeugt eine gleichmäßige, robuste Transportleistung. Der Algorithmus zeigt eine Stärke bei mittleren Populationen: 10 Ameisen liefern pro überlebendem Tier die höchste Ausbeute.

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
- **Parameter:** 10 Ameisen, E=200, Wahrnehmung=4, Verdunstungsrate=0.04, max_ticks=600, seed=42

### Simulationsverlauf

#### Simulation 1: Vollständige Pheromonspur (Baseline)

Die vorplatzierte Spur entfaltet sofort ihre Wirkung: Bereits bei T=10 tragen 2 Ameisen Nahrung. Die erste Lieferung erfolgt bei T=19. Die Kolonie folgt der vorhandenen Route ohne Erkundungsaufwand und steigert die Effizienz gleichmäßig: 26.7% bei T=50, 43.3% bei T=100, 76.7% bei T=200. Die vollständige Ausbeutung aller 30 Einheiten (100%) ist bei T=255 erreicht. Danach setzt das Absterben durch Energiemangel ein — bei T=600 sind noch 4 von 10 Ameisen am Leben.

#### Simulation 2: Unterbrochene Pheromonspur (Lücke bei x=3,4)

Die Ameisen folgen der Spur bis x=5, treffen bei x=3 und x=4 auf keine Pheromonspuren und wechseln in die Zufallserkundung. Die erste Nahrung wird dennoch bei T=15 gefunden (5 Ticks später als in Sim 1), die erste Lieferung bei T=28 (9 Ticks Verzögerung). Der entscheidende Unterschied zeigt sich im Aufbau: Bei T=50 sind erst 3 Einheiten geliefert (10%), gegenüber 8 (26.7%) in Sim 1. Die Lücke wird schrittweise überbrückt, indem Ameisen, die die Quelle über Umwege finden, neue Pheromonspuren durch den leeren Bereich legen. Die Effizienz steigt langsam: 26.7% bei T=100, 30% bei T=200, 66.7% bei T=400. Bis T=600 werden 25 von 30 Einheiten (83.3%) geliefert; die Quelle bleibt unvollständig geleert.

### Ergebnisse

| Simulation | Erste Lieferung | Effizienz (T=100) | Effizienz (T=200) | Effizienz (T=600) | Erschöpfung |
|---|---|---|---|---|---|
| sim_complete | T=19 | 43.3% | 76.7% | 100.0% | T=255 |
| sim_gap      | T=28 | 26.7% | 30.0% | 83.3%  | nicht erreicht |

### Interpretation

Der Algorithmus zeigt eine begrenzte Selbstreparaturfähigkeit: Die Lücke wird durch Zufallserkundung überbrückt, aber erheblich langsamer als im Idealfall. Die kritische Schwäche liegt im Zeitraum T=100–T=200: In Sim 2 stagniert die Effizienz bei 30%, während Sim 1 bereits 76.7% erreicht. Die Verdunstungsrate von 0.04 lässt die vorplatzierten Spuren in der Lückenumgebung schnell schwächer werden, ohne dass ausreichend neue Spuren aufgebaut werden. Das Experiment zeigt, dass der Algorithmus robust genug ist, um eine Spur prinzipiell wiederherzustellen, aber bei begrenztem Zeithorizont deutliche Effizienzeinbußen hinnimmt.

Im Kontext der Forschungsfrage ist relevant, dass eine größere Population (mehr Ameisen) die Spurlücke schneller schließen würde: Mehr zufällig erkundende Tiere erhöhen die Wahrscheinlichkeit, den Überbrückungspfad früh zu entdecken und durch Pheromonabgabe zu verstärken. Wenige Ameisen mit hoher Energie dagegen erkunden seltener alternative Wege, da sie bevorzugt etablierten Spuren folgen. Robustheit gegenüber Spurunterbrechungen ist damit ein weiterer Vorteil größerer Kolonien.

---

## 5. Experiment 3: Skalierbarkeit

### Motivation

Experiment 3 untersucht, wie sich die Effizienz der Kolonie mit steigender Populationsgröße auf einem deutlich größeren Grid entwickelt. Vier Nahrungsquellen in den Ecken des 25×25-Grids (je ~22 Schritte vom Nest) stellen hohe Anforderungen an Erkundung und Transportkapazität. Das Experiment zeigt, ab wann Diminishing Returns einsetzen und ob die Kolonie bei sehr großen Populationen durch Engpässe an den Hindernismauern limitiert wird.

### Versuchsaufbau

- **Grid:** 25×25, Nest bei (12,12)
- **Nahrungsquellen:** (1,1), (23,1), (1,23), (23,23), je 50 Einheiten (gesamt 200)
- **Hindernismauern:** (8,10–13), (16,11–14), (11–13,8), (12–14,16) — vier kurze Barrieren um das Nest
- **Populationen:** 10, 20, 30, 39 Ameisen
- **Parameter:** E=500, Wahrnehmung=4, Pheromon-Abgabe=12.0, Verdunstungsrate=0.03, max_ticks=1500, seed=42

### Simulationsverlauf

#### Simulation 1: 10 Ameisen

Die geringe Anzahl von Suchern führt zu einer langen Erkundungsphase: Erste Nahrung bei T=66, erste Lieferung bei T=119. Der Spuraufbau ist langsam; bei T=500 sind erst 4.5% (9 Einheiten) geliefert. Die Kolonie wächst organisch in die Aufgabe hinein — bei T=1500 sind 8 von 10 Ameisen noch am Leben, da E=500 auf dem großen Grid für mehrere Runden ausreicht. Insgesamt 28 Einheiten (14%) geliefert.

#### Simulation 2: 20 Ameisen

Trotz doppelter Ameisenanzahl fällt die erste Lieferung mit T=147 später aus als bei 10 Ameisen (T=119) — ein Hinweis auf stochastische Varianz und die Schwierigkeit, auf dem großen Grid günstige Routen zu etablieren. Ab T=750 übernimmt die Masse: 15 der 20 Träger sind aktiv im Transport. Bei T=1500 sind 47 Einheiten (23.5%) geliefert; 15 Ameisen überleben.

#### Simulation 3: 30 Ameisen

Die 30-Ameisen-Kolonie zeigt den besten Start: Erste Nahrung bei T=32 (frühester Fund aller Simulationen), erste Lieferung bei T=63. Die hohe Ameisenanzahl führt zu schnellem parallelen Spuraufbau in mehrere Richtungen: 9% bei T=300, 15.5% bei T=500. Ab T=750 setzen Tode ein (E=500 wird nach vielen Runden erschöpft); dennoch bleibt die Kolonie aktiv und liefert bis T=1500 insgesamt 67 Einheiten (33.5%). 18 von 30 Ameisen überleben.

#### Simulation 4: 39 Ameisen

Die größte Population erzielt die höchste Gesamtausbeute. Erste Nahrung bei T=52, erste Lieferung bei T=101. Bei T=300 sind bereits 22 Einheiten (11%) geliefert; der Anstieg ist steil bis T=500 (17.5%) und verlangsamt sich danach durch zunehmende Tode. Ab T=750 sterben viele Tiere (35→20 Überlebende bis T=1500). Insgesamt werden 84 Einheiten (42%) geliefert.

### Ergebnisse

| Simulation | Erste Nahrung | Erste Lieferung | Effizienz (T=1500) | Tode | Überlebende |
|---|---|---|---|---|---|
| sim_10ants | T=66  | T=119 | 14.0% (28/200) | 2  | 8/10  |
| sim_20ants | T=74  | T=147 | 23.5% (47/200) | 5  | 15/20 |
| sim_30ants | T=32  | T=63  | 33.5% (67/200) | 12 | 18/30 |
| sim_39ants | T=52  | T=101 | 42.0% (84/200) | 19 | 20/39 |

Effizienz-Verlauf:

| Tick  | 10 Ameisen | 20 Ameisen | 30 Ameisen | 39 Ameisen |
|---|---|---|---|---|
| T=300  | 2.0%  | 4.0%  | 9.0%  | 11.0% |
| T=500  | 4.5%  | 6.5%  | 15.5% | 17.5% |
| T=750  | 8.0%  | 9.5%  | 21.0% | 24.5% |
| T=1000 | 11.5% | 16.0% | 25.5% | 32.5% |
| T=1500 | 14.0% | 23.5% | 33.5% | 42.0% |

### Interpretation

Die Effizienz steigt monoton mit der Populationsgröße, jedoch mit abnehmenden Zuwächsen: +9.5 Prozentpunkte von 10 auf 20 Ameisen, +10 von 20 auf 30, aber nur +8.5 von 30 auf 39. Echte Diminishing Returns zeigen sich deutlich im Verhältnis gelieferter Einheiten pro Ameise: 10 Ameisen liefern 2.8 Einheiten/Tier, 20 liefern 2.35, 30 liefern 2.23, 39 liefern 2.15.

Die Hindernismauern um das Nest erzwingen Flaschenhälse, die bei großen Populationen zunehmend spürbar werden. Konkurrierende Pheromonspuren zu vier Eckenquellen können sich gegenseitig abschwächen, was den Spuraufbau verlangsamt. Das überraschend späte erste Fund-Ereignis bei 20 Ameisen (T=74 vs. T=66 bei 10 Ameisen) ist auf stochastische Pfadwahl zurückzuführen und zeigt, dass auf dem großen 25×25-Grid der Zufall der frühen Exploration eine größere Rolle spielt als auf kleineren Grids.

Bezogen auf die Forschungsfrage bestätigt Experiment 3 die in Experiment 1 gefundene Tendenz: Auch bei gleicher individueller Energie liefern mehr Ameisen stets mehr Nahrung. Der Skalierungsvorteil ist jedoch nicht linear — die Effizienz pro Ameise nimmt mit steigender Populationsgröße ab (2.8 → 2.15 Einheiten/Tier). Wenige Ameisen mit hoher Energie wären auf diesem Grid noch deutlich im Nachteil, da die langen Distanzen zu den Eckquellen viele Hin- und Rückwege erfordern und ein dünner Spuraufbau die Erkundung kaum parallelisiert.

---

## 6. Zusammenfassung und Ausblick

Die Experimente zeigen, dass größere Ameisenkolonien — bei gleicher Gesamtenergie — stets effizienter Nahrung sammeln als kleinere, da parallele Erkundung schnelleren Spuraufbau ermöglicht und frühere Lieferungen erzeugt. Die Forschungsfrage ist klar zu beantworten: *Mehr Ameisen mit geringerer Energie sind effizienter*, solange die individuelle Energie ausreicht, um Hin- und Rückweg zur nächsten Quelle zu bewältigen. An dieser unteren Energiegrenze (Exp1: E=150 bei 10 Schritten Weglänge) kollabiert die Kolonie nach dem ersten Ausbeutungsschub fast vollständig. Der Algorithmus zeigt zudem begrenzte Selbstreparaturfähigkeit bei unterbrochenen Pheromonspuren (Exp2) und skaliert auf größeren Grids mit Diminishing Returns ab ~30 Ameisen (Exp3).

Als sinnvolle Anschlussuntersuchungen bieten sich an: dynamische Hindernisse oder sich verändernde Nahrungsquellen zur Beobachtung von Adaption; mehrere Nester mit geteilter Pheromon-Infrastruktur; alternative Verdunstungsstrategien (z.B. kontextabhängige Raten); sowie eine quantitative Auswertung der Brokering-Variante im Direktvergleich mit der Basis-Implementierung auf denselben Experimentkonfigurationen.

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
