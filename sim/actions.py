from dataclasses import dataclass, field


@dataclass
class Action:
    agent_id: str


@dataclass
class MoveAction(Action):
    dx: int
    dy: int


@dataclass
class PickupAction(Action):
    item_type: str
    quantity: float = 1.0


@dataclass
class DropAction(Action):
    item_type: str
    quantity: float = 1.0


@dataclass
class WaitAction(Action):
    pass


@dataclass
class ActionResult:
    success: bool
    action: Action
    message: str = ""
