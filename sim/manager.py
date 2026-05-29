from __future__ import annotations
import random
from typing import Optional

from .grid import Grid
from .field import Field
from .spawn import Spawn, AgentSpawnConfig
from .agent import Agent, AntAgent
from .actions import (
    Action, MoveAction, PickupAction, DropAction, WaitAction, ActionResult
)
from .logger import Logger
from .items import ItemConfig


class Manager:
    def __init__(self):
        self.grid: Optional[Grid] = None
        self.agents: list[Agent] = []
        self.tick: int = 0
        self.max_ticks: int = 0
        self.item_configs: dict[str, ItemConfig] = {}
        self.agent_type_configs: dict[str, dict] = {}
        self.spawns: dict[str, Spawn] = {}
        self.nest_positions: dict[str, tuple[int, int]] = {}
        self.logger: Optional[Logger] = None
        self._actions_queue: list[tuple[Agent, Action]] = []
        self._total_food_delivered: int = 0
        self._food_source_positions: list[tuple[int, int]] = []
        self._visual_mode: bool = False
        self._grid_state_every_n_ticks: int = 1
        self._tick_summary_every_n_ticks: int = 1
        self._initial_food_total: float = 0.0

    def load_model(self, config: dict) -> None:
        seed = config.get("seed")
        if seed is not None:
            random.seed(seed)

        self.max_ticks = config.get("max_ticks", 500)

        for item_cfg in config.get("item_types", []):
            ic = ItemConfig(
                id=item_cfg["id"],
                name=item_cfg["name"],
                evaporation_rate=item_cfg.get("evaporation_rate", 0.0),
            )
            self.item_configs[ic.id] = ic

        for agent_cfg in config.get("agent_types", []):
            self.agent_type_configs[agent_cfg["id"]] = agent_cfg

        for spawn_cfg in config.get("spawns", []):
            spawn = Spawn(id=spawn_cfg["id"], name=spawn_cfg["name"])
            for asc in spawn_cfg.get("agent_spawns", []):
                spawn.agent_spawn_configs.append(
                    AgentSpawnConfig(
                        agent_type_id=asc["agent_type_id"],
                        count=asc["count"],
                    )
                )
            self.spawns[spawn.id] = spawn

        grid_cfg = config.get("grid", {})
        self.grid = Grid(width=grid_cfg["width"], height=grid_cfg["height"])
        default_cap = grid_cfg.get("default_capacity", 5)

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.grid.fields[(x, y)] = Field(x=x, y=y, capacity=default_cap)

        for field_cfg in grid_cfg.get("fields", []):
            x, y = field_cfg["x"], field_cfg["y"]
            f = self.grid.get_field(x, y)
            if f is None:
                continue
            if "capacity" in field_cfg:
                f.capacity = field_cfg["capacity"]
            if "spawn_id" in field_cfg:
                f.spawn_id = field_cfg["spawn_id"]
                self.nest_positions[field_cfg["spawn_id"]] = (x, y)
            has_food = False
            for item_cfg in field_cfg.get("items", []):
                f.add_item(item_cfg["item_type_id"], item_cfg["quantity"])
                if item_cfg["item_type_id"] == "food":
                    has_food = True
            if has_food:
                self._food_source_positions.append((x, y))

        self._initial_food_total = sum(
            f.get_item_quantity("food") for f in self.grid.get_all_fields()
        )

        for spawn_id, spawn in self.spawns.items():
            nest_pos = self.nest_positions.get(spawn_id)
            if nest_pos is None:
                continue
            spawn_field = self.grid.get_field(*nest_pos)
            new_agents = spawn.create_agents(self.agent_type_configs, spawn_field)
            self.agents.extend(new_agents)

        log_cfg = config.get("logging", {})
        self.logger = Logger(log_cfg.get("output_file", "logs/simulation.jsonl"))
        self._grid_state_every_n_ticks = max(1, int(log_cfg.get("grid_state_every_n_ticks", 1)))
        self._tick_summary_every_n_ticks = max(1, int(log_cfg.get("tick_summary_every_n_ticks", 1)))

    def run(self) -> None:
        for tick in range(1, self.max_ticks + 1):
            self.tick = tick
            self._process_actions()
            self._refresh_energy_at_special_fields()
            self._evaporate_pheromones()
            self._check_deaths()
            self._log_tick_summary()
            self._trigger_agents()

        if self.logger:
            self.logger.save()

    def _trigger_agents(self) -> None:
        self._actions_queue.clear()
        for agent in [a for a in self.agents if a.alive]:
            perception = self._build_perception(agent)
            agent.sense(perception)
            agent.reason()
            action = agent.act()
            if action is not None:
                self._actions_queue.append((agent, action))

    def _process_actions(self) -> None:
        random.shuffle(self._actions_queue)
        for agent, action in self._actions_queue:
            if not agent.alive:
                continue
            result = self._apply_action(agent, action)
            agent.inbox.append(result)

    def _apply_action(self, agent: Agent, action: Action) -> ActionResult:
        if isinstance(action, MoveAction):
            return self._apply_move(agent, action)
        if isinstance(action, PickupAction):
            return self._apply_pickup(agent, action)
        if isinstance(action, DropAction):
            return self._apply_drop(agent, action)
        if isinstance(action, WaitAction):
            agent.energy -= 1
            return ActionResult(success=True, action=action)
        return ActionResult(success=False, action=action, message="unknown action")

    def _apply_move(self, agent: Agent, action: MoveAction) -> ActionResult:
        if agent.energy <= 0:
            return ActionResult(success=False, action=action, message="no energy")
        cur = agent.position
        nx, ny = cur.x + action.dx, cur.y + action.dy
        if not self.grid.in_bounds(nx, ny):
            return ActionResult(success=False, action=action, message="out of bounds")
        target = self.grid.get_field(nx, ny)
        if target is None or target.is_obstacle():
            return ActionResult(success=False, action=action, message="obstacle")
        if target.is_full():
            return ActionResult(success=False, action=action, message="field full")

        if isinstance(agent, AntAgent):
            pheromone_type = "pheromone_food" if agent.carrying else "pheromone_nest"
            drop = max(0.5, agent.pheromone_drop_amount * (0.97 ** agent._steps_since_event))
            cur.add_item(pheromone_type, drop)
            agent._steps_since_event += 1

        cur.agents.remove(agent)
        target.agents.append(agent)
        agent.position = target
        if isinstance(agent, AntAgent):
            agent.remember_position(target.x, target.y)
        agent.energy -= 1

        if target.spawn_id or target.get_item_quantity("food") > 0:
            agent.energy = agent.max_energy

        return ActionResult(success=True, action=action)

    def _apply_pickup(self, agent: Agent, action: PickupAction) -> ActionResult:
        if agent.energy <= 0:
            return ActionResult(success=False, action=action, message="no energy")
        field = agent.position
        if field.spawn_id and action.item_type == "food":
            return ActionResult(success=False, action=action, message="cannot pick food from nest")
        if field.get_item_quantity(action.item_type) < action.quantity:
            return ActionResult(success=False, action=action, message="item not available")
        if isinstance(agent, AntAgent):
            if agent.carrying is not None:
                return ActionResult(success=False, action=action, message="already carrying")
            field.remove_item(action.item_type, action.quantity)
            agent.carrying = action.item_type
            agent._steps_since_event = 0
            if self.logger:
                self.logger.log_food_found(self.tick, agent.id, field.x, field.y)
        agent.energy -= 1
        return ActionResult(success=True, action=action)

    def _apply_drop(self, agent: Agent, action: DropAction) -> ActionResult:
        if not isinstance(agent, AntAgent):
            return ActionResult(success=False, action=action, message="not an ant")
        if agent.carrying != action.item_type:
            return ActionResult(success=False, action=action, message="not carrying this item")
        field = agent.position
        source = agent._last_food_source
        field.add_item(action.item_type, action.quantity)
        agent.carrying = None
        agent._steps_since_event = 0
        agent.energy -= 1
        if field.spawn_id:
            self._total_food_delivered += 1
            if self.logger:
                src_x, src_y = source if source else (-1, -1)
                self.logger.log_food_delivered(self.tick, agent.id, src_x, src_y)
        return ActionResult(success=True, action=action)

    def _evaporate_pheromones(self) -> None:
        for field in self.grid.get_all_fields():
            expired = []
            for item in field.items:
                ic = self.item_configs.get(item.item_type)
                if ic and ic.evaporation_rate > 0:
                    if item.evaporate(ic.evaporation_rate):
                        expired.append(item)
            for item in expired:
                field.items.remove(item)

    def _check_deaths(self) -> None:
        for agent in self.agents:
            if not agent.alive or agent.energy > 0:
                continue
            agent.alive = False
            pos = agent.position
            if pos and agent in pos.agents:
                pos.agents.remove(agent)
            if self.logger:
                self.logger.log_agent_death(
                    self.tick, agent.id,
                    pos.x if pos else -1,
                    pos.y if pos else -1,
                )

    def _refresh_energy_at_special_fields(self) -> None:
        for agent in [a for a in self.agents if a.alive]:
            pos = agent.position
            if pos is None:
                continue
            if pos.spawn_id or pos.get_item_quantity("food") > 0:
                agent.energy = agent.max_energy

    def _build_perception(self, agent: Agent) -> dict:
        field = agent.position
        if field is None:
            return {}
        neighbors_data = []
        for nf in self.grid.get_neighbors(field.x, field.y):
            neighbors_data.append({
                "dx": nf.x - field.x,
                "dy": nf.y - field.y,
                "is_obstacle": nf.is_obstacle(),
                "is_full": nf.is_full(),
                "is_nest": nf.spawn_id is not None,
                "pheromone_nest": nf.get_pheromone_strength("pheromone_nest"),
                "pheromone_food": nf.get_pheromone_strength("pheromone_food"),
            })
        at_nest = field.spawn_id is not None
        return {
            "current_field": {
                "x": field.x,
                "y": field.y,
                "is_nest": at_nest,
                "food": 0.0 if at_nest else field.get_item_quantity("food"),
            },
            "neighbors": neighbors_data,
        }

    def _log_tick_summary(self) -> None:
        if not self.logger:
            return
        living = [a for a in self.agents if a.alive]
        carriers = [a for a in living if isinstance(a, AntAgent) and a.carrying is not None]
        searchers = [a for a in living if isinstance(a, AntAgent) and a.carrying is None]
        if self.tick % self._tick_summary_every_n_ticks == 0:
            food_sources = {}
            for x, y in self._food_source_positions:
                f = self.grid.get_field(x, y)
                if f is not None:
                    food_sources[f"{x},{y}"] = round(f.get_item_quantity("food"), 2)
            efficiency_pct = round(
                self._total_food_delivered / self._initial_food_total * 100, 1
            ) if self._initial_food_total > 0 else 0.0
            self.logger.log_tick_summary(
                self.tick,
                alive_count=len(living),
                food_at_nest=self._total_food_delivered,
                searcher_count=len(searchers),
                carrier_count=len(carriers),
                food_sources=food_sources,
                efficiency_pct=efficiency_pct,
            )
        if self._visual_mode and self.tick % self._grid_state_every_n_ticks == 0:
            self._log_grid_state()

    def _log_grid_state(self) -> None:
        fields_data = []
        for f in self.grid.get_all_fields():
            food = f.get_item_quantity("food")
            ph_nest = round(f.get_pheromone_strength("pheromone_nest"), 2)
            ph_food = round(f.get_pheromone_strength("pheromone_food"), 2)
            n_agents = len(f.agents)
            if f.is_obstacle() or f.spawn_id or food > 0 or ph_nest > 0 or ph_food > 0 or n_agents > 0:
                fields_data.append({
                    "x": f.x, "y": f.y,
                    "food": food,
                    "pn": ph_nest,
                    "pf": ph_food,
                    "obs": f.is_obstacle(),
                    "nest": f.spawn_id is not None,
                    "n": n_agents,
                })
        agents_data = []
        for a in self.agents:
            if a.alive and a.position:
                agents_data.append({
                    "id": a.id,
                    "x": a.position.x,
                    "y": a.position.y,
                    "c": getattr(a, "carrying", None),
                    "e": a.energy,
                })
        self.logger.log_grid_state(
            self.tick, self.grid.width, self.grid.height, fields_data, agents_data
        )
