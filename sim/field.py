from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from .items import ItemInstance


@dataclass
class Field:
    x: int
    y: int
    capacity: int
    items: list[ItemInstance] = field(default_factory=list)
    agents: list = field(default_factory=list)
    spawn_id: Optional[str] = None

    def is_obstacle(self) -> bool:
        return self.capacity == 0

    def is_full(self) -> bool:
        if self.capacity < 0:
            return False
        return len(self.agents) >= self.capacity

    def get_pheromone_strength(self, item_type: str) -> float:
        return sum(i.quantity for i in self.items if i.item_type == item_type)

    def get_item_quantity(self, item_type: str) -> float:
        return sum(i.quantity for i in self.items if i.item_type == item_type)

    def add_item(self, item_type: str, quantity: float) -> None:
        for item in self.items:
            if item.item_type == item_type:
                item.quantity += quantity
                return
        self.items.append(ItemInstance(item_type=item_type, quantity=quantity))

    def remove_item(self, item_type: str, quantity: float) -> bool:
        for item in self.items:
            if item.item_type == item_type:
                if item.quantity < quantity:
                    return False
                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)
                return True
        return False
