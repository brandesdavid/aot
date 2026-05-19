# Review-Übersicht – Gruppe 18

Zusammenfassung aller erhaltenen Anmerkungen aus den drei Review-Quellen.

---

## Quelle 1: ZweitesReview

### 1. Forschungsfrage – konfundierte Variablen
Essen wurde konstant skaliert, was aber kein sinn macht weil die quellgröße konstant skaliert, d.h. 8 ameisen 80 energie, 20 ameisen 200 energie etc. Ein Vergleich wäre sinnlos, weil die aufgabengröße auch variiert

Empfehlung war: Quellenmengen konstant halten oder den Effekt isolieren.
Ist stand jetzt: Exp1 hat jetzt je 30 Einheiten pro Quelle (konstant über alle Simulationen).

---

### 2. warmstart-experiment fehlt

Ist jetzt: `experiment2_warmstart.json` zeigt vollständige vs. unterbrochene Pheromonspur.

---

### 3. pheromonablage konstant statt abnehmend 
`pheromone_drop_amount: 10.0` war als konstanter Wert definiert... Die Aufgabenstellung fordert explizit "drop Pheromone *at a decreasing rate*".

Empfehlung war: Schrittzähler seit letztem Pickup/Drop führen und Ablagemenge linear oder exponentiell ableiten.
Ist stand jetzt: `drop = max(0.5, base × 0.97^steps_since_event)` in `manager.py`.

---

### 4. probabilistische navigation nicht spezifiziert
"Navigation erfolgt probabilistisch" und "isFacing wird probabilistisch benachteiligt" wurde mehrfach erwähnt, aber nirgends irgendwie formal beschrieben: welche Score-Funktion? Wie stark ist die Rückrichtung benachteiligt? Was passiert in pheromonfreier Umgebung?

Empfehlung war: Wahrscheinlichkeitsformel `P(f) = score(f) / Σscore(f')` dokumentieren.
Ist stand jetzt: Formel und Penalty-Logik in der Projektdokumentation beschrieben.

---

### 5. logging-tiefe vs. forschungsfrage
Die geloggten Events erlauben die Berechnung der "Zeit zur Ausbeutung", aber Pheromonwerte und Quellen-Restmengen wurden nicht erfasst...

Empfehlung war: `tick_summary` um verbleibende Mengen pro Quelle ergänzen und optional Pheromon-Snapshot alle k Ticks.
Ist stand jetzt: `food_sources` ( also die Restmengen pro Quelle) und `efficiency_pct` werden in jedem `tick_summary` mitgeloggt.

---

### 6. kleinere anmerkungen

- `capacity: -1` für "unbegrenzt" ist ungewöhnlich und unerwartet, was aber jetzt in der Projektdokumentation erklärt wird.
- `Field.agents` und `Agent.position` sind redundant, was aber eine bewusste Designentscheidung für Performance ist , dsewegen kein handlungsbedarf
- 4-Nachbarschaft vs. 8-Nachbarschaft nicht explizit begründet. *(In Projektdokumentation erwähnt)*

---

## Quelle 2: AOT_G17_Review_for_G18

### forschungsfrage – "effizienz" nicht definiert
das wort "effizienz" in der forschungsfrage ist nicht erklärt. offene fragen:

- prozentuale ausbeutung nach einer bestimmten zeit oder wenn das programm abbricht?
- spielt die benötigte zeit eine rolle (also z.b. 90% schnell vs. 100% langsam)?
- wird die sterberate in die effizienz eingerechnet?

ist jetzt: effizienz ist definiert als `% gelieferter Nahrung / Gesamtnahrung` (`efficiency_pct` im Log) sowie Ausbeutungsrate (Einheiten/Tick).

---

### Parameter "Futterquellen Größe" bei 5 Ameisen problematisch
bei sehr kleiner population (5 ameisen) können einzelne ameisen quellen alleine ausbeuten, ohne dass schwarmintelligenz entsteht -> das macht den vergleich mit größeren populationen schwer. außerdem ist die aussagekraft durch hohe zufallsabhängigkeit begrenzt -> viele durchläufe nötig.

ist: noch Offen, Seed wurde hinzugefügt (Reproduzierbarkeit), aber die inhärente Problematik kleiner Populationen bleibt (ist Bestandteil der Forschungsfrage).

---

### redundante datenspeicherung (positionen gemeint)
item-positionen sind doppelt gespeichert: über das `field` und direkt beim item. gefahr von inkonsistenzen bei bewegungen.

ist: noch offen, bewusste Designentscheidung, kein Handlungsbedarf.

---

### Umgang mit falschen Aktionen unklar
unklar, ob ungültige Aktionen ignoriert werden oder ob der agent nach einer neuen handlung gefragt wird.

ist: noch offen, im code werden ungültige aktionen mit `ActionResult(success=False)` beantwortet und ins `inbox` des agents geschrieben (der agent ignoriert das ergebnis aktuell). kann in der doku kurz erwähnt werden.

---

## quelle 3: anmerkungen des tutors

### 1. seed für zufallsgenerator
einen festen seed für den zufallsgenerator hinzufügen, um die reproduzierbarkeit des experiments zu erhöhen.

ist jetzt: `"seed": 42` in allen drei experiment-JSONs; `random.seed()` wird in `manager.load_model()` gesetzt. (beho]ben also)

---

### 2. effizienz-metrik überdenken (x)
woran wird "effizienz in der ausbeutung der nahrungsquellen" gemessen? insbesondere bei unterschiedlich großen quellen für verschiedene koloniengrößen ist die *gesamtmenge gesammelter nahrung* keine gute metrik.

ist jetzt: `efficiency_pct = food_delivered / initial_total_food × 100` wird pro tick geloggt. quellenmengen in exp1 sind jetzt konstant (je 30), damit der vergleich zwischen populationsgrößen fair ist. (behoben also)

---


BTW: wir müssen gucken, dass wir die parameterwahl begründen, oder irgendwie analyterischer herleiten. WIESO nutzen wir genau 20 ameisen etc?