from __future__ import annotations
from collections import deque
import random
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .field import Field
    from .actions import Action


class Agent(ABC):
    def __init__(self, agent_id: str, energy: int, max_energy: int):
        self.id = agent_id
        self.energy = energy
        self.max_energy = max_energy
        self.position: Optional[Field] = None
        self.inbox: list = []
        self.pending_action: Optional[Action] = None
        self.alive: bool = True

    @abstractmethod
    def sense(self, perception: dict) -> None:
        pass

    @abstractmethod
    def reason(self) -> None:
        pass

    @abstractmethod
    def act(self) -> Optional[Action]:
        pass


class AntAgent(Agent):
    def __init__(
        self,
        agent_id: str,
        energy: int,
        max_energy: int,
        perception_range: int = 4,
        pheromone_drop_amount: float = 10.0,
        capacity_config: list = None,
    ):
        super().__init__(agent_id, energy, max_energy)
        self.perception_range = perception_range
        self.pheromone_drop_amount = pheromone_drop_amount
        self.carrying: Optional[str] = None
        self.capacity_config: list = capacity_config or []
        self._last_food_source: Optional[tuple[int, int]] = None
        self._perception: dict = {}
        self._recent_positions: deque[tuple[int, int]] = deque(maxlen=12)
        self._trail: list[tuple[int, int]] = []
        self._steps_since_event: int = 0

    def sense(self, perception: dict) -> None:
        self._perception = perception
        current = perception.get("current_field", {})
        x = current.get("x")
        y = current.get("y")
        if isinstance(x, int) and isinstance(y, int):
            pos = (x, y)
            if not self._trail:
                self._trail = [pos]
            elif self.carrying is None and self._trail[-1] != pos:
                self._trail.append(pos)
        self.inbox.clear()

    def reason(self) -> None:
        from .actions import MoveAction, PickupAction, DropAction, WaitAction

        current = self._perception.get("current_field", {})
        neighbors = self._perception.get("neighbors", [])

        has_food_here = current.get("food", 0) > 0
        is_at_nest = current.get("is_nest", False)

        if self.carrying == "food":
            if is_at_nest:
                cx = current.get("x")
                cy = current.get("y")
                if isinstance(cx, int) and isinstance(cy, int):
                    self._trail = [(cx, cy)]
                self.pending_action = DropAction(agent_id=self.id, item_type="food", quantity=1.0)
                return
            nest_neighbor = next((n for n in neighbors if n.get("is_nest") and not n.get("is_full")), None)
            if nest_neighbor is not None:
                self.pending_action = MoveAction(agent_id=self.id, dx=nest_neighbor["dx"], dy=nest_neighbor["dy"])
                return
            self.pending_action = self._climb_gradient("pheromone_nest", neighbors, deterministic=False)
            return

        if has_food_here:
            self._last_food_source = (current.get("x", -1), current.get("y", -1))
            self.pending_action = PickupAction(agent_id=self.id, item_type="food")
            return

        self.pending_action = self._climb_gradient("pheromone_food", neighbors)

    def act(self) -> Optional[Action]:
        return self.pending_action

    def remember_position(self, x: int, y: int) -> None:
        pos = (x, y)
        self._recent_positions.append(pos)
        if self.carrying is None:
            if not self._trail:
                self._trail = [pos]
            elif self._trail[-1] != pos:
                self._trail.append(pos)

    def _climb_gradient(self, pheromone_type: str, neighbors: list, deterministic: bool = False) -> Action:
        from .actions import MoveAction, WaitAction

        candidates = [
            n for n in neighbors
            if not n.get("is_obstacle", True) and not n.get("is_full", False)
        ]

        if not candidates:
            return WaitAction(agent_id=self.id)

        current = self._perception.get("current_field", {})
        cx = current.get("x")
        cy = current.get("y")
        if isinstance(cx, int) and isinstance(cy, int) and not self._recent_positions:
            self._recent_positions.append((cx, cy))

        strengths = [n.get(pheromone_type, 0.0) for n in candidates]
        max_strength = max(strengths) if strengths else 0.0

        recent = list(self._recent_positions)
        penalty = {}
        decay = 0.7
        for i, pos in enumerate(reversed(recent)):
            penalty[pos] = max(penalty.get(pos, 0), decay ** i)

        scored = []
        penalty_scale = 5.0
        for n in candidates:
            if not isinstance(cx, int) or not isinstance(cy, int):
                target = None
            else:
                target = (cx + n["dx"], cy + n["dy"])
            base = n.get(pheromone_type, 0.0)
            cycle_penalty = penalty.get(target, 0) * penalty_scale if target is not None else 0.0
            score = max(0.01, base + 0.05 - cycle_penalty)
            scored.append((n, score))

        if deterministic:
            best_score = max(score for _, score in scored)
            best_choices = [n for n, score in scored if score == best_score]
            chosen = random.choice(best_choices)
        elif max_strength > 0 and random.random() < 0.8:
            choices = [n for n, _ in scored]
            weights = [w for _, w in scored]
            chosen = random.choices(choices, weights=weights, k=1)[0]
        else:
            weights = [w for _, w in scored]
            total = sum(weights)
            probs = [w / total for w in weights]
            choices = [n for n, _ in scored]
            chosen = random.choices(choices, weights=probs, k=1)[0]

        return MoveAction(agent_id=self.id, dx=chosen["dx"], dy=chosen["dy"])

