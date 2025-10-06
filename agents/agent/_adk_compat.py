"""Compatibility helpers for optional Google ADK dependencies.

This repository targets the Google AI Developer Kit (ADK).  However, the
package may not always be installed in local or CI environments used for
linting and static analysis.  Importing the public modules would then raise a
``ModuleNotFoundError`` during module initialisation, preventing the rest of the
package from loading.  The small shim defined here mirrors the minimal surface
area required by the project so that imports succeed even without the real
dependency, while seamlessly delegating to the official implementations when
they are available.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any, Callable, Iterable, List, Protocol, Sequence

try:  # pragma: no cover - exercised in production environments
    from google.adk.agents import Agent, LlmAgent  # type: ignore
    from google.adk.tools import AgentTool, ToolContext  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - executed in constrained envs

    class ToolContext(Protocol):
        """Minimal protocol for tool execution context."""

        session: Any


    @dataclass
    class _SessionState:
        state: dict[str, Any] = field(default_factory=dict)


    @dataclass
    class _DefaultToolContext:
        session: Any = field(default_factory=lambda: SimpleNamespace(state={}))


    class AgentTool:  # type: ignore[misc]
        """Fallback representation for ``google.adk.tools.AgentTool``."""

        def __init__(self, tool: Callable[..., Any]) -> None:
            self.tool = tool

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return self.tool(*args, **kwargs)


    class Agent:  # type: ignore[misc]
        """Fallback stand-in for :class:`google.adk.agents.Agent`."""

        def __init__(
            self,
            *,
            name: str,
            description: str,
            sub_agents: Sequence[object] | None = None,
        ) -> None:
            self.name = name
            self.description = description
            self.sub_agents: List[object] = list(sub_agents or [])

        def __repr__(self) -> str:  # pragma: no cover - debugging helper
            return (
                "Agent(name={!r}, description={!r}, sub_agents={!r})".format(
                    self.name,
                    self.description,
                    self.sub_agents,
                )
            )


    class LlmAgent(Agent):  # type: ignore[misc]
        """Fallback stand-in for :class:`google.adk.agents.LlmAgent`."""

        def __init__(
            self,
            *,
            name: str,
            model: str,
            description: str,
            instruction: str,
            tools: Iterable[Callable[..., Any]] | None = None,
        ) -> None:
            super().__init__(name=name, description=description, sub_agents=None)
            self.model = model
            self.instruction = instruction
            self.tools: List[Callable[..., Any]] = list(tools or [])


    ToolContext = ToolContext  # type: ignore[assignment]

