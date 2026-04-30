import sys

from sim.parser import Parser
from sim.manager import Manager


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <experiment.json>")
        sys.exit(1)

    config = Parser.load(sys.argv[1])
    manager = Manager()
    manager.load_model(config)

    exp = config.get("experiment", {})
    print(f"Running: {exp.get('name', 'Unnamed')} ({exp.get('max_ticks', '?')} ticks)")

    manager.run()

    log_file = manager.logger.output_file if manager.logger else "N/A"
    print(f"Done. Log: {log_file}")


if __name__ == "__main__":
    main()
