# Run an experiment
# Usage: just run-exp experiments/experiment1_coldstart.json
run-exp exp:
    python main.py {{exp}}

# Run an experiment with visual mode and open the visualizer afterwards
# Usage: just run-exp-visual experiments/experiment1_coldstart.json
run-exp-visual exp:
    python main.py {{exp}} --visual
