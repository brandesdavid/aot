from __future__ import annotations
import copy
import json
from pathlib import Path


class Parser:
    @staticmethod
    def load(filepath: str) -> list[dict]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        with open(path) as f:
            raw = json.load(f)
        return Parser.resolve_simulations(raw)

    @staticmethod
    def resolve_simulations(raw: dict) -> list[dict]:
        simulations = raw.get("simulations")
        base = {k: v for k, v in raw.items() if k != "simulations"}

        if not simulations:
            config = copy.deepcopy(base)
            Parser._ensure_log_file(config, None)
            return [config]

        result = []
        for sim in simulations:
            sim_id = sim.get("id", f"sim_{len(result)}")
            overrides = {k: v for k, v in sim.items() if k not in ("id", "name")}
            merged = Parser._deep_merge(copy.deepcopy(base), overrides)
            merged["simulation"] = {"id": sim_id, "name": sim.get("name", sim_id)}
            Parser._ensure_log_file(merged, sim_id)
            result.append(merged)
        return result

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        result = dict(base)
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = Parser._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def _ensure_log_file(config: dict, sim_id: str | None) -> None:
        logging = config.setdefault("logging", {})
        if "grid_state_every_n_ticks" not in logging:
            logging["grid_state_every_n_ticks"] = 1
        if "tick_summary_every_n_ticks" not in logging:
            logging["tick_summary_every_n_ticks"] = 1
        if "output_file" not in logging:
            exp_id = config.get("experiment", {}).get("id", "sim")
            suffix = f"_{sim_id}" if sim_id else ""
            logging["output_file"] = f"logs/{exp_id}{suffix}.jsonl"
