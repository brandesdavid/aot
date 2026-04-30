# Skizze und Arch von ant colony

## Manager (der Gott/ kein Agent)

- manager liest json datei und verteilt damit die wichtigen informationen zu den jeweiligen klassen, d.h. grid wird erstellt, instanzen erstellt für agenten,
- gibt zeit tick/takt vor und inkrementiert diese oder dekrementiert
- manager kann ameisen/agent pheromon ablegen zwingen, aber besser (wir machen das so) wenn ameise es "automatisch" unbewusst ablegt
- bei jedem takt wird energie level  von ameise um eins verringert. wenn er nur noch eins hat, und geht auf ein weiteres feld im nächsten takt, wird erst nach dem takt von "energielevel 0" sterben (weil wenn er 1 energie level hat, und im nächsten takt mit energie level 0 auf nest ist, ist er wieder am leben)

## Modelldatei Elemente (json)

## Items (beschreibt Itemklassen)

- id
- name
- value (bspw. agent/ameise legt 10 pheromone, und pheroverdunstung passiert indem dekrementiert wird)
(bspw. nestPheromon oder Nahrungpheromon oder FOODpiece)

## Spawn (beschreibt abstrakt ein nest, später für andere agenten )

- id
- name
- Agents(liste was für agenten er spawnt):
  - pro Agent:
    - agent id (halt ameise)
    - n bzw. count (wieviele werden gespawned?)

## Agent (beschreibt den Ameisenagent, kann aber in zukunft abstrahiert werden)

- id
- capacity:
  - pro item:
    - id
    - count (bspw. "infinite" pheromon nahrung + nest, aber nur 1 food item)
- items (trägt ameisen)
- energie (int, stellt lebenszeit dar)
- perception (wieviele nachbarfelder kann agent sehen? 4 oder 8 etc. um herum, erstmal nur aber sozusagen viereck und kein kreis)
- (muss koordinate nicht kennen, kann aber)
- (legt pheromon item ab, kostet aber keine zeit und keine energie)
- (wahrnehmung vom ameise ist nur beschränkt auf die items, also nahrung + nest auf den feld wo sie stehen. für die felder umherum kann ameise nur pheromone sehen. hier )
- (die ameise läuft aber dann probabilistisch herum, und geht natürlich EHER zum pheromon mit nahrung bspw., muss aber nicht.)
- (wir machen erstmal kein kurzzeitgedächtnis, bspw. nicht merken wo ameise war, erstmal nur navigation durch pheromone)

## Grid

- Parameter width und size
- Felder (matrix oben links ist x,y unten links ist 0,0 und oben rechts width,height):
  - pro Feld:
    - koordinate (x,y)
    - capacity (int, wieviele agenten/ameisen können max. drauf, 0=hindernis)
    - Items (nur bei felder capacity!=0 und jedes feld kann unendlich viele items haben):
      - pro Item (instanz):
        - id von item
        - menge/stärke
      - (wir geben hier an, welche items vielleicht schon liegen könnten, wie pheromone, um ein warmstart festzulegen)
    - agents: (ob ein agent da steht)
      - pro Agent:
        - agent id / instanz
    - Spawn:
      - id (halt die id vom nest)
      - (count von wieviele ameisen gespawned werden steht ja schon in der instanz von spawn nest)
      - (eigentlich haben wir für diese aufgabe nur ein nest, aber abstrahieren es falls irgendwann mehre neste. hier schwärmen ja die ameisen raus)
      - (hier wird agent seine energie auf 100% aufgefrischt, kostet keine zeit und keine energie, also direkt wenn agent drauf ist sofort auffüllen)

# Sequenz diagramm

bzw. ablauf einer simulation:

## kommunikation zwischen rollen

parser: liest einfach json und gibt manager alle instanzen vor
manager ist "gott": kreiert die grid welt etc, die agenten typen etc.

- pro takt werden alle agent aufgerufen ihren prozess zu starten (sense reason act)
- danach führt halt agent alles aus was er machen wollte aus seinem prozess
- danach check der manager nach sterben, updates wie items dekrementieren (pheromone) etc.
- sendet zum logger was alles passiert ist (aktionen ausgeführt, items dekrementiert, food ggefunden etc. zunächst loggen wir für den anfang einfach nur welche agenten essen gefunden haben, welche ameisen gestorben sind und welche essen zurückgebracht haben + zeittick dazu )
