"""Convenience exports for the ADK entry point."""

from agents.agent.root_agent import root_agent

# Some ADK flows look for either a ``root_agent`` symbol or a generic
# ``agent`` attribute exposed by the package.  Export both names so that the
# project works regardless of which discovery strategy is used.
agent = root_agent

__all__ = ["root_agent", "agent"]
