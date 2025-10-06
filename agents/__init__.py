"""Top-level package for ADK agents."""

from .agent.root_agent import root_agent

# Mirror the same alias that the repository root exposes so ADK can find the
# agent through either symbol depending on its discovery heuristics.
agent = root_agent

__all__ = ["root_agent", "agent"]
