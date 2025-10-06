"""Specialised agent responsible for crafting visualisations."""

from __future__ import annotations

from agents.agent._adk_compat import LlmAgent
from agents.agent.tools.chart_generator import generate_chart
from agents.agent.tools.memory_manager import manage_memory


def visualization_expert_agent(model: str) -> LlmAgent:
    """Build the visualisation expert agent for the provided model."""

    instruction = """
Você é especialista em visualizações.
Use generate_chart para criar histogramas, scatters, boxplots, heatmaps e barras conforme o contexto.
Armazene caminhos de imagens com manage_memory.
Descreva os insights das visualizações.
""".strip()

    return LlmAgent(
        name="visualization_expert",
        model=model,
        description=(
            "Seleciona e gera visualizações apropriadas e interpreta padrões "
            "visuais."
        ),
        instruction=instruction,
        tools=[generate_chart, manage_memory],
    )


__all__ = ["visualization_expert_agent"]
