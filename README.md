# Ant Simulation

Ant colony simulation (Ameisen-Simulation) for the AOT Module.

## Prerequisites

- Python 3.10+ (stdlib only for the simulator; `pandas` is listed in `requirements.txt` for analysis scripts)
- Optional: [just](https://github.com/casey/just) for shortcut commands

## Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the simulation

Run an experiment by passing a JSON model file under `experiments/`:

```bash
python main.py experiments/experiment1_coldstart.json
```

With `just` installed:

```bash
just run-exp experiments/experiment1_coldstart.json
```

The program prints each sub-simulation name, tick count, and output log path. One experiment file can define several variants via a top-level `"simulations"` array (for example different ant counts); each variant runs in sequence.

### Available experiments

| File | Description |
|------|-------------|
| `experiments/experiment1_coldstart.json` | Cold start, multiple population sizes |
| `experiments/experiment1_coldstarttest.json` | Shorter cold-start test run |
| `experiments/experiment2_warmstart.json` | Warm start with existing pheromone trails |
| `experiments/experiment3_scalability.json` | Scalability / larger populations |
| `experiments/experiment4_maze.json` | Maze layout |

### Logs

Simulation output is written as JSONL (one JSON object per line) under `logs/`, for example:

```
logs/exp1_coldstart_basic_sim_10ants.jsonl
```

Logged events include food collection, deliveries, agent deaths, and per-tick summaries. Paths are set in each experiment’s `logging.output_file` or generated automatically from the experiment id.

### Visual playback

To record full grid state every tick (for the HTML visualizer), add `--visual`:

```bash
python main.py experiments/experiment1_coldstart.json --visual
# or: just run-exp-visual experiments/experiment1_coldstart.json
```

Visual logs are written under `logs/visual/`. Open `gui/visualizer.html` in a browser and load a visual `.jsonl` file (drag-and-drop or file picker).

## PlantUML

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
```

## Project structure

```
sim/          Core (Manager, Grid, agents, items)
experiments/  JSON model files
gui/          HTML visualizer (visualizer.html)
logs/         Simulation logs (JSONL)
docs/         Assignment sheets and project sketch
review/       Review / analysis material
```

## Architecture

See `docs/` for diagrams and design notes.
