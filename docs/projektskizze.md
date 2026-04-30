# projektskizze

TU Berlin -Soße 2026 - Agententechnologien

---

## 1. Systemdesign – Klassendiagramm


![klassendiag](klassendiag.png)


### Erläuterung

**Manager** ist der zentrale Koordinator
- liest die modelldatei per `parser`, baut die gridwelt auf,
-  instanziiert die agenten und steuert den zeittakt.
-  pro takt verarbeitet er zuerst die ausstehenden aktionen, aktualisiert die umgebung (pheromonverdunstung, energieauffrischung, tode) 
- und triggert dann jeden lebenden agenten für einen neuen sense-reason-act-zyklus. 
- konflikte nach dem "first come, first served" aufgelöst.

**grid** ist eine n x   m-matrix von `field`-objekten. koordinatenursprung (0,0) ist unten links.

**field** repräsentiert eine zelle. `capacity == 0` bedeutet hindernis. felder mit `spawn_id` sind nester und frischen die energie eintreffender agenten sofort und kostenlos auf.

**spawn (nest)** konfiguriert, welche agenten in welcher anzahl erzeugt werden. für diese aufgabe gibt es ein nest, die abstraktion erlaubt mehrere.

**item** ist in drei konkrete konfigurationstypen unterteilt: `foodconfig`, `nestpheromoneconfig`, `foodpheromoneconfig`. zur laufzeit existieren `iteminstance` objekte auf den feldern. pheromone haben eine `evaporation_rate` und werden nach jedem takt vom manager dekrementiert; bei stärke 0 wird die instanz entfernt.

**agent** ist abstrakt. `antagent` implementiert den reaktiven ameisenalgorithmus. die wahrnehmung umfasst die items auf dem eigenen feld (nahrung, nest) sowie die pheromonwerte der direkten nachbarfelder (4-nachbarschaft). die navigation erfolgt probabilistisch: der agent bewegt sich mit wahrscheinlichkeit 0,8 entlang des stärksten relevanten pheromons, sonst zufällig.

**action** kapselt die absicht eines agenten. gültige aktionen: `moveaction`, `pickupaction`, `dropaction`, `waitaction`. der manager prüft jede aktion auf gültigkeit und legt das ergebnis (`actionresult`) in die inbox des agenten.

---

## 2. simulationsmodell (json)

das folgende beispiel zeigt die struktur der modelldatei für experiment 1. 

```json
{
  "experiment": {
    "id": "exp1_coldstart_basic",
    "name": "Experiment 1: Cold Start – Grundlegende Nahrungsversorgung",
    "description": "Kaltstartexperiment zur Verifikation des Algorithmus. 15x15-Grid mit Hindernisreihen, zwei Nahrungsquellen in unterschiedlicher Entfernung zum Nest. Drei Simulationen mit 5, 10 und 20 Ameisen zeigen den Einfluss der Populationsgröße auf die Versorgungseffizienz.",
    "max_ticks": 800,
    "warmstart": false
  },
  "item_types": [
    { "id": "food",           "name": "Nahrung",          "evaporation_rate": 0.0 },
    { "id": "pheromone_nest", "name": "Nest-Pheromon",    "evaporation_rate": 0.5 },
    { "id": "pheromone_food", "name": "Nahrung-Pheromon", "evaporation_rate": 0.5 }
  ],
  "agent_types": [
    {
      "id": "ant",
      "name": "Ameise",
      "energy": 120,
      "perception_range": 4,
      "pheromone_drop_amount": 10.0,
      "capacity": [
        { "item_type_id": "food",           "max": 1  },
        { "item_type_id": "pheromone_nest", "max": -1 },
        { "item_type_id": "pheromone_food", "max": -1 }
      ]
    }
  ],
  "spawns": [
    {
      "id": "nest_main",
      "name": "Hauptnest",
      "agent_spawns": [
        { "agent_type_id": "ant", "count": 10 }
      ]
    }
  ],
  "grid": {
    "width": 15,
    "height": 15,
    "default_capacity": 5,
    "fields": [
      { "x": 7,  "y": 7,  "capacity": 999, "spawn_id": "nest_main", "items": [] },
      { "x": 2,  "y": 2,  "capacity": 5,   "items": [{ "item_type_id": "food", "quantity": 25 }] },
      { "x": 12, "y": 12, "capacity": 5,   "items": [{ "item_type_id": "food", "quantity": 25 }] },
      { "x": 4,  "y": 6,  "capacity": 0,   "items": [] },
      { "x": 5,  "y": 6,  "capacity": 0,   "items": [] },
      { "x": 6,  "y": 6,  "capacity": 0,   "items": [] },
      { "x": 8,  "y": 8,  "capacity": 0,   "items": [] },
      { "x": 9,  "y": 8,  "capacity": 0,   "items": [] },
      { "x": 10, "y": 8,  "capacity": 0,   "items": [] }
    ]
  },
  "logging": {
    "output_file": "logs/exp1_coldstart.jsonl",
    "events": ["food_found", "food_delivered", "agent_death", "tick_summary"]
  }
}
```

felder: die nicht explizit in `fields` aufgeführt sind, erhalten `default_capacity`. 
hindernisse werden durch `capacity: 0` ausgedrückt. 

warmstart szenarien können beliebige pheromonmengen auf feldern vorbelegen. das feld `description` dient als experiment-kommentar.

---

## 3. Ablauf einer Simulation (Sequenzdiagramm)

![ablaufsim](ablaufsim.png)

### erläuterung

parser übergibt alle konfigurationen an manager, der daraus gridwelt und agenten aufbaut. in jedem takt verarbeitet manager zuerst die aktionswarteschlange aus vorperiode, validiert jede aktion und legt das ergebnis in die inbox des jeweiligen agenten. danach erfolgen pheromonverdunstung, todeskontrolle und energieauffrischung bei nestern und nahrungsfeldern. anschließend triggert manager sequenziell jeden lebenden agenten: dieser liest seine wahrnehmung (inklusive inbox-feedback), entscheidet probabilistisch und stellt die nächste aktion in die warteschlange. logger erhält nach jedem takt eine zusammenfassung.

---

## 4. Loggin

geloggt wird im jsonl-format (eine json-zeile pro ereignis). folgende ereignisse werden erfasst:

1. `food_found`: zeittakt, agent-id, position der nahrungsquelle
2. `food_delivered`: zeittakt, agent-id, ursprungsposition der nahrung
3. `agent_death`: zeittakt, agent-id, letzte position
4. `tick_summary`: zeittakt, anzahl lebender agenten, gesamtnahrung im nest, anzahl nahrungssucher, anzahl nahrungsträger



---

## 5. forschungsfrage

Was ist der Zusammenhang mit der Größe des Ameisenarmees und der Lebensdauer einer Ameise, bspw. 1 Ameise mit 1000 Lebenszyklen vs 1000 Ameisen mit 1 Lebenszyklus

**experiment 1 (kaltstart, grundversorgung):** 

**experiment 2 (warmstart, spurwiederherstellung):** .

**experiment 3 (skalierung):** .
