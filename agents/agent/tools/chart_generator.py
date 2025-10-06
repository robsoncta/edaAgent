"""Utility functions that generate charts from the loaded dataset."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class SupportsDataset(Protocol):
    session: Any


def _get_dataset(context: SupportsDataset):
    try:
        import pandas as pd
    except ModuleNotFoundError as exc:  # pragma: no cover - environment limitation
        raise ModuleNotFoundError("pandas é necessário para generate_chart") from exc

    session_state = getattr(context, "session", None)
    if session_state is None:
        return None
    state = getattr(session_state, "state", None)
    if not isinstance(state, dict):
        return None
    dataset_json = state.get("current_dataset")
    if dataset_json is None:
        return None
    return pd.read_json(dataset_json, orient="records")


def generate_chart(
    context: SupportsDataset,
    chart_type: str,
    column_x: str | None = None,
    column_y: str | None = None,
    output_path: str | None = None,
) -> dict[str, Any]:
    """Gera visualizações a partir do dataset atual."""

    try:
        df = _get_dataset(context)
    except ModuleNotFoundError as exc:
        return {"status": "error", "error_message": str(exc)}

    if df is None:
        return {"status": "error", "error_message": "Dataset não carregado."}

    if output_path is None:
        output_path = "chart.png"

    path = Path(output_path)

    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:  # pragma: no cover - environment limitation
        return {"status": "error", "error_message": str(exc)}

    plt.figure()

    try:
        if chart_type == "histogram" and column_x:
            df[column_x].plot(kind="hist")
        elif chart_type == "scatter" and column_x and column_y:
            df.plot(kind="scatter", x=column_x, y=column_y)
        elif chart_type == "box" and column_x:
            df.boxplot(column=column_x)
        elif chart_type == "heatmap":
            plt.imshow(df.corr(), cmap="viridis", interpolation="nearest")
            plt.colorbar()
        elif chart_type == "bar" and column_x:
            df[column_x].value_counts().plot(kind="bar")
        else:
            return {"status": "error", "error_message": "Configuração inválida de gráfico."}

        plt.tight_layout()
        plt.savefig(path)
    except Exception as exc:  # pragma: no cover - relies on plotting backend
        return {"status": "error", "error_message": str(exc)}
    finally:
        plt.close()

    state = getattr(getattr(context, "session", None), "state", None)
    if isinstance(state, dict):
        state.setdefault("generated_charts", []).append(str(path))

    return {"status": "success", "path": str(path)}


__all__ = ["generate_chart"]
