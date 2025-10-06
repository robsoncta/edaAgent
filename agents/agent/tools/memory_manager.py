"""Simple helpers to persist conversational state across tool invocations."""

from __future__ import annotations

from typing import Any, Protocol


class SupportsState(Protocol):
    session: Any


def manage_memory(context: SupportsState, key: str, value: Any) -> dict[str, Any]:
    """Armazena pares chave/valor na memória da sessão."""

    state = getattr(getattr(context, "session", None), "state", None)
    if not isinstance(state, dict):
        return {"status": "error", "error_message": "Estado de sessão indisponível."}

    state[key] = value
    return {"status": "success"}


__all__ = ["manage_memory"]
