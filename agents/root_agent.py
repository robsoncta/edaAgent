"""Compatibility re-export for ADK root agent discovery."""

from __future__ import annotations

import sys

from agents.agent.root_agent import root_agent as _root_agent

root_agent = _root_agent

# When Python imports ``agents.root_agent`` it automatically registers the
# submodule on the parent package under the ``root_agent`` attribute.  Restore
# the original agent instance so ADK discovery can still fetch it from the
# package namespace.
_package = sys.modules.get("agents")
if _package is not None:
    setattr(_package, "root_agent", _root_agent)
    # Mirror the ``agent`` alias exposed at the package root for consistency.
    setattr(_package, "agent", _root_agent)

__all__ = ["root_agent"]
