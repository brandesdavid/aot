import sys

from sim.parser import Parser
from sim.manager import Manager


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <experiment.json>")
        sys.exit(1)

    configs = Parser.load(sys.argv[1])
    exp = configs[0].get("experiment", {}) if configs else {}
    print(f"Experiment: {exp.get('name', 'Unnamed')} ({len(configs)} simulation(s))\n")

    for config in configs:
        sim = config.get("simulation", {})
        sim_name = sim.get("name") or sim.get("id", "Unnamed")
        print(f"  Running: {sim_name} ({config.get('experiment', {}).get('max_ticks', '?')} ticks)")

        manager = Manager()
        manager.load_model(config)
        manager.run()

        log_file = manager.logger.output_file if manager.logger else "N/A"
        print(f"  Done.    Log: {log_file}")


if __name__ == "__main__":
    main()
