from __future__ import annotations
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

    def sense(self, perception: dict) -> None:
        self._perception = perception
        self.inbox.clear()

    def reason(self) -> None:
        from .actions import MoveAction, PickupAction, DropAction, WaitAction

        current = self._perception.get("current_field", {})
        neighbors = self._perception.get("neighbors", [])

        has_food_here = current.get("food", 0) > 0
        is_at_nest = current.get("is_nest", False)

        if self.carrying == "food":
            if is_at_nest:
                self.pending_action = DropAction(agent_id=self.id, item_type="food", quantity=1.0)
                return
            self.pending_action = self._climb_gradient("pheromone_nest", neighbors)
            return

        if has_food_here:
            self._last_food_source = (current.get("x", -1), current.get("y", -1))
            self.pending_action = PickupAction(agent_id=self.id, item_type="food")
            return

        self.pending_action = self._climb_gradient("pheromone_food", neighbors)

    def act(self) -> Optional[Action]:
        return self.pending_action

    def _climb_gradient(self, pheromone_type: str, neighbors: list) -> Action:
        from .actions import MoveAction, WaitAction

        candidates = [
            n for n in neighbors
            if not n.get("is_obstacle", True) and not n.get("is_full", False)
        ]
        if not candidates:
            return WaitAction(agent_id=self.id)

        strengths = [n.get(pheromone_type, 0.0) for n in candidates]
        max_strength = max(strengths)

        if max_strength > 0 and random.random() < 0.8:
            weights = [s + 0.01 for s in strengths]
            total = sum(weights)
            probs = [w / total for w in weights]
            chosen = random.choices(candidates, weights=probs, k=1)[0]
        else:
            chosen = random.choice(candidates)

        return MoveAction(agent_id=self.id, dx=chosen["dx"], dy=chosen["dy"])
