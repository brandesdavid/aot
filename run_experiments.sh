#!/bin/bash
set -e
python main.py experiments/experiment1_coldstart.json
python main.py experiments/experiment2_warmstart.json
python main.py experiments/experiment3_scalability.json

python main.py experiments/experiment1_coldstart.json --visual
python main.py experiments/experiment2_warmstart.json --visual
python main.py experiments/experiment3_scalability.json --visual

python3 - <<'EOF'
import json

def analyze(path, label):
    events = []
    with open(path) as f:
        for line in f:
            events.append(json.loads(line))
    summaries = {e['tick']: e for e in events if e['event'] == 'tick_summary'}
    deliveries = [e for e in events if e['event'] == 'food_delivered']
    deaths     = [e for e in events if e['event'] == 'agent_death']
    finds      = [e for e in events if e['event'] == 'food_found']
    last = summaries[max(summaries)] if summaries else {}
    milestones = {t: round(summaries[t].get('efficiency_pct', 0), 1)
                  for t in [100, 200, 300, 500, 750, 1000, 1250, 1500] if t in summaries}
    print(f"\n=== {label} ===")
    print(f"  First find: T={finds[0]['tick'] if finds else None}  "
          f"First deliver: T={deliveries[0]['tick'] if deliveries else None}")
    print(f"  Final eff:  {last.get('efficiency_pct',0):.1f}%  ({last.get('food_at_nest',0):.0f} units)  "
          f"Deaths: {len(deaths)}  Alive: {last.get('alive',0)}")
    print(f"  Milestones: {milestones}")

for f, l in [
    ("logs/exp1_coldstart_basic_sim_5ants.jsonl",  "Exp1 – 5 Ameisen  (E=600)"),
    ("logs/exp1_coldstart_basic_sim_10ants.jsonl", "Exp1 – 10 Ameisen (E=300)"),
    ("logs/exp1_coldstart_basic_sim_20ants.jsonl", "Exp1 – 20 Ameisen (E=150)"),
    ("logs/exp2_warmstart_sim_complete.jsonl",     "Exp2 – Vollständig"),
    ("logs/exp2_warmstart_sim_gap.jsonl",          "Exp2 – Lücke"),
    ("logs/exp3_scalability_sim_10ants.jsonl",     "Exp3 – 10 Ameisen"),
    ("logs/exp3_scalability_sim_20ants.jsonl",     "Exp3 – 20 Ameisen"),
    ("logs/exp3_scalability_sim_30ants.jsonl",     "Exp3 – 30 Ameisen"),
    ("logs/exp3_scalability_sim_39ants.jsonl",     "Exp3 – 39 Ameisen"),
]:
    analyze(f, l)
EOF
