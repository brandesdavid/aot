from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .field import Field


@dataclass
class AgentSpawnConfig:
    agent_type_id: str
    count: int


@dataclass
class Spawn:
    id: str
    name: str
    agent_spawn_configs: list[AgentSpawnConfig] = field(default_factory=list)

    def create_agents(self, agent_type_configs: dict, spawn_field: Field) -> list:
        from .agent import AntAgent

        agents = []
        for config in self.agent_spawn_configs:
            agent_type = agent_type_configs.get(config.agent_type_id)
            if agent_type is None:
                continue
            for i in range(config.count):
                agent = AntAgent(
                    agent_id=f"{config.agent_type_id}_{self.id}_{i}",
                    energy=agent_type["energy"],
                    max_energy=agent_type["energy"],
                    perception_range=agent_type.get("perception_range", 4),
                    pheromone_drop_amount=agent_type.get("pheromone_drop_amount", 10.0),
                    capacity_config=agent_type.get("capacity", []),
                )
                agent.position = spawn_field
                spawn_field.agents.append(agent)
                agents.append(agent)
        return agents
