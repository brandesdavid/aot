from __future__ import annotations
import json
from pathlib import Path


class Logger:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self._events: list[dict] = []
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    def _record(self, tick: int, event_type: str, data: dict) -> None:
        self._events.append({"tick": tick, "event": event_type, **data})

    def log_food_found(self, tick: int, agent_id: str, x: int, y: int) -> None:
        self._record(tick, "food_found", {"agent_id": agent_id, "x": x, "y": y})

    def log_food_delivered(self, tick: int, agent_id: str, source_x: int, source_y: int) -> None:
        self._record(tick, "food_delivered", {
            "agent_id": agent_id,
            "source_x": source_x,
            "source_y": source_y,
        })

    def log_agent_death(self, tick: int, agent_id: str, x: int, y: int) -> None:
        self._record(tick, "agent_death", {"agent_id": agent_id, "x": x, "y": y})

    def log_tick_summary(
        self,
        tick: int,
        alive_count: int,
        food_at_nest: float,
        searcher_count: int,
        carrier_count: int,
    ) -> None:
        self._record(tick, "tick_summary", {
            "alive": alive_count,
            "food_at_nest": food_at_nest,
            "searchers": searcher_count,
            "carriers": carrier_count,
        })

    def save(self) -> None:
        with open(self.output_file, "w") as f:
            for event in self._events:
                f.write(json.dumps(event) + "\n")
