# AOT casino  

ameisen sim

## plantuml:

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty 
```
## simulation starten

```bash
python main.py experiments/experiment1_coldstart.json
```

logs werden im jsonl-format unter `logs/` gespeichert.

##  structure  

```
sim/          core (Manager, Grid, Agenten, Items)
experiments/  json modelldateien 
gui/          (vielleicht geplant noch so gui darstellen?)
logs/         simulations logs pro zeiteinheit 
docs/         aufgabenblätter und projektskizze
```

##architecture 

in docs/ lesen.
