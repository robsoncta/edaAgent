"""Tool that loads CSV files and stores them in the session state."""

from __future__ import annotations

from typing import Any, Protocol


class SupportsSessionState(Protocol):
    """Protocol for the subset of ``ToolContext`` used by the tool."""

    session: Any


def load_csv(context: SupportsSessionState, file_path: str) -> dict[str, Any]:
    """Carrega um arquivo CSV e retorna o conteúdo formatado."""

    try:
        import pandas as pd
    except ModuleNotFoundError as exc:  # pragma: no cover - environment limitation
        return {"status": "error", "error_message": str(exc)}

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:  # pragma: no cover - pandas raises many types
        return {"status": "error", "error_message": str(exc)}

    session_state = getattr(context, "session", None)
    if session_state is not None:
        state = getattr(session_state, "state", None)
        if isinstance(state, dict):
            state["current_dataset"] = df.to_json(orient="records")

    return {"status": "success", "data": df.to_string(index=False)}


__all__ = ["load_csv"]
