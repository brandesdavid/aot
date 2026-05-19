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

<!-- ca. ½ Seite -->

### Ansatz

<!-- Welche Brokering-Variante (aus Kapitel 6.3 des Skripts) wird vorgeschlagen? Kurze Beschreibung des Mechanismus. -->

### Erwartete Veränderungen im Systemverhalten

<!-- Was ändert sich durch die Brokering-Variante? Welche Stärken/Schwächen der reinen Pheromon-Navigation werden adressiert? -->

### Begründung der Wahl

<!-- Warum ist diese Variante am besten geeignet? Analyse der Informationsasymmetrien im System (welcher Agent weiß was, welche Information fehlt wo?). Warum nicht eine andere Variante? -->
