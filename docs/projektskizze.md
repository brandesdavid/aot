# Projektskizze
TU Berlin -Soße 2026 - Agententechnologien

---

## 1. Systemdesign – Klassendiagramm

![klassendiag](klassendiag.png)


### Erläuterung

Der `Manager` ist die zentrale Instanz des Systems.
Der `Manager` liest die Modelldatei für ein Experiment per `parser` ein und führt die zu dem Experiment gehörenden Simulationen durch. Die relevanten Ereignisse loggt der `Manager` mithilfe des `Logger`.

Ein `Grid` ist eine n x m-matrix von `field`-objekten. Koordinatenursprung (0,0) ist unten links.

Ein `Field` repräsentiert eine Zelle. `capacity == 0` bedeutet Hindernis. Felder mit einer `spawn_id="nest_*"` sind Nester und frischen die Energie eines eintreffenden `AntAgent` sofort und kostenlos auf.

Ein `Spawn` konfiguriert, welche Agenten in welcher Anzahl erzeugt werden. Für diese Aufgabe gibt es ein `Spawn` an dem ausschließlich Ant-Agenten gespawnt werden, die Abstraktion erlaubt mehrere Spawnpunkte und auch, dass verschiedene Agententypen an der gleichen Stelle gespawnt werden können.

`ItemInstance` ist nicht ein einzelnes Item, sondern eine Anzahl von Items, da nicht jedes Item einzeln instantiiert wird. Über `item_type` wird definiert um welches Item es sich handelt und in den Subklassen von `ItemConfig` werden die Details zu einem Item definiert. Aktuell sind diese Infos nur `id` (diese dient zum linken zwischen `ItemInstance` und der jeweiligen `ItemConfig`), `name` und `evaporation_rate`.

> Info: Config Klassen wie ItemConfig werden in Python benutzt für Daten, die nur gespeichert werden. In den ItemConfig Subklassen werden lediglich Daten über die Eigenschaften von Items gespeichert, deswegen wurde diese Namenskonvention gewählt.

Die `quantity` von einer `ItemInstance` mit `item_type="food"` wird durch Ant-Agenten dekrementiert. Die `quantity` von einer `ItemInstance` mit `item_type="pheromone_nest"` oder `item_type="pheromone_food"` wird in jedem Zeittakt von dem `Manager` basierend auf ihrer `evaporation_rate` dekrementiert, bei Stärke 0 wird die Pheromonen-Instanz entfernt.
Es gibt lediglich zwei Pheremonentypen, Food- und Nestpheremone.

Die Klasse `Agent` ist abstrakt, sodass potentiell weitere Agententypen eingeführt werden können. Die konkrete Subklasse `AntAgent` implementiert den reaktiven Ameisenalgorithmus. Die Wahrnehmung umfasst die Items auf dem eigenen Feld sowie die Pheromonwerte der direkten Nachbarfelder (4-Nachbarschaft). Die Navigation erfolgt probabilistisch: Der Agent bewegt sich mit wahrscheinlichkeit 0,8 entlang des stärksten relevanten Pheromons, sonst zufällig.

In einer `Action` steckt die Absicht eines Agenten. Die konkreten Subklassen der abstrakten `Action` Klasse sind: `MoveAction`, `PickupAction`, `DropAction`, `WaitAction`. Der `Manager` prüft jede Aktion auf Gültigkeit und legt das `ActionResult` in die Inbox des Agenten.

---

## 2. Simulationsmodell (json)

Das folgende Beispiel zeigt die Struktur der Modelldatei für Experiment 1.

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
    "events": ["food_found", "food_delivered", "agent_death", "tick_summary"]
  },
  "simulations": [
    {
      "id": "sim_5ants",
      "name": "5 Ameisen",
      "spawns": [
        { "id": "nest_main", "name": "Hauptnest", "agent_spawns": [{ "agent_type_id": "ant", "count": 5 }] }
      ]
    },
    {
      "id": "sim_10ants",
      "name": "10 Ameisen"
    },
    {
      "id": "sim_20ants",
      "name": "20 Ameisen",
      "spawns": [
        { "id": "nest_main", "name": "Hauptnest", "agent_spawns": [{ "agent_type_id": "ant", "count": 20 }] }
      ]
    }
  ]
}
```

Felder, die nicht explizit in `fields` aufgeführt sind, erhalten die für das Grid definierte `default_capacity`.
Hindernisse werden durch `capacity: 0` ausgedrückt.

Warmstart Szenarien können beliebige Pheromonmengen auf Feldern vorbelegen. Das Feld `description` dient dazu, dass durchgeführte Experiment zu beschreiben.

---

## 3. Ablauf einer Simulation (Sequenzdiagramm)

![ablaufsim](ablaufsim.png)

### Erläuterung

`Parser` übergibt alle Konfigurationen an den `Manager`, der daraus die Gridwelt aufbaut und die Agenten spawnt.
In jedem Takt verarbeitet der `Manager` zuerst die Aktionswarteschlange aus der Vorperiode indem er jede Aktion validiert und das Ergebnis in die Inbox des jeweiligen Agenten legt.
Konflikte zwischen den Aktionen werden nach dem First-Come-First-Serve Prinzip aufgelöst.
Anschließend erfolgen Pheromonverdunstung, Todeskontrolle und Energieauffrischung für alle Ant-Agenten, die sich beim Nest oder bei einem Nahrungsfeld befinden. Zu guter Letzt triggert der Manager sequenziell jeden lebenden `Agent i`, sodass dieser seinen Sense-Reason-Act-Zyklus durchführt.
`Agent i` liest seine Wahrnehmung (inklusive Inbox-Feedback), entscheidet probabilistisch und stellt die nächste Aktion in die Warteschlange. Somit wird die in Zyklus /k/ von `Agent i` beschlossene Aktion erst in Zyklus /k+1/ von dem `Manager` ausgeführt (oder als ungültig zurückgewiesen).
Der `Logger` erhält nach jedem Takt eine Zusammenfassung.

---

## 4. Logging

Geloggt wird im jsonl-format (eine json-Zeile pro Ereignis). Folgende Ereignisse werden erfasst:

1. `food_found`: zeittakt, agent-id, position der nahrungsquelle ("Ant Agent hat Nahrung aufgenommen")
2. `food_delivered`: zeittakt, agent-id, ursprungsposition der nahrung ("Ant Agent hat Nahrung im Nest abgelegt")
3. `agent_death`: zeittakt, agent-id, letzte position ("Ant Agent ist gestorben")
4. `tick_summary`: zeittakt, anzahl lebender agenten, gesamtnahrung im nest, anzahl nahrungssucher, anzahl nahrungsträger ("Ein Zeittakt ist vorbei")



---

## 5. Forschungsfrage

Was ist der Zusammenhang mit der Größe des Ameisenarmees und der Lebensdauer einer Ameise, bspw. 1 Ameise mit 1000 Lebenszyklen vs 1000 Ameisen mit 1 Lebenszyklus

**experiment 1 (kaltstart, grundversorgung):** 

**experiment 2 (warmstart, spurwiederherstellung):** .

**experiment 3 (skalierung):** .
