"""Collection of utilities for statistical analysis."""

from __future__ import annotations

from typing import Any, Mapping, Protocol


class SupportsDataset(Protocol):
    """Subset of the tool context used by the analysis helpers."""

    session: Any


def _get_dataset(context: SupportsDataset):
    try:
        import pandas as pd
    except ModuleNotFoundError as exc:  # pragma: no cover - environment limitation
        raise ModuleNotFoundError("pandas é necessário para analyze_data") from exc

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


def analyze_data(
    context: SupportsDataset,
    analysis_type: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Executa análises estatísticas específicas no dataset."""

    try:
        df = _get_dataset(context)
    except ModuleNotFoundError as exc:
        return {"status": "error", "error_message": str(exc)}

    if df is None:
        return {"status": "error", "error_message": "Dataset não carregado."}

    params = dict(params or {})

    try:
        if analysis_type == "describe":
            result = df.describe().to_string()
        elif analysis_type == "outliers":
            column = params.get("column")
            if column not in df.columns:
                raise KeyError("Coluna inválida para detecção de outliers.")
            try:
                import numpy as np
                from scipy import stats
            except ModuleNotFoundError as exc:  # pragma: no cover - env limitation
                return {"status": "error", "error_message": str(exc)}

            z_scores = np.abs(stats.zscore(df[column].astype(float)))
            outliers = df[z_scores > 3]
            result = outliers.to_string()
        elif analysis_type == "correlation":
            result = df.corr().to_string()
        elif analysis_type == "distribution":
            column = params.get("column")
            if column not in df.columns:
                raise KeyError("Coluna inválida para distribuição.")
            result = df[column].value_counts().to_string()
        else:
            return {"status": "error", "error_message": "Tipo de análise inválido."}
    except Exception as exc:  # pragma: no cover - relies on pandas/scipy edge cases
        return {"status": "error", "error_message": str(exc)}

    return {"status": "success", "result": result}


__all__ = ["analyze_data"]
