# parameterwahl, herleitung und begründung

## warum ist n x e_max = konstant?

die forschungsfrage lautet: *sind wenige ameisen mit höherer maximalenergie effizienter als viele ameisen mit geringerer maximalenergie?*

ABER um diese frage sauber zu beantworten, muss sichergestellt werden, dass >>nicht zwei variablen gleichzeitig variiert<< werden. wenn man einfach nur die ameisenzahl erhöht und die energie gleich lässt: dann ändert sich automatisch auch die gesamtkapazität der kolonie (mehr ameisen = mehr gesamtenergie = mehr arbeit). der unterschied in der effizienz wäre dann nicht auf die *verteilung* der energie zurückzuführen, sondern eifnach auf auf mehr verfügbare ressourcen.

die LÖSUNG: >>n × e_max = konstant halten<<. alle kolonien haben dieselbe gesamtkapazität, verteilen sie aber unterschiedlich. das ist eine klassische technik in der experimentellen forschung zur isolation einer unabhängigen variablen.

---

## wie wurde der konkrete wert 3000 bestimmt?

ekeine ahnung, wir müssen aber gucken, ob wir das vielleicht etwas formaler einleiten wollen

### idee schritt 1, eine untergrenze
j
für eine 15 mal 15-karte mit nest bei (7,7) und nahrung bei (2,2) und (12,12):

```
manhattan-distanz nest -> futter: 10 schritte
minimale rundreise:     10 (hin)+ 1 (pickup)+ 10 (zurück) + 1 (drop) = 22 schritte
initiale exploration:   circa 50–80 schritte zufallslauf bis trail gefunden
```

daraus ergibt sich eine mindestenergie von circa 70–120 für eine einzelne ameise, um überhaupt eine runde zu schaffen. darunter würden ameisen aber schon in der explorationsphase sterben, bevor sie jemals futter gefunden haben.

### idee schritt 2, pilot-test mit 10 ameisen

der wert e=300 für 10 ameisen war der originalwert aus der projektskizze, der sich in ersten tests als ausreichend erwiesen hatte (ameisen überlebten und sammelten futter). daraus wurde das produkt abgeleitet:

```
n x e = 10 x 300 = 3000
```

### idee schritt 3, ableitung der anderen werte

| simulation | ameisen | energie | n x  e | rundreisen vor tod (min.) |
|---|---|---|---|---|
| sim_5ants  | 5  | 600 | 3000 | ~27 |
| sim_10ants | 10 | 300 | 3000 | ~13 |
| sim_20ants | 20 | 150 | 3000 | ~6  |

*"rundreisen vor tod" = energie / 22 schritte pro rundreise, ohne energieauffüllung am nest.*

bei 20 ameisen mit e=150 haben die ameisen knapp genug buffer für ~6 trips plus initiale exploration. das liegt bewusst an der unteren grenze – zu wenige ameisen mit zu hoher energie würden den vergleich verfälschen.

---

## wie würde man das in echter forschung bestimmen?

in einer echten wissenschaftlichen studie würde man diese schritte durchführen:

**1. sensitivitätsanalyse**
mehrere produkte testen (z.b. 2000, 3000, 4000) und prüfen, ob die ergebnisstruktur stabil bleibt. wenn bei allen produkten gilt "mehr ameisen = effizienter", ist die aussage robust gegenüber der parameterwahl.

**2. statistische absicherung**
jede simulation mehrfach mit verschiedenen seeds laufen lassen und mittelwert ± standardabweichung angeben. unser ansatz mit einem festen seed (42) erzeugt reproduzierbare, aber nicht statistisch abgesicherte ergebnisse.

**3. theoretische begründung**
den energiewert relativ zur kartengeometrie begründen: z.b. "e_min = 3 × distanz_nest_futter, damit jede ameise bei optimalem verhalten mindestens 3 trips macht." dann daraus n × e_min als kontrollkonstante ableiten.

**4. orthogonale parameter**
sicherstellen, dass grid-größe, hindernis-dichte und quellen-menge über alle simulationen eines experiments konstant bleiben – was wir mit den je 30 einheiten pro quelle in exp1 bereits tun.

---

## zusammenfassung

die wahl n×e=3000 ist **begründet aber nicht beweisbar optimal**. sie stellt sicher, dass:
- 20 ameisen mit e=150 die exploration überleben können (>mindestenergie 70–120)
- 5 ameisen mit e=600 ausreichend zeit haben, trails aufzubauen
- die gesamtkapazität der kolonie konstant gehalten wird, um die forschungsfrage sauber zu isolieren

für eine publikation würde man eine sensitivitätsanalyse über mehrere produkte und mehrere seeds ergänzen.
