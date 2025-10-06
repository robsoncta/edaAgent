"""Specialised agent responsible for statistical exploration."""

from __future__ import annotations

from agents.agent._adk_compat import LlmAgent
from agents.agent.tools.data_analyzer import analyze_data
from agents.agent.tools.memory_manager import manage_memory


def data_explorer_agent(model: str) -> LlmAgent:
    """Build the data exploration agent for a given foundation model."""

    instruction = """
Você é especialista em exploração de dados.
Use data_analyzer para estatísticas, outliers, correlações, distribuições.
Armazene resultados importantes com manage_memory.
Responda com insights claros.
""".strip()

    return LlmAgent(
        name="data_explorer",
        model=model,
        description=(
            "Especialista em análise estatística, executa cálculos, identifica "
            "padrões e detecta anomalias."
        ),
        instruction=instruction,
        tools=[analyze_data, manage_memory],
    )


__all__ = ["data_explorer_agent"]
