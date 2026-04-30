from dataclasses import dataclass


@dataclass
class ItemConfig:
    id: str
    name: str
    evaporation_rate: float = 0.0


@dataclass
class ItemInstance:
    item_type: str
    quantity: float

    def evaporate(self, rate: float) -> bool:
        self.quantity = max(0.0, self.quantity - rate)
        return self.quantity <= 0.0
