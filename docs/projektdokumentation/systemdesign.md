# Systemdesign

## Überblick

Das System besteht aus drei Schichten: **Infrastruktur** (Parser, Manager, Logger), **Gridwelt** (Grid, Field, ItemInstance) und **Agenten** (AntAgent mit Aktionen). Der Manager orchestriert den gesamten Simulationsablauf; Agenten sind reaktiv und kommunizieren ausschließlich über Pheromonspuren auf dem Grid.

![systemdesign](systemdesign.png)

---

## Kernkomponenten

**Parser** liest eine JSON-Modelldatei ein und löst Simulationsvarianten (Override-Mechanismus) auf. Mit dem Flag `--visual` werden Logs in `logs/visual/` statt `logs/` geschrieben, sodass visuelle und reguläre Logs nie überschrieben werden.

**Manager** führt pro Tick folgende Schritte aus (in dieser Reihenfolge):

```
1. process_actions()          – Aktionen aus dem Vorschritt ausführen
2. refresh_energy()           – Energie an Nest/Futterfeld auffüllen
3. evaporate_pheromones()     – multiplikative Verdunstung aller Pheromontypen
4. check_deaths()             – Ameisen mit Energie ≤ 0 entfernen
5. log_tick_summary()         – Effizienz, Quellrestmengen, alive/carriers loggen
6. trigger_agents()           – sense → reason → act für jeden lebenden Agenten
```

**Field** speichert Agenten und Items (Nahrung, pheromone_nest, pheromone_food). `capacity = 0` markiert ein Hindernis; `capacity = -1` ist unbegrenzt (Nest). Pheromone sind reguläre Items mit `evaporation_rate > 0`.

**ItemInstance** verwendet **multiplikative Verdunstung** (`quantity *= 1 − rate`): veraltete Spuren verschwinden exponentiell in ~60 Ticks, aktive Spuren stabilisieren sich auf einem Gleichgewichtswert.

---

### navigationslogik (es wurde gemeckert, dass die isfacing logik nicht spezifiziert wurde)

der `antagent` setzt den reactive ameisenalgorithmus mit folgenden designentscheidungen um:

1. 4-nachbarschaft: jedes feld hat vier nachbarfelder (oben, unten, links, rechts).
2. probabilistische navigation: die wahrscheinlichkeit, ein nachbarfeld zu wählen, ergibt sich aus:

$$P(f) = \frac{\text{score}(f)}{\sum_{f'} \text{score}(f')}$$

wobei `score(f) = max(0.01, pheromon(f) + 0.05 − penalty(f))`. Die `penalty` bestraft zuletzt besuchte Felder, um Kurzzyklen zu vermeiden (Kurzzeitgedächtnis der letzten 8 Positionen).

3. rückweg zum nest: beim tragen von nahrung verfolgt die ameise zunächst den gespeicherten hinlauf-pfad (`_trail`) zurück, bevor sie dem Nest-Pheromon-Gradienten folgt.

4. isfacing-benachteiligung:die entgegengesetzte richtung zum letzten schritt wird durch die penalty-logik probabilistisch benachteiligt (Anti-Backtrack).

5. kapazität -1: im kapazitäts-array eines agents steht `"max": -1` für "keine Obergrenze". diese konvention betrifft ausschließlich pheromon-items, da ameisen beliebig viel pheromon ablegen dürfen. nahrung dagegen hat `"max": 1`, weil jede ameise genau eine einheit tragen kann.

---

## logging & effizienzmetrik

jedes `tick_summary`-event enthält:

| feld | beschreibung |
|---|---|
| `food_at_nest` | absolut gelieferte einheiten |
| `efficiency_pct` | `food_at_nest / initial_total × 100` (normalisiert) |
| `food_sources` | restmenge pro quelle (key: `"x,y"`) |
| `alive` / `carriers` / `searchers` | koloniezustand |

`efficiency_pct` ist die primäere metrik zur beantwortung der forschungsfrag, da sie unabhängig von absoluter quellgröße ist.

---

## änderungen gegenüber der projektskizze

| aspekt | projektskizze | aktuelle implementierung |
|---|---|---|
| pheromonabgabe | konstanter wert | abnehmend: `base × 0.97^steps` |
| verdunstung | linear (`quantity − rate`) | multiplikativ (`quantity × (1−rate)`) |
| isfacing | explizites richtungsfeld | implizit via `_recent_positions`-penalty |
| logging | food_found / delivered / death | + `food_sources`, `efficiency_pct` pro tick |
| log-pfade | einheitlich `logs/` | getrennt: `logs/` vs. `logs/visual/` |
| reproduzierbarkeit | kein seed | `"seed": 42` in allen experimenten |
| energiewerte exp1 | alle gleich | n×e=3000 konstant (5→600, 10→300, 20→150) |
