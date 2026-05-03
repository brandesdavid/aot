import sys

from sim.parser import Parser
from sim.manager import Manager


def main() -> None:
    args = sys.argv[1:]
    visual_mode = "--visual" in args
    pos_args = [a for a in args if not a.startswith("--")]

    if not pos_args:
        print("Usage: python main.py <experiment.json> [--visual]")
        print("  --visual  Log full grid state per tick (required for visualizer.html)")
        sys.exit(1)

    configs = Parser.load(pos_args[0])
    exp = configs[0].get("experiment", {}) if configs else {}
    mode_label = " [visual mode]" if visual_mode else ""
    print(f"Experiment: {exp.get('name', 'Unnamed')} ({len(configs)} simulation(s)){mode_label}\n")

    for config in configs:
        sim = config.get("simulation", {})
        sim_name = sim.get("name") or sim.get("id", "Unnamed")
        print(f"  Running: {sim_name} ({config.get('experiment', {}).get('max_ticks', '?')} ticks)")

        manager = Manager()
        manager.load_model(config)
        manager._visual_mode = visual_mode
        manager.run()

        log_file = manager.logger.output_file if manager.logger else "N/A"
        print(f"  Done.    Log: {log_file}")


if __name__ == "__main__":
    main()
