"""Definition of the repository's root agent entry point."""

from __future__ import annotations

from agents.agent._adk_compat import Agent
from agents.agent.coordenador import CoordenadorAgent

root_agent = Agent(
    name="root_agent",
    description="Agente principal que orquestra os subagentes.",
    sub_agents=[CoordenadorAgent()],
)

__all__ = ["root_agent"]
